import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Add your Telegram bot token here
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Set up logging to log information level messages
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Create a bot object and start it with the token
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Handler function for the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm a Telegram bot!")

# Handler function for the /help command
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Help message will be written here.")

# Handler function that echoes the incoming message
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Add command handlers and text handler
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(echo_handler)

# Start the bot
updater.start_polling()

# Keep the bot running until Ctrl+C is pressed
updater.idle()
