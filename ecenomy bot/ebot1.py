import logging
import random

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define a dictionary to store users' balances
user_balances = {}

# Define a dictionary to store users' daily claim status
daily_claimed = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("start massage here", callback_data="button_data")]]
    )
    await update.message.reply_html(
        rf"start message here!",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help message here!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def cash(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the user's balance."""
    user_id = update.effective_user.id
    balance = user_balances.get(user_id, 0)
    await update.message.reply_text(f"Your balance is {balance} wed.")


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Grant the user their daily salary."""
    user_id = update.effective_user.id
    if user_id in daily_claimed:
        await update.message.reply_text("You have already claimed your daily salary.")
        return

    # Grant a random amount between 100 and 1000 wed as the daily salary
    daily_salary = random.randint(100, 1000)
    user_balances[user_id] = user_balances.get(user_id, 0) + daily_salary
    daily_claimed[user_id] = True
    await update.message.reply_text(f"You earned {daily_salary} wed as your daily salary.")


async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allow the user to deposit money."""
    user_id = update.effective_user.id
    # Check if the user provided a valid amount to deposit
    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Please specify a valid amount to deposit.")
        return

    if amount <= 0:
        await update.message.reply_text("Please specify a positive amount to deposit.")
        return

    user_balances[user_id] = user_balances.get(user_id, 0) + amount
    await update.message.reply_text(f"You deposited {amount} wed into your account.")


async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allow the user to withdraw money."""
    user_id = update.effective_user.id
    # Check if the user provided a valid amount to withdraw
    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Please specify a valid amount to withdraw.")
        return

    if amount <= 0:
        await update.message.reply_text("Please specify a positive amount to withdraw.")
        return

    if amount > user_balances.get(user_id, 0):
        await update.message.reply_text("Insufficient balance.")
        return

    user_balances[user_id] -= amount
    await update.message.reply_text(f"You withdrew {amount} wed from your account.")


async def transfer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allow the user to transfer money to another user."""
    user_id = update.effective_user.id
    # Check if the user provided a valid amount and recipient
    try:
        amount = int(context.args[0])
        recipient_id = int(context.args[1])
    except (IndexError, ValueError):
        await update.message.reply_text("Please specify a valid amount and recipient.")
        return

    if amount <= 0:
        await update.message.reply_text("Please specify a positive amount to transfer.")
        return

    if recipient_id == user_id:
        await update.message.reply_text("You cannot transfer to yourself.")
        return

    if amount > user_balances.get(user_id, 0):
        await update.message.reply_text("Insufficient balance.")
        return

    user_balances[user_id] -= amount
    user_balances[recipient_id] = user_balances.get(recipient_id, 0) + amount
    await update.message.reply_text(f"You transferred {amount} wed to user {recipient_id}.")


async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allow the user to bet and potentially double their money."""
    user_id = update.effective_user.id
    # Check if the user provided a valid amount to bet
    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Please specify a valid amount to bet.")
        return

    # Check if the user has enough balance to place the bet
    if amount > user_balances.get(user_id, 0):
        await update.message.reply_text("You don't have enough balance to place this bet.")
        return

    # Flip a coin (50% chance)
    if random.random() < 0.5:
        user_balances[user_id] += amount  # User wins, double the bet
        await update.message.reply_text(f"Congratulations! You won {amount} wed.")
    else:
        user_balances[user_id] -= amount  # User loses, subtract the bet
        await update.message.reply_text(f"Sorry, you lost {amount} wed.")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cash", cash))  # Add bakiye command handler
    application.add_handler(CommandHandler("daily", daily))  # Add gÃ¼nlÃ¼k command handler
    application.add_handler(CommandHandler("deposit", deposit))  # Add yatÄ±r command handler
    applicatio.add_handler(CommandHandler("withdraw", withdraw))  # Add Ã§ek command handler
    application.add_handler(CommandHandler("transfer", transfer))  # Add transfer command handler
    application.add_handler(CommandHandler("bet", bet))  # Add bet command handler

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
