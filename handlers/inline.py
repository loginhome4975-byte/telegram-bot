"""Inline queries handler."""

import hashlib
from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from database import get_user_history, supabase
from os import getenv

ADMIN_IDS = [int(i.strip()) for i in getenv("ADMIN_IDS", "").split(",") if i.strip()]

router = Router()


@router.inline_query(F.query == "history")
async def inline_history_handler(inline_query: InlineQuery):
    """Foydalanuvchi tarixini inline rejimda ko'rsatish."""
    user_id = inline_query.from_user.id
    history = await get_user_history(user_id)
    
    results = []
    
    if not history:
        results.append(
            InlineQueryResultArticle(
                id="no_history",
                title="Tarix bo'sh",
                description="Sizda hali hech qanday amal bajarilmagan.",
                input_message_content=InputTextMessageContent(
                    message_text="Mening tarixim hozircha bo'sh."
                )
            )
        )
    else:
        for idx, item in enumerate(history):
            action_type = item.get("action_type", "Noma'lum")
            status = item.get("status", "Noma'lum")
            amount = item.get("amount", 0)
            created_at = item.get("created_at", "")[:10]  # Just date
            
            # Create a unique ID for the result
            result_id = hashlib.md5(f"{user_id}_{idx}_{created_at}".encode()).hexdigest()
            
            text_content = (
                f"📝 <b>Amal:</b> {action_type}\n"
                f"💰 <b>Summa:</b> {amount:,.0f} UZS\n"
                f"📊 <b>Holat:</b> {status}\n"
                f"📅 <b>Sana:</b> {created_at}"
            )
            
            results.append(
                InlineQueryResultArticle(
                    id=result_id,
                    title=f"{action_type} - {amount:,.0f} UZS",
                    description=f"Holat: {status} | Sana: {created_at}",
                    input_message_content=InputTextMessageContent(
                        message_text=text_content,
                        parse_mode="HTML"
                    )
                )
            )
            
            # Limit to 50 results (Telegram's max per query)
            if len(results) >= 50:
                break
                
    await inline_query.answer(results, cache_time=1, is_personal=True)

@router.inline_query(F.query == "ok")
async def inline_admin_ok_handler(inline_query: InlineQuery):
    """Barcha foydalanuvchilar tarixini adminlarga ko'rsatish."""
    if inline_query.from_user.id not in ADMIN_IDS:
        return
        
    # Oxirgi 50 ta amaliyotni olish
    res = supabase.table("user_history").select("*").order("created_at", desc=True).limit(50).execute()
    history = res.data or []
    
    results = []
    
    if not history:
        results.append(
            InlineQueryResultArticle(
                id="no_global_history",
                title="Tarix bo'sh",
                description="Hali hech qanday foydalanuvchi amal bajarmagan.",
                input_message_content=InputTextMessageContent(
                    message_text="Umumiy tarix hozircha bo'sh."
                )
            )
        )
    else:
        for idx, item in enumerate(history):
            action_type = item.get("action_type", "Noma'lum")
            status = item.get("status", "Noma'lum")
            amount = item.get("amount", 0)
            created_at = item.get("created_at", "")[:19].replace("T", " ")
            u_id = item.get("user_id", "Noma'lum")
            
            result_id = hashlib.md5(f"global_{u_id}_{idx}_{created_at}".encode()).hexdigest()
            
            text_content = (
                f"👤 <b>User ID:</b> <code>{u_id}</code>\n"
                f"📝 <b>Amal:</b> {action_type}\n"
                f"💰 <b>Summa:</b> {amount:,.0f} UZS\n"
                f"📊 <b>Holat:</b> {status}\n"
                f"📅 <b>Vaqt:</b> {created_at}"
            )
            
            status_emoji = "✅" if status == "Tasdiqlandi" else "❌" if status == "Rad etildi" else "⏳"
            
            results.append(
                InlineQueryResultArticle(
                    id=result_id,
                    title=f"{status_emoji} {action_type} - {amount:,.0f} UZS",
                    description=f"User ID: {u_id} | Holat: {status}",
                    input_message_content=InputTextMessageContent(
                        message_text=text_content,
                        parse_mode="HTML"
                    )
                )
            )
                
    await inline_query.answer(results, cache_time=1, is_personal=True)

