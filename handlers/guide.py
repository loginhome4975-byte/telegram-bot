"""Qo'llanma handlerlari - Pagination bilan."""

import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from deep_translator import GoogleTranslator

from database import get_guide_page, get_guide_pages_count, get_user_language
from keyboards import get_back_keyboard
from translations import get_text

router = Router()

async def translate_text(text: str, target_lang: str) -> str:
    if target_lang == 'uz' or not text:
        return text
    try:
        loop = asyncio.get_event_loop()
        translated = await loop.run_in_executor(
            None,
            lambda: GoogleTranslator(source='uz', target=target_lang).translate(text)
        )
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def get_guide_keyboard(current_page: int, total_pages: int, lang: str) -> InlineKeyboardMarkup:
    """Qo'llanma sahifalari uchun klaviatura."""
    buttons = []
    
    # Oldingi sahifa tugmasi
    if current_page > 1:
        buttons.append(InlineKeyboardButton(text=get_text("guide_prev", lang), callback_data=f"guide_page_{current_page - 1}"))
    
    # Keyingi sahifa tugmasi
    if current_page < total_pages:
        buttons.append(InlineKeyboardButton(text=get_text("guide_next", lang), callback_data=f"guide_page_{current_page + 1}"))
    
    keyboard = []
    if buttons:
        keyboard.append(buttons)
        
    # Sahifa raqami
    keyboard.append([InlineKeyboardButton(text=f"📄 {current_page}/{total_pages}", callback_data="ignore")])
    
    # Agar oxirgi sahifa bo'lsa, "Ishni boshlash" tugmasi chiqadi
    if current_page == total_pages:
        keyboard.append([InlineKeyboardButton(text=get_text("guide_start", lang), callback_data="generate_data")])
    
    # Orqaga (Asosiy menyuga)
    keyboard.append([InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.callback_query(F.data.startswith("guide"))
async def show_guide_page(callback: CallbackQuery, state: FSMContext):
    """Qo'llanma sahifasini ko'rsatish."""
    lang = await get_user_language(callback.from_user.id)
    
    total_pages = await get_guide_pages_count()
    if total_pages == 0:
        await callback.answer(get_text("guide_empty", lang), show_alert=True)
        return
        
    # Sahifani aniqlash
    if callback.data == "guide":
        page_num = 1
    else:
        try:
            page_num = int(callback.data.split("_")[2])
        except (IndexError, ValueError):
            page_num = 1
            
    # Sahifa ma'lumotlarini olish
    page_data = await get_guide_page(page_num)
    if not page_data:
        await callback.answer(get_text("guide_not_found", lang), show_alert=True)
        return
        
    keyboard = get_guide_keyboard(page_num, total_pages, lang)
    raw_text = page_data["text_content"]
    text = await translate_text(raw_text, lang)
    
    photo_id_str = page_data.get("photo_id")
    photo_ids = photo_id_str.split(",") if photo_id_str else []
    
    # Oldingi sahifadan qolgan albom rasmlarini o'chirish (tozalash)
    data = await state.get_data()
    old_msg_ids = data.get("guide_msg_ids", [])
    for msg_id in old_msg_ids:
        try:
            await callback.bot.delete_message(callback.message.chat.id, msg_id)
        except Exception:
            pass
    await state.update_data(guide_msg_ids=[])
    
    # Avvalgi xabarni o'chirish
    try:
        await callback.message.delete()
    except Exception:
        pass
    
    if len(photo_ids) > 1:
        # Albom yuborish (media group)
        media_group = [InputMediaPhoto(media=pid) for pid in photo_ids]
        msgs = await callback.message.answer_media_group(media=media_group)
        
        # Albom xabarlarini kelajakda o'chirish uchun saqlab qolish
        sent_ids = [m.message_id for m in msgs]
        await state.update_data(guide_msg_ids=sent_ids)
        
        # Matn va tugmani alohida yuborish
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        
    elif len(photo_ids) == 1:
        # Bitta rasm yuborish
        await callback.message.answer_photo(photo=photo_ids[0], caption=text, reply_markup=keyboard, parse_mode="HTML")
        
    else:
        # Faqat matn yuborish
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
            
    await callback.answer()
