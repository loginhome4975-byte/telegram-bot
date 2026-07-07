"""Admin buyruqlari handlerlari - broadcast va boshqaruv."""

import logging
from os import getenv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database import (
    get_users_with_notifications, get_user_language, add_guide_page, 
    clear_guide, get_guide_pages_count, set_setting, get_all_users_for_admin,
    get_user, get_user_history, supabase
)
from translations import get_text

logger = logging.getLogger(__name__)

router = Router()

# Admin ID larini muhit o'zgaruvchisidan olish (vergul bilan ajratilgan)
_admin_ids_raw = getenv("ADMIN_IDS", "")
ADMIN_IDS: list[int] = [
    int(x.strip()) for x in _admin_ids_raw.split(",") if x.strip().isdigit()
]


class BroadcastStates(StatesGroup):
    """Broadcast jarayoni uchun FSM holatlari."""
    waiting_for_message = State()


class AddGuideStates(StatesGroup):
    """Qo'llanma qo'shish jarayoni uchun FSM holatlari."""
    waiting_for_photo = State()
    waiting_for_text = State()


class SetPicStates(StatesGroup):
    """Rasm o'rnatish jarayoni uchun."""
    waiting_for_pic = State()


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, state: FSMContext):
    """/broadcast buyrug'i — faqat adminlar uchun.

    Admin xabar matnini kiritishi uchun FSM holatiga o'tkazadi.
    """
    # Foydalanuvchi admin ekanligini tekshirish
    if message.from_user.id not in ADMIN_IDS:
        lang = await get_user_language(message.from_user.id)
        await message.answer(get_text("broadcast_no_permission", lang))
        return

    # Admin tilini olish
    lang = await get_user_language(message.from_user.id)

    # FSM holatini broadcast xabar kutish holatiga o'tkazish
    await state.set_state(BroadcastStates.waiting_for_message)
    await message.answer(get_text("broadcast_enter_message", lang))


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """/cancel buyrug'i — joriy jarayonni bekor qilish."""
    # Joriy holatni tekshirish
    current_state = await state.get_state()
    if current_state is None:
        return

    # Admin tilini olish
    lang = await get_user_language(message.from_user.id)

    # FSM holatini tozalash
    await state.clear()
    await message.answer(get_text("broadcast_cancelled", lang))


@router.message(BroadcastStates.waiting_for_message, F.text)
async def process_broadcast_message(message: Message, state: FSMContext):
    """Broadcast xabar matnini qabul qilib, barcha foydalanuvchilarga yuborish.

    Faqat bildirishnomalar yoqilgan foydalanuvchilarga yuboradi.
    Muvaffaqiyatli va xatolik bilan yuborilgan xabarlar sonini hisobot qiladi.
    """
    # Admin tilini olish
    lang = await get_user_language(message.from_user.id)

    # FSM holatini tozalash
    await state.clear()

    # Bildirishnomalar yoqilgan foydalanuvchilarni olish
    users = await get_users_with_notifications()
    total = len(users)
    success = 0
    failed = 0

    # Har bir foydalanuvchiga xabar yuborish
    for user in users:
        try:
            await message.bot.send_message(
                chat_id=user["user_id"],
                text=message.text,
                parse_mode="HTML",
            )
            success += 1
        except Exception as e:
            # Xatolikni log qilish va davom ettirish
            logger.error(
                f"Broadcast xatolik — user_id={user['user_id']}: {e}"
            )
            failed += 1

    # Natijalarni adminga yuborish
    result_text = get_text(
        "broadcast_success",
        lang,
        count=f"{success}/{total}",
    )
    await message.answer(result_text)


