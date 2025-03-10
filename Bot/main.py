from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7821045045:AAEJT7wxqvE2HA7VZW24RjDZKHjlAgpwRfM'
BOT_USERNAME: Final = '@theScrap_bot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        await update.message.reply_text("""I'm the Scrap bot, I will list your scrap on the website www.theScrapCo.com,
                                            To list enter the details specified below:

                                            *upload an image of the scrap material*

                                            Full Name
                                            Phone Number
                                            Address
                                            material
                                            quantity(weight)
                                            pick up date and time
                                            price

                                        [For Rewards and other features create an account on www.theScrapCo.com]

                                        ------------------------------------------------------------------------

                                        मैं Scrap Bot हूँ, मैं आपकी कबाड़ सामग्री को हमारी वेबसाइट www.theScrapCo.com पर सूचीबद्ध करूंगा।
                                            सूचीबद्ध करने के लिए नीचे दिए गए विवरण दर्ज करें:

                                            कृपया कबाड़ सामग्री की एक छवि अपलोड करें

                                            पूरा नाम
                                            फ़ोन नंबर
                                            पता
                                            सामग्री का प्रकार
                                            मात्रा (वज़न)
                                            पिकअप समय
                                            मूल्य

                                        [पुरस्कार और अन्य सुविधाओं के लिए www.theScrapCo.com पर एक खाता बनाएं]

                                        -----------------------------------------------------------------------

                                        John Doe
                                        1231231231
                                        Fake Street, Brown Alley
                                        Copper
                                        7.9kg
                                        1-03-2025, 5:00 AM
                                        12300Rs

                                        """)

# Responses
def handle_response(text: str) -> str:
    text = text.lower()
    if "hello" in text:
        return "hey there"
    return "I do not understand"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        message_type: str = update.message.chat.type  # This will tell if it's a group chat or private chat
        if update.message.text:
            text: str = update.message.text  # Incoming message
            print(f"User ({update.message.chat.id}) in {message_type} : {text}")
            if message_type == 'group':
                if BOT_USERNAME in text:
                    new_text: str = text.replace(BOT_USERNAME, '').strip()
                    response: str = handle_response(new_text)
                else: 
                    return
            else:  # private chats
                response: str = handle_response(text)
            print('Bot:', response)
            await update.message.reply_text(response)

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors - Fixed this line
    app.add_error_handler(error_handler)
    
    # Constantly check for updates
    # Checks every 3 seconds for new messages
    print("Starting bot...")
    app.run_polling(poll_interval=3)
