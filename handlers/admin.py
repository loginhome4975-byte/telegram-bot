"""Admin buyruqlari handlerlari - broadcast va boshqaruv."""

import logging
from os import getenv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile
import csv
import io
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database import (
    get_users_with_notifications, get_user_language, add_guide_page, 
    clear_guide, get_guide_pages_count, set_setting, get_all_users_for_admin,
    get_user, get_user_history, supabase, get_user_history_by_action,
    update_history_status, update_user_balances, get_history_by_id
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


@router.message(Command("ok"))
async def cmd_ok(message: Message):
    """/ok <user_id> buyrug'i - pul yechishni boshqarish."""
    if message.from_user.id not in ADMIN_IDS:
        return

    parts = message.text.split()
    if len(parts) == 1:
        await message.answer("❌ Foydalanuvchi ID sini kiriting: /ok <user_id>")
        return

    user_id_str = parts[1]
    if not user_id_str.isdigit():
        await message.answer("❌ Noto'g'ri ID format.")
        return

    user_id = int(user_id_str)
    
    history = await get_user_history_by_action(user_id, "Pul yechish", "Kutilmoqda")
    
    if not history:
        await message.answer(f"❌ {user_id} uchun kutilayotgan pul yechish so'rovlari topilmadi.")
        return
        
    for h in history:
        history_id = h.get("id")
        amount = h.get("amount", 0)
        date = h.get("created_at", "")[:19].replace("T", " ")
        
        text = (
            f"💸 <b>Pul yechish so'rovi</b>\n\n"
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
            f"💰 <b>Miqdor:</b> {amount:,.0f} UZS\n"
            f"📅 <b>Sana:</b> {date}"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlandi (Approve)", callback_data=f"withdraw_approve_{history_id}_{user_id}"),
                InlineKeyboardButton(text="❌ Rad etildi (Reject)", callback_data=f"withdraw_reject_{history_id}_{user_id}")
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("withdraw_approve_"))
async def cb_withdraw_approve(callback: CallbackQuery):
    """Pul yechishni tasdiqlash."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    parts = callback.data.split("_")
    history_id = int(parts[2])
    user_id = int(parts[3])
    
    await update_history_status(history_id, "Tasdiqlandi")
    
    await callback.answer("Tasdiqlandi!", show_alert=True)
    await callback.message.edit_text(callback.message.text + "\n\n✅ <b>Holati:</b> Tasdiqlandi")


@router.callback_query(F.data.startswith("withdraw_reject_"))
async def cb_withdraw_reject(callback: CallbackQuery):
    """Pul yechishni rad etish va pulni qaytarish."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    parts = callback.data.split("_")
    history_id = int(parts[2])
    user_id = int(parts[3])
    
    history = await get_history_by_id(history_id)
    if not history or history.get("status") != "Kutilmoqda":
        await callback.answer("So'rov topilmadi yoki allaqachon ko'rib chiqilgan.", show_alert=True)
        return
        
    amount = float(history.get("amount", 0))
    
    await update_history_status(history_id, "Rad etildi")
    await update_user_balances(user_id, balance_change=amount)
    
    await callback.answer("Rad etildi. Pul balansga qaytarildi.", show_alert=True)
    await callback.message.edit_text(callback.message.text + "\n\n❌ <b>Holati:</b> Rad etildi (Pul balansga qaytarildi)")


@router.message(Command("edit"))
async def cmd_edit(message: Message):
    """/edit buyrug'i - ro'yxatdan o'tishni tasdiqlash."""
    if message.from_user.id not in ADMIN_IDS:
        return

    parts = message.text.split()
    if len(parts) == 1:
        await message.answer("❌ Foydalanuvchi ID sini kiriting: /edit <user_id>")
        return

    user_id_str = parts[1]
    if not user_id_str.isdigit():
        await message.answer("❌ Noto'g'ri ID format.")
        return

    user_id = int(user_id_str)
    
    history = await get_user_history_by_action(user_id, "Ro'yxatdan o'tish", "Kutilmoqda")
    
    if not history:
        await message.answer(f"❌ {user_id} uchun kutilayotgan ro'yxatdan o'tish so'rovlari topilmadi.")
        return
        
    for h in history:
        history_id = h.get("id")
        amount = h.get("amount", 0)
        date = h.get("created_at", "")[:19].replace("T", " ")
        
        text = (
            f"👤 <b>Ro'yxatdan o'tish so'rovi</b>\n\n"
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
            f"💰 <b>Miqdor:</b> {amount:,.0f} UZS\n"
            f"📅 <b>Sana:</b> {date}"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Asosiy balansga o'tkazish", callback_data=f"reg_approve_{history_id}_{user_id}"),
                InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reg_reject_{history_id}_{user_id}")
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("reg_approve_"))
async def cb_reg_approve(callback: CallbackQuery):
    """Kutilayotgan ro'yxatdan o'tish pulini asosiyga o'tkazish."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    parts = callback.data.split("_")
    history_id = int(parts[2])
    user_id = int(parts[3])
    
    history = await get_history_by_id(history_id)
    if not history or history.get("status") != "Kutilmoqda":
        await callback.answer("So'rov topilmadi yoki allaqachon ko'rib chiqilgan.", show_alert=True)
        return
        
    amount = float(history.get("amount", 0))
    
    await update_history_status(history_id, "Tasdiqlandi")
    await update_user_balances(user_id, balance_change=amount, pending_balance_change=-amount)
    
    await callback.answer("Tasdiqlandi va balansga qo'shildi!", show_alert=True)
    await callback.message.edit_text(callback.message.text + "\n\n✅ <b>Holati:</b> Tasdiqlandi (Asosiy balansga o'tkazildi)")


@router.callback_query(F.data.startswith("reg_reject_"))
async def cb_reg_reject(callback: CallbackQuery):
    """Ro'yxatdan o'tishni rad etish va kutilayotgan balansni kamaytirish."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    parts = callback.data.split("_")
    history_id = int(parts[2])
    user_id = int(parts[3])
    
    history = await get_history_by_id(history_id)
    if not history or history.get("status") != "Kutilmoqda":
        await callback.answer("So'rov topilmadi yoki allaqachon ko'rib chiqilgan.", show_alert=True)
        return
        
    amount = float(history.get("amount", 0))
    
    await update_history_status(history_id, "Rad etildi")
    await update_user_balances(user_id, balance_change=0, pending_balance_change=-amount)
    
    await callback.answer("Rad etildi va kutilayotgan balansdan ayirildi.", show_alert=True)
    await callback.message.edit_text(callback.message.text + "\n\n❌ <b>Holati:</b> Rad etildi (Kutilayotgan balansdan ayirildi)")

@router.callback_query(F.data.startswith("reg_skip_"))
async def cb_reg_skip(callback: CallbackQuery):
    """Vazifa to'g'risidagi xabarni e'tiborsiz qoldirish."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    try:
        await callback.message.delete()
    except Exception:
        await callback.message.edit_text(callback.message.text + "\n\n⏭ <b>Holati:</b> E'tiborsiz qoldirildi (Skip)")
    await callback.answer("Xabar o'chirildi.", show_alert=False)

@router.callback_query(F.data == "admin_tasks")
async def cb_admin_tasks(callback: CallbackQuery):
    """Admin uchun barcha ishlarni CSV formatida yuklab berish."""
    if callback.from_user.id not in ADMIN_IDS:
        return
        
    res = supabase.table("user_history").select("*").eq("action_type", "Ro'yxatdan o'tish").order("created_at", desc=True).execute()
    data = res.data or []
    
    if not data:
        await callback.answer("Hozircha hech qanday ishlar mavjud emas.", show_alert=True)
        return
        
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User ID", "Holat", "Summa", "Sana", "Email", "Parol", "Ism", "Familiya", "Manzil", "Shahar", "Viloyat", "Pochta indeksi", "Telefon"])
    
    for item in data:
        details = item.get("details") or {}
        writer.writerow([
            item.get("id", ""),
            item.get("user_id", ""),
            item.get("status", ""),
            item.get("amount", ""),
            item.get("created_at", "")[:19].replace("T", " "),
            details.get("email", ""),
            details.get("password", ""),
            details.get("first_name", ""),
            details.get("last_name", ""),
            details.get("address", ""),
            details.get("city", ""),
            details.get("state", ""),
            details.get("postal", ""),
            details.get("phone", ""),
        ])
        
    csv_bytes = output.getvalue().encode('utf-8')
    file = BufferedInputFile(csv_bytes, filename="ishlar_royxati.csv")
    
    await callback.message.answer_document(
        document=file,
        caption="📁 Barcha ishlar ro'yxati (CSV formatda)"
    )
    await callback.answer()
