#!/usr/bin/env python3
"""
🍽 DASTIRXAN — Telegram Bot
Ресторан узбекской кухни | Uzbek Cuisine Restaurant | O'zbek taomlari restorани
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

BOT_TOKEN      = "8731975018:AAGoek-E4YgnW8EV7P_eSwgImLGzxNT2RVA"
ADMIN_CHAT_ID  = 6584619457
ADMIN_TG       = "@rmnshin"
PHONE1         = "010-3247-4734"
PHONE2         = "032-817-4734"
ADDRESS        = "인천 연수구 연수동 507-7 2층, Incheon, Korea"
WORK_HOURS     = "11:00 — 23:00"
INSTAGRAM      = "@dastirxan_incheon"
PARKING        = "연수길프라자주차장입구"

# ══════════════════════════════════════════════════════════
#                          МЕНЮ
# ══════════════════════════════════════════════════════════

MENU = [
    {
        "id": "bread",
        "ru": "🍞 Хлеб",
        "en": "🍞 Bread",
        "uz": "🍞 Non",
        "items": [
            {"ru": "Лепёшка",       "en": "Flatbread",          "uz": "Lepyoshka",              "price": 4000},
            {"ru": "Патыр",         "en": "Patyr",              "uz": "Patir",                  "price": 4000},
            {"ru": "Патыр слоёный", "en": "Layered Patyr",      "uz": "Qatlamali patir",        "price": 7000},
            {"ru": "Лаваш",         "en": "Lavash",             "uz": "Lavash",                 "price": 3000},
            {"ru": "Хлеб ассорти",  "en": "Bread Assortment",   "uz": "Non assortisi",          "price": 12000},
            {"ru": "Чёрный хлеб",   "en": "Dark Bread",         "uz": "Qora non",               "price": 7000},
        ]
    },
    {
        "id": "fastfood",
        "ru": "🌯 Фастфуд",
        "en": "🌯 Fast Food",
        "uz": "🌯 Tezkor ovqat",
        "items": [
            {"ru": "Тандырная самса",           "en": "Tandoor Samsa",              "uz": "Tandir samsa",               "price": 5000},
            {"ru": "Бургер сет",                "en": "Burger Set",                 "uz": "Burger set",                 "price": 15000},
            {"ru": "Самаркандская самса",        "en": "Samarkand Samsa",            "uz": "Samarqand somsa",            "price": 6000},
            {"ru": "Шаурма-шашлык с сыром",     "en": "Shawarma-Shashlik w/ Cheese","uz": "Pishloqli shawarma-kabob",   "price": 15000},
            {"ru": "Слоёная самса",              "en": "Flaky Samsa",                "uz": "Qatlamali samsa",            "price": 4000},
            {"ru": "Чебуреки с сыром",           "en": "Chebureki with Cheese",      "uz": "Pishloqli cheburek",         "price": 12000},
        ]
    },
    {
        "id": "salads",
        "ru": "🥗 Салаты",
        "en": "🥗 Salads",
        "uz": "🥗 Salatlar",
        "items": [
            {"ru": "Овощная нарезка",        "en": "Vegetable Platter",          "uz": "Sabzavot kesimi",            "price": 11000},
            {"ru": "Соленья",                "en": "Pickles",                    "uz": "Turshilar",                  "price": 10000},
            {"ru": "Французский",            "en": "French Salad",               "uz": "Frantsuz salati",            "price": 13000},
            {"ru": "Самарканд",              "en": "Samarkand Salad",            "uz": "Samarqand salati",           "price": 10000},
            {"ru": "Сельдь под шубой",       "en": "Herring Under a Fur Coat",   "uz": "Mo'ynali seld' salati",      "price": 13000},
            {"ru": "Греческий салат",         "en": "Greek Salad",                "uz": "Grek salati",                "price": 12000},
            {"ru": "Салат Каприз",            "en": "Caprice Salad",              "uz": "Kapriz salati",              "price": 12000},
            {"ru": "Салат Цезарь",            "en": "Caesar Salad",               "uz": "Sezar salati",               "price": 13000},
            {"ru": "Ачичук",                  "en": "Achichuk Salad",             "uz": "Achchiqchuchuk",             "price": 7000},
            {"ru": "Жареные баклажаны",       "en": "Fried Eggplant",             "uz": "Qovurilgan baqlajon",        "price": 14000},
            {"ru": "Смак",                    "en": "Smak Salad",                 "uz": "Smak salati",                "price": 11000},
            {"ru": "Салат Оливье",            "en": "Olivier Salad",              "uz": "Olive salati",               "price": 10000},
        ]
    },
    {
        "id": "soups",
        "ru": "🍲 Супы",
        "en": "🍲 Soups",
        "uz": "🍲 Sho'rvalar",
        "items": [
            {"ru": "Лагман",                    "en": "Lagman Soup",            "uz": "Lag'mon",                    "price": 12000},
            {"ru": "Шурпа из баранины",          "en": "Lamb Shurpa",            "uz": "Qo'y go'shti sho'rva",       "price": 12000},
            {"ru": "Окрошка",                    "en": "Okroshka",               "uz": "Okroshka",                   "price": 11000},
            {"ru": "Борщ",                       "en": "Borscht",                "uz": "Borscht",                    "price": 12000},
            {"ru": "Мастава",                    "en": "Mastava",                "uz": "Mastava",                    "price": 12000},
            {"ru": "Шурпа из говядины",          "en": "Beef Shurpa",            "uz": "Mol go'shti sho'rva",        "price": 12000},
            {"ru": "Пельмени с бульоном",        "en": "Pelmeni in Broth",       "uz": "Pelmenli sho'rva",           "price": 12000},
            {"ru": "Суп с фрикадельками",        "en": "Meatball Soup",          "uz": "Ko'ftali sho'rva",           "price": 12000},
        ]
    },
    {
        "id": "mains",
        "ru": "🍽 Вторые блюда",
        "en": "🍽 Main Courses",
        "uz": "🍽 Ikkinchi taomlar",
        "items": [
            {"ru": "Манты",                                             "en": "Manti",                                      "uz": "Manti",                                          "price": 14000},
            {"ru": "Уйгурский лагман",                                  "en": "Uyghur Lagman",                              "uz": "Uyg'ur lag'moni",                                "price": 14000},
            {"ru": "Ханум",                                             "en": "Khanum",                                     "uz": "Xonim",                                          "price": 14000},
            {"ru": "Жареный лагман",                                    "en": "Fried Lagman",                               "uz": "Qovurilgan lag'mon",                             "price": 14000},
            {"ru": "Хинкали",                                           "en": "Khinkali",                                   "uz": "Xinkali",                                        "price": 17000},
            {"ru": "Жареные пельмени",                                  "en": "Fried Pelmeni",                              "uz": "Qovurilgan pelmeni",                             "price": 14000},
            {"ru": "Нарын",                                             "en": "Naryn",                                      "uz": "Norin",                                          "price": 16000},
            {"ru": "Пельмени",                                          "en": "Pelmeni",                                    "uz": "Pelmeni",                                        "price": 14000},
            {"ru": "Бешбармак",                                         "en": "Beshbarmak",                                 "uz": "Beshbarmaq",                                     "price": 17000},
            {"ru": "Жаркое с гарниром",                                 "en": "Roast with Side Dish",                       "uz": "Qovurma garnir bilan",                           "price": 15000},
            {"ru": "Цыплёнок табака с картошкой фри",                   "en": "Chicken Tabaka with Fries",                  "uz": "Tovuq tabaka kartoshka fri bilan",                "price": 15000},
            {"ru": "Долма говядина",                                    "en": "Beef Dolma",                                 "uz": "Mol go'shti dolma",                              "price": 14000},
            {"ru": "Куртоб",                                            "en": "Qurtoб",                                     "uz": "Qurtoб",                                         "price": 17000},
            {"ru": "Бифштекс",                                         "en": "Beefsteak",                                  "uz": "Bifshteks",                                      "price": 14000},
            {"ru": "Мошкчири",                                          "en": "Moshkichiri",                                "uz": "Moshkichiri",                                    "price": 15000},
            {"ru": "Туйкабоб",                                          "en": "Tuyqabob",                                   "uz": "Tuyqabob",                                       "price": 15000},
            {"ru": "Котлеты с сыром",                                   "en": "Cheese Cutlets",                             "uz": "Pishloqli kotlet",                               "price": 18000},
            {"ru": "Казан-кебаб",                                       "en": "Kazan Kebab",                                "uz": "Qozon kabob",                                    "price": 15000},
            {"ru": "Джиз-быз из баранины с картошкой по-деревенски",    "en": "Lamb Jiz-Biz with Country Potatoes",         "uz": "Qo'y jiz-biz qishloq kartoshkasi bilan",         "price": 16000},
            {"ru": "Джиз-быз говядина с картошкой фри",                 "en": "Beef Jiz-Biz with Fries",                    "uz": "Mol jiz-biz kartoshka fri bilan",                 "price": 17000},
            {"ru": "Баранья корейка на гриле",                          "en": "Grilled Lamb Rack",                          "uz": "Qo'y qovurg'asi grilda",                         "price": 48000},
            {"ru": "Бараньи рёбра с картошкой фри и рисом",             "en": "Lamb Ribs with Fries and Rice",              "uz": "Qo'y qovurg'asi kartoshka fri va guruch bilan",   "price": 18000},
            {"ru": "Баранья корейка на гриле 1кг с картошкой по-деревенски", "en": "Grilled Lamb Rack 1kg with Country Potatoes", "uz": "Qo'y qovurg'asi grilda 1kg qishloq kartoshkasi bilan", "price": 90000},
            {"ru": "Жареный сазан",                                     "en": "Fried Carp",                                 "uz": "Qovurilgan sazan",                               "price": 15000},
            {"ru": "Стейк из сёмги с гарниром",                         "en": "Salmon Steak with Side Dish",                "uz": "Semga steyki garnir bilan",                      "price": 19000},
            {"ru": "Самаркандский плов",                                 "en": "Samarkand Plov",                             "uz": "Samarqand palovi",                               "price": 14000},
            {"ru": "Плов с казы и долмой",                              "en": "Plov with Kazy and Dolma",                   "uz": "Qazi va dolmali palov",                          "price": 16000},
            {"ru": "Самаркандский плов сет на одного",                  "en": "Samarkand Plov Set for One",                 "uz": "Samarqand palov seti (1 kishi)",                 "price": 20000},
        ]
    },
    {
        "id": "grill",
        "ru": "🔥 Мангал",
        "en": "🔥 Grill",
        "uz": "🔥 Mangal",
        "items": [
            {"ru": "Стейк из говядины 300г",                "en": "Beef Steak 300g",                        "uz": "Mol go'shti steyki 300g",             "price": 21000},
            {"ru": "Стейк из баранины 300г",                "en": "Lamb Steak 300g",                        "uz": "Qo'y go'shti steyki 300g",            "price": 19000},
            {"ru": "Стейк рибай 500г",                      "en": "Ribeye Steak 500g",                      "uz": "Ribay steyki 500g",                   "price": 30000},
            {"ru": "Стейк рибай с костью 550г",             "en": "Bone-in Ribeye Steak 550g",              "uz": "Suyakli ribay steyki 550g",           "price": 35000},
            {"ru": "Рулет-шашлык говядина",                 "en": "Beef Roll Shashlik",                     "uz": "Mol go'shti rulet-kabob",             "price": 13000},
            {"ru": "Куриный шашлык",                        "en": "Chicken Shashlik",                       "uz": "Tovuq kabob",                         "price": 9000},
            {"ru": "Овощи на гриле",                        "en": "Grilled Vegetables",                     "uz": "Grilda sabzavotlar",                  "price": 10000},
            {"ru": "Шашлык из бараньей корейки",            "en": "Lamb Rack Shashlik",                     "uz": "Qo'y qovurg'asi kabob",               "price": 24000},
            {"ru": "Сет шашлык",                            "en": "Shashlik Set",                           "uz": "Kabob seti",                          "price": 60000},
            {"ru": "Наполеон шашлык",                       "en": "Napoleon Shashlik",                      "uz": "Napoleon kabob",                      "price": 14000},
            {"ru": "Шашлык медальоны",                      "en": "Shashlik Medallions",                    "uz": "Medalon kabob",                       "price": 14000},
            {"ru": "Молотый шашлык",                        "en": "Ground Shashlik",                        "uz": "To'qilgan kabob",                     "price": 10000},
            {"ru": "Кусковой шашлык (баранина)",            "en": "Chunk Shashlik (Lamb)",                  "uz": "Bo'lakli kabob (qo'y)",               "price": 11000},
            {"ru": "Куриные крылышки",                      "en": "Chicken Wings",                          "uz": "Tovuq qanotlari",                     "price": 9000},
            {"ru": "Шашлык из говяжьей печени",             "en": "Beef Liver Shashlik",                    "uz": "Mol jigar kabob",                     "price": 9000},
            {"ru": "Кусковой шашлык из говяжьей вырезки",  "en": "Beef Tenderloin Shashlik",               "uz": "Mol vyreza bo'lakli kabob",            "price": 12000},
            {"ru": "Шашлык из курдюка",                    "en": "Fat Tail Shashlik",                       "uz": "Dumba kabob",                         "price": 14000},
            {"ru": "Универсальный рулет",                   "en": "Universal Roll",                         "uz": "Universal rulet",                     "price": 10000},
            {"ru": "Чесночный соус",                        "en": "Garlic Sauce",                           "uz": "Sarimsoqli sous",                     "price": 3000},
            {"ru": "Томатный соус",                         "en": "Tomato Sauce",                           "uz": "Pomidor sous",                        "price": 3000},
            {"ru": "Мясное ассорти (4-5 чел.)",             "en": "Meat Assortment (4-5 ppl)",              "uz": "Go'sht assortisi (4-5 kishi)",         "price": 155000},
            {"ru": "Мясное большое ассорти (7-8 чел.)",    "en": "Large Meat Assortment (7-8 ppl)",         "uz": "Katta go'sht assortisi (7-8 kishi)",   "price": 195000},
            {"ru": "Дастархан барбекю сет",                 "en": "Dastarkhan BBQ Set",                     "uz": "Dastarxon barbeku seti",              "price": 90000},
            {"ru": "Дастархан барбекю сет большой",        "en": "Dastarkhan BBQ Set Large",                "uz": "Dastarxon barbeku seti katta",         "price": 125000},
        ]
    },
    {
        "id": "sides",
        "ru": "🍳 Гарниры",
        "en": "🍳 Side Dishes",
        "uz": "🍳 Garnirllar",
        "items": [
            {"ru": "Яичница 3 яйца с сосисками и варёной колбасой", "en": "Fried Eggs 3pcs with Sausages & Boiled Sausage", "uz": "Tuxum qovurma 3 dona sosiska va qaynatilgan kolbasa bilan", "price": 12000},
            {"ru": "Мясное копчёное ассорти",   "en": "Smoked Meat Assortment",     "uz": "Dudlangan go'sht assortisi",  "price": 25000},
            {"ru": "Холодец",                   "en": "Meat Jelly",                 "uz": "Xolodets",                   "price": 9000},
            {"ru": "Рис",                       "en": "Rice",                       "uz": "Guruch",                     "price": 3000},
            {"ru": "Гречка",                    "en": "Buckwheat",                  "uz": "Grechka",                    "price": 7000},
            {"ru": "Картошка фри",              "en": "French Fries",               "uz": "Kartoshka fri",              "price": 8000},
            {"ru": "Макароны",                  "en": "Pasta",                      "uz": "Makaron",                    "price": 5000},
            {"ru": "Пюре",                      "en": "Mashed Potatoes",            "uz": "Kartoshka püre",             "price": 8000},
        ]
    },
    {
        "id": "desserts",
        "ru": "🍰 Десерты",
        "en": "🍰 Desserts",
        "uz": "🍰 Shirinliklar",
        "items": [
            {"ru": "Большое фруктовое ассорти",  "en": "Large Fruit Assortment",    "uz": "Katta meva assortisi",       "price": 30000},
            {"ru": "Фруктовое ассорти",          "en": "Fruit Assortment",          "uz": "Meva assortisi",             "price": 20000},
            {"ru": "Ферреро Роше",               "en": "Ferrero Rocher",            "uz": "Ferrero Rocher",             "price": 13000},
            {"ru": "Молочная девочка",           "en": "Milk Girl Cake",            "uz": "Sut qizi torti",             "price": 12000},
            {"ru": "Чизкейк",                    "en": "Cheesecake",                "uz": "Chizkeyk",                   "price": 12000},
            {"ru": "Пахлава",                    "en": "Baklava",                   "uz": "Pahlava",                    "price": 11000},
            {"ru": "Наполеон",                   "en": "Napoleon Cake",             "uz": "Napoleon torti",             "price": 13000},
            {"ru": "Медовик",                    "en": "Honey Cake",                "uz": "Asal torti",                 "price": 12000},
            {"ru": "Красный бархат",             "en": "Red Velvet Cake",           "uz": "Qizil baxmal torti",         "price": 12000},
            {"ru": "Шоколадный торт Орео",       "en": "Oreo Chocolate Cake",       "uz": "Oreo shokolad torti",        "price": 12000},
            {"ru": "Фруктовый салат",            "en": "Fruit Salad",               "uz": "Meva salati",                "price": 13000},
            {"ru": "Мороженое",                  "en": "Ice Cream",                 "uz": "Muzqaymoq",                  "price": 12000},
        ]
    },
    {
        "id": "tea",
        "ru": "🍵 Чай",
        "en": "🍵 Tea",
        "uz": "🍵 Choy",
        "items": [
            {"ru": "Марокканский чай",           "en": "Moroccan Tea",              "uz": "Marokash choy",              "price": 12000},
            {"ru": "Чай жасмин",                 "en": "Jasmine Tea",               "uz": "Yasmin choy",                "price": 8000},
            {"ru": "Имбирный чай",               "en": "Ginger Tea",                "uz": "Zanjabil choy",              "price": 12000},
            {"ru": "Горный чай",                 "en": "Mountain Tea",              "uz": "Tog' choy",                  "price": 8000},
            {"ru": "Ягодный чай",                "en": "Berry Tea",                 "uz": "Rezavorli choy",             "price": 13000},
            {"ru": "Турецкий чай",               "en": "Turkish Tea",               "uz": "Turk choy",                  "price": 12000},
            {"ru": "Имбирно-марокканский чай",   "en": "Ginger-Moroccan Tea",       "uz": "Zanjabil-Marokash choy",     "price": 13000},
            {"ru": "Тропический чай",            "en": "Tropical Tea",              "uz": "Tropik choy",                "price": 12000},
            {"ru": "Имбирно-ягодный чай",        "en": "Ginger-Berry Tea",          "uz": "Zanjabil-rezavorli choy",    "price": 12000},
            {"ru": "Earl Grey",                  "en": "Earl Grey",                 "uz": "Earl Grey",                  "price": 8000},
        ]
    },
    {
        "id": "coffee",
        "ru": "☕ Кофе",
        "en": "☕ Coffee",
        "uz": "☕ Qahva",
        "items": [
            {"ru": "Американо",                  "en": "Americano",                 "uz": "Amerikano",                  "price": 5000},
            {"ru": "Капучино",                   "en": "Cappuccino",                "uz": "Kapuchino",                  "price": 6000},
            {"ru": "Флэт уайт",                  "en": "Flat White",                "uz": "Flat white",                 "price": 6000},
            {"ru": "Латте с корицей и мёдом",    "en": "Cinnamon Honey Latte",      "uz": "Dolchin va asalli latte",    "price": 7000},
            {"ru": "Горячий шоколад",            "en": "Hot Chocolate",             "uz": "Issiq shokolad",             "price": 7000},
            {"ru": "Матча латте",                "en": "Matcha Latte",              "uz": "Matcha latte",               "price": 7000},
            {"ru": "Айс американо",              "en": "Iced Americano",            "uz": "Muz amerikano",              "price": 5000},
            {"ru": "Айс латте",                  "en": "Iced Latte",                "uz": "Muz latte",                  "price": 6000},
            {"ru": "Sunset",                     "en": "Sunset",                    "uz": "Sunset",                     "price": 9000},
            {"ru": "Sunrise",                    "en": "Sunrise",                   "uz": "Sunrise",                    "price": 8000},
            {"ru": "Клубничный матча латте",     "en": "Strawberry Matcha Latte",   "uz": "Qulupnayli matcha latte",    "price": 9000},
            {"ru": "Айс матча",                  "en": "Iced Matcha",               "uz": "Muz matcha",                 "price": 7000},
        ]
    },
    {
        "id": "fresh",
        "ru": "🍊 Фреши",
        "en": "🍊 Fresh Juices",
        "uz": "🍊 Yangi sharbatlar",
        "items": [
            {"ru": "Апельсиновый фреш",      "en": "Orange Juice",              "uz": "Apelsin freshi",             "price": 10000},
            {"ru": "Лимонный фреш",          "en": "Lemon Juice",               "uz": "Limon freshi",               "price": 10000},
            {"ru": "Киви-щавель",            "en": "Kiwi-Sorrel Juice",         "uz": "Kivi-qo'ng'irbosh",          "price": 10000},
            {"ru": "Морковный фреш",         "en": "Carrot Juice",              "uz": "Sabzi freshi",               "price": 6000},
            {"ru": "Апельсин-морковь",       "en": "Orange-Carrot Juice",       "uz": "Apelsin-sabzi",              "price": 8000},
            {"ru": "Киви-сельдерей",         "en": "Kiwi-Celery Juice",         "uz": "Kivi-selderei",              "price": 10000},
        ]
    },
    {
        "id": "lemonades1",
        "ru": "🍹 Лимонады (1л)",
        "en": "🍹 Lemonades (1L)",
        "uz": "🍹 Limonadlar (1L)",
        "items": [
            {"ru": "Тропический лимонад/айсти",  "en": "Tropical Lemonade/Iced Tea",    "uz": "Tropik limonad/aysti",       "price": 14000},
            {"ru": "Лимонный лимонад/айсти",     "en": "Lemon Lemonade/Iced Tea",       "uz": "Limonli limonad/aysti",      "price": 14000},
            {"ru": "Мохито клубничный",          "en": "Strawberry Mojito",             "uz": "Qulupnayli mohito",          "price": 14000},
            {"ru": "Манго-маракуйя",             "en": "Mango-Passion Fruit",           "uz": "Mango-marakuya",             "price": 16000},
            {"ru": "Тархун",                     "en": "Tarragon Lemonade",             "uz": "Tarxun",                     "price": 16000},
            {"ru": "Мохито маракуйя",            "en": "Passion Fruit Mojito",          "uz": "Marakuyali mohito",          "price": 16000},
            {"ru": "Мохито классический",        "en": "Classic Mojito",                "uz": "Klassik mohito",             "price": 14000},
            {"ru": "Компот вишнёвый",            "en": "Cherry Compote",                "uz": "Gilos kompoti",              "price": 11000},
        ]
    },
    {
        "id": "lemonades05",
        "ru": "🍹 Лимонады (0.5л)",
        "en": "🍹 Lemonades (0.5L)",
        "uz": "🍹 Limonadlar (0.5L)",
        "items": [
            {"ru": "Ягодный",            "en": "Berry Lemonade",            "uz": "Rezavorli",          "price": 7000},
            {"ru": "Тропический",        "en": "Tropical Lemonade",         "uz": "Tropik",             "price": 7000},
            {"ru": "Манго-маракуйя",     "en": "Mango-Passion Fruit",       "uz": "Mango-marakuya",     "price": 8000},
            {"ru": "Мохито маракуйя",    "en": "Passion Fruit Mojito",      "uz": "Marakuyali mohito",  "price": 8000},
            {"ru": "Лимонный",           "en": "Lemon Lemonade",            "uz": "Limonli",            "price": 7000},
            {"ru": "Мохито классический","en": "Classic Mojito",            "uz": "Klassik mohito",     "price": 7000},
            {"ru": "Мохито клубничный",  "en": "Strawberry Mojito",         "uz": "Qulupnayli mohito",  "price": 7000},
            {"ru": "Тархун",             "en": "Tarragon Lemonade",         "uz": "Tarxun",             "price": 8000},
        ]
    },
    {
        "id": "drinks",
        "ru": "🥤 Напитки",
        "en": "🥤 Drinks",
        "uz": "🥤 Ichimliklar",
        "items": [
            {"ru": "Зелёный чай",                "en": "Green Tea",                 "uz": "Yashil choy",                "price": 4000},
            {"ru": "Чёрный чай",                 "en": "Black Tea",                 "uz": "Qora choy",                  "price": 4000},
            {"ru": "Чёрный чай с лимоном",       "en": "Black Tea with Lemon",      "uz": "Limonli qora choy",          "price": 5000},
            {"ru": "Зелёный чай с лимоном",      "en": "Green Tea with Lemon",      "uz": "Limonli yashil choy",        "price": 5000},
            {"ru": "Ташкентский чай",            "en": "Tashkent Tea",              "uz": "Toshkent choy",              "price": 6000},
            {"ru": "Чай с молоком",              "en": "Milk Tea",                  "uz": "Sutli choy",                 "price": 8000},
            {"ru": "Fanta 0.36л",                "en": "Fanta 0.36L",               "uz": "Fanta 0.36L",                "price": 4000},
            {"ru": "Кока-кола 0.36л",            "en": "Coca-Cola 0.36L",           "uz": "Coca-Cola 0.36L",            "price": 4000},
            {"ru": "Кока-кола 1.25л",            "en": "Coca-Cola 1.25L",           "uz": "Coca-Cola 1.25L",            "price": 8000},
            {"ru": "Спрайт 0.36л",               "en": "Sprite 0.36L",              "uz": "Sprite 0.36L",               "price": 4000},
            {"ru": "Зелёный чай (бутылка)",      "en": "Green Tea (bottle)",        "uz": "Yashil choy (shisha)",       "price": 6000},
            {"ru": "Айран",                      "en": "Ayran",                     "uz": "Ayron",                      "price": 5000},
            {"ru": "Кефир",                      "en": "Kefir",                     "uz": "Kefir",                      "price": 4000},
            {"ru": "Газированная вода 0.3л",     "en": "Sparkling Water 0.3L",      "uz": "Gazli suv 0.3L",             "price": 5000},
            {"ru": "Газированная вода 0.5л",     "en": "Sparkling Water 0.5L",      "uz": "Gazli suv 0.5L",             "price": 7000},
        ]
    },
]

CAT_IDS = [c["id"] for c in MENU]

# ══════════════════════════════════════════════════════════
#                        ТЕКСТЫ
# ══════════════════════════════════════════════════════════

TEXT = {
    "ru": {
        "welcome":       "🍽 Добро пожаловать в *DASTIRXAN*!\n\nРесторан узбекской кухни в Инчхоне.\nВыберите раздел:",
        "menu_title":    "📋 Выберите раздел меню:",
        "add_to_cart":   "Нажмите ➕ чтобы добавить в корзину:",
        "cart_title":    "🛒 *Ваша корзина:*\n",
        "cart_empty":    "🛒 Корзина пуста",
        "total":         "💰 Итого",
        "back":          "◀️ Назад",
        "home":          "🏠 Главное меню",
        "checkout":      "✅ Оформить заказ",
        "clear_cart":    "🗑 Очистить корзину",
        "more":          "📋 Продолжить выбор",
        "delivery_type": "Как получить заказ?",
        "pickup":        "🚶 Самовывоз",
        "delivery":      "🛵 Доставка",
        "ask_name":      "✏️ Введите ваше *имя:*",
        "ask_phone":     "📱 Введите ваш *номер телефона:*",
        "ask_address":   "🏠 Введите адрес *доставки:*",
        "ask_payment":   "💳 Выберите способ оплаты:",
        "pay_cash":      "💵 Наличными при получении",
        "pay_card":      "💳 Картой при получении",
        "order_confirm": f"✅ *Заказ принят!*\n\nМы свяжемся с вами для подтверждения.\n\n📞 {PHONE1}\n💬 {ADMIN_TG}",
        "info_text":     f"🍽 *DASTIRXAN — Ресторан узбекской кухни*\n\n📍 *Адрес:* {ADDRESS}\n🕐 *Часы работы:* {WORK_HOURS}\n📞 {PHONE1}\n📞 {PHONE2}\n🅿️ Парковка: {PARKING}\n📸 Instagram: {INSTAGRAM}",
        "book_title":    "📅 *Бронирование столика*",
        "ask_book_name": "✏️ Введите ваше *имя:*",
        "ask_book_date": "📅 Введите *дату и время* (например: 25 декабря, 19:00):",
        "ask_book_pax":  "👥 Введите *количество гостей:*",
        "ask_book_phone":"📱 Введите ваш *номер телефона:*",
        "book_confirm":  f"✅ *Столик забронирован!*\n\nМы подтвердим бронь по телефону.\n\n📞 {PHONE1}\n💬 {ADMIN_TG}",
        "menu_btn":      "📋 Меню",
        "order_btn":     "🛒 Корзина",
        "book_btn":      "📅 Забронировать столик",
        "info_btn":      "📍 О ресторане",
    },
    "en": {
        "welcome":       "🍽 Welcome to *DASTIRXAN*!\n\nAuthentic Uzbek cuisine restaurant in Incheon.\nChoose a section:",
        "menu_title":    "📋 Choose a menu section:",
        "add_to_cart":   "Press ➕ to add to cart:",
        "cart_title":    "🛒 *Your cart:*\n",
        "cart_empty":    "🛒 Cart is empty",
        "total":         "💰 Total",
        "back":          "◀️ Back",
        "home":          "🏠 Main Menu",
        "checkout":      "✅ Place order",
        "clear_cart":    "🗑 Clear cart",
        "more":          "📋 Continue selecting",
        "delivery_type": "How would you like to receive your order?",
        "pickup":        "🚶 Pickup",
        "delivery":      "🛵 Delivery",
        "ask_name":      "✏️ Enter your *name:*",
        "ask_phone":     "📱 Enter your *phone number:*",
        "ask_address":   "🏠 Enter your *delivery address:*",
        "ask_payment":   "💳 Choose payment method:",
        "pay_cash":      "💵 Cash on delivery",
        "pay_card":      "💳 Card on delivery",
        "order_confirm": f"✅ *Order accepted!*\n\nWe will contact you to confirm.\n\n📞 {PHONE1}\n💬 {ADMIN_TG}",
        "info_text":     f"🍽 *DASTIRXAN — Uzbek Cuisine Restaurant*\n\n📍 *Address:* {ADDRESS}\n🕐 *Working hours:* {WORK_HOURS}\n📞 {PHONE1}\n📞 {PHONE2}\n🅿️ Parking: {PARKING}\n📸 Instagram: {INSTAGRAM}",
        "book_title":    "📅 *Table Reservation*",
        "ask_book_name": "✏️ Enter your *name:*",
        "ask_book_date": "📅 Enter *date and time* (e.g. Dec 25, 7:00 PM):",
        "ask_book_pax":  "👥 Enter *number of guests:*",
        "ask_book_phone":"📱 Enter your *phone number:*",
        "book_confirm":  f"✅ *Table reserved!*\n\nWe will confirm your reservation by phone.\n\n📞 {PHONE1}\n💬 {ADMIN_TG}",
        "menu_btn":      "📋 Menu",
        "order_btn":     "🛒 Cart",
        "book_btn":      "📅 Reserve a table",
        "info_btn":      "📍 About us",
    },
    "uz": {
        "welcome":       "🍽 *DASTIRXAN*ga xush kelibsiz!\n\nIncheon shahridagi o'zbek taomlari restorани.\nBo'limni tanlang:",
        "menu_title":    "📋 Menyu bo'limini tanlang:",
        "add_to_cart":   "Savatga qo'shish uchun ➕ ni bosing:",
        "cart_title":    "🛒 *Savatchangiz:*\n",
        "cart_empty":    "🛒 Savat bo'sh",
        "total":         "💰 Jami",
        "back":          "◀️ Orqaga",
        "home":          "🏠 Bosh menyu",
        "checkout":      "✅ Buyurtma berish",
        "clear_cart":    "🗑 Savatni tozalash",
        "more":          "📋 Tanlashni davom ettirish",
        "delivery_type": "Buyurtmani qanday olasiz?",
        "pickup":        "🚶 O'zi olib ketish",
        "delivery":      "🛵 Yetkazib berish",
        "ask_name":      "✏️ *Ismingizni* kiriting:",
        "ask_phone":     "📱 *Telefon raqamingizni* kiriting:",
        "ask_address":   "🏠 *Yetkazib berish manzilini* kiriting:",
        "ask_payment":   "💳 To'lov usulini tanlang:",
        "pay_cash":      "💵 Qabul qilganda naqd",
        "pay_card":      "💳 Qabul qilganda karta",
        "order_confirm": f"✅ *Buyurtma qabul qilindi!*\n\nTasdiqlash uchun siz bilan bog'lanamiz.\n\n📞 {PHONE1}\n💬 {ADMIN_TG}",
        "info_text":     f"🍽 *DASTIRXAN — O'zbek taomlari restorани*\n\n📍 *Manzil:* {ADDRESS}\n🕐 *Ish vaqti:* {WORK_HOURS}\n📞 {PHONE1}\n📞 {PHONE2}\n🅿️ Avtoturargoh: {PARKING}\n📸 Instagram: {INSTAGRAM}",
        "book_title":    "📅 *Stol band qilish*",
        "ask_book_name": "✏️ *Ismingizni* kiriting:",
        "ask_book_date": "📅 *Sana va vaqtni* kiriting (masalan: 25 dekabr, 19:00):",
        "ask_book_pax":  "👥 *Mehmonlar sonini* kiriting:",
        "ask_book_phone":"📱 *Telefon raqamingizni* kiriting:",
        "book_confirm":  f"✅ *Stol band qilindi!*\n\nTelefon orqali tasdiqlash uchun bog'lanamiz.\n\n📞 {PHONE1}\n💬 {ADMIN_TG}",
        "menu_btn":      "📋 Menyu",
        "order_btn":     "🛒 Savat",
        "book_btn":      "📅 Stol band qilish",
        "info_btn":      "📍 Restoran haqida",
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

def lang(context): return context.user_data.get("lang", "ru")
def t(context, key): return TEXT[lang(context)][key]

def get_cat(cat_id):
    for c in MENU:
        if c["id"] == cat_id:
            return c
    return None

def get_cart(context):
    if "cart" not in context.user_data:
        context.user_data["cart"] = {}
    return context.user_data["cart"]

def cart_total(cart):
    total = 0
    for key, qty in cart.items():
        cat_id, idx = key.rsplit("_", 1)
        cat = get_cat(cat_id)
        if cat:
            total += cat["items"][int(idx)]["price"] * qty
    return total

def cart_summary(cart, context):
    if not cart:
        return t(context, "cart_empty")
    l = lang(context)
    lines = [t(context, "cart_title")]
    total = 0
    for key, qty in cart.items():
        cat_id, idx = key.rsplit("_", 1)
        cat = get_cat(cat_id)
        if cat:
            item = cat["items"][int(idx)]
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

def categories_kb(context):
    l = lang(context)
    rows = [[InlineKeyboardButton(c[l], callback_data=f"cat_{c['id']}")] for c in MENU]
    rows.append([InlineKeyboardButton(t(context, "back"), callback_data="home")])
    return InlineKeyboardMarkup(rows)

def items_kb(context, cat_id):
    l = lang(context)
    cart = get_cart(context)
    cat = get_cat(cat_id)
    rows = []
    for i, item in enumerate(cat["items"]):
        key = f"{cat_id}_{i}"
        qty = cart.get(key, 0)
        label = f"{item[l]} ₩{item['price']:,}" + (f" ✅{qty}" if qty else "")
        rows.append([
            InlineKeyboardButton("➖", callback_data=f"rm_{cat_id}_{i}"),
            InlineKeyboardButton(label, callback_data="x"),
            InlineKeyboardButton("➕", callback_data=f"ad_{cat_id}_{i}"),
        ])
    rows.append([InlineKeyboardButton(t(context, "back"), callback_data="menu")])
    rows.append([InlineKeyboardButton("🛒", callback_data="cart")])
    return InlineKeyboardMarkup(rows)

def cart_kb(context):
    cart = get_cart(context)
    rows = []
    if cart:
        rows.append([InlineKeyboardButton(t(context, "checkout"),   callback_data="checkout")])
        rows.append([InlineKeyboardButton(t(context, "clear_cart"), callback_data="clear_cart")])
    rows.append([InlineKeyboardButton(t(context, "more"), callback_data="menu")])
    rows.append([InlineKeyboardButton(t(context, "home"), callback_data="home")])
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

    if d.startswith("lang_"):
        context.user_data["lang"] = d.split("_")[1]
        await q.edit_message_text(t(context, "welcome"), parse_mode="Markdown", reply_markup=main_menu_kb(context))

    elif d == "home":
        await q.edit_message_text(t(context, "welcome"), parse_mode="Markdown", reply_markup=main_menu_kb(context))

    elif d == "menu":
        await q.edit_message_text(t(context, "menu_title"), parse_mode="Markdown", reply_markup=categories_kb(context))

    elif d.startswith("cat_"):
        cat_id = d[4:]
        cat = get_cat(cat_id)
        l = lang(context)
        await q.edit_message_text(
            f"*{cat[l]}*\n\n{t(context, 'add_to_cart')}",
            parse_mode="Markdown",
            reply_markup=items_kb(context, cat_id)
        )

    elif d.startswith("ad_"):
        parts = d[3:].rsplit("_", 1)
        cat_id, idx = parts[0], parts[1]
        key = f"{cat_id}_{idx}"
        cart = get_cart(context)
        cart[key] = cart.get(key, 0) + 1
        await q.edit_message_reply_markup(reply_markup=items_kb(context, cat_id))

    elif d.startswith("rm_"):
        parts = d[3:].rsplit("_", 1)
        cat_id, idx = parts[0], parts[1]
        key = f"{cat_id}_{idx}"
        cart = get_cart(context)
        if cart.get(key, 0) > 0:
            cart[key] -= 1
            if cart[key] == 0:
                del cart[key]
        await q.edit_message_reply_markup(reply_markup=items_kb(context, cat_id))

    elif d == "cart":
        await q.edit_message_text(cart_summary(get_cart(context), context), parse_mode="Markdown", reply_markup=cart_kb(context))

    elif d == "clear_cart":
        context.user_data["cart"] = {}
        await q.edit_message_text(
            t(context, "cart_empty"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(context, "more"), callback_data="menu")],
                [InlineKeyboardButton(t(context, "home"), callback_data="home")],
            ])
        )

    elif d == "checkout":
        cart = get_cart(context)
        if not cart:
            await q.edit_message_text(t(context, "cart_empty"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(context, "more"), callback_data="menu")]]))
            return
        await q.edit_message_text(
            t(context, "delivery_type"), parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(context, "pickup"),   callback_data="type_pickup")],
                [InlineKeyboardButton(t(context, "delivery"), callback_data="type_delivery")],
                [InlineKeyboardButton(t(context, "back"),     callback_data="cart")],
            ])
        )

    elif d == "info":
        await q.edit_message_text(
            t(context, "info_text"), parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(context, "back"), callback_data="home")]])
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
    pay = "💵 Наличные" if q.data == "pay_cash" else "💳 Карта"
    order_type = context.user_data.get("order_type")
    name    = context.user_data.get("order_name", "—")
    phone   = context.user_data.get("order_phone", "—")
    address = context.user_data.get("order_address", "—")
    cart    = get_cart(context)
    total   = cart_total(cart)
    type_label = {"ru": {"pickup": "🚶 Самовывоз", "delivery": "🛵 Доставка"},
                  "en": {"pickup": "🚶 Pickup",    "delivery": "🛵 Delivery"},
                  "uz": {"pickup": "🚶 O'zi olish","delivery": "🛵 Yetkazib berish"}}[l][order_type]

    await q.edit_message_text(
        t(context, "order_confirm"), parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(context, "home"), callback_data="home")]])
    )

    items_text = "\n".join(
        f"• {get_cat(k.rsplit('_',1)[0])['items'][int(k.rsplit('_',1)[1])]['ru']} × {v} = ₩{get_cat(k.rsplit('_',1)[0])['items'][int(k.rsplit('_',1)[1])]['price']*v:,}"
        for k, v in cart.items() if get_cat(k.rsplit('_',1)[0])
    )
    admin_msg = (f"🔔 *НОВЫЙ ЗАКАЗ — DASTIRXAN!*\n\n"
                 f"👤 {name}\n📱 {phone}\n📦 {type_label}\n💳 {pay}\n")
    if order_type == "delivery":
        admin_msg += f"🏠 {address}\n"
    admin_msg += f"\n📋 Заказ:\n{items_text}\n\n💰 Итого: ₩{total:,}"

    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка: {e}")

    context.user_data["cart"] = {}
    return ConversationHandler.END

# ══════════════════════════════════════════════════════════
#              ДИАЛОГ БРОНИРОВАНИЯ СТОЛИКА
# ══════════════════════════════════════════════════════════

async def book_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(f"{t(context, 'book_title')}\n\n{t(context, 'ask_book_name')}", parse_mode="Markdown")
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
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(context, "home"), callback_data="home")]])
    )

    admin_msg = (f"📅 *НОВОЕ БРОНИРОВАНИЕ — DASTIRXAN!*\n\n"
                 f"👤 {name}\n📅 {date}\n👥 {pax} гостей\n📱 {phone}")
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка: {e}")

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
