"""Inline klaviaturalar moduli."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from translations import get_text


def get_main_menu_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Asosiy menyu inline klaviaturasi.

    Args:
        lang: Foydalanuvchi tili
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_profile", lang), callback_data="profile"),
            InlineKeyboardButton(text=get_text("btn_stats", lang), callback_data="stats"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_help", lang), callback_data="help"),
            InlineKeyboardButton(text=get_text("btn_settings", lang), callback_data="settings"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_guide", lang), callback_data="guide"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_channel", lang), url="https://t.me/your_channel"),
        ],
    ])
    return keyboard


def get_back_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Orqaga qaytish tugmasi.

    Args:
        lang: Foydalanuvchi tili
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_menu"),
        ],
    ])
    return keyboard


def get_profile_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Profil inline klaviaturasi.

    Args:
        lang: Foydalanuvchi tili
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_withdraw", lang), callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_menu"),
        ],
    ])
    return keyboard


def get_settings_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Sozlamalar inline klaviaturasi.

    Args:
        lang: Foydalanuvchi tili
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_change_lang", lang), callback_data="change_lang"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_add_card", lang), callback_data="add_card"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_notifications", lang), callback_data="notifications"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_menu"),
        ],
    ])
    return keyboard


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """Tasdiqlash klaviaturasi."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_no"),
        ],
    ])
    return keyboard


def get_language_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Til tanlash inline klaviaturasi.

    Args:
        lang: Foydalanuvchining joriy tili
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        ],
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="settings"),
        ],
    ])
    return keyboard


def get_notifications_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Bildirishnomalar sozlamalari inline klaviaturasi.

    Args:
        lang: Foydalanuvchi tili
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_notif_on", lang), callback_data="notif_on"),
            InlineKeyboardButton(text=get_text("btn_notif_off", lang), callback_data="notif_off"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="settings"),
        ],
    ])
    return keyboard
