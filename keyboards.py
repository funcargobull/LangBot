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

# Обучение (английский)
kb_learning = InlineKeyboardMarkup()
kb_learning.row(InlineKeyboardButton("🎶 произношение", callback_data="pronunciation"),
                InlineKeyboardButton("🔟 числа", callback_data="numbers"))
kb_learning.row(InlineKeyboardButton("🕒 времена", callback_data="tenses"),
                InlineKeyboardButton("📖 словарь", callback_data="vocabulary"))
kb_learning.row(InlineKeyboardButton("🌪️ пунктуация", callback_data="punctuation"),
                InlineKeyboardButton("❓ условия", callback_data="if"))
kb_learning.add(InlineKeyboardButton("📜 степени сравнения", callback_data="degrees"))
kb_learning.add(InlineKeyboardButton("🔢 исчисляемые/неисчисляемые", callback_data="uncount"))
kb_learning.row(InlineKeyboardButton("🫴 пассивный залог", callback_data="passive_voice"),
                InlineKeyboardButton("🗣️ косвенная речь", callback_data="reported_speech"))
kb_learning.add(InlineKeyboardButton("🔖 каузативная форма", callback_data="causative"))

kb_learning.add(button_main_menu)

# Обучение (немецкий)
kb_learning_2 = InlineKeyboardMarkup()
kb_learning_2.row(InlineKeyboardButton("🎶 произношение", callback_data="pronunciation_ger"),
                  InlineKeyboardButton("🫵 местоимения", callback_data="pronouns"))
kb_learning_2.row(InlineKeyboardButton("🗒️ артикли", callback_data="articles"),
                  InlineKeyboardButton("💀 падежи", callback_data="cases"),
                  InlineKeyboardButton("🌩️ склонения", callback_data="declination"))
kb_learning_2.add(InlineKeyboardButton("🧮 имена числительные", callback_data="counts"))
kb_learning_2.add(InlineKeyboardButton("⏲ времена и спряжения глаголов", callback_data="tenses_gerr"))
kb_learning_2.add(InlineKeyboardButton("🧱 построение предложений", callback_data="building_ger"))
kb_learning_2.row(InlineKeyboardButton("⏰ время суток", callback_data="time"),
                  InlineKeyboardButton("❓ условия", callback_data="if_ger"))
kb_learning_2.add(button_main_menu)

# Обучение (немецкий, произношение)
kb_pronunciation_ger = InlineKeyboardMarkup()
kb_pronunciation_ger.add(InlineKeyboardButton("📚 курс 1. гласные и согласные", callback_data="vowels_consonants"))
kb_pronunciation_ger.add(InlineKeyboardButton("📚 курс 2. буквосочетания", callback_data="combination"))
kb_pronunciation_ger.add(InlineKeyboardButton("📚 курс 3. ударение", callback_data="accent_ger"))
kb_pronunciation_ger.add(InlineKeyboardButton("📚 курс 4. долгие и краткие гласные", callback_data="long_short"))
kb_pronunciation_ger.add(InlineKeyboardButton("📚 курс 5. звук R в немецком", callback_data="r"))
button_back = InlineKeyboardButton("⬅ вернуться к разделам", callback_data="back_to_learning")
kb_pronunciation_ger.add(button_back)

button_back_to_learning_ger = InlineKeyboardButton("⬅ вернуться к разделам",
                                                   callback_data="button_back_to_learning_ger")

# Обучение (немецкий, местоимения, 1 страница)
kb_pronouns = InlineKeyboardMarkup()
kb_pronouns.add(InlineKeyboardButton("📗 на 2 страницу", callback_data="farther_pronouns_2"))
kb_pronouns.add(button_back_to_learning_ger)

# Обучение (немецкий, местоимения, 2 страница)
kb_pronouns_2 = InlineKeyboardMarkup()
kb_pronouns_2.add(InlineKeyboardButton("📗 на 1 страницу", callback_data="farther_pronouns_1"))
kb_pronouns_2.add(button_back_to_learning_ger)

# Обучение (немецкий, имена числительные)
kb_counts = InlineKeyboardMarkup()
kb_counts.add(InlineKeyboardButton("📚 курс 1. количественные", callback_data="countable"))
kb_counts.add(InlineKeyboardButton("📚 курс 2. порядковые", callback_data="ordinal"))
kb_counts.add(InlineKeyboardButton("📚 курс 3. дроби", callback_data="fractions"))
kb_counts.add(button_back_to_learning_ger)