@router.message(Command("add_guide"))
async def cmd_add_guide(message: Message, state: FSMContext):
    """/add_guide buyrug'i — qo'llanmaga yangi sahifa qo'shish."""
    if message.from_user.id not in ADMIN_IDS:
        return

    await state.set_state(AddGuideStates.waiting_for_photo)
    await state.update_data(photo_ids=[])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Rasmlar tayyor, matnga o'tish", callback_data="guide_photos_done")]
    ])
    await message.answer(
        "🖼 <b>1-qadam:</b> Yangi sahifa uchun rasmlarni yuboring (1 ta yoki birdaniga 3-4 ta albom qilib).\n\n"
        "<i>Rasmlarni yuborib bo'lgach, pastdagi tugmani bosing. Agar umuman rasm kerak bo'lmasa ham to'g'ridan-to'g'ri shu tugmani bosing.</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.message(AddGuideStates.waiting_for_photo, F.photo)
async def process_guide_photo(message: Message, state: FSMContext):
    """Qo'llanma rasmini qabul qilish (bir nechta bo'lishi mumkin)."""
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    photo_ids.append(message.photo[-1].file_id)
    await state.update_data(photo_ids=photo_ids)
    # Hech narsa yozmaymiz, chunki albom kelganda xabar ko'payib ketadi


@router.callback_query(F.data == "guide_photos_done", AddGuideStates.waiting_for_photo)
async def cb_guide_photos_done(callback: CallbackQuery, state: FSMContext):
    """Rasmlar yuklanib bo'lgach matnga o'tish."""
    await state.set_state(AddGuideStates.waiting_for_text)
    await callback.message.edit_text(
        "📝 <b>2-qadam:</b> Endi ushbu sahifa uchun matnni yuboring:",
        parse_mode="HTML"
    )


@router.message(AddGuideStates.waiting_for_text, F.text)
async def process_guide_text(message: Message, state: FSMContext):
    """Qo'llanma matnini qabul qilish va bazaga saqlash."""
    text_content = message.text or ""
    
    if not text_content:
        await message.answer("Sahifada matn bo'lishi shart! Matnni yuboring:")
        return

    # Oldin saqlangan rasm ID larini olamiz
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    photo_id_str = ",".join(photo_ids) if photo_ids else None

    # Telegram rasm izohi uchun 1024 belgi cheklovi (faqat bitta rasm bo'lsa bu limit ishlaydi)
    if len(photo_ids) == 1 and len(text_content) > 1000:
        await message.answer(f"⚠️ Xatolik: Bitta rasm bilan birga yuboriladigan matn 1000 ta belgidan oshmasligi kerak (Sizniki: {len(text_content)} belgi).\n\nIltimos, matnni qisqartirib qaytadan yuboring:")
        return

    # Sahifa tartib raqamini aniqlash (oldindagilar soni + 1)
    current_count = await get_guide_pages_count()
    page_number = current_count + 1

    # Bazaga qo'shish
    await add_guide_page(page_number, photo_id_str, text_content)

    await state.clear()
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Yana sahifa qo'shish", callback_data="add_guide_next")],
        [InlineKeyboardButton(text="✅ Yakunlash", callback_data="add_guide_finish")]
    ])
    
    await message.answer(
        f"✅ Qo'llanmaning {page_number}-sahifasi muvaffaqiyatli saqlandi!\n\nDavom etamizmi?",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "add_guide_next")
async def cb_add_guide_next(callback: CallbackQuery, state: FSMContext):
    """Yana sahifa qo'shish tugmasi."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    await state.set_state(AddGuideStates.waiting_for_photo)
    await state.update_data(photo_ids=[])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Rasmlar tayyor, matnga o'tish", callback_data="guide_photos_done")]
    ])
    await callback.message.edit_text(
        "🖼 <b>1-qadam:</b> Yangi sahifa uchun rasmlarni yuboring (1 ta yoki birdaniga 3-4 ta albom qilib).\n\n"
        "<i>Rasmlarni yuborib bo'lgach, pastdagi tugmani bosing.</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data == "add_guide_finish")
async def cb_add_guide_finish(callback: CallbackQuery, state: FSMContext):
    """Qo'llanma qo'shishni yakunlash tugmasi."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    await state.clear()
    await callback.message.edit_text("✅ Qo'llanma yaratish yakunlandi. Barcha sahifalar saqlandi!")


@router.message(Command("clear_guide"))
async def cmd_clear_guide(message: Message):
    """/clear_guide buyrug'i — barcha qo'llanmani o'chirish."""
    if message.from_user.id not in ADMIN_IDS:
        return

    await clear_guide()
    await message.answer("🗑 Barcha qo'llanma sahifalari o'chirildi.")


@router.message(Command("pic1", "pic2", "pic3", "pic4", "pic5", "pic6"))
async def cmd_pic(message: Message, state: FSMContext):
    """/pic1.../pic6 buyruqlari — ro'yxatdan o'tish qadamlari uchun rasmlarni o'rnatish."""
    if message.from_user.id not in ADMIN_IDS:
        return

    # Qaysi komanda bosilganini aniqlash (masalan: "pic1")
    command_name = message.text.split()[0][1:]
    
    await state.update_data(current_pic_key=command_name)
    await state.set_state(SetPicStates.waiting_for_pic)
    await message.answer(f"📸 Iltimos, <b>{command_name}</b> uchun rasmni yuboring:", parse_mode="HTML")


