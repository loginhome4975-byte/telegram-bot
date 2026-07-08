"""Tarjimalar moduli - 3 tilda (uz, en, ru) bot xabarlari."""

# Barcha tarjimalar lug'ati
TRANSLATIONS = {
    "uz": {
        # Asosiy xabarlar
        "welcome": "👋 Assalomu alaykum, {name}!\n\n🤖 Botimizga xush kelibsiz!\nQuyidagi menyudan kerakli bo'limni tanlang:",
        "main_menu": "🏠 Asosiy menyu\n\nQuyidagi tugmalardan birini tanlang:",
        "info_text": (
            "Assalomu alaykum.\n\n"
            "Bu bot hosting xizmatlari uchun beriladigan bepul va vaqtinchalik imkoniyatlardan foydalanib bizu sizga beriladigan resurslarni naxtlashtirish maqsidida ish yurityapti. "
            "Sizda o'zingiz bilmaydigan imkonoyatlar mavjud. Bu imkoniyatlarni biz oylaymizki sizga kerak bolmaganligi uchun pulga aylantirib berishdan mamnunmiz. "
            "Agar bot sizga vazifa bajargansiz deb javob qaytarsa yangi kvotalar kelishini kuting va xabar yuborishimiz uchun bildirishnoma funksiyasini yoqib qoying."
        ),
        "understood_thanks": "Tashakkur! Barchasi tushunarli bo'lsa, davom etishingiz mumkin.",
        "unknown_command": "Noma'lum buyruq. Iltimos, menyudan foydalaning.",

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
        "btn_info": "ℹ️ Haqida",
        "btn_settings": "⚙️ Sozlamalar",
        "btn_channel": "📢 Kanalimiz",
        "btn_back": "⬅️ Orqaga",
        "btn_understood": "✅ Tushundim",
        "btn_change_lang": "🌐 Tilni o'zgartirish",
        "btn_notifications": "🔔 Bildirishnomalar",
        "btn_notif_on": "🔔 Yoqish",
        "btn_notif_off": "🔕 O'chirish",

        # Balans xabarlari
        "profile_balance": "💰 Balans",
        "profile_pending_balance": "⏳ Kutilayotgan balans",
        "btn_withdraw": "💸 Pul yechish",
        "withdraw_prompt": "Joriy balans: {balance} UZS\nKutilayotgan balans: {pending_balance} UZS\n\nQancha pul yechmoqchisiz? (Minimal 25000 UZS)\nIltimos, summani kiriting:",
        "withdraw_min_error": "❌ Minimal yechish summasi 25000 UZS.",
        "withdraw_no_card": "❌ Iltimos, oldin karta raqamingizni kiriting.",
        "withdraw_success": "✅ {amount} UZS yechish uchun arizangiz qabul qilindi. Tez orada kartangizga tushirib beriladi.",
        "withdraw_insufficient": "❌ Balansingizda yetarli mablag' mavjud emas. (Siz kiritgan summa: {amount} UZS, Balansingiz: {balance} UZS)",
        "withdraw_invalid_amount": "❌ Noto'g'ri summa kiritdingiz. Iltimos, faqat raqam kiriting.",

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
        
        # Qo'llanma sahifalari
        "guide_prev": "⬅️ Oldingi",
        "guide_next": "Keyingi ➡️",
        "guide_start": "🚀 Ishni boshlash",
        "guide_empty": "Qo'llanma hali tayyor emas.",
        "guide_not_found": "Sahifa topilmadi.",

        # Generatsiya xabarlari
        "already_registered": "❌ Kechirasiz, siz allaqachon ro'yxatdan o'tish vazifasini bajargansiz! Bu ish bir kishiga faqat bir marta beriladi.",
        "gen_reg_data": (
            "📋 <b>Sizning ro'yxatdan o'tish ma'lumotlaringiz:</b>\n\n"
            "<b>Email address:</b> <code>{email}</code>\n"
            "<b>Password:</b> <code>{password}</code>\n"
            "<b>Repeat password:</b> <code>{password}</code>\n"
            "<b>First name:</b> <code>{first_name}</code>\n"
            "<b>Last name:</b> <code>{last_name}</code>\n"
            "<b>Address 1:</b> <code>{address1}</code>\n"
            "<b>Address 2:</b> <i>(To'ldirilmaydi)</i>\n"
            "<b>City:</b> <code>{city}</code>\n"
            "<b>State:</b> <code>{state}</code>\n"
            "<b>Country:</b> <code>Uzbekistan</code>\n"
            "<b>Postal code:</b> <code>{postal}</code>\n"
            "<b>Mobile phone number:</b> <code>{phone}</code>\n"
            "<b>Account type:</b> <code>Personal</code>\n"
            "<b>Phone:</b> <i>(To'ldirilmaydi)</i>\n\n"
            "<i>Ma'lumotlardan foydalanib, rasmdagi formani to'ldiring!</i>"
        ),
        "btn_reg_step_1": "✅ To'ldirdim va ro'yxatdan o'tish yakunlandi",
        "gen_step_2": (
            "🎉 Muvaffaqiyatli ro'yxatdan o'tganingiz bilan tabriklaymiz!!!\n\n"
            "Davom etamiz, ehtimol siz rasmdagi holatga yetib keldingiz.\n"
            "Yetib kelgan bo'lsangiz, ikkinchi rasmda belgilab ko'rsatilgan sariq tugma <b>'Order more'</b> ni bosing."
        ),
        "btn_clicked": "✅ Bosdim",
        "btn_back_nav": "⬅️ Orqaga",
        "gen_step_3": (
            "👍 Yaxshi, bosilgan bo'lsa sizda rasmdagi holat ochiladi.\n"
            "Bu ro'yxatdan belgilab ko'rsatilgani tanlab bosiladi."
        ),
        "gen_step_4": "Endi sizda mana bu rasmdagidek to'ldirilmagan holat ochiladi.",
        "btn_next": "Keyingisi ➡️",
        "gen_step_5": (
            "Endi siz bu holatni xuddi rasmdagidek qilib konfiguratsiya qilasiz.\n"
            "Bunga taxminan 2 daqiqa ketadi.\n\n"
            "⚠️ <b>Eslataman:</b> Hech narsa rasmdagidan ortiqcha yoki kam bo'lmasligi zarur, hammasi huddi rasmdagidek bo'lsin!"
        ),
        "gen_step_6": (
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
        ),
        "btn_finish": "✅ Yakunlash",
        "gen_finish": (
            "🎉 <b>Tashakkur! Barcha bosqichlar muvaffaqiyatli yakunlandi.</b>\n\n"
            "Sizning kutilayotgan balansingizga <b>{amount} UZS</b> qo'shildi!\n\n"
            "⏳ Ushbu mablag' tez orada asosiy balansingizga o'tadi, iltimos kuting."
        ),
    },

    "en": {
        # Asosiy xabarlar (ingliz tilida)
        "welcome": "👋 Hello, {name}!\n\n🤖 Welcome to our bot!\nChoose from the menu below:",
        "main_menu": "🏠 Main Menu\n\nSelect one of the buttons below:",
        "info_text": (
            "Hello.\n\n"
            "This bot operates to monetize the free and temporary resources provided to you and us by hosting services. "
            "You have opportunities you might not be aware of. We are happy to convert these opportunities into money for you, assuming you don't need them. "
            "If the bot replies that you have already completed the task, please wait for new quotas to arrive and make sure to turn on the notification function so we can inform you."
        ),
        "understood_thanks": "Thank you! You can continue using the bot.",
        "unknown_command": "Unknown command. Please use the menu.",

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
        "btn_info": "ℹ️ Info",
        "btn_settings": "⚙️ Settings",
        "btn_channel": "📢 Our Channel",
        "btn_back": "🔙 Back",
        "btn_understood": "✅ Understood",
        "btn_change_lang": "🌐 Change Language",
        "btn_notifications": "🔔 Notifications",
        "btn_notif_on": "🔔 Enable",
        "btn_notif_off": "🔕 Disable",

        # Balans xabarlari (ingliz tilida)
        "profile_balance": "💰 Balance",
        "profile_pending_balance": "⏳ Pending balance",
        "btn_withdraw": "💸 Withdraw Money",
        "withdraw_prompt": "Current balance: {balance} UZS\nPending balance: {pending_balance} UZS\n\nHow much do you want to withdraw? (Minimum 25000 UZS)\nPlease enter the amount:",
        "withdraw_min_error": "❌ Minimum withdrawal amount is 25000 UZS.",
        "withdraw_no_card": "❌ Please add a card first.",
        "withdraw_success": "✅ Your request to withdraw {amount} UZS has been accepted. It will be transferred to your card shortly.",
        "withdraw_insufficient": "❌ Insufficient funds in your balance. (You entered: {amount} UZS, Your balance: {balance} UZS)",
        "withdraw_invalid_amount": "❌ Invalid amount entered. Please enter numbers only.",

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
        
        # Qo'llanma sahifalari (ingliz)
        "guide_prev": "⬅️ Previous",
        "guide_next": "Next ➡️",
        "guide_start": "🚀 Start Working",
        "guide_empty": "The guide is not ready yet.",
        "guide_not_found": "Page not found.",

        # Generatsiya xabarlari
        "already_registered": "❌ Sorry, you have already completed the registration task! This task is given only once per person.",
        "gen_reg_data": (
            "📋 <b>Your registration details:</b>\n\n"
            "<b>Email address:</b> <code>{email}</code>\n"
            "<b>Password:</b> <code>{password}</code>\n"
            "<b>Repeat password:</b> <code>{password}</code>\n"
            "<b>First name:</b> <code>{first_name}</code>\n"
            "<b>Last name:</b> <code>{last_name}</code>\n"
            "<b>Address 1:</b> <code>{address1}</code>\n"
            "<b>Address 2:</b> <i>(Leave empty)</i>\n"
            "<b>City:</b> <code>{city}</code>\n"
            "<b>State:</b> <code>{state}</code>\n"
            "<b>Country:</b> <code>Uzbekistan</code>\n"
            "<b>Postal code:</b> <code>{postal}</code>\n"
            "<b>Mobile phone number:</b> <code>{phone}</code>\n"
            "<b>Account type:</b> <code>Personal</code>\n"
            "<b>Phone:</b> <i>(Leave empty)</i>\n\n"
            "<i>Please use this data to fill out the form shown in the picture!</i>"
        ),
        "btn_reg_step_1": "✅ Filled out and registration complete",
        "gen_step_2": (
            "🎉 Congratulations on successful registration!!!\n\n"
            "Let's continue, you probably reached the state shown in the picture.\n"
            "If so, click the yellow button marked <b>'Order more'</b> in the second picture."
        ),
        "btn_clicked": "✅ Clicked",
        "btn_back_nav": "⬅️ Back",
        "gen_step_3": (
            "👍 Great, once clicked you will see the state shown in the picture.\n"
            "Select the marked item from this list."
        ),
        "gen_step_4": "Now an empty state like this picture will open for you.",
        "btn_next": "Next ➡️",
        "gen_step_5": (
            "Now configure this state exactly as shown in the picture.\n"
            "This will take about 2 minutes.\n\n"
            "⚠️ <b>Reminder:</b> Nothing should be more or less than in the picture, keep it exactly the same!"
        ),
        "gen_step_6": (
            "Now scroll down the opened page a bit (just like in the picture).\n"
            "When you get to the bottom, you'll be asked to fill in your <b>card details</b>.\n\n"
            "For that card, you will:\n"
            "🔹 Select its type\n"
            "🔹 Enter the card number\n"
            "🔹 Enter the expiration date\n"
            "🔹 Put the cardholder's name in the 'Name' field\n"
            "🔹 And enter the 3-digit CVV code from the back\n\n"
            "After that, click <b>Checkout</b>. You will be charged 13,000 UZS (you might receive an SMS code or it may be deducted automatically).\n"
            "Once everything is done, something will 'load' at the top, wait for it to finish spinning (about 5-6 minutes).\n\n"
            "And finally, press the finish button."
        ),
        "btn_finish": "✅ Finish",
        "gen_finish": (
            "🎉 <b>Thank you! All steps have been successfully completed.</b>\n\n"
            "<b>{amount} UZS</b> has been added to your pending balance!\n\n"
            "⏳ These funds will be transferred to your main balance shortly, please wait."
        ),
    },

    "ru": {
        # Asosiy xabarlar (rus tilida)
        "welcome": "👋 Здравствуйте, {name}!\n\n🤖 Добро пожаловать в наш бот!\nВыберите из меню ниже:",
        "main_menu": "🏠 Главное меню\n\nВыберите одну из кнопок ниже:",
        "info_text": (
            "Здравствуйте.\n\n"
            "Этот бот работает с целью монетизации бесплатных и временных ресурсов, предоставляемых нам и вам хостинговыми услугами. "
            "У вас есть возможности, о которых вы можете не знать. Мы рады превратить эти возможности в деньги для вас, предполагая, что они вам не нужны. "
            "Если бот ответит, что вы уже выполнили задание, пожалуйста, подождите поступления новых квот и включите функцию уведомлений, чтобы мы могли отправить вам сообщение."
        ),
        "understood_thanks": "Спасибо! Вы можете продолжать использовать бота.",
        "unknown_command": "Неизвестная команда. Пожалуйста, используйте меню.",

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
        "btn_info": "ℹ️ О нас",
        "btn_settings": "⚙️ Настройки",
        "btn_channel": "📢 Наш канал",
        "btn_back": "⬅️ Назад",
        "btn_understood": "✅ Понятно",
        "btn_change_lang": "🌐 Изменить язык",
        "btn_notifications": "🔔 Уведомления",
        "btn_notif_on": "🔔 Включить",
        "btn_notif_off": "🔕 Отключить",

        # Balans xabarlari (rus tilida)
        "profile_balance": "💰 Баланс",
        "profile_pending_balance": "⏳ Ожидаемый баланс",
        "btn_withdraw": "💸 Снять деньги",
        "withdraw_prompt": "Текущий баланс: {balance} UZS\nОжидаемый баланс: {pending_balance} UZS\n\nСколько вы хотите снять? (Минимум 25000 UZS)\nПожалуйста, введите сумму:",
        "withdraw_min_error": "❌ Минимальная сумма для снятия 25000 UZS.",
        "withdraw_no_card": "❌ Пожалуйста, сначала добавьте карту.",
        "withdraw_success": "✅ Ваш запрос на вывод {amount} UZS принят. Средства будут зачислены на вашу карту в ближайшее время.",
        "withdraw_insufficient": "❌ Недостаточно средств на балансе. (Вы ввели: {amount} UZS, Ваш баланс: {balance} UZS)",
        "withdraw_invalid_amount": "❌ Введена неверная сумма. Пожалуйста, введите только числа.",

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

        # Qo'llanma sahifalari (rus)
        "guide_prev": "⬅️ Назад",
        "guide_next": "Вперед ➡️",
        "guide_start": "🚀 Начать работу",
        "guide_empty": "Руководство еще не готово.",
        "guide_not_found": "Страница не найдена.",

        # Generatsiya xabarlari
        "already_registered": "❌ Извините, вы уже выполнили задание по регистрации! Это задание выдается только один раз на человека.",
        "gen_reg_data": (
            "📋 <b>Ваши регистрационные данные:</b>\n\n"
            "<b>Email address:</b> <code>{email}</code>\n"
            "<b>Password:</b> <code>{password}</code>\n"
            "<b>Repeat password:</b> <code>{password}</code>\n"
            "<b>First name:</b> <code>{first_name}</code>\n"
            "<b>Last name:</b> <code>{last_name}</code>\n"
            "<b>Address 1:</b> <code>{address1}</code>\n"
            "<b>Address 2:</b> <i>(Не заполняется)</i>\n"
            "<b>City:</b> <code>{city}</code>\n"
            "<b>State:</b> <code>{state}</code>\n"
            "<b>Country:</b> <code>Uzbekistan</code>\n"
            "<b>Postal code:</b> <code>{postal}</code>\n"
            "<b>Mobile phone number:</b> <code>{phone}</code>\n"
            "<b>Account type:</b> <code>Personal</code>\n"
            "<b>Phone:</b> <i>(Не заполняется)</i>\n\n"
            "<i>Используйте эти данные, чтобы заполнить форму на картинке!</i>"
        ),
        "btn_reg_step_1": "✅ Заполнил и регистрация завершена",
        "gen_step_2": (
            "🎉 Поздравляем с успешной регистрацией!!!\n\n"
            "Продолжаем, вероятно, вы дошли до состояния на картинке.\n"
            "Если да, нажмите желтую кнопку <b>'Order more'</b>, отмеченную на второй картинке."
        ),
        "btn_clicked": "✅ Нажал",
        "btn_back_nav": "⬅️ Назад",
        "gen_step_3": (
            "👍 Отлично, после нажатия откроется состояние на картинке.\n"
            "Выберите отмеченный пункт из списка."
        ),
        "gen_step_4": "Теперь у вас откроется незаполненное состояние, как на этой картинке.",
        "btn_next": "Далее ➡️",
        "gen_step_5": (
            "Теперь настройте это состояние точно так, как на картинке.\n"
            "Это займет около 2 минут.\n\n"
            "⚠️ <b>Напоминание:</b> Ничего не должно быть больше или меньше, чем на картинке, всё должно быть точно так же!"
        ),
        "gen_step_6": (
            "Теперь прокрутите открытую страницу немного вниз (как на картинке).\n"
            "Когда дойдете до низа, вас попросят заполнить <b>данные карты</b>.\n\n"
            "Для вашей карты вы:\n"
            "🔹 Выберете тип\n"
            "🔹 Введете номер карты\n"
            "🔹 Введете срок действия\n"
            "🔹 Укажете имя владельца в поле 'Name'\n"
            "🔹 И введете 3-значный код CVV с обратной стороны\n\n"
            "После этого нажмите <b>Checkout</b>. С вас будет списано 13 000 UZS (может прийти SMS-код или списаться автоматически).\n"
            "Когда всё будет готово, сверху что-то начнет 'загружаться', подождите, пока оно перестанет крутиться (около 5-6 минут).\n\n"
            "И, наконец, нажмите кнопку завершения."
        ),
        "btn_finish": "✅ Завершить",
        "gen_finish": (
            "🎉 <b>Спасибо! Все этапы успешно завершены.</b>\n\n"
            "На ваш ожидаемый баланс добавлено <b>{amount} UZS</b>!\n\n"
            "⏳ Эти средства вскоре поступят на ваш основной баланс, пожалуйста, подождите."
        ),
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