# Обучение (немецкий, количественные)
kb_countable = InlineKeyboardMarkup()
back_to_counts = InlineKeyboardButton("⬅ вернуться к курсам", callback_data="back_to_counts")
kb_countable.add(back_to_counts)

# Обучение (немецкий, гласные и согласные)
kb_vowels_consonants = InlineKeyboardMarkup()
kb_vowels_consonants.add(InlineKeyboardButton("📗 на 2 страницу", callback_data="farther_vc_2"))
button_back_courses_ger = InlineKeyboardButton("⬅ вернуться к курсам", callback_data="back_to_courses_ger")
kb_vowels_consonants.add(button_back_courses_ger)

# Обучение (немецкий, гласные и согласные, 2 страница)
kb_vowels_consonants_2 = InlineKeyboardMarkup()
kb_vowels_consonants_2.add(InlineKeyboardButton("📗 на 1 страницу", callback_data="farther_vc_1"))
kb_vowels_consonants_2.add(button_back_courses_ger)

# Обучение (немецкий, буквосочетания, 1 страница)
kb_combination = InlineKeyboardMarkup()
kb_combination.add(InlineKeyboardButton("📘 на 2 страницу", callback_data="farther_comb_2"))
kb_combination.add(button_back_courses_ger)

# Обучение (немецкий, буквосочетания, 2 страница)
kb_combination_2 = InlineKeyboardMarkup()
kb_combination_2.add(InlineKeyboardButton("📘 на 1 страницу", callback_data="farther_comb_1"))
kb_combination_2.add(button_back_courses_ger)

# Обучение (немецкий, ударение, 1 страница)
kb_accent_ger = InlineKeyboardMarkup()
kb_accent_ger.add(InlineKeyboardButton("📙 на 2 страницу", callback_data="farther_accent_2"))
kb_accent_ger.add(button_back_courses_ger)

# Обучение (немецкий, ударение, 2 страница)
kb_accent_ger_2 = InlineKeyboardMarkup()
kb_accent_ger_2.add(InlineKeyboardButton("📙 на 1 страницу", callback_data="farther_accent_1"))
kb_accent_ger_2.add(button_back_courses_ger)

# Обучение (долгие и краткие гласные)
kb_long_short = InlineKeyboardMarkup()
kb_long_short.add(button_back_courses_ger)

# Обучение (времена и спряжение глаголов)
kb_tenses_ger = InlineKeyboardMarkup()
kb_tenses_ger.add(InlineKeyboardButton("📚 курс 1. настоящее время", callback_data="present"))
kb_tenses_ger.add(InlineKeyboardButton("📚 курс 2. прошедшее время", callback_data="past"))
kb_tenses_ger.add(InlineKeyboardButton("📚 курс 3. будущее время", callback_data="future"))
kb_tenses_ger.add(button_back)

# Обучение (настоящее время)
button_back_to_tenses = InlineKeyboardButton("⬅ вернуться к курсам", callback_data="back_to_tenses")
kb_present = InlineKeyboardMarkup().add(button_back_to_tenses)

# Обучение (прошедшее время, 1 страница)
kb_past = InlineKeyboardMarkup()
kb_past.add(InlineKeyboardButton("📘 на 2 страницу", callback_data="farther_past_2"))
kb_past.add(button_back_to_tenses)

# Обучение (прошедшее время, 2 страница)
kb_past_2 = InlineKeyboardMarkup()
kb_past_2.add(InlineKeyboardButton("📘 на 1 страницу", callback_data="farther_past_1"))
kb_past_2.add(button_back_to_tenses)

# Обучение (будущее время, 1 страница)
kb_future = InlineKeyboardMarkup()
kb_future.add(InlineKeyboardButton("📗 на 2 страницу", callback_data="farther_future_2"))
kb_future.add(button_back_to_tenses)

# Обучение (будущее время, 2 страница)
kb_future_2 = InlineKeyboardMarkup()
kb_future_2.add(InlineKeyboardButton("📗 на 1 страницу", callback_data="farther_future_1"))
kb_future_2.add(button_back_to_tenses)

# Обучение (построение предложений)
kb_building = InlineKeyboardMarkup()
kb_building.add(InlineKeyboardButton("📚 курс 1. порядок слов", callback_data="word_order"))
kb_building.add(InlineKeyboardButton("📚 курс 2. второстепенные члены", callback_data="minor_members"))
kb_building.add(InlineKeyboardButton("📚 курс 3. два глагола", callback_data="two_verbs"))
kb_building.add(button_back)

