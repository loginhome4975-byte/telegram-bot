# Telegram Bot

Aiogram 3 asosida yaratilgan to'liq funksional Telegram bot.

## Xususiyatlar

- ✅ /start va /help buyruqlari
- ✅ Inline tugmalar va callback handler'lar
- ✅ SQLite ma'lumotlar bazasi (foydalanuvchilarni saqlash)
- ✅ Profil ko'rish funksiyasi
- ✅ Statistika (admin uchun)

## O'rnatish

```bash
# Virtual muhit yaratish
python3 -m venv venv
source venv/bin/activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt
```

## Sozlash

1. [@BotFather](https://t.me/BotFather) orqali yangi bot yarating
2. `.env` faylida `BOT_TOKEN` ni o'zgartiring

## Ishga tushirish

```bash
python3 bot.py
```

## Loyiha tuzilishi

```
telegram-bot/
├── bot.py              # Asosiy bot fayli
├── database.py         # Ma'lumotlar bazasi
├── handlers/
│   ├── __init__.py
│   ├── start.py        # /start va /help
│   ├── profile.py      # Profil buyruqlari
│   └── callbacks.py    # Inline tugma callback'lari
├── keyboards/
│   ├── __init__.py
│   └── inline.py       # Inline klaviaturalar
├── requirements.txt
├── .env
└── .gitignore
```
