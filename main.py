# -*- coding: utf-8 -*-

import asyncio
import logging
import os
from contextlib import suppress
from random import choice

from aiogram import Bot, types, Dispatcher
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from googletrans import Translator

import base
import functions as fn
import keyboards as kb

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5911147477:AAEsJtQB0A4DQlXPbvdefbQu2EyvYjGGCok", parse_mode="HTML")
dp = Dispatcher(bot)
translator = Translator()


async def edit_media(callback_query, url, caption, keyboard):
    await callback_query.message.edit_media(InputMediaPhoto(media=url, caption=caption), reply_markup=keyboard)


@dp.message_handler(text="/start")
async def start_(msg: types.Message):
    # /start
    await bot.send_photo(str(msg.from_user.id),
                         photo="https://i.postimg.cc/WbC1cr9r/file-1-1.jpg",
                         caption="👋 <b>итак</b>, это - <b>главное меню.</b>\n🌍 выберите язык:",
                         reply_markup=kb.kb_main)


@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def start_2(callback_query: types.CallbackQuery):
    # Главное меню
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query, "https://i.postimg.cc/WbC1cr9r/file-1-1.jpg",
                     "👋 <b>итак</b>, это - <b>главное меню.</b>\n🌍 выберите язык:", kb.kb_main)