# Обучение (порядок слов, 1 страница)
kb_word_order = InlineKeyboardMarkup()
kb_word_order.add(InlineKeyboardButton("📘 на 2 страницу", callback_data="farther_word_order_2"))
back_to_word_order = InlineKeyboardButton("⬅ вернуться к курсам", callback_data="back_to_word_order")
kb_word_order.add(back_to_word_order)

# Обучение (порядок слов, 2 страница)
kb_word_order_2 = InlineKeyboardMarkup()
kb_word_order_2.add(InlineKeyboardButton("📘 на 1 страницу", callback_data="farther_word_order_1"))
kb_word_order_2.add(back_to_word_order)

# Обучение (второстепенные члены)
kb_minor_members = InlineKeyboardMarkup().add(back_to_word_order)

# Обучение (время суток)
kb_time = InlineKeyboardMarkup().add(button_back_to_learning_ger)

# Обучение (условия, 1 страница)
kb_if_ger = InlineKeyboardMarkup()
kb_if_ger.add(InlineKeyboardButton("📓 на 2 страницу", callback_data="farther_if_ger_2"))
kb_if_ger.add(button_back_to_learning_ger)

# Обучение (условия, 2 страница)
kb_if_ger_2 = InlineKeyboardMarkup()
kb_if_ger_2.add(InlineKeyboardButton("📓 на 1 страницу", callback_data="farther_if_ger_1"))
kb_if_ger_2.add(button_back_to_learning_ger)

# Обучение (склонения, 1 страница)
kb_declination = InlineKeyboardMarkup()
kb_declination.add(InlineKeyboardButton("📒 на 2 страницу", callback_data="farther_declination_2"))
kb_declination.add(button_back_to_learning_ger)

# Обучение (склонения, 2 страница)
kb_declination_2 = InlineKeyboardMarkup()
kb_declination_2.add(InlineKeyboardButton("📒 на 3 страницу", callback_data="farther_declination_3"))
kb_declination_2.add(InlineKeyboardButton("📒 на 1 страницу", callback_data="farther_declination_1"))
kb_declination_2.add(button_back_to_learning_ger)

# Обучение (склонения, 3 страница)
kb_declination_3 = InlineKeyboardMarkup()
kb_declination_3.add(InlineKeyboardButton("📒 на 4 страницу", callback_data="farther_declination_4"))
kb_declination_3.add(InlineKeyboardButton("📒 на 2 страницу", callback_data="farther_declination_2"))
kb_declination_3.add(button_back_to_learning_ger)

# Обучение (склонения, 4 страница)
kb_declination_4 = InlineKeyboardMarkup()
kb_declination_4.add(InlineKeyboardButton("📒 на 5 страницу", callback_data="farther_declination_5"))
kb_declination_4.add(InlineKeyboardButton("📒 на 3 страницу", callback_data="farther_declination_3"))
kb_declination_4.add(button_back_to_learning_ger)

# Обучение (склонения, 5 страница)
kb_declination_5 = InlineKeyboardMarkup()
kb_declination_5.add(InlineKeyboardButton("📒 на 4 страницу", callback_data="farther_declination_4"))
kb_declination_5.add(button_back_to_learning_ger)

# Обучение (артикли)
kb_articles = InlineKeyboardMarkup()
kb_articles.add(button_back_to_learning_ger)

# Обучение (падежи, 1 страница)
kb_cases = InlineKeyboardMarkup()
kb_cases.add(InlineKeyboardButton("📕 на 2 страницу", callback_data="farther_cases_2"))
kb_cases.add(button_back_to_learning_ger)

# Обучение (падежи, 2 страница)
kb_cases_2 = InlineKeyboardMarkup()
kb_cases_2.add(InlineKeyboardButton("📕 на 3 страницу", callback_data="farther_cases_3"))
kb_cases_2.add(InlineKeyboardButton("📕 на 1 страницу", callback_data="farther_cases_1"))
kb_cases_2.add(button_back_to_learning_ger)

# Обучение (падежи, 3 страница)
kb_cases_3 = InlineKeyboardMarkup()
kb_cases_3.add(InlineKeyboardButton("📕 на 2 страницу", callback_data="farther_cases_2"))
kb_cases_3.add(button_back_to_learning_ger)

# Обучение (времена)
kb_learning_tenses = InlineKeyboardMarkup()
kb_learning_tenses.add(button_back)
button_back_to_learning = InlineKeyboardButton("⬅ вернуться к курсам", callback_data="back_to_courses")

