import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


load_dotenv()

BOT_TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
KILL_SWITCH = False


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    START_TEXT = "🌟 Welcome to ZenithiaBot! Your intelligent companion on Telegram. I'm here to enhance your messaging experience with seamless interactions and a touch of sophistication. Feel free to explore and make your conversations smarter! 🚀✨"
    await update.message.reply_text(
        f"Hello, {update.effective_user.first_name}! {START_TEXT}"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HELP_TEXT = "I'm ZenithiaBot. I can help you with your queries. Send me any message and I'll try to get back to you."
    await update.message.reply_text(
        f"Hello, {update.effective_user.first_name}! {HELP_TEXT}"
    )


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CUSTOM_TEXT = "This is a custom command!"
    await update.message.reply_text(f"{CUSTOM_TEXT}")


# Responses


def handle_responses(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hey there!"

    if "bye" in processed:
        return "Bye!"

    if "i love you" in processed:
        return "I love you too!"

    return "I don't understand. Please try again!"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: '{text}'")

    if KILL_SWITCH:
        if message_type == "group":
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, "").strip()
                response: str = handle_responses(new_text)
            else:
                return
        else:
            response: str = handle_responses(text)
    else:

        response: str = handle_responses(text)

    print("Bot:", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting Telegram bot...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("custom", custom_command))

    # Messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Errors
    application.add_error_handler(error)

    # Polls the bot
    print("Starting polling...")
    application.run_polling(poll_interval=3)
