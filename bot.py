import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = os.getenv("BOT_TOKEN", "8417631546:AAFGGOTf7ckVLAfr0_AGf0SpUADqU44Gj4w")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

CHAT_LINK = "https://t.me/YOUR_GROUP_LINK"
MINIAPP_URL = "https://mafia-2lu6.onrender.com"

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "👋 Welcome to Mafia!\n\n"
        "📜 Rules:\n"
        "1. The bot assigns roles.\n"
        "2. Discussion is in the group chat.\n"
        "3. Mini App is for profile and in-game chat.\n\n"
        "Click *Play* to join!"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Group Chat", url=CHAT_LINK)],
            [InlineKeyboardButton(
                text="🎮 Play (Mini App)",
                web_app=WebAppInfo(url=MINIAPP_URL)
            )]
        ]
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