# Обучение (основы произношения)
kb_pronunciation = InlineKeyboardMarkup()
kb_pronunciation.add(
    InlineKeyboardButton("📚 курс 1. открытый и закрытый слоги", callback_data="open_close_syllable"))
kb_pronunciation.add(
    InlineKeyboardButton("📚 курс 2. соответствие букв и звуков", callback_data="letters_sounds"))
kb_pronunciation.add(
    InlineKeyboardButton("📚 курс 3. дифтонги и трифтонги", callback_data="diphthongs_triphthongs"))
kb_pronunciation.add(InlineKeyboardButton("📚 курс 4. интонация. тоны", callback_data="intonation"))
kb_pronunciation.add(InlineKeyboardButton("📚 курс 5. ударения", callback_data="accents"))
kb_pronunciation.add(InlineKeyboardButton("📚 курс 6. сложности", callback_data="hard_things"))
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

# Обучение (пунктуация)
kb_punctuation = InlineKeyboardMarkup()
kb_punctuation.row(InlineKeyboardButton("📚 курс 1. запятая", callback_data="comma"),
                   InlineKeyboardButton("📚 курс 2. точка", callback_data="period"))
kb_punctuation.add(InlineKeyboardButton("📚 курс 3. кавычки", callback_data="quote_marks"))
kb_punctuation.add(InlineKeyboardButton("📚 курс 4. вопросительный и восклицательный знаки", callback_data="marks"))
kb_punctuation.add(InlineKeyboardButton("📚 курс 5. двоеточие и точка с запятой", callback_data="colons"))
kb_punctuation.row(InlineKeyboardButton("📚 курс 6. скобки", callback_data="parentheses"),
                   InlineKeyboardButton("📚 курс 7. тире и дефис", callback_data="dash_hyphen"))
kb_punctuation.add(InlineKeyboardButton("📚 курс 8. апостроф", callback_data="apostrophe"))
kb_punctuation.add(button_back)

# Обучение (запятая, 1 страница)
kb_comma = InlineKeyboardMarkup()
kb_comma.add(InlineKeyboardButton("📕 на 2 страницу", callback_data="farther_comma_2"))
button_back_to_punctuation = InlineKeyboardButton("⬅ вернуться к курсам", callback_data="back_to_punctuation")
kb_comma.add(button_back_to_punctuation)

# Обучение (запятая, 2 страница)
kb_comma_2 = InlineKeyboardMarkup()
kb_comma_2.add(InlineKeyboardButton("📕 на 1 страницу", callback_data="farther_comma_1"))
kb_comma_2.add(button_back_to_punctuation)

# Обучение (точка)
kb_period = InlineKeyboardMarkup().add(button_back_to_punctuation)

# Обучение (апостроф, 1 страница)
kb_apostrophe = InlineKeyboardMarkup()
kb_apostrophe.add(InlineKeyboardButton("📙 на 2 страницу", callback_data="farther_apostrophy_2"))
kb_apostrophe.add(button_back_to_punctuation)

# Обучение (апостроф, 2 страница)
kb_apostrophe_2 = InlineKeyboardMarkup()
kb_apostrophe_2.add(InlineKeyboardButton("📙 на 1 страницу", callback_data="farther_apostrophy_1"))
kb_apostrophe_2.add(button_back_to_punctuation)

# Обучение (словарь)
kb_vocabulary = InlineKeyboardMarkup().add(button_back)

# Степени сравнения (1 страница)
kb_degrees = InlineKeyboardMarkup()
kb_degrees.add(InlineKeyboardButton("📘 на 2 страницу", callback_data="farther_degrees_2"))
kb_degrees.add(button_back)

# Степени сравнения (2 страница)
kb_degrees_2 = InlineKeyboardMarkup()
kb_degrees_2.add(InlineKeyboardButton("📘 на 3 страницу", callback_data="farther_degrees_3"))
kb_degrees_2.add(InlineKeyboardButton("📘 на 1 страницу", callback_data="farther_degrees_1"))
kb_degrees_2.add(button_back)

# Степени сравнения (3 страница)
kb_degrees_3 = InlineKeyboardMarkup()
kb_degrees_3.add(InlineKeyboardButton("📘 на 2 страницу", callback_data="farther_degrees_2"))
kb_degrees_3.add(button_back)

# Английские числа
kb_numbers = InlineKeyboardMarkup()
kb_numbers.add(button_back)

# Тесты на знание языка
kb_test = InlineKeyboardMarkup()
kb_test.add(button_main_menu)
