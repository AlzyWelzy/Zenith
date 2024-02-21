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


# Commands


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello There, I'm ZenithiaBot. I can help you with your queries. Send me any message and I'll try to get back to you."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "I'm ZenithiaBot. I can help you with your queries. Send me any message and I'll try to get back to you."
    )


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This is a custom command!")


# Response


def handle_response(text: str) -> str:
    processed_text = text.lower()

    if "hello" in processed_text:
        return "Hello there!"

    if "how are you" in processed_text:
        return "I'm good. How about you?"

    if "bye" in processed_text:
        return "Bye!"

    if "i love you" in processed_text:
        return "I love you too!"

    return "I don't understand. Please try again!"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat_id}) in {message_type}: '{text}'")

    if message_type in {"group", "supergroup"}:
        print(f"Text: {text}, Bot username: {BOT_USERNAME}")
        if BOT_USERNAME in text:
            print("Bot found in text")
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            print("Bot not found in text")
            return
    else:
        print("Bot not in group")
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")


def main() -> None:
    print("Starting bot...")
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
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
