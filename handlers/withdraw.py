"""Pul yechish handlerlari - FSM bilan."""

from os import getenv
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from database import get_user, update_balance, get_user_language, add_user_history
from keyboards import get_profile_keyboard
from translations import get_text

router = Router()


class WithdrawStates(StatesGroup):
    """Pul yechish holatlari."""
    waiting_for_amount = State()


@router.callback_query(F.data == "withdraw")
async def callback_withdraw(callback: CallbackQuery, state: FSMContext):
    """Pul yechish tugmasi bosilganda."""
    user_id = callback.from_user.id
    lang = await get_user_language(user_id)
    user_data = await get_user(user_id)

    if not user_data:
        await callback.answer(get_text("profile_not_found", lang), show_alert=True)
        return

    # Karta borligini tekshirish
    card_number = user_data.get('card_number')
    if not card_number:
        await callback.answer(get_text("withdraw_no_card", lang), show_alert=True)
        return

    # Balansni tekshirish
    balance = user_data.get('balance', 0)
    pending_balance = user_data.get('pending_balance', 0)

    if balance < 25000:
        await callback.answer(get_text("withdraw_min_error", lang), show_alert=True)
        return

    prompt_text = get_text("withdraw_prompt", lang, balance=balance, pending_balance=pending_balance)
    await callback.message.edit_text(prompt_text, parse_mode="HTML")
    await state.set_state(WithdrawStates.waiting_for_amount)
    await callback.answer()


@router.message(WithdrawStates.waiting_for_amount)
async def process_withdraw_amount(message: Message, state: FSMContext):
    """Yechiladigan summani qabul qilish."""
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    user_data = await get_user(user_id)

    if not user_data:
        await state.clear()
        return

    text_amount = message.text.strip()
    if not text_amount.isdigit():
        await message.answer(get_text("withdraw_invalid_amount", lang), parse_mode="HTML")
        return

    amount = int(text_amount)
    balance = user_data.get('balance', 0)

    if amount < 25000:
        await message.answer(get_text("withdraw_min_error", lang), parse_mode="HTML")
        return

    if amount > balance:
        await message.answer(get_text("withdraw_insufficient", lang, amount=amount, balance=balance), parse_mode="HTML")
        return

    # Balansdan ayirish
    new_balance = balance - amount
    await update_balance(user_id, new_balance)

    # Tarixga qo'shish
    await add_user_history(user_id, "Pul yechish", "Kutilmoqda", amount)

    # Adminlarga bildirishnoma yuborish
    admin_ids_str = getenv("ADMIN_IDS", "")
    admin_ids = [int(aid.strip()) for aid in admin_ids_str.split(",") if aid.strip().isdigit()]
    
    admin_text = (
        f"💸 <b>Yangi pul yechish arizasi!</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {message.from_user.full_name} (@{message.from_user.username or 'yoq'})\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"💳 <b>Karta:</b> <code>{user_data.get('card_number')}</code>\n"
        f"💰 <b>Summa:</b> {amount} UZS"
    )

    for admin_id in admin_ids:
        try:
            await message.bot.send_message(admin_id, admin_text, parse_mode="HTML")
        except TelegramBadRequest:
            pass
        except Exception:
            pass

    # Holatni tozalash va foydalanuvchiga muvaffaqiyat xabarini yuborish
    await state.clear()
    await message.answer(
        get_text("withdraw_success", lang, amount=amount),
        reply_markup=get_profile_keyboard(lang),
        parse_mode="HTML"
    )
