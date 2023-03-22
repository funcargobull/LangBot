from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# /start, /main
button_eng = InlineKeyboardButton("🇬🇧 английский", callback_data="english")
button_de = InlineKeyboardButton("🇩🇪 немецкий", callback_data="german")
kb_main = InlineKeyboardMarkup()
kb_main.add(button_eng)
kb_main.add(button_de)

# 🇬🇧 Английский, 🇩🇪 Немецкий
button_word_of_day = InlineKeyboardButton("🕛 слово дня", callback_data="word_of_day")
button_test = InlineKeyboardButton("✅ тест на уровень знания языка", callback_data="language_test")
button_facts = InlineKeyboardButton("🤔 факты о стране", callback_data="facts_about_country")
button_learn = InlineKeyboardButton("📚 обучение", callback_data="learning")
button_main_menu = InlineKeyboardButton("🏠 главное меню", callback_data="main_menu")
button_marathon = InlineKeyboardButton("🏁 марафон слов", callback_data="word_marathon")
kb_english = InlineKeyboardMarkup()
kb_english.row(button_learn, button_word_of_day)
kb_english.add(button_test)
kb_english.row(button_facts, button_marathon)
kb_english.add(button_main_menu)

# Слово дня
kb_word_of_day = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅ назад", callback_data="back"))

# Факты о стране
kb_facts_about_country = InlineKeyboardMarkup()
kb_facts_about_country.add(InlineKeyboardButton("➡ дальше", callback_data="farther"))
kb_facts_about_country.add(button_main_menu)

# Словесный марафон
kb_word_marathon = InlineKeyboardMarkup()
kb_word_marathon.add(InlineKeyboardButton("❤ все части речи", callback_data="all_parts"))
kb_word_marathon.row(InlineKeyboardButton("🧡 существительные", callback_data="nouns"),
                     InlineKeyboardButton("💚 глаголы", callback_data="verbs"))
kb_word_marathon.row(InlineKeyboardButton("💙 прилагательные", callback_data="adjectives"),
                     InlineKeyboardButton("🖤 наречия", callback_data="adverbs"))
kb_word_marathon.add(button_main_menu)

# Словесный марафон (все части речи)
kb_word_marathon_all = InlineKeyboardMarkup()
kb_word_marathon_all.add(InlineKeyboardButton("❤ дальше", callback_data="farther_all"))
kb_word_marathon_category = InlineKeyboardButton("⬅ выбор категории", callback_data="choose_category")
kb_word_marathon_all.add(kb_word_marathon_category)
kb_word_marathon_all.add(button_main_menu)

# Словесный марафон (существительные)
kb_word_marathon_nouns = InlineKeyboardMarkup()
kb_word_marathon_nouns.add(InlineKeyboardButton("🧡 дальше", callback_data="farther_nouns"))
kb_word_marathon_nouns.add(kb_word_marathon_category)
kb_word_marathon_nouns.add(button_main_menu)

# Словесный марафон (глаголы)
kb_word_marathon_verbs = InlineKeyboardMarkup()
kb_word_marathon_verbs.add(InlineKeyboardButton("💚 дальше", callback_data="farther_verbs"))
kb_word_marathon_verbs.add(kb_word_marathon_category)
kb_word_marathon_verbs.add(button_main_menu)

# Словесный марафон (прилагательные)
kb_word_marathon_adjectives = InlineKeyboardMarkup()
kb_word_marathon_adjectives.add(InlineKeyboardButton("💙 дальше", callback_data="farther_adjectives"))
kb_word_marathon_adjectives.add(kb_word_marathon_category)
kb_word_marathon_adjectives.add(button_main_menu)

# Словесный марафон (наречия)
kb_word_marathon_adverbs = InlineKeyboardMarkup()
kb_word_marathon_adverbs.add(InlineKeyboardButton("🖤 дальше", callback_data="farther_adverbs"))
kb_word_marathon_adverbs.add(kb_word_marathon_category)
kb_word_marathon_adverbs.add(button_main_menu)

# Обучение
kb_learning = InlineKeyboardMarkup()
kb_learning.add(InlineKeyboardButton("🎶 основы произношения", callback_data="pronunciation"))
kb_learning.add(InlineKeyboardButton("🕒 времена", callback_data="tenses"))
kb_learning.add(InlineKeyboardButton("🧠 подготовка к экзаменам", callback_data="exams"))
kb_learning.add(button_main_menu)

