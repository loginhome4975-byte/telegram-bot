"""Ma'lumotlarni generatsiya qilish handlerlari."""

import random
import string
import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import get_setting, supabase

router = Router()

class RegistrationStates(StatesGroup):
    data_generated = State()

# ===================== Generatsiya ma'lumotlari =====================

FIRST_NAMES = [
    "Aziz", "Sardor", "Nodir", "Alisher", "Bekzod", "Rustam", "Jasur", "Timur",
    "Dilshod", "Sherzod", "Malika", "Zarina", "Nigora", "Shahnoza", "Dildora",
    "Nilufar", "Umida", "Gulnoza", "Sevara", "Madina"
]

LAST_NAMES = [
    "Karimov", "Abdullayev", "Rahimov", "Nazarov", "Yusupov", "Ibragimov", 
    "Sodiqov", "Turdiyev", "Jalilov", "Qosimov", "Karimova", "Abdullayeva",
    "Rahimova", "Nazarova", "Yusupova", "Ibragimova"
]

CITIES_DATA = [
    {"city": "Tashkent", "state": "Tashkent", "postal": "100000"},
    {"city": "Samarkand", "state": "Samarkand", "postal": "140100"},
    {"city": "Bukhara", "state": "Bukhara", "postal": "200100"},
    {"city": "Fergana", "state": "Fergana", "postal": "150100"},
    {"city": "Namangan", "state": "Namangan", "postal": "160100"},
    {"city": "Andijan", "state": "Andijan", "postal": "170100"},
    {"city": "Navoi", "state": "Navoi", "postal": "210100"},
    {"city": "Nukus", "state": "Karakalpakstan", "postal": "230100"},
    {"city": "Urgench", "state": "Khorezm", "postal": "220100"},
    {"city": "Karshi", "state": "Kashkadarya", "postal": "180100"},
    {"city": "Jizzakh", "state": "Jizzakh", "postal": "130100"},
    {"city": "Termez", "state": "Surkhandarya", "postal": "190100"},
    {"city": "Gulistan", "state": "Syrdarya", "postal": "120100"},
]

STREETS = [
    "Navoi street", "Amir Temur avenue", "Mirzo Ulugbek street", 
    "Pushkin street", "Tashkent street", "Shota Rustaveli street",
    "Mukimi street", "Furkat street", "Buyuk Ipak Yuli"
]

PHONE_PREFIXES = ["90", "91", "93", "94", "97", "98", "99", "33", "88", "77", "55"]

def generate_password(length=10):
    """Tasodifiy parol generatsiya qilish."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(characters) for _ in range(length))

def generate_phone():
    """Tasodifiy O'zbekiston raqamini generatsiya qilish."""
    prefix = random.choice(PHONE_PREFIXES)
    number = "".join(random.choice(string.digits) for _ in range(7))
    return f"+998{prefix}{number}"


@router.callback_query(F.data == "generate_data")
async def callback_generate_data(callback: CallbackQuery, state: FSMContext):
    """Ishni boshlash tugmasi bosilganda ma'lumotlarni generatsiya qilib yuborish (1-qadam)."""
    
    # Ma'lumotlarni generatsiya qilish yoki oldingisini olish
    data = await state.get_data()
    if "reg_email" not in data:
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        password = generate_password(random.randint(8, 12))
        city_data = random.choice(CITIES_DATA)
        address1 = f"{random.choice(STREETS)}, {random.randint(1, 150)}"
        phone = generate_phone()
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@gmail.com"
        
        await state.update_data(
            reg_email=email, reg_password=password, reg_first=first_name,
            reg_last=last_name, reg_address=address1, reg_city=city_data['city'],
            reg_state=city_data['state'], reg_postal=city_data['postal'],
            reg_phone=phone
        )
    else:
        email = data["reg_email"]
        password = data["reg_password"]
        first_name = data["reg_first"]
        last_name = data["reg_last"]
        address1 = data["reg_address"]
        city_data = {"city": data["reg_city"], "state": data["reg_state"], "postal": data["reg_postal"]}
        phone = data["reg_phone"]

    text = (
        "📋 <b>Sizning ro'yxatdan o'tish ma'lumotlaringiz:</b>\n\n"
        f"<b>Email address:</b> <code>{email}</code>\n"
        f"<b>Password:</b> <code>{password}</code>\n"
        f"<b>Repeat password:</b> <code>{password}</code>\n"
        f"<b>First name:</b> <code>{first_name}</code>\n"
        f"<b>Last name:</b> <code>{last_name}</code>\n"
        f"<b>Address 1:</b> <code>{address1}</code>\n"
        f"<b>Address 2:</b> <i>(To'ldirilmaydi)</i>\n"
        f"<b>City:</b> <code>{city_data['city']}</code>\n"
        f"<b>State:</b> <code>{city_data['state']}</code>\n"
        f"<b>Country:</b> <code>Uzbekistan</code>\n"
        f"<b>Postal code:</b> <code>{city_data['postal']}</code>\n"
        f"<b>Mobile phone number:</b> <code>{phone}</code>\n"
        f"<b>Account type:</b> <code>Personal</code>\n"
        f"<b>Phone:</b> <i>(To'ldirilmaydi)</i>\n\n"
        "<i>Ma'lumotlardan foydalanib, rasmdagi formani to'ldiring!</i>"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ To'ldirdim va ro'yxatdan o'tish yakunlandi", callback_data="reg_step_2")]
    ])

    pic1_id = await get_setting("pic1")
    
    # Xabarni tozalash va yangisini yuborish
    try:
        await callback.message.delete()
    except Exception:
        pass

    if pic1_id:
        await callback.message.answer_photo(photo=pic1_id, caption=text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        
    await callback.answer()

@router.callback_query(F.data == "reg_step_2")
async def cb_reg_step_2(callback: CallbackQuery):
    """2-qadam."""
    text = (
        "🎉 Muvaffaqiyatli ro'yxatdan o'tganingiz bilan tabriklaymiz!!!\n\n"
        "Davom etamiz, ehtimol siz rasmdagi holatga yetib keldingiz.\n"
        "Yetib kelgan bo'lsangiz, ikkinchi rasmda belgilab ko'rsatilgan sariq tugma <b>'Order more'</b> ni bosing."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Bosdim", callback_data="reg_step_3")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="generate_data")]
    ])
    await _send_step(callback, "pic2", text, keyboard)