@router.message(SetPicStates.waiting_for_pic, F.photo)
async def process_pic(message: Message, state: FSMContext):
    """Rasm qabul qilib saqlash."""
    data = await state.get_data()
    pic_key = data.get("current_pic_key")
    
    if not pic_key:
        await state.clear()
        return

    photo_id = message.photo[-1].file_id
    await set_setting(pic_key, photo_id)
    await state.clear()
    await message.answer(f"✅ <b>{pic_key}</b> muvaffaqiyatli saqlandi! Endi u ro'yxatdan o'tish jarayonida yuboriladi.", parse_mode="HTML")


@router.message(Command("edit"))
async def cmd_edit(message: Message):
    """/edit buyrug'i - foydalanuvchilarni tahrirlash."""
    if message.from_user.id not in ADMIN_IDS:
        return

    parts = message.text.split()
    if len(parts) == 1:
        # Show list of 10 users
        users = await get_all_users_for_admin()
        text = "👥 <b>Oxirgi foydalanuvchilar:</b>\n\n"
        for u in users:
            text += f"ID: <code>{u['user_id']}</code> - {u['full_name']} (@{u.get('username') or 'yoq'})\n"
        text += "\n<i>Boshqarish uchun /edit <user_id> deb yozing.</i>"
        await message.answer(text, parse_mode="HTML")
    else:
        user_id_str = parts[1]
        if not user_id_str.isdigit():
            await message.answer("❌ Noto'g'ri ID format.")
            return
            
        user_id = int(user_id_str)
        user = await get_user(user_id)
        if not user:
            await message.answer("❌ Foydalanuvchi topilmadi.")
            return
            
        history = await get_user_history(user_id)
        
        text = (
            f"👤 <b>Foydalanuvchi:</b> {user['full_name']}\n"
            f"🆔 <b>ID:</b> <code>{user['user_id']}</code>\n"
            f"💰 <b>Asosiy balans:</b> {user.get('balance', 0):,.0f} UZS\n"
            f"⏳ <b>Kutilayotgan balans:</b> {user.get('pending_balance', 0):,.0f} UZS\n\n"
            f"📋 <b>Oxirgi amallar:</b>\n"
        )
        
        for h in history[:5]: # Show last 5
            text += f"- {h['action_type']} ({h['amount']:,.0f} UZS) - {h['status']}\n"
            
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ro'yxatdan o'tishni tasdiqlash", callback_data=f"approve_reg_{user_id}")],
            [InlineKeyboardButton(text="✅ Pul yechishni tasdiqlash", callback_data=f"approve_withdraw_{user_id}")]
        ])
        
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("approve_reg_"))
async def cb_approve_reg(callback: CallbackQuery):
    """Kutilayotgan ro'yxatdan o'tish pulini asosiyga o'tkazish."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    user_id = int(callback.data.split("_")[2])
    user = await get_user(user_id)
    
    if not user:
        await callback.answer("Foydalanuvchi topilmadi.", show_alert=True)
        return
        
    pending = float(user.get("pending_balance") or 0)
    balance = float(user.get("balance") or 0)
    
    if pending <= 0:
        await callback.answer("Kutilayotgan pul yo'q.", show_alert=True)
        return
        
    new_balance = balance + pending
    supabase.table("users").update({
        "balance": new_balance,
        "pending_balance": 0
    }).eq("user_id", user_id).execute()
    
    # Tarixni yangilash
    supabase.table("user_history").update({"status": "Tasdiqlandi"}).eq("user_id", user_id).eq("action_type", "Ro'yxatdan o'tish").eq("status", "Kutilmoqda").execute()
    
    await callback.answer("Tasdiqlandi!", show_alert=True)
    await callback.message.edit_text(f"✅ Foydalanuvchi ({user_id}) tasdiqlandi.\nAsosiy balansiga qo'shildi.")


@router.callback_query(F.data.startswith("approve_withdraw_"))
async def cb_approve_withdraw(callback: CallbackQuery):
    """Pul yechishni tasdiqlash."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    user_id = int(callback.data.split("_")[2])
    # Pul yechish allaqachon balansdan ayirilgan, shunchaki statusni yangilaymiz
    supabase.table("user_history").update({"status": "Tasdiqlandi"}).eq("user_id", user_id).eq("action_type", "Pul yechish").eq("status", "Kutilmoqda").execute()
    
    await callback.answer("Tasdiqlandi!", show_alert=True)
    await callback.message.edit_text(f"✅ Pul yechish ({user_id}) tasdiqlandi.")