# Обучение (времена)
kb_learning_tenses = InlineKeyboardMarkup()
button_back = InlineKeyboardButton("⬅ вернуться к разделам", callback_data="back_to_learning")
kb_learning_tenses.add(button_back)
button_back_to_learning = InlineKeyboardButton("⬅ вернуться к курсам", callback_data="back_to_courses")

# Обучение (основы произношения)
kb_pronunciation = InlineKeyboardMarkup()
kb_pronunciation.add(
    InlineKeyboardButton("📚 1. открытый и закрытый слоги (~2 мин)", callback_data="open_close_syllable"))
kb_pronunciation.add(
    InlineKeyboardButton("📚 2. соответствие букв и звуков (~10 мин)", callback_data="letters_sounds"))
kb_pronunciation.add(
    InlineKeyboardButton("📚 3. дифтонги и трифтонги (~5 мин)", callback_data="diphthongs_triphthongs"))
kb_pronunciation.add(InlineKeyboardButton("📚 4. интонация. тоны (~4 мин)", callback_data="intonation"))
kb_pronunciation.add(InlineKeyboardButton("📚 5. ударения (~1.5 мин)", callback_data="accents"))
kb_pronunciation.add(InlineKeyboardButton("📚 6. сложности (~4 мин)", callback_data="hard_things"))
kb_pronunciation.add(button_back)

# Обучение (открытый и закрытый слог, 1 страница)
kb_open_close_syllables = InlineKeyboardMarkup()
kb_open_close_syllables.add(InlineKeyboardButton("📗 на 2 страницу", callback_data="farther_open_close"))
kb_open_close_syllables.add(button_back_to_learning)

# Обучение (открытый и закрытый слог, 2 страница)
kb_open_close_syllables_2 = InlineKeyboardMarkup()
kb_open_close_syllables_2.add(InlineKeyboardButton("📗 на 1 страницу", callback_data="first_page_syllables"))
kb_open_close_syllables_2.add(button_back_to_learning)

# Обучение (соответствие букв и звуков, 1 страница)
kb_letters_sounds = InlineKeyboardMarkup()
kb_letters_sounds.add(InlineKeyboardButton("📘 на 2 страницу", callback_data="farther_letters_sounds_2"))
kb_letters_sounds.add(button_back_to_learning)

# Обучение (соответствие букв и звуков, 2 страница)
kb_letters_sounds_2 = InlineKeyboardMarkup()
kb_letters_sounds_2.add(InlineKeyboardButton("📘 на 3 страницу", callback_data="farther_letters_sounds_3"))
kb_letters_sounds_2.add(InlineKeyboardButton("📘 на 1 страницу", callback_data="farther_letters_sounds_1"))
kb_letters_sounds_2.add(button_back_to_learning)

# Обучение (соответствие букв и звуков, 3 страница)
kb_letters_sounds_3 = InlineKeyboardMarkup()
kb_letters_sounds_3.add(InlineKeyboardButton("📘 на 4 страницу", callback_data="farther_letters_sounds_4"))
kb_letters_sounds_3.add(InlineKeyboardButton("📘 на 2 страницу", callback_data="farther_letters_sounds_2"))
kb_letters_sounds_3.add(button_back_to_learning)

# Обучение (соответствие букв и звуков, 4 страница)
kb_letters_sounds_4 = InlineKeyboardMarkup()
kb_letters_sounds_4.add(InlineKeyboardButton("📘 на 5 страницу", callback_data="farther_letters_sounds_5"))
kb_letters_sounds_4.add(InlineKeyboardButton("📘 на 3 страницу", callback_data="farther_letters_sounds_3"))
kb_letters_sounds_4.add(button_back_to_learning)

# Обучение (соответствие букв и звуков, 5 страница)
kb_letters_sounds_5 = InlineKeyboardMarkup()
kb_letters_sounds_5.add(InlineKeyboardButton("📘 на 4 страницу", callback_data="farther_letters_sounds_4"))
kb_letters_sounds_5.add(button_back_to_learning)

# Обучение (дифтонги и трифтонги)
kb_diphthongs_triphthongs = InlineKeyboardMarkup()
kb_diphthongs_triphthongs.add(button_back_to_learning)

# Обучение (интонация. тоны)
kb_intonation = InlineKeyboardMarkup()
kb_intonation.add(button_back_to_learning)

# Обучение (ударения)
kb_accents = InlineKeyboardMarkup()
kb_accents.add(button_back_to_learning)

# Обучение (сложности)
kb_hard = InlineKeyboardMarkup()
kb_hard.add(button_back_to_learning)

# Тесты на знание языка
kb_test = InlineKeyboardMarkup()
kb_test.add(button_main_menu)
