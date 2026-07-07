"""Ma'lumotlar bazasi moduli - Supabase bilan ishlash."""

from os import getenv
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ESLATMA: 'users' jadvalida quyidagi ustunlar bo'lishi kerak:
# - user_id (int8, primary key)
# - username (text)
# - full_name (text)
# - language_code (text, default: 'uz')
# - joined_at (timestamptz)
# - message_count (int4, default: 0)
# - notifications (bool, default: true) — bildirishnomalar uchun yangi ustun
# - balance (numeric, default: 0) — foydalanuvchi balansi
# - pending_balance (numeric, default: 0) — kutilayotgan balans
# - card_number (text, nullable) — Visa/Mastercard karta raqami
#
# ESLATMA: 'guide_pages' jadvalida quyidagi ustunlar bo'lishi kerak:
# - id (int8, primary key)
# - page_number (int4)
# - photo_id (text, nullable)
# - text_content (text)


async def add_user(user_id: int, username: str, full_name: str, language_code: str):
    """Yangi foydalanuvchini bazaga qo'shish yoki mavjudini yangilash."""
    user_data = {
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "language_code": language_code,
        "joined_at": datetime.now().isoformat(),
        "message_count": 0,
    }

    # Avval foydalanuvchi borligini tekshirish
    existing = supabase.table("users").select("*").eq("user_id", user_id).execute()

    if existing.data:
        # Mavjud foydalanuvchini yangilash
        supabase.table("users").update({
            "username": username,
            "full_name": full_name,
            "language_code": language_code,
        }).eq("user_id", user_id).execute()
    else:
        # Yangi foydalanuvchi qo'shish
        supabase.table("users").insert(user_data).execute()


async def get_user(user_id: int) -> dict | None:
    """Foydalanuvchi ma'lumotlarini olish."""
    result = supabase.table("users").select("*").eq("user_id", user_id).execute()
    if result.data:
        return result.data[0]
    return None


async def increment_message_count(user_id: int):
    """Foydalanuvchining xabarlar sonini oshirish."""
    user = supabase.table("users").select("message_count").eq("user_id", user_id).execute()
    if user.data:
        current_count = user.data[0]["message_count"] or 0
        supabase.table("users").update({
            "message_count": current_count + 1
        }).eq("user_id", user_id).execute()


async def get_users_count() -> int:
    """Barcha foydalanuvchilar sonini olish."""
    result = supabase.table("users").select("user_id", count="exact").execute()
    return result.count or 0


async def get_total_messages() -> int:
    """Barcha xabarlar sonini olish."""
    result = supabase.table("users").select("message_count").execute()
    total = sum(row["message_count"] or 0 for row in result.data)
    return total


async def update_user_language(user_id: int, language: str):
    """Foydalanuvchining tilini yangilash.

    Args:
        user_id: Foydalanuvchi ID raqami
        language: Yangi til kodi (uz, en, ru)
    """
    supabase.table("users").update({
        "language_code": language
    }).eq("user_id", user_id).execute()


async def get_user_language(user_id: int) -> str:
    """Foydalanuvchining til kodini qaytarish.

    Agar foydalanuvchi topilmasa yoki til belgilanmagan bo'lsa,
    standart 'uz' tilini qaytaradi.

    Args:
        user_id: Foydalanuvchi ID raqami

    Returns:
        Til kodi (uz, en, ru)
    """
    result = supabase.table("users").select("language_code").eq("user_id", user_id).execute()
    if result.data and result.data[0].get("language_code"):
        return result.data[0]["language_code"]
    return "uz"


async def update_notifications(user_id: int, enabled: bool):
    """Foydalanuvchining bildirishnomalar holatini yangilash.

    Args:
        user_id: Foydalanuvchi ID raqami
        enabled: True — yoqish, False — o'chirish
    """
    supabase.table("users").update({
        "notifications": enabled
    }).eq("user_id", user_id).execute()


async def get_all_users() -> list:
    """Barcha foydalanuvchilarni qaytarish (broadcast uchun).

    Returns:
        Foydalanuvchilar ro'yxati
    """
    result = supabase.table("users").select("*").execute()
    return result.data or []


async def get_users_with_notifications() -> list:
    """Bildirishnomalar yoqilgan foydalanuvchilarni qaytarish.

    Faqat notifications=True bo'lgan foydalanuvchilarni qaytaradi.

    Returns:
        Bildirishnomalar yoqilgan foydalanuvchilar ro'yxati
    """
    result = supabase.table("users").select("*").eq("notifications", True).execute()
    return result.data or []


async def update_card_number(user_id: int, card_number: str):
    """Foydalanuvchining karta raqamini saqlash.

    Args:
        user_id: Foydalanuvchi ID raqami
        card_number: 16 raqamli karta raqami
    """
    supabase.table("users").update({
        "card_number": card_number
    }).eq("user_id", user_id).execute()


async def update_balance(user_id: int, new_balance: float):
    """Foydalanuvchi balansini yangilash.

    Args:
        user_id: Foydalanuvchi ID raqami
        new_balance: Yangi balans qiymati
    """
    supabase.table("users").update({
        "balance": new_balance
    }).eq("user_id", user_id).execute()


async def add_guide_page(page_number: int, photo_id: str | None, text_content: str):
    """Qo'llanma sahifasini qo'shish."""
    supabase.table("guide_pages").insert({
        "page_number": page_number,
        "photo_id": photo_id,
        "text_content": text_content
    }).execute()


async def clear_guide():
    """Barcha qo'llanma sahifalarini o'chirish."""
    # Supabase'da barchasini o'chirish uchun filtrlash kerak, masalan, id > 0
    supabase.table("guide_pages").delete().gt("id", 0).execute()


async def get_guide_page(page_number: int) -> dict | None:
    """Belgilangan sahifani olish."""
    result = supabase.table("guide_pages").select("*").eq("page_number", page_number).execute()
    if result.data:
        return result.data[0]
    return None


async def get_guide_pages_count() -> int:
    """Jami sahifalar sonini olish."""
    result = supabase.table("guide_pages").select("id", count="exact").execute()
    return result.count or 0


async def get_setting(key: str) -> str | None:
    """Bot sozlamasini olish (masalan, pic1)."""
    result = supabase.table("bot_settings").select("value").eq("key", key).execute()
    if result.data:
        return result.data[0]["value"]
    return None


async def set_setting(key: str, value: str):
    """Bot sozlamasini saqlash yoki yangilash."""
    # Avval bor yoki yo'qligini tekshiramiz
    existing = await get_setting(key)
    if existing is not None:
        supabase.table("bot_settings").update({"value": value}).eq("key", key).execute()
    else:
        supabase.table("bot_settings").insert({"key": key, "value": value}).execute()


async def add_user_history(user_id: int, action_type: str, status: str, amount: float = 0):
    """Foydalanuvchi tarixini qo'shish."""
    supabase.table("user_history").insert({
        "user_id": user_id,
        "action_type": action_type,
        "status": status,
        "amount": amount,
        "created_at": datetime.now().isoformat()
    }).execute()


async def get_user_history(user_id: int) -> list:
    """Foydalanuvchi tarixini olish."""
    result = supabase.table("user_history").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return result.data or []


async def get_all_users_for_admin() -> list:
    """Admin uchun barcha foydalanuvchilarni oxirgi qo'shilganidan boshlab olish."""
    result = supabase.table("users").select("user_id, full_name, username, balance, pending_balance").order("joined_at", desc=True).limit(10).execute()
    return result.data or []
