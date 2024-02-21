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


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello There, I'm ZenithiaBot. I can help you with your queries. Send me any message and I'll try to get back to you."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I'm ZenithiaBot. I can help you with your queries. Send me any message and I'll try to get back to you."
    )


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat_id}) in {message_type}: '{text}'")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)
