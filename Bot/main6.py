from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import os
from dotenv import load_dotenv
import tempfile
import uuid
from supabase import create_client


load_dotenv()
YOUR_BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")

# Initialize Supabase client
if SUPABASE_URL and SUPABASE_API_KEY :
    supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Conversation states
IMAGE, NAME, PHONE, ADDRESS, MATERIAL, DESCRIPTION, QUANTITY, TIME, PRICE = range(9)
# Dictionary to store user data temporarily
user_data = {}

async def add_item(user_data):
    try:
        response = supabase.table("Item").insert({
            "seller_name": user_data["name"],
            "seller_phone": user_data["phone"],
            "pictures": [user_data["image"]["supabase_url"]],
            "description": user_data["description"],
            "quantity": float(user_data["quantity"]),
            "pickUpAddress": user_data["address"],
            "pickUpTime": user_data["pickup_time"],
            "price": float(user_data["price"]),
            "listPlat": "TELEGRAM",
            "telegram_id": str(user_data["telegram_id"]),
            "material": "OTHER",  # You can dynamically map materials here
        }).execute()
        print("Data Inserted Successfully ✅", response)
        return response

    except Exception as e:
        print("Failed to insert data ❌", e)
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("hey")
    if update.message:
        await update.message.reply_text(
            "मैं Scrap Bot हूँ, मैं आपकी कबाड़ सामग्री को हमारी वेबसाइट www.theScrapCo.com पर सूचीबद्ध करूंगा।\n"
            "I am Scrap Bot, I will list your scrap material on our website www.theScrapCo.com.\n"
            "\nकृपया कबाड़ सामग्री की एक छवि अपलोड करें\nPlease upload an image of the scrap material."
        )
        return IMAGE

async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Hello babu")
    if update.message and update.message.photo:
        # Get the file ID of the largest photo
        file_id = update.message.photo[-1].file_id
        
        # Get the file from Telegram
        file = await context.bot.get_file(file_id)
        
        # Generate a unique filename with UUID
        file_extension = "jpg"  # Default extension for Telegram photos
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Download the file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            await file.download_to_drive(temp_file.name)
            
            # Upload the file to Supabase
            with open(temp_file.name, "rb") as f:
                file_bytes = f.read()
                
            try:
                if SUPABASE_BUCKET_NAME :
                    result = supabase.storage.from_(SUPABASE_BUCKET_NAME).upload(
                        unique_filename, 
                        file_bytes, 
                        {"content-type": f"image/{file_extension}"}
                    )
                
                # Get the public URL
                image_url=""
                if SUPABASE_BUCKET_NAME :
                    image_url = supabase.storage.from_(SUPABASE_BUCKET_NAME).get_public_url(unique_filename)
                
                # Store both the file_id and the Supabase URL
                user_data["image"] = {
                    "telegram_file_id": file_id,
                    "supabase_url": image_url
                }
                
                # Remove the temporary file
                os.unlink(temp_file.name)
                
                await update.message.reply_text("✅ पूरा नाम दर्ज करें\nEnter your full name.")
                return NAME
                
            except Exception as e:
                print(f"Error uploading to Supabase: {e}")
                os.unlink(temp_file.name)
                await update.message.reply_text("कृपया फिर से कोशिश करें, एक त्रुटि हुई है। \nPlease try again, there was an error.")
                return IMAGE
    
    elif update.message:
        await update.message.reply_text("कृपया एक छवि अपलोड करें\nPlease upload an image.")
        return IMAGE

async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["name"] = update.message.text
        await update.message.reply_text("✅ फ़ोन नंबर दर्ज करें\nEnter your phone number.")
        return PHONE

async def phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["phone"] = update.message.text
        await update.message.reply_text("✅ पता दर्ज करें\nEnter your address.")
        return ADDRESS

async def address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["address"] = update.message.text
        await update.message.reply_text("✅ सामग्री का प्रकार दर्ज करें\nEnter the type of material.")
        return MATERIAL

async def material_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["material"] = update.message.text
        await update.message.reply_text("✅ सामग्री का विवरण दर्ज करें\nEnter the material description.")
        return DESCRIPTION

async def description_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["description"] = update.message.text
        await update.message.reply_text("✅ मात्रा (वज़न) दर्ज करें\nEnter the quantity (weight).")
        return QUANTITY

async def quantity_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["quantity"] = update.message.text
        await update.message.reply_text("✅ पिकअप समय दर्ज करें\nEnter the pickup time.")
        return TIME

async def time_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["pickup_time"] = update.message.text
        await update.message.reply_text("✅ मूल्य दर्ज करें\nEnter the price.")
        return PRICE

async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["price"] = update.message.text
        await update.message.reply_text(
            "🎯 आपका अनुरोध सफलतापूर्वक लिया गया है!\nYour request has been successfully submitted!\nधन्यवाद!\nThank You!\n\n"
            "[पुरस्कार और अन्य सुविधाओं के लिए www.theScrapCo.com पर एक खाता बनाएं]\n"
            "[For Rewards and other features, create an account on www.theScrapCo.com]"
        )
        if update.message.from_user :
            user_data["telegram_id"] = update.message.from_user.id 
        print("User Data:", user_data)

        response = await add_item(user_data)
        if response:
            await update.message.reply_text("✅ आपके कबाड़ की सूची सफलतापूर्वक बनाई गई है!")
        else:
            await update.message.reply_text("❌ सर्वर त्रुटि! कृपया फिर से प्रयास करें।")


        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("❌ आपका अनुरोध रद्द कर दिया गया है!\nYour request has been cancelled!")
    return ConversationHandler.END

if __name__ == "__main__":
    if YOUR_BOT_TOKEN:
        app = Application.builder().token(YOUR_BOT_TOKEN).build()
        
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start_command)],
            states={
                IMAGE: [MessageHandler(filters.PHOTO, image_handler)],
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler)],
                PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_handler)],
                ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address_handler)],
                MATERIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, material_handler)],
                DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description_handler)],
                QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, quantity_handler)],
                TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, time_handler)],
                PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price_handler)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
        
        app.add_handler(conv_handler)
        print("Bot is running...🚀")
        app.run_polling(poll_interval=3)
    else:
        print("BOT_TOKEN not found in .env file")
