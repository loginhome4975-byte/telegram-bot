"""Karta qo'shish handlerlari - FSM bilan."""

import re

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import update_card_number, get_user_language
from keyboards import get_settings_keyboard
from translations import get_text

router = Router()


class CardStates(StatesGroup):
    """Karta qo'shish holatlari."""
    waiting_for_card = State()


@router.message(CardStates.waiting_for_card)
async def process_card_number(message: Message, state: FSMContext):
    """Foydalanuvchi yuborgan karta raqamini qayta ishlash."""
    lang = await get_user_language(message.from_user.id)

    # Karta raqamidan bo'shliqlar va chiziqlarni olib tashlash
    card_number = re.sub(r'[\s\-]', '', message.text)

    # 16 raqamli ekanligini tekshirish
    if not card_number.isdigit() or len(card_number) != 16:
        await message.answer(
            get_text("card_invalid", lang),
            parse_mode="HTML",
        )
        return

    # Karta raqamini formatlash (4 4 4 4)
    formatted_card = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"

    # Bazaga saqlash
    await update_card_number(message.from_user.id, formatted_card)

    # FSM holatini tozalash
    await state.clear()

    # Muvaffaqiyat xabarini yuborish
    await message.answer(
        get_text("card_saved", lang, card=formatted_card),
        reply_markup=get_settings_keyboard(lang),
        parse_mode="HTML",
    )
