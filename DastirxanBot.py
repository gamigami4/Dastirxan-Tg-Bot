#!/usr/bin/env python3
"""
🍽 DASTIRXAN — Telegram Bot
Ресторан узбекской кухни | Uzbek Cuisine | O'zbek taomlari
Incheon, Korea
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)

logging.basicConfig(level=logging.INFO)

# ══════════════════════════════════════════════════════════
#                        НАСТРОЙКИ
# ══════════════════════════════════════════════════════════

BOT_TOKEN     = "8731975018:AAGoek-E4YgnW8EV7P_eSwgImLGzxNT2RVA"
ADMIN_CHAT_ID = 6584619457
PHONE1        = "010-3247-4734"
PHONE2        = "032-817-4734"
ADDRESS       = "인천 연수구 연수동 507-7 2층, Incheon, Korea"
WORK_HOURS    = "11:00 — 23:00"
INSTAGRAM     = "@dastirxan_incheon"
ADMIN_TG      = "@rmnshin"

# ══════════════════════════════════════════════════════════
#                          МЕНЮ
# ══════════════════════════════════════════════════════════

MENU = {
    "main": {
        "ru": "🍖 Основные блюда",
        "en": "🍖 Main Dishes",
        "uz": "🍖 Asosiy taomlar",
        "items": [
            {"ru": "Плов (порция)",       "en": "Plov (portion)",      "uz": "Palov (porsiya)",      "price": 18000},
            {"ru": "Плов (большой)",      "en": "Plov (large)",        "uz": "Palov (katta)",        "price": 32000},
            {"ru": "Лагман",              "en": "Lagman",              "uz": "Lag'mon",              "price": 16000},
            {"ru": "Манты (6 шт)",        "en": "Manti (6 pcs)",       "uz": "Manti (6 dona)",       "price": 15000},
            {"ru": "Самса (1 шт)",        "en": "Samsa (1 pc)",        "uz": "Somsa (1 dona)",       "price": 4000},
            {"ru": "Димлама",             "en": "Dimlama",             "uz": "Dimlama",              "price": 17000},
            {"ru": "Нарын",               "en": "Naryn",               "uz": "Norin",                "price": 16000},
            {"ru": "Шурпа",               "en": "Shurpa soup",         "uz": "Sho'rva",              "price": 14000},
        ]
    },
    "grill": {
        "ru": "🔥 Шашлыки и мясо",
        "en": "🔥 Grill & Meat",
        "uz": "🔥 Kabob va go'shtlar",
        "items": [
            {"ru": "Шашлык из баранины (3 шт)",  "en": "Lamb shashlik (3 pcs)",   "uz": "Qo'y kabob (3 dona)",    "price": 22000},
            {"ru": "Шашлык из говядины (3 шт)",  "en": "Beef shashlik (3 pcs)",   "uz": "Mol kabob (3 dona)",     "price": 20000},
            {"ru": "Шашлык из курицы (3 шт)",    "en": "Chicken shashlik (3 pcs)","uz": "Tovuq kabob (3 dona)",   "price": 17000},
            {"ru": "Люля-кебаб (3 шт)",          "en": "Lula kebab (3 pcs)",      "uz": "Lula kabob (3 dona)",    "price": 19000},
            {"ru": "Рёбрышки барбекю",           "en": "BBQ ribs",                "uz": "BBQ qovurg'a",           "price": 28000},
            {"ru": "Котлета по-узбекски",        "en": "Uzbek-style cutlet",      "uz": "O'zbek kotletasi",       "price": 15000},
        ]
    },
    "salads": {
        "ru": "🥗 Салаты и закуски",
        "en": "🥗 Salads & Starters",
        "uz": "🥗 Salatlar va mazalar",
        "items": [
            {"ru": "Ачичук",             "en": "Achichuk salad",      "uz": "Achchiqchuchuk",       "price": 8000},
            {"ru": "Салат Ташкент",      "en": "Tashkent salad",      "uz": "Toshkent salati",      "price": 10000},
            {"ru": "Овощная тарелка",    "en": "Veggie plate",        "uz": "Sabzavot tarelkasi",   "price": 9000},
            {"ru": "Нон (лепёшка)",      "en": "Non (flatbread)",     "uz": "Non",                  "price": 3000},
            {"ru": "Курт",               "en": "Kurt",                "uz": "Qurt",                 "price": 4000},
        ]
    },
    "drinks": {
        "ru": "🥤 Напитки и бар",
        "en": "🥤 Drinks & Bar",
        "uz": "🥤 Ichimliklar va bar",
        "items": [
            {"ru": "Чай зелёный (чайник)", "en": "Green tea (pot)",    "uz": "Ko'k choy (choynak)",  "price": 7000},
            {"ru": "Чай чёрный (чайник)",  "en": "Black tea (pot)",    "uz": "Qora choy (choynak)",  "price": 7000},
            {"ru": "Айран",                "en": "Ayran",              "uz": "Ayron",                "price": 5000},
            {"ru": "Компот узбекский",     "en": "Uzbek compote",      "uz": "O'zbek kompoti",       "price": 6000},
            {"ru": "Мохито (безалк.)",     "en": "Mojito (non-alc.)",  "uz": "Mohito (alkogolsiz)",  "price": 9000},
            {"ru": "Свежевыжатый сок",     "en": "Fresh juice",        "uz": "Yangi sharbat",        "price": 10000},
            {"ru": "Кола / Спрайт",        "en": "Cola / Sprite",      "uz": "Kola / Sprite",        "price": 4000},
            {"ru": "Вино красное (бокал)", "en": "Red wine (glass)",   "uz": "Qizil vino (qadah)",   "price": 15000},
            {"ru": "Пиво (0.5л)",          "en": "Beer (0.5L)",        "uz": "Pivo (0.5L)",          "price": 8000},
        ]
    },
    "desserts": {
        "ru": "🍮 Десерты",
        "en": "🍮 Desserts",
        "uz": "🍮 Shirinliklar",
        "items": [
            {"ru": "Халва",              "en": "Halva",               "uz": "Halvo",                "price": 7000},
            {"ru": "Чак-чак",           "en": "Chak-chak",           "uz": "Chak-chak",            "price": 8000},
            {"ru": "Пахлава",           "en": "Pakhlava",            "uz": "Pahlava",              "price": 9000},
            {"ru": "Мороженое",         "en": "Ice cream",           "uz": "Muzqaymoq",            "price": 6000},
            {"ru": "Свежие фрукты",     "en": "Fresh fruits",        "uz": "Yangi mevalar",        "price": 12000},
        ]
    },
}

MENU_KEYS = list(MENU.keys())

# ══════════════════════════════════════════════════════════
#                        ТЕКСТЫ
# ══════════════════════════════════════════════════════════

TEXT = {
    "ru": {
        "welcome": (
            "🍽 Добро пожаловать в *DASTIRXAN*!\n\n"
            "Ресторан узбекской кухни в самом сердце Инчхона.\n"
            "Выберите раздел:"
        ),
        "menu_title":    "📋 Выберите раздел меню:",
        "order_title":   "🛒 Выберите блюда:",
        "cart_title":    "🛒 *Ваша корзина:*\n",
        "cart_empty":    "🛒 Корзина пуста",
        "back":          "◀️ Назад",
        "home":          "🏠 Главное меню",
        "checkout":      "✅ Оформить заказ",
        "clear_cart":    "🗑 Очистить корзину",
        "more_items":    "📋 Продолжить выбор",
        "delivery_type": "🚀 Как получить заказ?",
        "pickup":        "🚶 Самовывоз",
        "delivery":      "🛵 Доставка",
        "ask_name":      "✏️ Введите ваше *имя:*",
        "ask_phone":     "📱 Введите ваш *номер телефона:*",
        "ask_address":   "🏠 Введите адрес *доставки:*",
        "ask_payment":   "💳 Выберите способ оплаты:",
        "pay_cash":      "💵 Наличными при получении",
        "pay_card":      "💳 Картой при получении",
        "order_confirm": (
            "✅ *Заказ принят!*\n\n"
            "Мы свяжемся с вами для подтверждения.\n\n"
            f"📞 {PHONE1}\n"
            f"💬 {ADMIN_TG}"
        ),
        "info_text": (
            f"🍽 *DASTIRXAN — Ресторан узбекской кухни*\n\n"
            f"📍 {ADDRESS}\n"
            f"🕐 Часы работы: {WORK_HOURS}\n"
            f"📞 {PHONE1}\n"
            f"📞 {PHONE2}\n"
            f"📸 Instagram: {INSTAGRAM}\n\n"
            "🅿️ Парковка: 연수길프라자주차장입구"
        ),
        "book_title":    "📅 *Бронирование столика*",
        "ask_book_name": "✏️ Введите ваше *имя:*",
        "ask_book_date": "📅 Введите *дату и время* (например: 25 декабря, 19:00):",
        "ask_book_pax":  "👥 Введите *количество гостей:*",
        "ask_book_phone":"📱 Введите ваш *номер телефона:*",
        "book_confirm": (
            "✅ *Столик забронирован!*\n\n"
            "Мы подтвердим бронь по телефону.\n\n"
            f"📞 {PHONE1}\n"
            f"💬 {ADMIN_TG}"
        ),
        "menu_btn":  "📋 Меню",
        "book_btn":  "📅 Забронировать столик",
        "info_btn":  "📍 О ресторане",
        "order_btn": "🛒 Сделать заказ",
        "total":     "💰 Итого",
        "pcs":       "шт",
    },
    "en": {
        "welcome": (
            "🍽 Welcome to *DASTIRXAN*!\n\n"
            "Authentic Uzbek cuisine restaurant in the heart of Incheon.\n"
            "Choose a section:"
        ),
        "menu_title":    "📋 Choose a menu section:",
        "order_title":   "🛒 Select dishes:",
        "cart_title":    "🛒 *Your cart:*\n",
        "cart_empty":    "🛒 Cart is empty",
        "back":          "◀️ Back",
        "home":          "🏠 Main Menu",
        "checkout":      "✅ Place order",
        "clear_cart":    "🗑 Clear cart",
        "more_items":    "📋 Continue selecting",
        "delivery_type": "🚀 How to receive your order?",
        "pickup":        "🚶 Pickup",
        "delivery":      "🛵 Delivery",
        "ask_name":      "✏️ Enter your *name:*",
        "ask_phone":     "📱 Enter your *phone number:*",
        "ask_address":   "🏠 Enter your *delivery address:*",
        "ask_payment":   "💳 Choose payment method:",
        "pay_cash":      "💵 Cash on delivery",
        "pay_card":      "💳 Card on delivery",
        "order_confirm": (
            "✅ *Order accepted!*\n\n"
            "We will contact you to confirm.\n\n"
            f"📞 {PHONE1}\n"
            f"💬 {ADMIN_TG}"
        ),
        "info_text": (
            f"🍽 *DASTIRXAN — Uzbek Cuisine Restaurant*\n\n"
            f"📍 {ADDRESS}\n"
            f"🕐 Working hours: {WORK_HOURS}\n"
            f"📞 {PHONE1}\n"
            f"📞 {PHONE2}\n"
            f"📸 Instagram: {INSTAGRAM}\n\n"
            "🅿️ Parking: 연수길프라자주차장입구"
        ),
        "book_title":    "📅 *Table Reservation*",
        "ask_book_name": "✏️ Enter your *name:*",
        "ask_book_date": "📅 Enter *date and time* (e.g. Dec 25, 7:00 PM):",
        "ask_book_pax":  "👥 Enter *number of guests:*",
        "ask_book_phone":"📱 Enter your *phone number:*",
        "book_confirm": (
            "✅ *Table reserved!*\n\n"
            "We will confirm your reservation by phone.\n\n"
            f"📞 {PHONE1}\n"
            f"💬 {ADMIN_TG}"
        ),
        "menu_btn":  "📋 Menu",
        "book_btn":  "📅 Reserve a table",
        "info_btn":  "📍 About us",
        "order_btn": "🛒 Order food",
        "total":     "💰 Total",
        "pcs":       "pcs",
    },
    "uz": {
        "welcome": (
            "🍽 *DASTIRXAN*ga xush kelibsiz!\n\n"
            "Incheon shahrida haqiqiy o'zbek taomlari restorани.\n"
            "Bo'limni tanlang:"
        ),
        "menu_title":    "📋 Menyu bo'limini tanlang:",
        "order_title":   "🛒 Taomlarni tanlang:",
        "cart_title":    "🛒 *Savatchangiz:*\n",
        "cart_empty":    "🛒 Savat bo'sh",
        "back":          "◀️ Orqaga",
        "home":          "🏠 Bosh menyu",
        "checkout":      "✅ Buyurtma berish",
        "clear_cart":    "🗑 Savatni tozalash",
        "more_items":    "📋 Tanlashni davom ettirish",
        "delivery_type": "🚀 Buyurtmani qanday olasiz?",
        "pickup":        "🚶 O'zi olib ketish",
        "delivery":      "🛵 Yetkazib berish",
        "ask_name":      "✏️ *Ismingizni* kiriting:",
        "ask_phone":     "📱 *Telefon raqamingizni* kiriting:",
        "ask_address":   "🏠 *Yetkazib berish manzilini* kiriting:",
        "ask_payment":   "💳 To'lov usulini tanlang:",
        "pay_cash":      "💵 Qabul qilganda naqd",
        "pay_card":      "💳 Qabul qilganda karta",
        "order_confirm": (
            "✅ *Buyurtma qabul qilindi!*\n\n"
            "Tasdiqlash uchun siz bilan bog'lanamiz.\n\n"
            f"📞 {PHONE1}\n"
            f"💬 {ADMIN_TG}"
        ),
        "info_text": (
            f"🍽 *DASTIRXAN — O'zbek taomlari restorани*\n\n"
            f"📍 {ADDRESS}\n"
            f"🕐 Ish vaqti: {WORK_HOURS}\n"
            f"📞 {PHONE1}\n"
            f"📞 {PHONE2}\n"
            f"📸 Instagram: {INSTAGRAM}\n\n"
            "🅿️ Avtoturargoh: 연수길프라자주차장입구"
        ),
        "book_title":    "📅 *Stol band qilish*",
        "ask_book_name": "✏️ *Ismingizni* kiriting:",
        "ask_book_date": "📅 *Sana va vaqtni* kiriting (masalan: 25 dekabr, 19:00):",
        "ask_book_pax":  "👥 *Mehmonlar sonini* kiriting:",
        "ask_book_phone":"📱 *Telefon raqamingizni* kiriting:",
        "book_confirm": (
            "✅ *Stol band qilindi!*\n\n"
            "Telefon orqali tasdiqlash uchun bog'lanamiz.\n\n"
            f"📞 {PHONE1}\n"
            f"💬 {ADMIN_TG}"
        ),
        "menu_btn":  "📋 Menyu",
        "book_btn":  "📅 Stol band qilish",
        "info_btn":  "📍 Restoran haqida",
        "order_btn": "🛒 Buyurtma berish",
        "total":     "💰 Jami",
        "pcs":       "dona",
    },
}

# ══════════════════════════════════════════════════════════
#                   СОСТОЯНИЯ ДИАЛОГА
# ══════════════════════════════════════════════════════════

ORDER_NAME, ORDER_PHONE, ORDER_ADDRESS, ORDER_PAYMENT = range(4)
BOOK_NAME, BOOK_DATE, BOOK_PAX, BOOK_PHONE = range(4, 8)

# ══════════════════════════════════════════════════════════
#               ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ══════════════════════════════════════════════════════════

def lang(context):
    return context.user_data.get("lang", "ru")

def t(context, key):
    return TEXT[lang(context)][key]

def get_cart(context):
    if "cart" not in context.user_data:
        context.user_data["cart"] = {}
    return context.user_data["cart"]

def cart_total(cart):
    total = 0
    for key, qty in cart.items():
        cat, idx = key.split("_")
        total += MENU[cat]["items"][int(idx)]["price"] * qty
    return total

def cart_summary(cart, context):
    if not cart:
        return t(context, "cart_empty")
    l = lang(context)
    lines = [t(context, "cart_title")]
    total = 0
    for key, qty in cart.items():
        cat, idx = key.split("_")
        item = MENU[cat]["items"][int(idx)]
        sub = item["price"] * qty
        total += sub
        lines.append(f"• {item[l]} × {qty} = ₩{sub:,}")
    lines.append(f"\n{t(context, 'total')}: *₩{total:,}*")
    return "\n".join(lines)

def main_menu_kb(context):
    tx = TEXT[lang(context)]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(tx["menu_btn"],  callback_data="menu")],
        [InlineKeyboardButton(tx["order_btn"], callback_data="cart")],
        [InlineKeyboardButton(tx["book_btn"],  callback_data="book_start")],
        [InlineKeyboardButton(tx["info_btn"],  callback_data="info")],
    ])

def menu_categories_kb(context):
    l = lang(context)
    rows = [[InlineKeyboardButton(MENU[k][l], callback_data=f"cat_{k}")] for k in MENU_KEYS]
    rows.append([InlineKeyboardButton(t(context, "back"), callback_data="home")])
    return InlineKeyboardMarkup(rows)

def items_kb(context, cat):
    l = lang(context)
    cart = get_cart(context)
    rows = []
    for i, item in enumerate(MENU[cat]["items"]):
        key = f"{cat}_{i}"
        qty = cart.get(key, 0)
        label = f"{item[l]} ₩{item['price']:,}" + (f" ✅{qty}" if qty else "")
        rows.append([
            InlineKeyboardButton("➖", callback_data=f"rm_{cat}_{i}"),
            InlineKeyboardButton(label, callback_data="x"),
            InlineKeyboardButton("➕", callback_data=f"ad_{cat}_{i}"),
        ])
    rows.append([InlineKeyboardButton(t(context, "back"), callback_data="menu")])
    rows.append([InlineKeyboardButton("🛒 " + cart_summary(cart, context).split("\n")[-1], callback_data="cart")])
    return InlineKeyboardMarkup(rows)

def cart_kb(context):
    cart = get_cart(context)
    rows = []
    if cart:
        rows.append([InlineKeyboardButton(t(context, "checkout"),   callback_data="checkout")])
        rows.append([InlineKeyboardButton(t(context, "clear_cart"), callback_data="clear_cart")])
    rows.append([InlineKeyboardButton(t(context, "more_items"), callback_data="menu")])
    rows.append([InlineKeyboardButton(t(context, "home"),       callback_data="home")])
    return InlineKeyboardMarkup(rows)

# ══════════════════════════════════════════════════════════
#                  ОСНОВНЫЕ ОБРАБОТЧИКИ
# ══════════════════════════════════════════════════════════

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🍽 *DASTIRXAN*\n\nВыберите язык / Choose language / Tilni tanlang:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🇷🇺 Рус", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 Eng", callback_data="lang_en"),
            InlineKeyboardButton("🇺🇿 O'zb", callback_data="lang_uz"),
        ]])
    )

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    # ── Язык ─────────────────────────────────────────────
    if d.startswith("lang_"):
        context.user_data["lang"] = d.split("_")[1]
        await q.edit_message_text(
            t(context, "welcome"), parse_mode="Markdown",
            reply_markup=main_menu_kb(context)
        )

    # ── Главная ──────────────────────────────────────────
    elif d == "home":
        await q.edit_message_text(
            t(context, "welcome"), parse_mode="Markdown",
            reply_markup=main_menu_kb(context)
        )

    # ── Меню категории ───────────────────────────────────
    elif d == "menu":
        await q.edit_message_text(
            t(context, "menu_title"), parse_mode="Markdown",
            reply_markup=menu_categories_kb(context)
        )

    # ── Товары категории ─────────────────────────────────
    elif d.startswith("cat_"):
        cat = d.replace("cat_", "")
        l = lang(context)
        await q.edit_message_text(
            f"*{MENU[cat][l]}*\n\n{t(context, 'order_title')}",
            parse_mode="Markdown",
            reply_markup=items_kb(context, cat)
        )
        context.user_data["current_cat"] = cat

    # ── Добавить / убрать ────────────────────────────────
    elif d.startswith("ad_") or d.startswith("rm_"):
        action, cat, idx = d.split("_")
        key = f"{cat}_{idx}"
        cart = get_cart(context)
        if action == "ad":
            cart[key] = cart.get(key, 0) + 1
        else:
            if cart.get(key, 0) > 0:
                cart[key] -= 1
                if cart[key] == 0:
                    del cart[key]
        await q.edit_message_reply_markup(reply_markup=items_kb(context, cat))

    # ── Корзина ──────────────────────────────────────────
    elif d == "cart":
        await q.edit_message_text(
            cart_summary(get_cart(context), context),
            parse_mode="Markdown",
            reply_markup=cart_kb(context)
        )

    # ── Очистить корзину ─────────────────────────────────
    elif d == "clear_cart":
        context.user_data["cart"] = {}
        await q.edit_message_text(
            t(context, "cart_empty"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(context, "more_items"), callback_data="menu")],
                [InlineKeyboardButton(t(context, "home"),       callback_data="home")],
            ])
        )

    # ── Тип получения ────────────────────────────────────
    elif d == "checkout":
        await q.edit_message_text(
            t(context, "delivery_type"), parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(context, "pickup"),   callback_data="type_pickup")],
                [InlineKeyboardButton(t(context, "delivery"), callback_data="type_delivery")],
                [InlineKeyboardButton(t(context, "back"),     callback_data="cart")],
            ])
        )

    # ── Информация ───────────────────────────────────────
    elif d == "info":
        await q.edit_message_text(
            t(context, "info_text"), parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(context, "back"), callback_data="home")]
            ])
        )

    elif d == "x":
        pass

# ══════════════════════════════════════════════════════════
#              ДИАЛОГ ОФОРМЛЕНИЯ ЗАКАЗА
# ══════════════════════════════════════════════════════════

async def order_type_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["order_type"] = q.data.replace("type_", "")
    await q.edit_message_text(t(context, "ask_name"), parse_mode="Markdown")
    return ORDER_NAME

async def order_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_name"] = update.message.text
    await update.message.reply_text(t(context, "ask_phone"), parse_mode="Markdown")
    return ORDER_PHONE

async def order_get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_phone"] = update.message.text
    if context.user_data.get("order_type") == "delivery":
        await update.message.reply_text(t(context, "ask_address"), parse_mode="Markdown")
        return ORDER_ADDRESS
    await update.message.reply_text(
        t(context, "ask_payment"), parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(context, "pay_cash"), callback_data="pay_cash")],
            [InlineKeyboardButton(t(context, "pay_card"), callback_data="pay_card")],
        ])
    )
    return ORDER_PAYMENT

async def order_get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_address"] = update.message.text
    await update.message.reply_text(
        t(context, "ask_payment"), parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(context, "pay_cash"), callback_data="pay_cash")],
            [InlineKeyboardButton(t(context, "pay_card"), callback_data="pay_card")],
        ])
    )
    return ORDER_PAYMENT

async def order_get_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    l = lang(context)
    pay_method = "💵 Наличные" if q.data == "pay_cash" else "💳 Карта"
    order_type = context.user_data.get("order_type")
    name    = context.user_data.get("order_name", "—")
    phone   = context.user_data.get("order_phone", "—")
    address = context.user_data.get("order_address", "—")
    cart    = get_cart(context)
    total   = cart_total(cart)
    type_label = {
        "ru": {"pickup": "🚶 Самовывоз", "delivery": "🛵 Доставка"},
        "en": {"pickup": "🚶 Pickup",    "delivery": "🛵 Delivery"},
        "uz": {"pickup": "🚶 O'zi olish","delivery": "🛵 Yetkazib berish"},
    }[l][order_type]

    await q.edit_message_text(
        t(context, "order_confirm"), parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(context, "home"), callback_data="home")]
        ])
    )

    # Уведомление администратору
    items_text = "\n".join(
        f"• {MENU[k.split('_')[0]]['items'][int(k.split('_')[1])]['ru']} × {v} = ₩{MENU[k.split('_')[0]]['items'][int(k.split('_')[1])]['price'] * v:,}"
        for k, v in cart.items()
    )
    admin_msg = (
        f"🔔 *НОВЫЙ ЗАКАЗ — DASTIRXAN!*\n\n"
        f"👤 Имя: {name}\n"
        f"📱 Телефон: {phone}\n"
        f"📦 Тип: {type_label}\n"
        f"💳 Оплата: {pay_method}\n"
    )
    if order_type == "delivery":
        admin_msg += f"🏠 Адрес: {address}\n"
    admin_msg += f"\n📋 Заказ:\n{items_text}\n\n💰 Итого: ₩{total:,}"

    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Ошибка уведомления: {e}")

    context.user_data["cart"] = {}
    return ConversationHandler.END

# ══════════════════════════════════════════════════════════
#              ДИАЛОГ БРОНИРОВАНИЯ СТОЛИКА
# ══════════════════════════════════════════════════════════

async def book_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        f"{t(context, 'book_title')}\n\n{t(context, 'ask_book_name')}",
        parse_mode="Markdown"
    )
    return BOOK_NAME

async def book_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["book_name"] = update.message.text
    await update.message.reply_text(t(context, "ask_book_date"), parse_mode="Markdown")
    return BOOK_DATE

async def book_get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["book_date"] = update.message.text
    await update.message.reply_text(t(context, "ask_book_pax"), parse_mode="Markdown")
    return BOOK_PAX

async def book_get_pax(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["book_pax"] = update.message.text
    await update.message.reply_text(t(context, "ask_book_phone"), parse_mode="Markdown")
    return BOOK_PHONE

async def book_get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["book_phone"] = update.message.text
    name  = context.user_data.get("book_name", "—")
    date  = context.user_data.get("book_date", "—")
    pax   = context.user_data.get("book_pax", "—")
    phone = context.user_data.get("book_phone", "—")

    await update.message.reply_text(
        t(context, "book_confirm"), parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(context, "home"), callback_data="home")]
        ])
    )

    admin_msg = (
        f"📅 *НОВОЕ БРОНИРОВАНИЕ — DASTIRXAN!*\n\n"
        f"👤 Имя: {name}\n"
        f"📅 Дата и время: {date}\n"
        f"👥 Гостей: {pax}\n"
        f"📱 Телефон: {phone}"
    )
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Ошибка уведомления: {e}")

    return ConversationHandler.END

# ══════════════════════════════════════════════════════════
#                       ЗАПУСК БОТА
# ══════════════════════════════════════════════════════════

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(order_type_entry, pattern="^type_(pickup|delivery)$")],
        states={
            ORDER_NAME:    [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_name)],
            ORDER_PHONE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_phone)],
            ORDER_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_address)],
            ORDER_PAYMENT: [CallbackQueryHandler(order_get_payment, pattern="^pay_")],
        },
        fallbacks=[CommandHandler("start", cmd_start)],
        allow_reentry=True,
    )

    book_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(book_start, pattern="^book_start$")],
        states={
            BOOK_NAME:  [MessageHandler(filters.TEXT & ~filters.COMMAND, book_get_name)],
            BOOK_DATE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, book_get_date)],
            BOOK_PAX:   [MessageHandler(filters.TEXT & ~filters.COMMAND, book_get_pax)],
            BOOK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, book_get_phone)],
        },
        fallbacks=[CommandHandler("start", cmd_start)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(order_conv)
    app.add_handler(book_conv)
    app.add_handler(CallbackQueryHandler(btn))

    print("🍽 DASTIRXAN бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()