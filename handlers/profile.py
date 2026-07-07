"""Profil buyruqlari handlerlari."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import get_user, get_user_language
from keyboards import get_back_keyboard, get_profile_keyboard
from translations import get_text

router = Router()


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    """/profile buyrug'ini qayta ishlash."""
    # Foydalanuvchi tilini olish
    lang = await get_user_language(message.from_user.id)

    user_data = await get_user(message.from_user.id)

    if user_data:
        # Tarjima qilingan profil matnini tuzish
        username = user_data['username'] or get_text("profile_not_found", lang).split(".")[0]
        profile_text = (
            get_text("profile_title", lang)
            + f"{get_text('profile_id', lang)}: <code>{user_data['user_id']}</code>\n"
            + f"{get_text('profile_name', lang)}: {user_data['full_name']}\n"
            + f"{get_text('profile_username', lang)}: @{user_data['username'] or '—'}\n"
            + f"{get_text('profile_lang', lang)}: {user_data['language_code']}\n"
            + f"{get_text('profile_joined', lang)}: {user_data['joined_at'][:10]}\n"
            + f"{get_text('profile_messages', lang)}: {user_data['message_count']}\n"
            + f"{get_text('profile_balance', lang)}: {user_data.get('balance', 0)} so'm\n"
            + f"{get_text('profile_pending_balance', lang)}: {user_data.get('pending_balance', 0)} so'm\n"
            + f"{get_text('card_current', lang)}: {user_data.get('card_number') or get_text('card_not_set', lang)}\n"
        )
    else:
        # Profil topilmadi xabari
        profile_text = get_text("profile_not_found", lang)

    await message.answer(
        profile_text,
        reply_markup=get_profile_keyboard(lang),
        parse_mode="HTML",
    )
