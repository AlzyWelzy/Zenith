import asyncio
import telegram
from dotenv import load_dotenv

load_dotenv()
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def main():
    bot = telegram.Bot(BOT_TOKEN)
    async with bot:
        data = await bot.get_me()
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