@dp.callback_query_handler(lambda c: c.data == 'english' or c.data == 'german' or c.data == 'back')
async def start_lang(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # Английский (старт)
    if callback_query.data == "english":
        base.language(str(callback_query.from_user.id), "английский", set=True, get=False)
        await edit_media(callback_query, "https://i.postimg.cc/2S4gpjqt/2023-03-21-190241474.png",
                         f"🇬🇧 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыберите опцию:",
                         kb.kb_english)


    # Немецкий (старт)
    elif callback_query.data == "german":
        base.language(str(callback_query.from_user.id), "немецкий", set=True, get=False)
        await edit_media(callback_query, "https://i.postimg.cc/Dz7vHMzq/2023-03-21-190610782.png",
                         f"🇩🇪 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыберите опцию:",
                         kb.kb_english)

    # Назад
    elif callback_query.data == "back":
        if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
            await edit_media(callback_query, "https://i.postimg.cc/2S4gpjqt/2023-03-21-190241474.png",
                             f"🇬🇧 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыберите опцию:",
                             kb.kb_english)
        else:
            await edit_media(callback_query, "https://i.postimg.cc/Dz7vHMzq/2023-03-21-190610782.png",
                             f"🇩🇪 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыберите опцию:",
                             kb.kb_english)


# Слово дня
@dp.callback_query_handler(lambda c: c.data == "word_of_day")
async def word_of_the_day(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    file = InputMediaPhoto(media="https://i.postimg.cc/d3z66dQN/photo-2023-03-21-11-50-44-1.jpg",
                           caption="✨ подождите немного...")
    m = await callback_query.message.edit_media(file)
    await asyncio.sleep(3)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        text, name, send_pronunciation = fn.parse_english_word_of_the_day()
        file = InputMediaPhoto(media="https://i.postimg.cc/T3Hdxc7y/2.png",
                               caption=text)
        await m.edit_media(file, reply_markup=kb.kb_word_of_day)
        if send_pronunciation:
            x = await bot.send_audio(str(callback_query.from_user.id), open(f"{name}.mp3", "rb"),
                                     title="анг. произношение (удалится через 10 с)")
            asyncio.create_task(delete_message(x, 10))
            os.remove(f"{name}.mp3")
    else:
        text, name = fn.parse_german_word_of_the_day()
        file = InputMediaPhoto(media="https://i.postimg.cc/T3Hdxc7y/2.png",
                               caption=text)
        await m.edit_media(file, reply_markup=kb.kb_word_of_day)
        x = await bot.send_audio(str(callback_query.from_user.id), open(f"{name}.mp3", "rb"),
                                 title="нем. произношение (удалится через 10 с)")
        asyncio.create_task(delete_message(x, 10))
        os.remove(f"{name}.mp3")


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


# Факты о стране
@dp.callback_query_handler(lambda c: c.data == "facts_about_country" or c.data == "farther")
async def facts_about_country(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        with open("facts/english_facts.txt", "r", encoding="utf-8") as f:
            fact, photo = map(str, choice(f.readlines()).split("*"))
            s = fact.split("\\n")
            fact = s[0].lower() + "\n" + s[1].lower()
            f.close()
    else:
        with open("facts/german_facts.txt", "r", encoding="utf-8") as f:
            fact, photo = map(str, choice(f.readlines()).split("*"))
            f.close()
        fact_de, fact_ru = fact.split("\\n")
        fact = fact_de[0:3] + fact_de[3].lower() + fact_de[4:] + "\n" + fact_ru.lower()

    await edit_media(callback_query, photo, fact, kb.kb_facts_about_country)


# Словесный марафон
@dp.callback_query_handler(lambda c: c.data == "word_marathon" or c.data == "choose_category")
async def word_marathon(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        await edit_media(callback_query,
                         "https://i.postimg.cc/Y91q9HLv/1x20-The-One-with-the-Evil-Orthodontist-friends-28258398-1280-720.jpg",
                         "🇬🇧 выберите категорию:", kb.kb_word_marathon)

    else:
        await edit_media(callback_query,
                         "https://i.postimg.cc/Y91q9HLv/1x20-The-One-with-the-Evil-Orthodontist-friends-28258398-1280-720.jpg",
                         "🇩🇪 выберите категорию:", kb.kb_word_marathon)


@dp.callback_query_handler(lambda c: c.data == "all_parts" or c.data == "farther_all")
async def all_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/")
    text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    await edit_media(callback_query, image, text, kb.kb_word_marathon_all)


@dp.callback_query_handler(lambda c: c.data == "nouns" or c.data == "farther_nouns")
async def nouns_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/noun/")
        text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    else:
        word, article, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/noun/",
                                                                                True)
        text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript, article, True)

    await edit_media(callback_query, image, text, kb.kb_word_marathon_nouns)


@dp.callback_query_handler(lambda c: c.data == "verbs" or c.data == "farther_verbs")
async def verbs_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/verb/")
    text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    await edit_media(callback_query, image, text, kb.kb_word_marathon_verbs)


@dp.callback_query_handler(lambda c: c.data == "adjectives" or c.data == "farther_adjectives")
async def adjectives_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/adjective/")
    text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    await edit_media(callback_query, image, text, kb.kb_word_marathon_adjectives)


@dp.callback_query_handler(lambda c: c.data == "adverbs" or c.data == "farther_adverbs")
async def adverbs_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/adverb/")
    text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    await edit_media(callback_query, image, text, kb.kb_word_marathon_adverbs)


def parts_of_speech(id, word, translated, transcript, article="", is_german_noun=False):
    if base.language(str(id), '', set=False, get=True) == "английский":
        text = f'''
<b>слово: </b>{word}
<b>перевод: </b>{translated}
'''
    else:
        if not is_german_noun and base.language(str(id), '', set=False, get=True) == "немецкий":
            word = translator.translate(word, src="en", dest="de").text
        else:
            word = f"{article} {word}"
        text = f'''
<b>слово: </b>{word}
<b>перевод: </b>{translated}
'''
    if transcript == "[]":
        pass
    else:
        if base.language(str(id), '', set=False, get=True) == "английский":
            text += f"<b>транскрипция: </b>{transcript}"
    return text


# Тесты на знание языка
@dp.callback_query_handler(lambda c: c.data == "language_test")
async def knowledge_test(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(callback_query.from_user.id, '', set=False, get=True) == "английский":
        caption = "📓 чтобы пройти тест, перейдите по <b>ссылке:</b>\n💻 https://englishtest.pythonanywhere.com"
    else:
        caption = "📓 чтобы пройти тест, перейдите по <b>ссылке:</b>\n💻 https://germantest.pythonanywhere.com"
    await edit_media(callback_query, "https://i.postimg.cc/BvkMv55Y/2023-03-21-203513060.png", caption, kb.kb_test)


# Обучение
@dp.callback_query_handler(
    lambda c: c.data == "learning" or c.data == "back_to_learning" or c.data == "button_back_to_learning_ger")
async def learning(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        await edit_media(callback_query, "https://i.postimg.cc/8PfNJdr8/think.jpg",
                         '🎒 выберите раздел:\n\n⚠ <b>p.s. в курсах вы можете увидеть местоимение "I" с маленькой буквы. это сделано лишь для поддержания стиля бота. запомните, "I" всегда пишется с большой буквы.</b>',
                         kb.kb_learning)
    else:
        await edit_media(callback_query, "https://i.postimg.cc/8PfNJdr8/think.jpg",
                         '🎒 выберите раздел:\n\n⚠ <b>p.s. все существительные в немецком пишутся с большой буквы.</b>',
                         kb.kb_learning_2)


# Обучение (немецкий, произношение)
@dp.callback_query_handler(lambda c: c.data == 'pronunciation_ger' or c.data == "back_to_courses_ger")
async def pronunciation_ger(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query, "https://i.postimg.cc/8PfNJdr8/think.jpg",
                     '🎶 выбрана опция: <b>"произношение".</b>\nвыберите курс:',
                     kb.kb_pronunciation_ger)


# Обучение (немецкий, гласные и согласные, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'vowels_consonants' or c.data == "farther_vc_1")
async def vowels_consonants(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 <b>гласные буквы</b>
<b>A</b> [a], <b>O</b> [o], <b>E</b> [э], <b>U</b> [у], <b>I</b> [и] так и читаются.
также существуют гласные с <b>умлаутом</b> (двумя точками сверху). они произносятся с более узким ртом, например: <i>schon [шон] (уже)</i> - <i>schön [шён] (прекрасно)</i>.
<b>A</b> Umlaut читается как "э", например: <i>Mädchen [мэдхен] - девочка.</i>
<b>Y (эпсилон)</b> читается как "ю", например: <i>Lyrik [люрик] - лирика</i>
    '''
    await edit_media(callback_query,
                     "https://www.fluentin3months.com/wp-content/uploads/2021/09/german-pronunciation.jpg",
                     text,
                     kb.kb_vowels_consonants)


# Обучение (немецкий, гласные и согласные, 2 страница)
@dp.callback_query_handler(lambda c: c.data == "farther_vc_2")
async def vowels_consonants_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 <b>согласные буквы</b>
<b>W</b> [вэ] читается как "в": <i>was? [вас] – что?</i>.
<b>Z</b> [цэт] читается как "ц": <i>Ziel [циль] - цель</i>.
<b>S</b> [эс] читается как "с": <i>Haus [хаус] – дом</i>, но если <b>S</b> находится перед или между гласными, S читается как "з": <i>Sofa [зофа] – диван</i>.
<b>ß</b> [эсцэт] читается как долгое "с": <i>Straße [штрассэ] - улица</i>.
<b>F</b> [эф], <b>V</b> [фау] читаются как "ф": <i>Fuchs [фукс] - лиса, Volk [фольк] – народ</i>.
<b>J</b> [йот] читается как "й": <i>Joghurt [йогурт] – йогурт</i>
<b>L</b> [эль] – читается как "л": <i>Lampe [лампэ] – лампа</i>.
<b>R</b> [эр] читается как "р", но только нужно представить, что вы картавый, а на конце слова читается как короткое "а": <i>Russland [Руссланд] – Россия, Mutter [мутта] – мама</i>.
<b>H</b> [ха] в начале слова читается как выдох: <i>Haus [хаус] – дом</i>, а в середине или конце не читается вообще: <i>gehen [геен] – идти</i>.
    '''
    await callback_query.message.edit_caption(caption=text, reply_markup=kb.kb_vowels_consonants_2)


# Обучение (немецкий, буквосочетания, 1 страница)
@dp.callback_query_handler(lambda c: c.data == "combination" or c.data == "farther_comb_1")
async def combination(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 <b>буквосочетания согласных</b>
<b>ch</b> читается как "х": <i>Loch [лох] – дыра,</i>
<b>chs</b> читается как "кс": <i>Fuchs [фукс] – лиса,</i>
<b>sch</b> читается как "ш": <i>Schrank [шранк] - шкаф,</i>
<b>tsch</b> читается как "ч": <i>Deutsch [дойч] - немецкий язык,</i>
<b>ck</b> читается как твердое "к": <i>drücken [дрюкэн] – давить,</i>
<b>sp/st</b> в начале слова или корня читаются как "шп/шт": <i>spontan [шпонтан] - спонтанный,</i>
<b>qu</b> читается как "кв": <i>Quatsch [квач] - чепуха,</i>
<b>-tion</b> читается как "цион": <i>Station [штацион] - станция.</i>
    '''
    await edit_media(callback_query,
                     "https://www.de-online.ru/novosti/2022-1/Pravila_cteniya-urok.jpg",
                     text,
                     kb.kb_combination)


# Обучение (немецкий, буквосочетания, 2 страница)
@dp.callback_query_handler(lambda c: c.data == "farther_comb_2")
async def combination(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 <b>буквосочетания гласных</b>
<b>ei</b> читается как "ай": <i>Weimar [Ваймар],</i>
<b>ie</b> читается как долгое "и": <i>Liebe [либэ] – любовь,</i>
<b>eu</b> читается как "ой": <i>heute [хойтэ] – сегодня,</i>
<b>äu</b> читается также как "ой": <i>Häuser [хойзэр] – домa.</i>
    '''
    await callback_query.message.edit_caption(caption=text, reply_markup=kb.kb_combination_2)


# Обучение (немецкий, ударение, 1 страница)
@dp.callback_query_handler(lambda c: c.data == "accent_ger" or c.data == 'farther_accent_1')
async def accent_ger(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📙 ударение почти всегда падает на <b>первый слог</b>, кроме:
- слов с безударными приставками (be-, ge-, er-, ver-, zer-, ent-, emp-, miss-)
- заимствованных слов (Comp<b>u</b>ter)
- других исключений (war<b>u</b>m)
📙 <b>также действуют следующие правила:</b>
- спряжение и склонение на ударение не влияют
- в сложных словах ударение падает на первое (Wohnzimmer, Schwimmbad)
- в словах из трех частей ударение падает на первую и последнюю часть слова
- в аббревиатурах ударение ставится на <b>последнюю</b> букву (BMW, USA)
- сочетания <i>-ei, -ieren, ur-, un-</i> всегда ударные
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/XNDZRX7Y/accenrt.jpg",
                     text,
                     kb.kb_accent_ger)


# Обучение (немецкий, ударение, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_accent_2')
async def accent_ger_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📙 <b>список безударных суффиксов:</b>
- для прилагательных: <i>-bar, -haft, -ig, -isch, -lich</i>
- для существительных <i>-chen, -er, -heit, -keit, -in, -lein, -ling, -nis, -schaft, -tum, -ung</i>
📙 <b>список ударных приставок:</b>
<i>ab-, an-, auf, aus-, bei-, ein-, empor-, fort-, los-, mit-, nach-, nieder-, weg-, weiter-, wieder-</i>
    '''
    await callback_query.message.edit_caption(caption=text, reply_markup=kb.kb_accent_ger_2)


# Обучение (немецкий, долгие и краткие гласные)
@dp.callback_query_handler(lambda c: c.data == 'long_short')
async def accent_ger_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 <b>длинные</b> гласные:
- перед h <i>(gehen, stehen, sehen)</i>
- при двойных гласных <i>(Meer, See, Staat, Boot)</i>
- в сочетание "ie" <i>(fliegen, lieben)</i>
📕 <b>краткие</b> гласные:
- если после стоят двойные согласные <i>(schwimmen, vergessen)</i>
- чаще всего, если после стоят 2 или более согласных <i>(manchmal, interessant)</i>
    '''
    await edit_media(callback_query,
                     "https://www.brainscape.com/academy/content/images/size/w1340/2020/08/Accents-in-languages.jpg",
                     text, kb.kb_long_short)


# Обучение (немецкий, звук R в немецком)
@dp.callback_query_handler(lambda c: c.data == 'r')
async def r(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📒 <b>гортанная R произносится:</b>
- в начале слов
- после согласных в начале слова
- после кратких гласных и при двойной "R"
📒 <b>случаи, когда R произносится как "а":</b>
- местоимения с R на конце <i>(mir, ihr, deiner, ihrer)</i>
- артикли <i>(der, einer)</i> и предлоги <i>(unter, hinter)</i>
- после долгих гласных <i>(Ohr, Uhr)</i>
- в приставках <i>er-, her-, ver-, zer-, vor-, über-</i>
    '''
    await edit_media(callback_query,
                     "https://i.ytimg.com/vi/lc5WIxAsJU4/maxresdefault.jpg",
                     text, kb.kb_long_short)


# Обучение (немецкий, местоимения, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'pronouns' or c.data == "farther_pronouns_1")
async def pronouns(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 личные местоимения <b>(Personalpronomen)</b> изменяются по лицам, числам и падежам (курс по падежам немного позже)
📗 <b>du и ihr</b> употребляются чаще всего для неформального общения и в отношениях взрослых к детям:
<i>Du wirst heute Abendessen kochen. - Ты будешь готовить сегодня ужин. Geht ihr heute mit uns ins Theater? - Вы идёте с нами в театр?</i>
📗 местоимение <b>Sie</b> используется в официальных ситуациях. это - вежливая форма.
📗 местоимение <b>es</b> часто обозначает неопределенные связи или состояние: <i>Es regnet. - Идёт дождь.</i>
📗 <b>таблица личных местоимений приведена выше.</b>
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/SNwwgcXn/image.png",
                     text, kb.kb_pronouns)


# Обучение (немецкий, местоимения, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_pronouns_2')
async def pronouns_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 притяжательные местоимения <b>(Possessivpronomen)</b> выражают владение или принадлежность.
📗 выбор зависит от личного местоимения или существительного, к которому оно относится. какое окончание будет у притяжательного местоимения, зависит от рода существительного, стоящего за ним.
📗 <b>артикль</b> между притяжательными местоимениями и существительными <b>не ставится</b>, поэтому фраза: <i>Das ist das mein Kind - неверна.</i>
📗 если существительное уже упоминалось в разговоре или тексте, то в следующем предложении его вполне можно заменить на притяжательное местоимение:
<i>Wem gehören diese Taschen? - Das sind meine. (Чьи это сумки? - Это мои)</i>
<i>Geben Sie mir bitte Ihre Telefonnummer. - Meine? (Дайте, пожалуйста, Ваш номер телефона. - Мой?)</i>
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/7ZdDDRYX/image.png",
                     text, kb.kb_pronouns_2)


# Обучение (немецкий, времена и спряжение глаголов)
@dp.callback_query_handler(lambda c: c.data == 'tenses_gerr' or c.data == "back_to_tenses")
async def tenses_ger(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query, "https://i.postimg.cc/8PfNJdr8/think.jpg",
                     '⏲ выбрана опция: <b>"времена и спряжение глаголов".</b>\nвыберите курс:',
                     kb.kb_tenses_ger)


# Обучение (немецкий, настоящее время)
@dp.callback_query_handler(lambda c: c.data == 'present')
async def present(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 <b>настоящее время (Präsens) нужно для выражения того, что происходит в момент речи.</b> само действие могло начаться и в прошлом, главное, чтобы оно не завершилось в настоящем.
<i>Es ist (heute) sehr heiß. - (Сегодня) очень жарко.</i>
📕 если ситуацию невозможно привязать к определенному моменту, тоже употребляется Präsens:
<i>Neon ist ein Edelgas. - Неон - инертный газ.</i>
📕 <b>как образуется Präsens?</b>
<i>подлежащее</i> + <b>смысловой глагол в Präsens</b>
📕 <b>таблица спряжения глагола в настоящем времени показана выше</b>. например:
<i>ich gehe, du gehst, er/es/sie/man geht, wir gehen, ihr geht, sie/Sie gehen</i>
    '''
    await edit_media(callback_query, "https://i.postimg.cc/tTRL7N8m/present.png", text, kb.kb_present)


# Обучение (немецкий, прошедшее время, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'past' or c.data == "farther_past_1")
async def past(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 в немецком есть два варианта выражения прошедшего времени: <b>Präteritum и Perfekt.</b>
📘 <b>Präteritum</b> нужен для указания на действие, произошедшее в прошлом, но завершившееся к настоящему моменту.
<b>Präteritum</b> сильных глаголов довольно сложный, и его нужно учить, а у слабых и модальных глаголов между <b>основой и личным окончанием</b> встает <i>t(e)-</i>, а умлаут убегает.
📘 <b>как образуется Präteritum?</b>
<i>подлежащее</i> + <b>смысловой глагол в Präteritum</b>
📘 <b>таблица спряжения глагола в Präteritum показана выше</b>. например:
<i>ich sagte, du sagtest, er/es/sie/man sagte, wir sagten, ihr sagtet, sie/Sie sagten</i>
    '''
    await edit_media(callback_query, "https://i.postimg.cc/rsKvcGHX/past.png", text, kb.kb_past)


# Обучение (немецкий, прошедшее время, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_past_2')
async def past_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 <b>Perfekt нужен для обозначения действия, которое на момент речи завершилось, но его результат актуален для настоящего.</b>
сказуемое состоит из вспомогательного глагола <b>haben/sein</b> в настоящем времени и смыслового в <b>Partizip II</b>.
📘 <b>как образуется Perfekt?</b>
<i>подлежащее</i> + <b>haben/sein в Präsens</b> + <b>Partizip II смыслового глагола</b>
📘 у большинства слабых глаголов к основе прибавляется приставка <i>ge- и -t на конце</i>, у сильных на конце стоит <i>-en</i>.
📘 <b>таблица спряжения глагола в Perfekt показана выше</b>. например:
<i>ich habe gemacht, du hast gemacht, er/es/sie/man hat gemacht, wir haben gemacht, ihr habt gemacht, sie/Sie haben gemacht</i>
    '''
    await edit_media(callback_query, "https://i.postimg.cc/SRhkZMP6/perfect.png", text, kb.kb_past_2)


# Обучение (немецкий, будущее время, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'future' or c.data == "farther_future_1")
async def future(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 <b>Futur I нужен для указания на действие, которое произойдет в будущем, иногда в контексте твердого намерения или команды</b>
📗 <b>как образуется Futur I?</b>
<i>подлежащее</i> + <b>werden в Präsens</b> + <b>Partizip II смыслового глагола</b> + <b>haben в Infinitiv</b>
📗 <b>таблица спряжения глагола в Futur I показана выше</b>. например:
<i>ich werde machen, du wirst machen, er/es/sie/man wird machen, wir werden machen, ihr werdet machen, sie/Sie werden machen</i>
    '''
    await edit_media(callback_query, "https://i.postimg.cc/4x64rZtv/future-1.png", text, kb.kb_future)


# Обучение (немецкий, будущее время, 2 страница)
@dp.callback_query_handler(lambda c: c.data == "farther_future_2")
async def future_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 <b>Futur II нужен, чтобы показать действие, которое завершится в будущем, часто к определенному моменту.</b>
📗 <b>Futur II</b> соединяет в себе сразу два времени, получается Perfekt в Futur
📗 <b>таблица спряжения глагола в Futur II показана выше</b>. например:
<i>ich werde gemacht haben, du wirst gemacht haben, er/es/sie/man wird gemacht haben, wir werden gemacht haben, ihr werdet gemacht haben, sie/Sie werden gemacht haben</i>
    '''
    await edit_media(callback_query, "https://i.postimg.cc/ZRx4MLdT/future-2.png", text, kb.kb_future_2)


# Обучение (немецкий, построение предложений)
@dp.callback_query_handler(lambda c: c.data == 'building_ger' or c.data == "back_to_word_order")
async def building_ger(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query, "https://i.postimg.cc/8PfNJdr8/think.jpg",
                     '🧱 выбрана опция: <b>"построение предложений".</b>\nвыберите курс:',
                     kb.kb_building)


# Обучение (немецкий, порядок слов, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'word_order' or c.data == 'farther_word_order_1')
async def word_order(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 порядок слов в <b>утвердительном</b> предложений - <b>прямой</b>. это означает, что сначала идет подлежащее, затем - сказуемое.
<i>Ich suche eine Wohnung. – Я (подлежащее) ищу (сказуемое) квартиру.</i>
📘 но когда задается вопрос, порядок слов меняется на <b>обратный</b>, т.е. подлежащее и сказуемое меняются местами.
<i>Was suchst du? – Что ты ищешь?</i>
📘 обратный порядок слов возможен и в <b>восклицательных</b> предложениях
<i>Hat der vielleicht lange Haare! – Ну и длинные же у него волосы!</i>
    '''
    await edit_media(callback_query,
                     "https://www.de-online.ru/novosti/07-2022/poryadok-slov-v-nemetskom-predlozhenii-tablica_tek.jpg",
                     text, kb.kb_word_order)


# Обучение (немецкий, порядок слов, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_word_order_2')
async def word_order_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 в придаточном предложении сначала идет <b>слово, которое и делает его придаточным</b>. затем идет подлежащее, а сказуемое уходит в конец предложения. второстепенные члены помещаются между подлежащим и сказуемым.
<i>Ich weiß nicht,</i> <b>ob er</b> <i>heute nach Hause</i> <b>kommt</b>. <i>– Я не знаю, придет ли он сегодня домой.</i>
📘 <b>но</b> есть слова, не влияющие на порядок слов в предложении, например: <i>und, aber, denn, oder, sondern</i>. <b>но это только в придаточном предложении!</b>
📘 придаточное предложение может стоять как после главного, так и до него.
<i>Оb er heute nach Hause kommt, weiß ich nicht. – Придет ли он сегодня домой, я не знаю.</i>
📘 если в придаточном предложении <b>составная глагольная форма</b>, то на конец предложения будет уходить ее спрягаемый элемент:
<i>Ich glaube, dass er heute spät nach Hause kommen</i> <b>will</b>. <i>– Я полагаю, что он сегодня поздно домой прийти хочет.</i>
📘 <b>исключением</b> из этого правила является двойной инфинитив:
<i>Er sagt, dass er heute spät nach Hause</i> <b>hat</b> <i>kommen wollen. – Он говорит, что хотел сегодня поздно прийти домой.</i>
    '''
    await callback_query.message.edit_caption(caption=text, reply_markup=kb.kb_word_order_2)


# Обучение (немецкий, второстепенные члены)
@dp.callback_query_handler(lambda c: c.data == 'minor_members')
async def minor_members(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 здесь все просто. если вы захотите поставить в начало предложений второстепенный член, порядок слов изменится на <b>обратный</b>.
<i>Ich gehe heute ins Kino. – Я иду сегодня в кино.</i>
<i>Heute gehe ich ins Kino. – Сегодня иду я в кино.</i>
📗 глагол в повествовательном предложении всегда стоит на второй позиции, но <b>это не означает, что это второе слово в предложении</b>, например:
<i>Ins Kino gehe ich heute. – В кино иду я сегодня.</i>
    '''
    await edit_media(callback_query,
                     "https://www.de-online.ru/novosti/07-2022/poryadok-slov-v-nemetskom-predlozhenii-tablica_tek.jpg",
                     text, kb.kb_minor_members)


# Обучение (немецкий, два глагола)
@dp.callback_query_handler(lambda c: c.data == 'two_verbs')
async def minor_members(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📙 если в предложении два глагола, то спрягаемый становится в начале, а неспрягаемый - в конце.
<i>Ich</i> <b>will</b> <i>heute ins Kino</i> <b>gehen.</b> <i>– Я хочу сегодня пойти в кино.</i>
    '''
    await edit_media(callback_query,
                     "https://www.de-online.ru/novosti/07-2022/poryadok-slov-v-nemetskom-predlozhenii-tablica_tek.jpg",
                     text, kb.kb_minor_members)


# Обучение (немецкий, время суток)
@dp.callback_query_handler(lambda c: c.data == 'time')
async def time(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📒 есть 2 способа передачи информации о времени суток: <b>официальный и разговорный</b>.
официально о времени суток говорят по формуле: <i>часы + Uhr + минуты</i>, например: <i>Es ist sieben Uhr fünfzehn. - 07:15.</i>
в <b>неофициальной речи</b> добавляются слова: <i>morgens (утра), mittags (в обед), nachmittags (дня), abends (вечера), nachts (ночи)</i>, например: <i>Es ist elf Uhr abends. - 23:00.</i>
📒 для минут <b>после</b> какого-то часа используется предлог <b>nach (после)</b>, для минут до какого-то часа - <b>vor (перед)</b>.
<i>Es ist dreizehn Minuten nach zehn Uhr. - 10:13 - 13 минут одиннадцатого.</i>
📒 для 30 минут существует слово <b>halb (половина)</b>. оно используется без предлога и слова Uhr.
📒 для выражения минут можно использовать формулы:
<i>минуты от 1 до 24 = минуты от 1 до 24 + Minuten + nach + предыдущий час</i>
<i>минуты от 36 до 59 = минуты от 1 до 24 + Minuten + vor + последующий час</i>
📒 для 15 минут есть свое слово: <b>Viertel</b>. Viertel nach (четверть после), Viertel vor (четверть перед или без четверти)
📒 <b>таблица с примерами приведена выше.</b>
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/JzzJSPpp/image.png",
                     text, kb.kb_articles)


# Обучение (немецкий, условия, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'if_ger' or c.data == "farther_if_ger_1")
async def if_ger(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📓 <b>wenn</b> означает <i>когда/если</i> и вводит придаточное предложение:
<i>Wenn du eine neue Wohnung findest, ruf mich an. – Если (когда) ты найдешь новую квартиру, позвони мне.</i>
📓 в случае, когда нужно сказать именно <b>если</b> используется слово <b>Falls</b>
📓 можно поместить глаголы в обоих предложениях на первое место: <i><b>Bezahlen</b> Sie die Rechnung nicht rechtzeitig, <b>werden</b> wir Sie vor Gericht ziehen. – Не оплатите своевременно счет, мы Вас привлечем к суду.</i>
📓 связь между придаточным и главным предложениями можно подчеркнуть словом <i>dann (когда)</i>:
<i>Hättest du auf mich gehört, (dann) wäre das nicht passiert. – Послушал(ся) бы ты меня, (тогда) этого бы не случилось.</i>
    '''
    await edit_media(callback_query,
                     "https://www.studying-in-germany.org/wp-content/uploads/2019/02/Best-universities-in-Germany-for-international-students.jpg",
                     text, kb.kb_if_ger)


# Обучение (немецкий, условия, 2 страница)
@dp.callback_query_handler(lambda c: c.data == "farther_if_ger_2")
async def if_ger_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📓 выражение <b>angenommen, dass</b> означает <b>предположим, что</b>. например:
<i>Angenommen, dass Sie krank werden, so können Sie an dieser Konferenz nicht teilnehmen. – Предположим, что Вы заболеете, тогда Вы не сможете принять участие в этой конференции.</i>
📓 вместо этого выражения можно также использовать <i>unter der Bedingung, dass (при условии, что)</i>
📓 кроме того, существует оборот <b>es sei denn, (dass)</b>: <i>Ich gehe nicht zu ihm, <b>es sei denn, dass</b> er mich um Verzeihung bittet. – Я не пойду к нему, ну разве что он попросит у меня прощения.</i>
📓 нередко употребляется <b>sollte (должен бы) (с оттенком смысла: если окажется, что)</b>: <i>Wenn sie anrufen sollte, sagst du, dass ich nicht da bin. – Если она мне позвонит (дословно: должна бы позвонить), скажешь ей, что меня нет.</i>
    '''
    await callback_query.message.edit_caption(caption=text, reply_markup=kb.kb_if_ger_2)


# Обучение (немецкий, артикли)
@dp.callback_query_handler(lambda c: c.data == 'articles' or c.data == "back_to_learning_ger")
async def articles(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📓 различным родам соответствуют различные артикли. это отражено в <b>таблице выше.</b>
<i>Gibt es hier in der Nähe eine Bar? – Есть ли здесь поблизости (один) бар?</i>
здесь употребляется неопределенный артикль, так как вы не знаете, что за бар и есть ли он вообще.
📓 если вы что-то просто называете или характеризуете, то нужно использовать <b>неопределенный артикль.</b>
📓 <b>если вы называете род занятий, профессию, национальность, чувства, вещества, материалы лучше вообще обойтись без артикля.</b>
📓 с определенным артиклем слово может быть употреблено <b>не только если оно обозначает нечто конкретное</b>, но и если имеет обобщающее значение, то есть обозначает совокупность конкретных вещей (общее, но в то же время делимое, поддающееся исчислению):
<i>Der Mensch ist, was er isst. – Человек есть то, что он ест.</i>
📓 артикля может не быть при перечислении, в устойчивых выражениях, поговорках, газетных заголовках, объявлениях и командах.
📓 <b>таблица артиклей приведена выше.</b>
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/6p86CrS8/articles.png",
                     text, kb.kb_articles)


# Обучение (немецкий, падежи, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'cases' or c.data == "farther_cases_1")
async def cases(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 именительный падеж <b>(Nominativ)</b> - прямой падеж, остальные образованы от него и называются косвенными.
- местоимения, прилагательные, слово <i>kein</i> мужского/среднего родов не имеют окончания в именительном падеже, женском роде и множ. числе получают окончание <i>-e</i>
<i>Eine Frau - женщина, Ein Mann - мужчина</i>
- в случае слабого склонения прилагательное получает окончание <i>-e</i>, а множ. число - <i>-en</i>.
<i>Der ernste Mann - серьезный мужчина, Die guten Freunde - хорошие друзья</i>
- при сильном склонении прилагательное получает окончание, соответствующее роду существительного.
<i>Ernster Mann – серьезный мужчина</i>
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/85Q5bZfy/nominativ.png",
                     text, kb.kb_cases)


# Обучение (немецкий, падежи, 2 страница)
@dp.callback_query_handler(lambda c: c.data == "farther_cases_2")
async def cases_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 винительный падеж <b>(Akkusativ)</b>
- прилагательные, артикли, местоимения мужского рода приобретают окончание <i>-en</i>, существительное остается без изменений.
- формы множественного числа, женского/среднего родов совпадают с формами в <i>Nominativ</i>.
📕 дательный падеж <b>(Dativ)</b>
- прилагательные, артикли, местоимения мужского/среднего родов приобретают окончание <i>-m</i> без изменения самого существительного.
- прилагательные, артикли, местоимения женского рода получают окончание <i>-r</i>
- во множественном числе и существительное, и зависимое от него слово получают окончание <i>-(e)n</i>

    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/4xsDJh7F/akkusativ.png",
                     text, kb.kb_cases_2)


# Обучение (немецкий, падежи, 3 страница)
@dp.callback_query_handler(lambda c: c.data == "farther_cases_3")
async def cases_3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 родительный падеж <b>(Genitiv)</b>
- обозначает принадлежность одного предмета к другому.
- существительные мужского/среднего родов сильного склонения получают окончание <i>-(e)s</i>
- прилагательное мужского/среднего рода получает окончание <i>-en</i>
- прилагательные, артикли, местоимения женского рода и множественного числа получают окончание <i>-r</i>
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/cHyjbgSm/genitiv.png",
                     text, kb.kb_cases_3)


# Обучение (немецкий, имена числительные)
@dp.callback_query_handler(lambda c: c.data == "counts" or c.data == "back_to_counts")
async def counts(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query, "https://i.postimg.cc/8PfNJdr8/think.jpg",
                     '🧮 выбрана опция: <b>"имена числительные".</b>\nвыберите курс:',
                     kb.kb_counts)


# Обучение (немецкий, количественные)
@dp.callback_query_handler(lambda c: c.data == "countable")
async def countable(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 отвечают на вопрос: <b>сколько? - wie viel?</b>
📘 числительное <i>один</i> может иметь формы eins, einen, eine (если числительное заменяет собой существительное):
<i>Wie viele Kinder hast du? - Сколько у тебя детей? Ich habe eins (=ein Kind) - У меня один (=один ребенок)</i>
📘 если перед числительным стоит определенный артикль, то оно склоняется по <b>слабому</b> типу:
<i>die eine von Frauen - единственная из женщин</i>
📘 чтобы различать <b>zwei и drei</b>, иногда вместо <b>zwei</b> говорят <b>zwo</b> (непонятно, как вообще путают zwei и drei).
📘 числительные не влияют на падеж существительного.
    '''
    await edit_media(callback_query, "https://i.postimg.cc/447fByDK/countable.png", text, kb.kb_countable)


# Обучение (немецкий, порядковые)
@dp.callback_query_handler(lambda c: c.data == "ordinal")
async def ordinal(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📙 отвечают на вопрос: <b>который?</b>
📙 обычно употребляются с определенным артиклем и склоняются по правилам склонения прилагательных
<i>Ich bin am neunzehnten Mai geboren - Я родился 19 мая.</i>
📙 если числительное на письме обозначается <b>цифрой</b>, то после неё будет стоять точка:
<i>am 19. Mai - 19-го мая, der 20. Juni - 20-е июня</i>
    '''
    await edit_media(callback_query, "https://i.postimg.cc/PxVvwqCW/ordinal.png", text, kb.kb_countable)


# Обучение (немецкий, дроби)
@dp.callback_query_handler(lambda c: c.data == "fractions")
async def fractions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 <b>дроби</b> образуются от количественных числительных суффиксом <i>-(s)tel</i>
<b>от 2 до 19 (-tel): viertel (1/4), 20 и далее (-stel): zwanzigstel (1/20)</b>
📕 дроби пишутся с большой буквы и с артиклем: <b>das Achtel</b>
📕 1/2 (halb) имеет две формы: употребляющаяся без существительного и склоняющаяся как имя прилагательное:
<i>um half vier - в полчетвертого, ein halbes Jahr - полгода</i>
📕 существительные после числительных стоят во <b>множественном</b> числе: <i>anderthalb Seiten — полторы страницы</i>
📕 десятичные дроби выражаются через слово Komma (запятая): <i>4,141 – vier Komma eins vier eins</i>
📕 <b>читается сначала числитель, затем - знаменатель.</b>
    '''
    await edit_media(callback_query,
                     "https://res.cloudinary.com/dk-find-out/image/upload/q_80,w_1440,f_auto/whatisafraction_hy3hji.jpg",
                     text, kb.kb_countable)


# Обучение (немецкий, склонения, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'declination' or c.data == "farther_declination_1")
async def declination(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📒 существует три типа склонения прилагательных: <b>сильное, слабое, смешанное</b>.
прилагательные склоняются только тогда, когда они стоят перед именем существительным.
📒 <b>как понять, по какому типу склоняется прилагательное?</b>
- если прилагательное стоит перед существительным без сопровождающего слова, то оно склоняется по <i>сильному</i> типу
- если сопровождающее слово есть, но неоднозначно показывается род, число и падеж, прилагательное склоняется по <i>смешанному</i> типу
- если сопровождающее слово есть и однозначно показывает род, число и падеж, то прилагательное склоняется по <i>слабому</i> типу
    '''
    await edit_media(callback_query,
                     "https://dammann-german-english-translations.com.au/wp-content/uploads/2016/03/bigstock-Women-and-man-speaking-German-92929733.jpg",
                     text, kb.kb_declination)


# Обучение (немецкий, склонения, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_declination_2')
async def declination_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📒 <b>сильное склонение</b>
имя прилагательное получает падежное окончание (окончание определенного артикля). исключение составляют прилагательные Genitiv в мужском и среднем роде (окончание <i>-en</i>)
📒 <b>таблица сильного склонения прилагательных приведена выше.</b>
📒 во множественном числе слова <b>Viele (много), Einige (несколько), Wenige (мало)</b> приобретают падежное окончание и не влияют на окончание имени прилагательного.
    '''
    await edit_media(callback_query, "https://i.postimg.cc/sxnvXQRR/strong.png", text, kb.kb_declination_2)


# Обучение (немецкий, склонения, 3 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_declination_3')
async def declination_3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📒 <b>слабое склонение</b>
в роли <b>сопровождающих</b> слов могут выступать определенный артикль, указательное местоимение и т.д., то есть те слова, которые уже в Nominativ определяют род существительного.
- к определенным артиклям относят также слова <i>diese, jede, welche, solche, alle</i>.
- определенный артикль, указательное местоимение и вопросительное местоимение с одним и тем же существительным одновременно <b>не используются</b>.
- в качестве <b>сопровождающего</b> слова могут выступать разные части речи, но все они однозначно показывают род и число существительного уже в <i>Nominativ</i>.
📗 <b>таблица слабого склонения прилагательных приведена выше.</b>
    '''
    await edit_media(callback_query, "https://i.postimg.cc/fRhW7fTR/weak.png", text, kb.kb_declination_3)


# Обучение (немецкий, склонения, 4 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_declination_4')
async def declination_4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📒 <b>смешанное склонение</b>
неопределенный артикль (ein/eine), отрицательное местоимение (kein/keine), притяжательные местоимения (mein/meine) показывают <i>род, число, падеж</i> существительного неоднозначно <i>(ein Tisch - может быть как мужской род, так и средний)</i>
📗 <b>таблица смешанного склонения прилагательных приведена выше.</b>
    '''
    await edit_media(callback_query, "https://i.postimg.cc/D088SrdP/mixed.png", text, kb.kb_declination_4)


# Обучение (немецкий, склонения, 5 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_declination_5')
async def declination_5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📒 <b>склонение однородных прилагательных</b>
однородные имена прилагательные, стоящие перед существительным, склоняются одинаково, например:
<i>ein klein<b>es</b> neu<b>es</b> Haus / das klein<b>e</b> neu<b>e</b> Haus</i>
📒 <b>склонение составных прилагательных</b>
когда имя прилагательное состоит из нескольких (является многокоренным или составным словом), окончание ставится только в конце слова: <i>mathematisch-naturwissenschaftlich<b>es</b> Thema</i>
    '''
    await edit_media(callback_query,
                     "https://dammann-german-english-translations.com.au/wp-content/uploads/2016/03/bigstock-Women-and-man-speaking-German-92929733.jpg",
                     text, kb.kb_declination_5)


# Обучение (английский, произношение)
@dp.callback_query_handler(lambda c: c.data == 'pronunciation' or c.data == "back_to_courses")
async def learning_pronunciation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query,
                     "https://i.postimg.cc/8PfNJdr8/think.jpg",
                     '🎶 выбрана опция: <b>"произношение".</b>\nвыберите курс:',
                     kb.kb_pronunciation)


# Обучение (английский, открытый и закрытый слоги, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'open_close_syllable' or c.data == "first_page_syllables")
async def open_close_syllable(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📓 <b>что такое открытый и закрытый слог?</b>
⚠ <b>открытый слог</b> – слог, оканчивающийся на гласный звук. как правило, он встречается в <b>следующих</b> случаях:
- слово оканчивается на гласную и последний слог всегда открытый: ta<b>ke</b> [тэйк]
- за гласной буквой следует согласная, после которой вновь идет гласный звук: ed<b>uca</b>tion [эдьюкэйшн]
- в слове соседствуют две гласных: cr<b>ue</b>l [круэл].
в открытых слогах гласная буква проговаривается всегда плавно и протянуто. 
    '''
    await edit_media(callback_query,
                     "https://storage.kun.uz/source/3/8cMEWm-mnI0u4LZb-cDrJ9ibm1vawnm-.jpg",
                     text,
                     kb.kb_open_close_syllables)


# Обучение (английский, открытый и закрытый слоги, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_open_close')
async def farther_open_close(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
⚠ <b>закрытый слог</b> – слог, в котором гласный звук замкнут согласным и поэтому звучит кратко и отрывисто: c<b>ut</b> [кат].
для слогов характерны особые правила чтения, в которых гласный звук замыкается буквой <b>r</b>. дело в том, что в британском варианте 
произношения таких слогов буква <b>r</b> часто <b>не произносится</b>. поэтому существует два варианта чтения подобных буквосочетаний:
- в <b>открытом</b> слоге, когда <b>r</b> стоит в окружении гласных, читаются только обе гласные: c<b>are</b> [кээа]
- в <b>закрытом слоге</b> <b>r</b> также не читается, но влияет на звучание гласного звука, делая его более протяжным: start [стаат]
    '''
    await callback_query.message.edit_caption(caption=text, reply_markup=kb.kb_open_close_syllables_2)


# Обучение (английский, соответствие букв и звуков, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'letters_sounds' or c.data == "farther_letters_sounds_1")
async def letters_sounds(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query,
                     "https://i.postimg.cc/02hBMHzp/2023-03-22-200736.png",
                     "📘 начнем с самого легкого: с таблицы <b>согласных</b>, произношение которых аналогично русскому звучанию.",
                     kb.kb_letters_sounds)


# Обучение (английский, соответствие букв и звуков, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_letters_sounds_2')
async def letters_sounds_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query,
                     "https://i.postimg.cc/d3GDvxpJ/Opera-2023-03-22-201553-speakenglishwell-ru.png",
                     "📘 теперь разберемся с более <b>сложными</b> буквами.",
                     kb.kb_letters_sounds_2)


# Обучение (английский, соответствие букв и звуков, 3 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_letters_sounds_3')
async def letters_sounds_3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 изучим <b>буквосочетания</b> согласных в английском языке.
<b>кстати</b>, согласные, стоящие в самом конце слова, нельзя оглушать.
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/qvsYnxVg/2023-03-22-202219052.png",
                     text,
                     kb.kb_letters_sounds_3)


# Обучение (английский, соответствие букв и звуков, 4 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_letters_sounds_4')
async def letters_sounds_4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 намного <b>сложнее</b> обстоит ситуация с произношением <b>гласных</b>.
не забывайте о том, что в закрытом слоге все буквы произносятся <b>кратко</b>.
в открытом слоге - <b>плавно и протяжно</b>.
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/PxyKrSDn/shhhh.jpg",
                     text,
                     kb.kb_letters_sounds_4)


# Обучение (английский, соответствие букв и звуков, 5 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_letters_sounds_5')
async def letters_sounds_5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query,
                     "https://i.postimg.cc/1XPG6wpc/dakjfopiq.jpg",
                     "📘 не забываем, что буква <b>r</b> после гласного, как правило, <b>не произносится.</b>",
                     kb.kb_letters_sounds_5)


# Обучение (английский, дифтонги и трифтонги)
@dp.callback_query_handler(lambda c: c.data == 'diphthongs_triphthongs')
async def diphthongs_triphthongs(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
❓ <b>дифтонги и трифтонги</b> - это сочетания двух или трех букв, обладающие особым звучанием.
сначала <b>усиленно</b> произносят главный звук, а потом плавно его переводят во второстепенный звук.
дифтонги и трифтонги не подчиняются <b>никаким</b> грамматическим законам, поэтому остается только учить их наизусть.
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/CxqKT1Bb/Opera-2023-03-22-204609-speakenglishwell-ru.png",
                     text,
                     kb.kb_diphthongs_triphthongs)


# Обучение (английский, интонация. тоны)
@dp.callback_query_handler(lambda c: c.data == 'intonation')
async def intonation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
👽 <b>интонация</b> является основным средством выражения сказанного. она формируется за счет сочетания <b>темпа</b>, <b>фразового ударения</b>, 
<b>высоты тона</b>, <b>ритма произношения</b>. существует <b>два</b> основных типа мелодики (тона):
- <b>нисходящий</b>. используется в повествовательных, утвердительных предложениях, передает законченные мысли, суждения, факты. 
также свойственен повелительным предложениям.
📋 <b>например: we found a cat. – мы нашли кота.</b>
- <b>восходящий</b>. показывает незаконченность высказывания. он часто применяется при перечислении и в вопросительных 
предложениях. интонация медленно поднимается от первого ударного слога фразы к последнему.
📋 <b>например: have you swept the floor? - ты подмел пол?</b>
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/N01JnW6Q/1.jpg",
                     text,
                     kb.kb_intonation)


# Обучение (английский, сложности)
@dp.callback_query_handler(lambda c: c.data == 'hard_things')
async def hard_things(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📙 есть <b>много</b> слов, которые пишутся одинаково, но произносятся по-разному. много исключений.
📕 <b>например</b>, слово <b>read</b> может произноситься как <b>[рид]</b>, так и <b>[ред]</b>. это зависит от времени.
подобных слов много. <b>например: live, reading, wind, use, lead, bow.</b>
📓 для запоминания таких слов рекомендуется составлять <b>предложения</b>, в которых присутствовали бы оба слова в разной 
интерпретации. тогда в будущем вы сможете правильно их применять и произносить. 
    '''
    await edit_media(callback_query,
                     "https://att.by/images/news/24341_big.jpg",
                     text,
                     kb.kb_hard)


# Обучение (английский, ударения)
@dp.callback_query_handler(lambda c: c.data == 'accents')
async def accents(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
🔖 в английском языке существует <b>три</b> типа ударений:
- <b>словесное</b>. подразумевает выделение голосом одного слога в слове. в транскрипции перед ударным слогом ставится знак '
📋 <b>например</b>, present [pri:‘sent] – представлять, present [‘preznt] – подарок
- <b>фразовое</b>. с его помощью выделяются <b>части предложения</b>.
📋 <b>например</b>, what ‘happened? – что произошло?
- <b>логическое</b>. используется для выделения слов, на которые говорящий делает акцент.
📋 <b>например</b>, ‘she did that! – она это сделала!
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/XNDZRX7Y/accenrt.jpg",
                     text,
                     kb.kb_accents)


# Обучение (английский, числа)
@dp.callback_query_handler(lambda c: c.data == 'numbers')
async def numbers(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📙 для образования последующих чисел нам потребуются всего лишь два суффикса <i>-teen и -ty.</i>
📙 ударение всегда нужно ставить на <i>-teen</i>, а <i>-ty</i> всегда безударный. так будет проще различать суффиксы.
📙 <b>таблица чисел показана выше.</b>
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/CLtPPpKh/image.png",
                     text,
                     kb.kb_numbers)


# Обучение (английский, времена)
@dp.callback_query_handler(lambda c: c.data == 'tenses')
async def learning_tenses(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
🎁 это - шпаргалка по временам. в каждой клетке указана характеристика времени, 
метод образования и маркеры (слова, по которым можно различать времена).
<b>p.s.</b> главное - помнить порядок слов в предложении:
1. <b>утвердительное</b> - подлежащее, сказуемое (возможен вспомогательный глагол), другие члены предложения
2. <b>отрицательное</b> - обстоятельство, подлежащее (возможно с определением), вспомогательный глагол + not,
основной глагол, дополнение (возможно с определением)
3. <b>вопросительное</b> - вспомогательный глагол, подлежащее (возможно с определением), основной глагол,
дополнение (возможно с определением), обстоятельство
    '''
    await edit_media(callback_query, "https://i.postimg.cc/gkc7Gb6J/tenses.jpg", text, kb.kb_learning_tenses)


# Обучение (английский, пунктуация)
@dp.callback_query_handler(lambda c: c.data == 'punctuation' or c.data == "back_to_punctuation")
async def punctuation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await edit_media(callback_query,
                     "https://i.postimg.cc/8PfNJdr8/think.jpg",
                     '🌪️ выбрана опция: <b>"пунктуация".</b>\nвыберите курс:',
                     kb.kb_punctuation)


# Обучение (английский, запятая, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'comma' or c.data == 'farther_comma_1')
async def comma(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 запятые используются для разделения <b>простых</b> предложений, объединенных при помощи союзов, например:
<b>– the lesson was over, but the students remained in the classroom. - урок закончился, но учащиеся остались в классе.</b>
📕 если предложение <b>короткое</b>, запятая перед союзами <i>and</i> или <i>or</i> может опускаться, например:
<b>– the rain stopped and it got much warmer. - дождь прекратился, и стало гораздо теплее.</b>
📕 запятые используются после вводных слов, фраз или придаточных предложений, которые предшествуют главному, например:
<b>– while I was talking on the phone, the cat stole my steak. - пока я разговаривал по телефону, кот украл мой бифштекс.</b>
📕 утвердительное слово <i>yes</i>, отрицательное слово <i>no</i>, а также вводные слова <i>well, you know, i mean</i> отделяются запятыми, например:
<b>– yes, you can come in - да, можете войти.</b>
'''
    await edit_media(callback_query,
                     "https://i.pinimg.com/736x/59/94/78/5994789723c2c0ce7197774271e2c912--punctuation-humor-teaching-punctuation.jpg",
                     text,
                     kb.kb_comma)


# Обучение (английский, запятая, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_comma_2')
async def comma(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 пояснительная <b>вводная фраза</b> выделяется запятыми с двух сторон, например:
<b>– he and she, my former classmates, got married a week ago. - он и она, мои бывшие одноклассники, поженились неделю назад.</b>
📕 запятая <b>не</b> ставится в сложноподчиненном предложении перед союзом <i>that</i>, например:
<b>– he said that he was going to quit. - он сказал, что собирается увольняться.</b>
📕 при перечислении однородных членов предложения запятая ставится также и перед союзом <i>and</i>, например:
<b>– at the supermarket i bought sugar, tea, coffee, and matches - в супермаркете я купил сахар, чай, кофе и спички.</b>
📕 запятые используются для выделения <b>прямой</b> речи, например:
<b>– he said indifferently, “i don’t mind.” - он сказал безразлично: «я не возражаю»</b>
📕 запятые используются для выделения <b>всех</b> географических названий, дат, (кроме месяца и дня), адресов (кроме номера улицы и названия), и заголовков в названиях, например:
<b>– december 15, 2009, was an important day in his life. - 15 декабря 2009 года был важный день в его жизни.</b>
'''
    await callback_query.message.edit_caption(caption=text, reply_markup=kb.kb_comma_2)


# Обучение (английский, точка)
@dp.callback_query_handler(lambda c: c.data == 'period')
async def period(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 основное предназначение этого знака препинания — <b>завершить предложение.</b>
📘 следует ставить точку в конце аббревиатуры, если последняя буква сокращения <b>не</b> является
последней буквой слова, например: <b>gen. secretary — general secretary</b>.
📘 если сокращенная фраза произносится, мы не ставим точки, например: <b>NASA, а не N.A.S.A.</b>
'''
    await edit_media(callback_query,
                     "https://i.postimg.cc/Hk2z7vdY/fullstophoriz-noart.jpg", text, kb.kb_period)


# Обучение (английский, кавычки)
@dp.callback_query_handler(lambda c: c.data == 'quote_marks')
async def quote_marks(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 кавычки используются для выделения <b>прямой речи</b>.
📗 кавычки могут использоваться для выражения <b>сарказма</b>, например:
<b>– your so called “friend” should have given you a lift home. - твой так называемый «друг» должен был бы подвезти тебя домой.</b>
📗 кавычки используются для выделения <b>цитаты</b>
'''
    await edit_media(callback_query,
                     "https://i.postimg.cc/vHPzGYwQ/11345a4cf6343afabfb2efca21056acf.png", text, kb.kb_period)


# Обучение (английский, вопросительный и восклицательный знаки)
@dp.callback_query_handler(lambda c: c.data == 'marks')
async def marks(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📙 вопросительный знак ставится в конце предложения, содержащего <b>вопрос</b>.
📙 однако в <b>косвенных вопросах</b> он не ставится, например:
<b>– he asked how many people would go on an excursion - он спросил, сколько человек поедут на экскурсию.</b>
📙 также вопросительный знак не ставится, если предложение начинается со слов <b>i wonder, he doesn't know, i don't remember</b>.
📓 восклицательный знак используется <b>только</b> для выражения команды, приказа, эмоции, например:
<b>– stop talking! - прекратите разговаривать!</b>
<b>– what a beautiful place! - какое живописное место!</b>
'''
    await edit_media(callback_query,
                     "https://i.postimg.cc/LXDt7nQz/png-transparent-exclamation-point-and-question-mark-illustrations-exclamation-mark-question-mark-emo.png",
                     text,
                     kb.kb_period)


# Обучение (английский, двоеточие и точка с запятой)
@dp.callback_query_handler(lambda c: c.data == 'colons')
async def colons(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📓 двоеточие используется для введения <b>перечисления, цитаты или другого комментария</b>, например:
<b>– music is more than something mechanical: it is an expression of deep feeling and ethical values. - музыка – это не просто механические звуки: это выражение глубокого чувства и нравственных ценностей.</b>
📓 точка с запятой используется для связи независимых предложений, <b>не соединенных союзом</b>, например:
<b>– the sky is covered with heavy clouds; it is going to rain soon. - небо покрыто тяжелыми тучами, скоро пойдет дождь.</b>
📓 точка с запятой также используется, чтобы соединить части предложения или сложные предложения, в которых уже <b>есть</b> запятые.
'''
    await edit_media(callback_query,
                     "https://media.proprofs.com/images/discuss/user_images/153336/88413107944.jpg", text, kb.kb_period)


# Обучение (английский, скобки)
@dp.callback_query_handler(lambda c: c.data == 'parentheses')
async def parentheses(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
🎒 скобки используются для выделения <b>дополнительного</b> материала, включенного как вводная информация, например:
<b>– he was appointed a head of the department (some people say, this is because he was a brother of the minister) - его назначили начальником отдела некоторые говорят, что это из-за того, что он был братом министра)</b>
'''
    await edit_media(callback_query,
                     "https://bravelittlenib.files.wordpress.com/2015/04/parentheses.jpg", text, kb.kb_period)


# Обучение (английский, тире или дефис)
@dp.callback_query_handler(lambda c: c.data == 'dash_hyphen')
async def dash_hyphen(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 тире используется, чтобы выделить <b>суть</b> предложения или <b>пояснительный</b> комментарий, например:
<b>– to some of you, my proposals may seem radical - even revolutionary. - для некоторых из вас мои предложения могут показаться радикальными - даже революционными.</b>
⚠ <i>p.s. не используйте тире слишком часто, иначе оно потеряет свое значение.</i>
📘 дефис используется в <b>сложных</b> словах или с префиксами <i>ex-, self-, all-, non-</i>, например:
<b>– ex-wife, self-esteemed, T-shirt, all-inclusive</b>
'''
    await edit_media(callback_query, "https://i.postimg.cc/8Cr8Gf2g/hd.jpg", text, kb.kb_period)


# Обучение (английский, апостроф, страница 1)
@dp.callback_query_handler(lambda c: c.data == 'apostrophe' or c.data == 'farther_apostrophy_1')
async def apostrophe(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📙 апостроф указывает на <b>сокращенную</b> грамматическую форму, но замена недостающей буквы <b>не</b> приветствуется в формальной и письменной речи, так как там все слова должны быть написаны <b>полностью</b>. выше показан полный перечень всех сокращенных форм.
'''
    await edit_media(callback_query, "https://englsecrets.ru/wp-content/uploads/2014/05/apostrophe1.jpg", text,
                     kb.kb_apostrophe)


# Обучение (английский, апостроф, страница 2)
@dp.callback_query_handler(lambda c: c.data == 'farther_apostrophy_2')
async def apostrophe_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📒 апостроф используется для образования притяжательного падежа существительных, например:
<b>my mom's bag - сумка моей мамы</b>
📒 апостроф нужно ставить <b>до буквы s</b> для существительных в единственном числе <i>(the student’s work - работа студента)</i> и <b>после буквы s</b>, если существительное стоит во множественном числе <i>(my friends' house)</i>
📒 также апострофы используются в выражениях, содержащих <b>время</b>, например:
<b>10 o'clock, two week's notice</b>
'''
    await edit_media(callback_query, "https://langtown.ru/wp-content/uploads/2021/07/Apostrophe.jpg", text,
                     kb.kb_apostrophe_2)


# Обучение (английский, словарь)
@dp.callback_query_handler(lambda c: c.data == 'vocabulary')
async def apostrophe_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '📚 словарный запас лучше всего развивается при постоянной практике: <b>смотрите фильмы, читайте книги, играйте в игры,</b> делайте все, что вам нравится. <i>но на английском.</i> учитесь переключаться. а бот вам в этом поможет: <b>"марафон слов"</b> отлично подойдет для изучения новых слов. <b>удачи!</b> ⭐'
    await edit_media(callback_query,
                     "https://razoom.mgutm.ru/pluginfile.php/24976/course/overviewfiles/Заблуждения-связанные-с-английским-языком.-Часть-1.jpg",
                     text,
                     kb.kb_vocabulary)


# английский, Условные предложения
@dp.callback_query_handler(lambda c: c.data == 'if')
async def if_(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
‼ условные предложения состоят из двух частей: <b>самого условия</b> и <b>следствия выполнения этого условия.</b> части предложения могут следовать в любом порядке, но если сначала идет условие, то нужна <b>запятая</b>. в противном случае - не нужна.
✅ выше показана таблица с объяснением <b>всех</b> типов условных предложений.
    '''
    await edit_media(callback_query,
                     "https://i.postimg.cc/44jMpyky/if-clauses.jpg", text, kb.kb_learning_tenses)


# английский, Степени сравнения (1 страница)
@dp.callback_query_handler(lambda c: c.data == 'degrees' or c.data == 'farther_degrees_1')
async def degrees(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 <b>положительная степень</b> - это изначальная форма прилагательного, например: old, big, small, good
📘 <b>сравнительная степень</b> используется для сравнения предметов/людей между собой.
для короткого прилагательного формируется с помощью окончания <i>-er</i>, например: small - smaller
если прилагательное заканчивается на <i>-y</i>, нужно <b>заменить</b> <i>-y</i> на <i>-i</i>, например: happy - happier, easy - easier
если <b>односложное</b> прилагательное заканчивается на сочетание гласной и согласной, то конечная согласная <b>удваивается</b>, например: hot - hotter
если в прилагательном больше двух слогов, то добавляется слово <i>more</i>, например: serious - more serious, famous - more famous
📘 <b>превосходная степень</b> предполагает, что наш предмет самый-самый.
к коротким прилагательным <b>добавляется</b> окончание <i>-est</i> и <i>the</i> в начале, например: weak - the weakest
если в конце прилагательного стоит <i>-y</i>, ситуация складывается такая же, как в сравнительной степени, например: happy - the happiest.
в длинных прилагательных добавляется <i>the most</i>, например: useful - the most useful.
    '''
    await edit_media(callback_query,
                     "https://weemss.com/wp-content/uploads/2017/11/fruit-1160552_1920.jpg", text, kb.kb_degrees)


# английский, Степени сравнения (2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_degrees_2')
async def degrees_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 <b>отрицательное сравнение</b> строится на словах <i>less, not as, not so</i>.
слово <i>less</i> не используется с короткими прилагательными; в таком случае уместнее <i>not as... as...</i>, например:
<b>– the second method was less complicated than the first one. - второй метод был менее сложный, чем первый</b>
<b>– my old smartphone was not as fast as my new one. - мой старый смартфон не был таким быстрым, как новый.</b>
'''
    await callback_query.message.edit_caption(caption=text, reply_markup=kb.kb_degrees_2)


# английский, Степени сравнения (3 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_degrees_3')
async def degrees(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 к <b>исключениям</b> не применяются стандартные правила сравнения прилагательных, но их <b>нетрудно</b> запомнить.
    '''
    await edit_media(callback_query,
                     "https://crownenglishclub.ru/wp-content/uploads/2019/05/Isklyucheniya_v_stepeni_sravneniya_prilagatelnyh_v_angliyskom_yazyke__pravila__tablicy_3.jpg",
                     text, kb.kb_degrees_3)


# английский, Исчисляемые/неисчисляемые
@dp.callback_query_handler(lambda c: c.data == 'uncount')
async def uncount(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 нетрудно догадаться, что исчисляемые существительные можно посчитать, а неисчисляемые - нельзя.
к классу <b>исчисляемых</b> существительных относятся бытовые предметы, люди и т.д. во множественном числе к ним прибавляется окончание <i>-s</i>
к <b>неисчисляемым</b> относятся: ощущения (hate, fear), абстрактные существительные (space, time), погодные явления (weather, cold), материалы (wood, water, salt)
<i>глагол to be принимает форму "is"</i>
📕 слова можно переводить из одного класса в другой. например: <b>bottle - бутылка, a bottle of water - бутылка воды.</b>
📕 как выбирать показатели количества? в общем, существует две вариации: <b>много и мало</b>. для <b>исчисляемых</b> "много" - это <i>many</i>, а для неисчисляемых - <i>much</i>. а "мало" для <b>исчисляемых</b> - это <i>few</i>, для неисчисляемых - это <i>little</i>.
📕 примеры: <b>many years (много лет), much love (много любви), few people (мало людей), little time (мало времени).</b>
'''
    await edit_media(callback_query,
                     "https://i.ytimg.com/vi/rduOjOijUU4/maxresdefault.jpg", text, kb.kb_learning_tenses)


# английский, Пассивный залог
@dp.callback_query_handler(lambda c: c.data == 'passive_voice')
async def passive_voice(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📗 в английском существует <b>два</b> залога: <i>активный (active)</i> и <i>пассивный (passive)</i>. в активном действие совершает <b>сам</b> субъект, а в пассивном - действие совершается <b>над</b> субъектом.
пример: <b>he cleans the office every day. - он убирает офис каждое утро.</b> (активный залог) <b>the office is cleaned every day. - офис убирают каждый день.</b> (пассивный залог)
📗 <b>метод образования пассивного залога отражен в таблице.</b>
'''
    await edit_media(callback_query, "https://i.postimg.cc/xdM1MRRC/passive-voice.jpg", text, kb.kb_learning_tenses)


# английский, Косвенная речь
@dp.callback_query_handler(lambda c: c.data == 'reported_speech')
async def reported_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📕 <b>косвенная речь (reported speech)</b> - это чьи-то слова, которые мы передаем от третьего лица. например:
<b>– she says, "i like english". - она говорит: "я люблю английский".</b>
<b>– she says that she likes english. - она говорит, что любит английский.</b>
📕 мы убрали кавычки, добавили союз <i>that</i>, заменили местоимение по смыслу и добавили <i>-s</i> в конец глагола.
📕 после глаголов <b>say, know, think</b> союз <i>that</i> можно опустить.
⚠ <b>при переводе в косвенную речь меняется время и (или) модальный глагол. таблица согласования времен приведена выше.</b>
⚠ <b>но время можно не менять, если вы говорите о научном факте, употребляете времена</b> <i>past simple/continuous</i> <b>с союзами</b> <i>when, since, if</i>.
    '''
    await edit_media(callback_query, "https://i.postimg.cc/SN5DNJLy/reported.jpg", text, kb.kb_learning_tenses)


# английский, Каузативная форма
@dp.callback_query_handler(lambda c: c.data == 'causative')
async def causative(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📚 каузатив описывает ситуацию, когда мы находим третьих лиц, которые выполнят какую-либо работу вместо нас.
📚 пример: <b>she has flowers in her yard watered three times a week – цветы в ее дворе поливают три раза в неделю.</b>
📚 схема: <b>подлежащее – каузативный глагол (have/get) – дополнение – 3 форма глагола</b>
📚 разница <b>have и get</b> заключается в том, что <b>have</b> используется при передаче ответственности и указывает на результат, а <b>get</b> - когда нам удается побудить человека что-то сделать и акцент идет на процесс убеждения.
также после <b>have</b> используется инфинитив без частицы <i>to</i>, а после <b>get</b> - полный инфинитив.
⚠ <b>каузатив может быть использован во всех видовременных формах. они отображены в таблице выше.</b>
    '''
    await edit_media(callback_query,
                     "https://mcenglish.ru/wp-content/uploads/2017/10/Screenshot_124-1.jpg", text,
                     kb.kb_learning_tenses)


# Запуск
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
