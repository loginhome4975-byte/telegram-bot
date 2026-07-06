"""
Telegram Bot - Asosiy fayl
Aiogram 3 asosida yaratilgan to'liq funksional bot.
"""

import asyncio
import logging
import os
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
from dotenv import load_dotenv

from database import increment_message_count
from handlers import start, profile, callbacks, admin, card, guide, generator

# .env faylni yuklash
load_dotenv()

# Bot tokenini olish
BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
    print("❌ Xato: BOT_TOKEN .env faylida o'rnatilmagan!")
    print("📝 .env faylini oching va bot tokeningizni qo'ying.")
    sys.exit(1)

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# Bot va Dispatcher yaratish
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(storage=MemoryStorage())

# Noma'lum xabarlar uchun alohida router (ENG OXIRIDA ishlanadi)
other_router = Router()


@other_router.message(F.text)
async def handle_any_message(message: Message):
    """Har qanday matnli xabarni qayta ishlash va hisoblagichni oshirish."""
    await increment_message_count(message.from_user.id)

    # Noma'lum buyruq bo'lsa, foydalanuvchiga xabar berish
    if message.text.startswith("/"):
        await message.answer(
            "❓ Noma'lum buyruq. /help ni ko'ring.",
            parse_mode="HTML",
        )


# Router'larni ulash (TARTIB MUHIM! start birinchi, other_router eng oxirida)
dp.include_router(start.router)
dp.include_router(profile.router)
dp.include_router(callbacks.router)
dp.include_router(admin.router)
dp.include_router(card.router)
dp.include_router(guide.router)
dp.include_router(generator.router)
# Noma'lum buyruqlar uchun (eng oxirida bo'lishi shart)
dp.include_router(other_router)


async def handle_dummy_request(request):
    """Render uchun soxta javob qaytaruvchi server."""
    return web.Response(text="Bot is running smoothly on Render!")


async def run_dummy_server():
    """Render port kutish xatoligini aylanib o'tish uchun server."""
    app = web.Application()
    app.router.add_get('/', handle_dummy_request)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render o'zi bergan portni yoki 8080 ni olamiz
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"🌐 Soxta veb-server ishga tushdi: {port}-port")


async def main():
    """Botni ishga tushirish uchun asosiy funksiya."""
    logging.info("🚀 Bot ishga tushmoqda...")
    
    # Soxta serverni orqa fonda ishga tushiramiz
    asyncio.create_task(run_dummy_server())

    # Botni ishga tushirishdan oldin barcha eski update'larni o'tkazib yuborish
    await bot.delete_webhook(drop_pending_updates=True)
    
    logging.info("✅ Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