@router.callback_query(F.data == "reg_step_3")
async def cb_reg_step_3(callback: CallbackQuery):
    """3-qadam."""
    text = (
        "👍 Yaxshi, bosilgan bo'lsa sizda rasmdagi holat ochiladi.\n"
        "Bu ro'yxatdan belgilab ko'rsatilgani tanlab bosiladi."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Bosdim", callback_data="reg_step_4")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="reg_step_2")]
    ])
    await _send_step(callback, "pic3", text, keyboard)

@router.callback_query(F.data == "reg_step_4")
async def cb_reg_step_4(callback: CallbackQuery):
    """4-qadam."""
    text = "Endi sizda mana bu rasmdagidek to'ldirilmagan holat ochiladi."
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Keyingisi ➡️", callback_data="reg_step_5")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="reg_step_3")]
    ])
    await _send_step(callback, "pic4", text, keyboard)

@router.callback_query(F.data == "reg_step_5")
async def cb_reg_step_5(callback: CallbackQuery):
    """5-qadam."""
    text = (
        "Endi siz bu holatni xuddi rasmdagidek qilib konfiguratsiya qilasiz.\n"
        "Bunga taxminan 2 daqiqa ketadi.\n\n"
        "⚠️ <b>Eslataman:</b> Hech narsa rasmdagidan ortiqcha yoki kam bo'lmasligi zarur, hammasi huddi rasmdagidek bo'lsin!"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Keyingisi ➡️", callback_data="reg_step_6")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="reg_step_4")]
    ])
    await _send_step(callback, "pic5", text, keyboard)

@router.callback_query(F.data == "reg_step_6")
async def cb_reg_step_6(callback: CallbackQuery):
    """6-qadam."""
    text = (
        "Endi esa ochilgan sahifani biroz pastga tushirasiz (xuddi rasmdagi holat bo'yicha).\n"
        "Pastga yetib kelganingizda sizdan <b>karta ma'lumotlarini</b> to'ldirish so'raladi.\n\n"
        "Siz o'sha kartangizning:\n"
        "🔹 Turini tanlaysiz\n"
        "🔹 Karta raqamini yozasiz\n"
        "🔹 Amal qilish muddatini yozasiz\n"
        "🔹 'Name' joyiga karta egasining ismini yozasiz\n"
        "🔹 Va orqasidagi 3 xonali tasdiq kodini (CVV) yozasiz\n\n"
        "Shundan keyin <b>Checkout</b> tugmasini bosasiz. Sizdan 13 000 UZS yechib olinadi (sms kod kelishi yoki avtomatik yechilishi mumkin).\n"
        "Hammasi bajarilgandan keyin yuqoridan nimadir 'loading' bo'ladi, uning aylanishini kutasiz (taxminan 5-6 daqiqa).\n\n"
        "Va oxirida yakunlash tugmasini bosasiz."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Yakunlash", callback_data="reg_step_finish")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="reg_step_5")]
    ])
    await _send_step(callback, "pic6", text, keyboard)

@router.callback_query(F.data == "reg_step_finish")
async def cb_reg_step_finish(callback: CallbackQuery, state: FSMContext):
    """Yakunlash va pul qo'shish."""
    amount = random.randint(60000, 80000)
    user_id = callback.from_user.id
    
    # Bazadagi pending_balance ga qo'shish
    user_data = supabase.table("users").select("pending_balance").eq("user_id", user_id).execute()
    if user_data.data:
        current_pending = float(user_data.data[0].get("pending_balance") or 0)
        new_pending = current_pending + amount
        supabase.table("users").update({"pending_balance": new_pending}).eq("user_id", user_id).execute()
    
    text = (
        "🎉 <b>Tashakkur! Barcha bosqichlar muvaffaqiyatli yakunlandi.</b>\n\n"
        f"Sizning kutilayotgan balansingizga <b>{amount:,.0f} UZS</b> qo'shildi!\n\n"
        "⏳ Ushbu mablag' tez orada asosiy balansingizga o'tadi, iltimos kuting."
    )
    
    try:
        await callback.message.delete()
    except Exception:
        pass
        
    await callback.message.answer(text, parse_mode="HTML")
    await state.clear()
    await callback.answer()

async def _send_step(callback: CallbackQuery, pic_key: str, text: str, keyboard: InlineKeyboardMarkup):
    """Qadamlarni yuborish uchun yordamchi funksiya."""
    pic_id = await get_setting(pic_key)
    
    try:
        await callback.message.delete()
    except Exception:
        pass

    if pic_id:
        await callback.message.answer_photo(photo=pic_id, caption=text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
        
    await callback.answer()
