"""Callback query handlerlari - inline tugmalar uchun."""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext

from database import (
    get_user,
    get_user_language,
    get_users_count,
    get_total_messages,
    update_user_language,
    update_notifications,
    update_card_number,
)
from keyboards import (
    get_main_menu_keyboard,
    get_back_keyboard,
    get_profile_keyboard,
    get_settings_keyboard,
    get_language_keyboard,
    get_notifications_keyboard,
)
from translations import get_text
from os import getenv

ADMIN_IDS = [int(i.strip()) for i in getenv("ADMIN_IDS", "").split(",") if i.strip()]

router = Router()


@router.callback_query(F.data == "profile")
async def callback_profile(callback: CallbackQuery):
    """Profil tugmasi bosilganda."""
    # Foydalanuvchi tilini olish
    lang = await get_user_language(callback.from_user.id)
    user_data = await get_user(callback.from_user.id)

    if user_data:
        # Tarjima qilingan profil matnini tuzish
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
        profile_text = get_text("profile_not_found", lang)

    await callback.message.edit_text(
        profile_text, reply_markup=get_profile_keyboard(lang), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "stats")
async def callback_stats(callback: CallbackQuery):
    """Statistika tugmasi bosilganda."""
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("Bu menyu faqat adminlar uchun.", show_alert=True)
        return
        
    # Foydalanuvchi tilini olish
    lang = await get_user_language(callback.from_user.id)
    users_count = await get_users_count()
    total_messages = await get_total_messages()

    # Tarjima qilingan statistika matnini tuzish
    stats_text = (
        get_text("stats_title", lang)
        + f"{get_text('stats_users', lang)}: {users_count}\n"
        + f"{get_text('stats_messages', lang)}: {total_messages or 0}\n"
    )

    await callback.message.edit_text(
        stats_text, reply_markup=get_back_keyboard(lang), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    """Yordam tugmasi bosilganda."""
    # Foydalanuvchi tilini olish
    lang = await get_user_language(callback.from_user.id)

    # Tarjima qilingan yordam matnini olish
    help_text = get_text("help_text", lang)

    await callback.message.edit_text(
        help_text, reply_markup=get_back_keyboard(lang), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "settings")
async def callback_settings(callback: CallbackQuery):
    """Sozlamalar tugmasi bosilganda."""
    # Foydalanuvchi tilini olish
    lang = await get_user_language(callback.from_user.id)

    # Tarjima qilingan sozlamalar matnini olish
    settings_text = get_text("settings_title", lang)

    await callback.message.edit_text(
        settings_text, reply_markup=get_settings_keyboard(lang), parse_mode="HTML"
    )
    await callback.answer()


# ===================== Til o'zgartirish handlerlari =====================


@router.callback_query(F.data == "change_lang")
async def callback_change_lang(callback: CallbackQuery):
    """Til tanlash klaviaturasini ko'rsatish."""
    # Foydalanuvchining joriy tilini olish
    lang = await get_user_language(callback.from_user.id)

    # Tilni tanlash matnini ko'rsatish
    text = get_text("change_lang_title", lang)

    await callback.message.edit_text(
        text, reply_markup=get_language_keyboard(lang), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "lang_uz")
async def callback_lang_uz(callback: CallbackQuery):
    """O'zbek tilini tanlash."""
    # Bazada tilni yangilash
    await update_user_language(callback.from_user.id, "uz")

    # Tasdiqlash xabarini yangi tilda ko'rsatish
    text = get_text("lang_changed", "uz")

    is_admin = callback.from_user.id in ADMIN_IDS
    await callback.message.edit_text(
        text, reply_markup=get_main_menu_keyboard("uz", is_admin), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "lang_en")
async def callback_lang_en(callback: CallbackQuery):
    """Ingliz tilini tanlash."""
    # Bazada tilni yangilash
    await update_user_language(callback.from_user.id, "en")

    # Tasdiqlash xabarini yangi tilda ko'rsatish
    text = get_text("lang_changed", "en")

    is_admin = callback.from_user.id in ADMIN_IDS
    await callback.message.edit_text(
        text, reply_markup=get_main_menu_keyboard("en", is_admin), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "lang_ru")
async def callback_lang_ru(callback: CallbackQuery):
    """Rus tilini tanlash."""
    # Bazada tilni yangilash
    await update_user_language(callback.from_user.id, "ru")

    # Tasdiqlash xabarini yangi tilda ko'rsatish
    text = get_text("lang_changed", "ru")

    is_admin = callback.from_user.id in ADMIN_IDS
    await callback.message.edit_text(
        text, reply_markup=get_main_menu_keyboard("ru", is_admin), parse_mode="HTML"
    )
    await callback.answer()


# ===================== Bildirishnomalar handlerlari =====================


@router.callback_query(F.data == "notifications")
async def callback_notifications(callback: CallbackQuery):
    """Bildirishnomalar sozlamalari klaviaturasini ko'rsatish."""
    # Foydalanuvchi tilini olish
    lang = await get_user_language(callback.from_user.id)

    # Bildirishnomalar sozlamalari matnini ko'rsatish
    text = get_text("notifications_title", lang)

    await callback.message.edit_text(
        text, reply_markup=get_notifications_keyboard(lang), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "notif_on")
async def callback_notif_on(callback: CallbackQuery):
    """Bildirishnomalarni yoqish."""
    # Bazada bildirishnomalarni yoqish
    await update_notifications(callback.from_user.id, True)

    # Foydalanuvchi tilini olish
    lang = await get_user_language(callback.from_user.id)

    # Tasdiqlash xabarini ko'rsatish
    text = get_text("notifications_enabled", lang)

    await callback.message.edit_text(
        text, reply_markup=get_settings_keyboard(lang), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "notif_off")
async def callback_notif_off(callback: CallbackQuery):
    """Bildirishnomalarni o'chirish."""
    # Bazada bildirishnomalarni o'chirish
    await update_notifications(callback.from_user.id, False)

    # Foydalanuvchi tilini olish
    lang = await get_user_language(callback.from_user.id)

    # Tasdiqlash xabarini ko'rsatish
    text = get_text("notifications_disabled", lang)

    await callback.message.edit_text(
        text, reply_markup=get_settings_keyboard(lang), parse_mode="HTML"
    )
    await callback.answer()


# ===================== Karta qo'shish va qo'llanma handlerlari =====================


@router.callback_query(F.data == "add_card")
async def callback_add_card(callback: CallbackQuery, state: FSMContext):
    """Karta qo'shish tugmasi bosilganda."""
    from handlers.card import CardStates
    lang = await get_user_language(callback.from_user.id)
    text = get_text("card_enter_number", lang)
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(CardStates.waiting_for_card)
    await callback.answer()


# ===================== Asosiy menyuga qaytish =====================


@router.callback_query(F.data == "back_to_menu")
async def callback_back_to_menu(callback: CallbackQuery):
    """Asosiy menyuga qaytish."""
    # Foydalanuvchi tilini olish
    lang = await get_user_language(callback.from_user.id)

    # Tarjima qilingan menyu matnini olish
    menu_text = get_text("main_menu", lang)

    is_admin = callback.from_user.id in ADMIN_IDS
    await callback.message.edit_text(
        menu_text, reply_markup=get_main_menu_keyboard(lang, is_admin), parse_mode="HTML"
    )
    await callback.answer()
