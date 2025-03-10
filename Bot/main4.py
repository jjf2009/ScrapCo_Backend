from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

YOUR_BOT_TOKEN = os.getenv("BOT_TOKEN")

# Conversation states
IMAGE, NAME, PHONE, ADDRESS, MATERIAL, DESCRIPTION, QUANTITY, TIME, PRICE = range(9)

# Dictionary to store user data temporarily
user_data = {}

async def start_command(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "मैं Scrap Bot हूँ, मैं आपकी कबाड़ सामग्री को हमारी वेबसाइट www.theScrapCo.com पर सूचीबद्ध करूंगा।\n"
            "I am Scrap Bot, I will list your scrap material on our website www.theScrapCo.com.\n"
            "\nकृपया कबाड़ सामग्री की एक छवि अपलोड करें\nPlease upload an image of the scrap material."
        )
        return IMAGE

async def image_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.photo:
        user_data["image"] = update.message.photo[-1].file_id
        await update.message.reply_text("✅ पूरा नाम दर्ज करें\nEnter your full name.")
        return NAME
    elif update.message:
        await update.message.reply_text("कृपया एक छवि अपलोड करें\nPlease upload an image.")
        return IMAGE

async def name_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["name"] = update.message.text
        await update.message.reply_text("✅ फ़ोन नंबर दर्ज करें\nEnter your phone number.")
        return PHONE

async def phone_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["phone"] = update.message.text
        await update.message.reply_text("✅ पता दर्ज करें\nEnter your address.")
        return ADDRESS

async def address_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["address"] = update.message.text
        await update.message.reply_text("✅ सामग्री का प्रकार दर्ज करें\nEnter the type of material.")
        return MATERIAL

async def material_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["material"] = update.message.text
        await update.message.reply_text("✅ सामग्री का विवरण दर्ज करें\nEnter the material description.")
        return DESCRIPTION

async def description_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["description"] = update.message.text
        await update.message.reply_text("✅ मात्रा (वज़न) दर्ज करें\nEnter the quantity (weight).")
        return QUANTITY

async def quantity_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["quantity"] = update.message.text
        await update.message.reply_text("✅ पिकअप समय दर्ज करें\nEnter the pickup time.")
        return TIME

async def time_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["pickup_time"] = update.message.text
        await update.message.reply_text("✅ मूल्य दर्ज करें\nEnter the price.")
        return PRICE

async def price_handler(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_data["price"] = update.message.text
        await update.message.reply_text(
            "🎯 आपका अनुरोध सफलतापूर्वक लिया गया है!\nYour request has been successfully submitted!\nधन्यवाद!\nThank You!\n\n"
            "[पुरस्कार और अन्य सुविधाओं के लिए www.theScrapCo.com पर एक खाता बनाएं]\n"
            "[For Rewards and other features, create an account on www.theScrapCo.com]"
        )
        
        print("User Data:", user_data)
        return ConversationHandler.END

async def cancel(update: Update, _: ContextTypes.DEFAULT_TYPE):
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

