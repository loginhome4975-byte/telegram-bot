"""Ma'lumotlarni generatsiya qilish handlerlari."""

import random
import string
import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import get_setting, supabase, get_user_language
from translations import get_text

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
    
    lang = await get_user_language(callback.from_user.id)
    
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

    text = get_text(
        "gen_reg_data", lang,
        email=email, password=password, first_name=first_name,
        last_name=last_name, address1=address1, city=city_data['city'],
        state=city_data['state'], postal=city_data['postal'], phone=phone
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_reg_step_1", lang), callback_data="reg_step_2")]
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
    lang = await get_user_language(callback.from_user.id)
    text = get_text("gen_step_2", lang)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_clicked", lang), callback_data="reg_step_3")],
        [InlineKeyboardButton(text=get_text("btn_back_nav", lang), callback_data="generate_data")]
    ])
    await _send_step(callback, "pic2", text, keyboard)

@router.callback_query(F.data == "reg_step_3")
async def cb_reg_step_3(callback: CallbackQuery):
    """3-qadam."""
    lang = await get_user_language(callback.from_user.id)
    text = get_text("gen_step_3", lang)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_clicked", lang), callback_data="reg_step_4")],
        [InlineKeyboardButton(text=get_text("btn_back_nav", lang), callback_data="reg_step_2")]
    ])
    await _send_step(callback, "pic3", text, keyboard)

@router.callback_query(F.data == "reg_step_4")
async def cb_reg_step_4(callback: CallbackQuery):
    """4-qadam."""
    lang = await get_user_language(callback.from_user.id)
    text = get_text("gen_step_4", lang)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_next", lang), callback_data="reg_step_5")],
        [InlineKeyboardButton(text=get_text("btn_back_nav", lang), callback_data="reg_step_3")]
    ])
    await _send_step(callback, "pic4", text, keyboard)

@router.callback_query(F.data == "reg_step_5")
async def cb_reg_step_5(callback: CallbackQuery):
    """5-qadam."""
    lang = await get_user_language(callback.from_user.id)
    text = get_text("gen_step_5", lang)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_next", lang), callback_data="reg_step_6")],
        [InlineKeyboardButton(text=get_text("btn_back_nav", lang), callback_data="reg_step_4")]
    ])
    await _send_step(callback, "pic5", text, keyboard)

@router.callback_query(F.data == "reg_step_6")
async def cb_reg_step_6(callback: CallbackQuery):
    """6-qadam."""
    lang = await get_user_language(callback.from_user.id)
    text = get_text("gen_step_6", lang)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_finish", lang), callback_data="reg_step_finish")],
        [InlineKeyboardButton(text=get_text("btn_back_nav", lang), callback_data="reg_step_5")]
    ])
    await _send_step(callback, "pic6", text, keyboard)

@router.callback_query(F.data == "reg_step_finish")
async def cb_reg_step_finish(callback: CallbackQuery, state: FSMContext):
    """Yakunlash va pul qo'shish."""
    lang = await get_user_language(callback.from_user.id)
    amount = random.randint(60000, 80000)
    user_id = callback.from_user.id
    
    # Bazadagi pending_balance ga qo'shish
    user_data = supabase.table("users").select("pending_balance").eq("user_id", user_id).execute()
    if user_data.data:
        current_pending = float(user_data.data[0].get("pending_balance") or 0)
        new_pending = current_pending + amount
        supabase.table("users").update({"pending_balance": new_pending}).eq("user_id", user_id).execute()
    
    text = get_text("gen_finish", lang, amount=f"{amount:,.0f}")
    
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
