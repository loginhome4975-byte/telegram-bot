"""/start va /help buyruqlari handlerlari."""

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database import add_user, get_user_language
from keyboards import get_main_menu_keyboard
from translations import get_text
from os import getenv

ADMIN_IDS = [int(i.strip()) for i in getenv("ADMIN_IDS", "").split(",") if i.strip()]

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Bot ishga tushganda /start buyrug'ini qayta ishlash."""
    user = message.from_user

    # Foydalanuvchini bazaga qo'shish
    await add_user(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name,
        language_code=user.language_code or "uz",
    )

    # Foydalanuvchi tilini olish (yangi foydalanuvchilar uchun 'uz')
    lang = await get_user_language(user.id)

    # Tarjima qilingan xush kelibsiz matnini olish
    welcome_text = get_text("welcome", lang, name=user.full_name)
    welcome_text += get_text("guide_notice", lang)

    is_admin = user.id in ADMIN_IDS

    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard(lang, is_admin),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """/help buyrug'ini qayta ishlash."""
    # Foydalanuvchi tilini olish
    lang = await get_user_language(message.from_user.id)

    # Tarjima qilingan yordam matnini olish
    help_text = get_text("help_text", lang)

    is_admin = message.from_user.id in ADMIN_IDS

    await message.answer(
        help_text,
        reply_markup=get_main_menu_keyboard(lang, is_admin),
        parse_mode="HTML",
    )
