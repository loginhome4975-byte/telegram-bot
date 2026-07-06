"""Tarjimalar moduli - 3 tilda (uz, en, ru) bot xabarlari."""

# Barcha tarjimalar lug'ati
TRANSLATIONS = {
    "uz": {
        # Asosiy xabarlar
        "welcome": "👋 Assalomu alaykum, {name}!\n\n🤖 Botimizga xush kelibsiz!\nQuyidagi menyudan kerakli bo'limni tanlang:",
        "main_menu": "🏠 Asosiy menyu\n\nQuyidagi tugmalardan birini tanlang:",
        "help_text": (
            "📚 <b>Yordam bo'limi</b>\n\n"
            "🔹 /start - Botni ishga tushirish\n"
            "🔹 /help - Yordam olish\n"
            "🔹 /profile - Mening profilim\n"
            "🔹 /stats - Statistika\n"
            "🔹 /settings - Sozlamalar\n"
            "🔹 /lang - Tilni o'zgartirish\n\n"
            "❓ Savollaringiz bo'lsa, adminlarga murojaat qiling."
        ),

        # Profil xabarlari
        "profile_title": "👤 <b>Mening profilim</b>\n",
        "profile_id": "🆔 ID",
        "profile_name": "📛 Ism",
        "profile_username": "🔗 Username",
        "profile_lang": "🌐 Til",
        "profile_joined": "📅 Qo'shilgan sana",
        "profile_messages": "💬 Xabarlar soni",
        "profile_not_found": "😔 Profil topilmadi. /start buyrug'ini yuboring.",

        # Statistika xabarlari
        "stats_title": "📊 <b>Statistika</b>\n",
        "stats_users": "👥 Foydalanuvchilar soni",
        "stats_messages": "💬 Jami xabarlar",

        # Sozlamalar xabarlari
        "settings_title": "⚙️ <b>Sozlamalar</b>\n\nQuyidagi sozlamalardan birini tanlang:",
        "change_lang_title": "🌐 <b>Tilni tanlang:</b>",
        "lang_changed": "✅ Til muvaffaqiyatli o'zgartirildi!",
        "unknown_command": "🤷 Noma'lum buyruq. /help ni bosing.",

        # Bildirishnomalar
        "notifications_title": "🔔 <b>Bildirishnomalar sozlamalari</b>\n\nBildirishnomalarni yoqish yoki o'chirish:",
        "notifications_enabled": "🔔 Bildirishnomalar yoqildi!",
        "notifications_disabled": "🔕 Bildirishnomalar o'chirildi!",

        # E'lon xabarlari
        "broadcast_no_permission": "🚫 Sizda e'lon yuborish huquqi yo'q!",
        "broadcast_enter_message": "📝 E'lon matnini yuboring:",
        "broadcast_success": "✅ E'lon {count} ta foydalanuvchiga yuborildi!",
        "broadcast_cancelled": "❌ E'lon bekor qilindi.",

        # Tugma matnlari
        "btn_profile": "👤 Mening profilim",
        "btn_stats": "📊 Statistika",
        "btn_help": "ℹ️ Yordam",
        "btn_settings": "⚙️ Sozlamalar",
        "btn_channel": "📢 Kanal",
        "btn_back": "🔙 Orqaga",
        "btn_change_lang": "🌐 Tilni o'zgartirish",
        "btn_notifications": "🔔 Bildirishnomalar",
        "btn_notif_on": "🔔 Yoqish",
        "btn_notif_off": "🔕 O'chirish",

        # Balans xabarlari
        "profile_balance": "💰 Balans",
        "profile_pending_balance": "⏳ Kutilayotgan balans",

        # Karta xabarlari
        "btn_add_card": "💳 Visa/Mastercard qo'shish",
        "card_enter_number": (
            "⚠️ <b>Siz qo'shayotgan Visa yoki Mastercard kartangiz virtual emasligiga ishon hosil qiling.</b> "
            "Agar u virtual bo'ladigan bo'lsa ko'zda tutilmagan muammolar paydo bo'ladi.\n\n"
            "💡 <i>Biz tavsiya qilamiz:</i> Uzum karta, Monix visa kartasi, Tez bank visa kartasi va qolgan har qanday jismoniy visa/master kartalari.\n\n"
            "❗️ <b>Unutmangki, kartangizda kamida 13 000 UZS borligiga e'tiborli bo'ling.</b>\n\n"
            "💳 Endi, iltimos, 16 raqamli karta raqamingizni yuboring:\n\n"
            "<i>Namuna: 1234 5678 9012 3456</i>"
        ),
        "card_invalid": "❌ Noto'g'ri karta raqami! Iltimos, 16 raqamli raqam kiriting.",
        "card_saved": "✅ Karta muvaffaqiyatli saqlandi!\n💳 Karta: {card}",
        "card_current": "💳 Joriy karta",
        "card_not_set": "belgilanmagan",

        # Qo'llanma
        "guide_notice": "\n\n📖 <b>Ishni boshlashdan oldin qo'llanmani ko'rib chiqing:</b>",
        "btn_guide": "📖 Qo'llanma",
    },

    "en": {
        # Asosiy xabarlar (ingliz tilida)
        "welcome": "👋 Hello, {name}!\n\n🤖 Welcome to our bot!\nChoose from the menu below:",
        "main_menu": "🏠 Main Menu\n\nSelect one of the buttons below:",
        "help_text": (
            "📚 <b>Help Section</b>\n\n"
            "🔹 /start - Start the bot\n"
            "🔹 /help - Get help\n"
            "🔹 /profile - My profile\n"
            "🔹 /stats - Statistics\n"
            "🔹 /settings - Settings\n"
            "🔹 /lang - Change language\n\n"
            "❓ If you have questions, contact the admins."
        ),

        # Profil xabarlari (ingliz tilida)
        "profile_title": "👤 <b>My Profile</b>\n",
        "profile_id": "🆔 ID",
        "profile_name": "📛 Name",
        "profile_username": "🔗 Username",
        "profile_lang": "🌐 Language",
        "profile_joined": "📅 Joined",
        "profile_messages": "💬 Messages",
        "profile_not_found": "😔 Profile not found. Send /start command.",

        # Statistika xabarlari (ingliz tilida)
        "stats_title": "📊 <b>Statistics</b>\n",
        "stats_users": "👥 Total users",
        "stats_messages": "💬 Total messages",

        # Sozlamalar xabarlari (ingliz tilida)
        "settings_title": "⚙️ <b>Settings</b>\n\nSelect a setting below:",
        "change_lang_title": "🌐 <b>Choose your language:</b>",
        "lang_changed": "✅ Language changed successfully!",
        "unknown_command": "🤷 Unknown command. Press /help.",

        # Bildirishnomalar (ingliz tilida)
        "notifications_title": "🔔 <b>Notification Settings</b>\n\nEnable or disable notifications:",
        "notifications_enabled": "🔔 Notifications enabled!",
        "notifications_disabled": "🔕 Notifications disabled!",

        # E'lon xabarlari (ingliz tilida)
        "broadcast_no_permission": "🚫 You don't have permission to broadcast!",
        "broadcast_enter_message": "📝 Enter the broadcast message:",
        "broadcast_success": "✅ Broadcast sent to {count} users!",
        "broadcast_cancelled": "❌ Broadcast cancelled.",

        # Tugma matnlari (ingliz tilida)
        "btn_profile": "👤 My Profile",
        "btn_stats": "📊 Statistics",
        "btn_help": "ℹ️ Help",
        "btn_settings": "⚙️ Settings",
        "btn_channel": "📢 Channel",
        "btn_back": "🔙 Back",
        "btn_change_lang": "🌐 Change Language",
        "btn_notifications": "🔔 Notifications",
        "btn_notif_on": "🔔 Enable",
        "btn_notif_off": "🔕 Disable",

        # Balans xabarlari (ingliz tilida)
        "profile_balance": "💰 Balance",
        "profile_pending_balance": "⏳ Pending balance",

        # Karta xabarlari (ingliz tilida)
        "btn_add_card": "💳 Add Visa/Mastercard",
        "card_enter_number": (
            "⚠️ <b>Please make sure the Visa or Mastercard you are adding is not a virtual card.</b> "
            "Using a virtual card may cause unexpected issues.\n\n"
            "💡 <i>We recommend:</i> Uzum card, Monix visa card, Tez bank visa card, and any other physical visa/master cards.\n\n"
            "❗️ <b>Please note that your card must have a minimum balance of 13,000 UZS.</b>\n\n"
            "💳 Now, please enter your 16-digit card number:\n\n"
            "<i>Example: 1234 5678 9012 3456</i>"
        ),
        "card_invalid": "❌ Invalid card number! Please enter a 16-digit number.",
        "card_saved": "✅ Card saved successfully!\n💳 Card: {card}",
        "card_current": "💳 Current card",
        "card_not_set": "not set",

        # Qo'llanma (ingliz tilida)
        "guide_notice": "\n\n📖 <b>Please review the guide before starting:</b>",
        "btn_guide": "📖 Guide",
    },

    "ru": {
        # Asosiy xabarlar (rus tilida)
        "welcome": "👋 Здравствуйте, {name}!\n\n🤖 Добро пожаловать в наш бот!\nВыберите из меню ниже:",
        "main_menu": "🏠 Главное меню\n\nВыберите одну из кнопок ниже:",
        "help_text": (
            "📚 <b>Раздел помощи</b>\n\n"
            "🔹 /start - Запустить бота\n"
            "🔹 /help - Получить помощь\n"
            "🔹 /profile - Мой профиль\n"
            "🔹 /stats - Статистика\n"
            "🔹 /settings - Настройки\n"
            "🔹 /lang - Изменить язык\n\n"
            "❓ Если есть вопросы, обратитесь к администраторам."
        ),

        # Profil xabarlari (rus tilida)
        "profile_title": "👤 <b>Мой профиль</b>\n",
        "profile_id": "🆔 ID",
        "profile_name": "📛 Имя",
        "profile_username": "🔗 Юзернейм",
        "profile_lang": "🌐 Язык",
        "profile_joined": "📅 Дата регистрации",
        "profile_messages": "💬 Сообщений",
        "profile_not_found": "😔 Профиль не найден. Отправьте команду /start.",

        # Statistika xabarlari (rus tilida)
        "stats_title": "📊 <b>Статистика</b>\n",
        "stats_users": "👥 Всего пользователей",
        "stats_messages": "💬 Всего сообщений",

        # Sozlamalar xabarlari (rus tilida)
        "settings_title": "⚙️ <b>Настройки</b>\n\nВыберите настройку ниже:",
        "change_lang_title": "🌐 <b>Выберите язык:</b>",
        "lang_changed": "✅ Язык успешно изменён!",
        "unknown_command": "🤷 Неизвестная команда. Нажмите /help.",

        # Bildirishnomalar (rus tilida)
        "notifications_title": "🔔 <b>Настройки уведомлений</b>\n\nВключить или отключить уведомления:",
        "notifications_enabled": "🔔 Уведомления включены!",
        "notifications_disabled": "🔕 Уведомления отключены!",

        # E'lon xabarlari (rus tilida)
        "broadcast_no_permission": "🚫 У вас нет прав для рассылки!",
        "broadcast_enter_message": "📝 Введите текст рассылки:",
        "broadcast_success": "✅ Рассылка отправлена {count} пользователям!",
        "broadcast_cancelled": "❌ Рассылка отменена.",

        # Tugma matnlari (rus tilida)
        "btn_profile": "👤 Мой профиль",
        "btn_stats": "📊 Статистика",
        "btn_help": "ℹ️ Помощь",
        "btn_settings": "⚙️ Настройки",
        "btn_channel": "📢 Канал",
        "btn_back": "🔙 Назад",
        "btn_change_lang": "🌐 Изменить язык",
        "btn_notifications": "🔔 Уведомления",
        "btn_notif_on": "🔔 Включить",
        "btn_notif_off": "🔕 Отключить",

        # Balans xabarlari (rus tilida)
        "profile_balance": "💰 Баланс",
        "profile_pending_balance": "⏳ Ожидаемый баланс",

        # Karta xabarlari (rus tilida)
        "btn_add_card": "💳 Добавить Visa/Mastercard",
        "card_enter_number": (
            "⚠️ <b>Убедитесь, что добавляемая вами карта Visa или Mastercard не является виртуальной.</b> "
            "Использование виртуальной карты может привести к непредвиденным проблемам.\n\n"
            "💡 <i>Мы рекомендуем:</i> Uzum карта, Monix visa, Tez bank visa и любые другие физические карты visa/master.\n\n"
            "❗️ <b>Обратите внимание, что на вашей карте должно быть минимум 13 000 UZS.</b>\n\n"
            "💳 Теперь введите 16-значный номер карты:\n\n"
            "<i>Пример: 1234 5678 9012 3456</i>"
        ),
        "card_invalid": "❌ Неверный номер карты! Введите 16-значный номер.",
        "card_saved": "✅ Карта успешно сохранена!\n💳 Карта: {card}",
        "card_current": "💳 Текущая карта",
        "card_not_set": "не указана",

        # Qo'llanma (rus tilida)
        "guide_notice": "\n\n📖 <b>Ознакомьтесь с руководством перед началом:</b>",
        "btn_guide": "📖 Руководство",
    },
}


def get_text(key: str, lang: str = "uz", **kwargs) -> str:
    """Tarjima matnini qaytarish.

    Berilgan kalit va tilga mos tarjimani qaytaradi.
    Agar kalit yoki til topilmasa, standart (uz) tildan qidiradi.

    Args:
        key: Tarjima kaliti (masalan: 'welcome', 'btn_profile')
        lang: Til kodi ('uz', 'en', 'ru'). Standart: 'uz'
        **kwargs: Matn ichidagi o'zgaruvchilar (masalan: name='Ali')

    Returns:
        Tarjima qilingan matn
    """
    # Til mavjudligini tekshirish, aks holda standart tilga o'tish
    if lang not in TRANSLATIONS:
        lang = "uz"

    # Kalitni tanlangan tildan qidirish
    text = TRANSLATIONS[lang].get(key)

    # Agar kalit topilmasa, standart (uz) tildan qidirish
    if text is None:
        text = TRANSLATIONS["uz"].get(key, key)

    # O'zgaruvchilarni matn ichiga joylashtirish
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass

    return text
