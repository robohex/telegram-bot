import logging
import requests
from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram bot token
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Joke API URL
JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"

# Function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a joke bot. You can ask me for a joke using the /joke command.")

# Function to handle the /joke command
def joke(update, context):
    # Get a random joke from the API
    response = requests.get(JOKE_API_URL)
    if response.status_code == 200:
        joke_data = response.json()
        joke_text = f"{joke_data['setup']}\n{joke_data['punchline']}"
    else:
        joke_text = "Sorry, I couldn't find a joke. Please try again later."

    # Send the joke to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=joke_text)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("joke", joke))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
