# -*- coding: utf-8 -*-

import asyncio
import logging
import os
from contextlib import suppress
from random import choice

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from googletrans import Translator

import base
import functions as fn
import keyboards as kb

logging.basicConfig(level=logging.INFO)
bot = Bot(token="", parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
translator = Translator()


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
    file = InputMediaPhoto(media="https://i.postimg.cc/WbC1cr9r/file-1-1.jpg",
                           caption="👋 <b>итак</b>, это - <b>главное меню.</b>\n🌍 выберите язык:")
    await callback_query.message.edit_media(file, reply_markup=kb.kb_main)


@dp.callback_query_handler(lambda c: c.data == 'english' or c.data == 'german' or c.data == 'back')
async def start_lang(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # Английский (старт)
    if callback_query.data == "english":
        base.language(str(callback_query.from_user.id), "английский", set=True, get=False)
        file = InputMediaPhoto(media="https://i.postimg.cc/2S4gpjqt/2023-03-21-190241474.png",
                               caption=f"🇬🇧 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыберите опцию:")
        await callback_query.message.edit_media(file, reply_markup=kb.kb_english)


    # Немецкий (старт)
    elif callback_query.data == "german":
        base.language(str(callback_query.from_user.id), "немецкий", set=True, get=False)
        file = InputMediaPhoto(media="https://i.postimg.cc/Dz7vHMzq/2023-03-21-190610782.png",
                               caption=f"🇩🇪 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыберите опцию:")
        await callback_query.message.edit_media(file, reply_markup=kb.kb_english)

    # Назад
    elif callback_query.data == "back":
        if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
            file = InputMediaPhoto(media="https://i.postimg.cc/2S4gpjqt/2023-03-21-190241474.png",
                                   caption=f"🇬🇧 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыберите опцию:")
            await callback_query.message.edit_media(file, reply_markup=kb.kb_english)
        else:
            file = InputMediaPhoto(media="https://i.postimg.cc/Dz7vHMzq/2023-03-21-190610782.png",
                                   caption=f"🇩🇪 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыберите опцию:")
            await callback_query.message.edit_media(file, reply_markup=kb.kb_english)


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

    file = InputMediaPhoto(media=photo,
                           caption=fact)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_facts_about_country)


# Словесный марафон
@dp.callback_query_handler(lambda c: c.data == "word_marathon" or c.data == "choose_category")
async def word_marathon(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        file = InputMediaPhoto(
            media="https://i.postimg.cc/Y91q9HLv/1x20-The-One-with-the-Evil-Orthodontist-friends-28258398-1280-720.jpg",
            caption="🇬🇧 выберите категорию:")
    else:
        file = InputMediaPhoto(
            media="https://i.postimg.cc/Y91q9HLv/1x20-The-One-with-the-Evil-Orthodontist-friends-28258398-1280-720.jpg",
            caption="🇩🇪 выберите категорию:")
    await callback_query.message.edit_media(file, reply_markup=kb.kb_word_marathon)


@dp.callback_query_handler(lambda c: c.data == "all_parts" or c.data == "farther_all")
async def all_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/")
    text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    file = InputMediaPhoto(media=image,
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_word_marathon_all)


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

    file = InputMediaPhoto(media=image,
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_word_marathon_nouns)


@dp.callback_query_handler(lambda c: c.data == "verbs" or c.data == "farther_verbs")
async def verbs_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/verb/")
    text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    file = InputMediaPhoto(media=image,
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_word_marathon_verbs)


@dp.callback_query_handler(lambda c: c.data == "adjectives" or c.data == "farther_adjectives")
async def adjectives_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/adjective/")
    text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    file = InputMediaPhoto(media=image,
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_word_marathon_adjectives)


@dp.callback_query_handler(lambda c: c.data == "adverbs" or c.data == "farther_adverbs")
async def adverbs_parts_of_speech(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    word, translated, transcript, image = fn.process_word_marathon("https://www.kreekly.com/random/adverb/")
    text = parts_of_speech(str(callback_query.from_user.id), word, translated, transcript)
    file = InputMediaPhoto(media=image,
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_word_marathon_adverbs)


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
    file = InputMediaPhoto(media="https://i.postimg.cc/BvkMv55Y/2023-03-21-203513060.png",
                           caption=caption)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_test)


# Обучение
@dp.callback_query_handler(lambda c: c.data == "learning" or c.data == "back_to_learning")
async def learning(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        file = InputMediaPhoto(
            media="https://i.postimg.cc/8PfNJdr8/think.jpg",
            caption="🎒 выберите раздел:")
        await callback_query.message.edit_media(file, reply_markup=kb.kb_learning)


# Обучение (основы произношения)
@dp.callback_query_handler(lambda c: c.data == 'pronunciation' or c.data == "back_to_courses")
async def learning_pronunciation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    file = InputMediaPhoto(
        media="https://i.postimg.cc/8PfNJdr8/think.jpg",
        caption='🎶 выбрана опция: <b>"основы произношения".</b>\nвыберите курс:')
    await callback_query.message.edit_media(file, reply_markup=kb.kb_pronunciation)


# Обучение (открытый и закрытый слоги, 1 страница)
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
    file = InputMediaPhoto(media="https://storage.kun.uz/source/3/8cMEWm-mnI0u4LZb-cDrJ9ibm1vawnm-.jpg",
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_open_close_syllables)


# Обучение (открытый и закрытый слоги, 2 страница)
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


# Обучение (соответствие букв и звуков, 1 страница)
@dp.callback_query_handler(lambda c: c.data == 'letters_sounds' or c.data == "farther_letters_sounds_1")
async def letters_sounds(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    file = InputMediaPhoto(media="https://i.postimg.cc/02hBMHzp/2023-03-22-200736.png",
                           caption="📘 начнем с самого легкого: с таблицы <b>согласных</b>, произношение которых аналогично русскому звучанию.")
    await callback_query.message.edit_media(file, reply_markup=kb.kb_letters_sounds)


# Обучение (соответствие букв и звуков, 2 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_letters_sounds_2')
async def letters_sounds_2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    file = InputMediaPhoto(media="https://i.postimg.cc/d3GDvxpJ/Opera-2023-03-22-201553-speakenglishwell-ru.png",
                           caption="📘 теперь разберемся с более <b>сложными</b> буквами.")
    await callback_query.message.edit_media(file, reply_markup=kb.kb_letters_sounds_2)


# Обучение (соответствие букв и звуков, 3 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_letters_sounds_3')
async def letters_sounds_3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 изучим <b>буквосочетания</b> согласных в английском языке.
<b>кстати</b>, согласные, стоящие в самом конце слова, нельзя оглушать.
    '''
    file = InputMediaPhoto(media="https://i.postimg.cc/qvsYnxVg/2023-03-22-202219052.png",
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_letters_sounds_3)


# Обучение (соответствие букв и звуков, 4 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_letters_sounds_4')
async def letters_sounds_4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
📘 намного <b>сложнее</b> обстоит ситуация с произношением <b>гласных</b>.
не забывайте о том, что в закрытом слоге все буквы произносятся <b>кратко</b>.
в открытом слоге - <b>плавно и протяжно</b>.
    '''
    file = InputMediaPhoto(media="https://i.postimg.cc/PxyKrSDn/shhhh.jpg",
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_letters_sounds_4)


# Обучение (соответствие букв и звуков, 5 страница)
@dp.callback_query_handler(lambda c: c.data == 'farther_letters_sounds_5')
async def letters_sounds_5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    file = InputMediaPhoto(media="https://i.postimg.cc/1XPG6wpc/dakjfopiq.jpg",
                           caption="📘 не забываем, что буква <b>r</b> после гласного, как правило, <b>не произносится.</b>")
    await callback_query.message.edit_media(file, reply_markup=kb.kb_letters_sounds_5)


# Обучение (дифтонги и трифтонги)
@dp.callback_query_handler(lambda c: c.data == 'diphthongs_triphthongs')
async def diphthongs_triphthongs(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
❓ <b>дифтонги и трифтонги</b> - это сочетания двух или трех букв, обладающие особым звучанием.
сначала <b>усиленно</b> произносят главный звук, а потом плавно его переводят во второстепенный звук.
дифтонги и трифтонги не подчиняются <b>никаким</b> грамматическим законам, поэтому остается только учить их наизусть.
    '''
    file = InputMediaPhoto(media="https://i.postimg.cc/CxqKT1Bb/Opera-2023-03-22-204609-speakenglishwell-ru.png",
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_diphthongs_triphthongs)


# Обучение (интонация. тоны)
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
    file = InputMediaPhoto(media="https://i.postimg.cc/N01JnW6Q/1.jpg",
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_intonation)


# Обучение (сложности)
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
    file = InputMediaPhoto(media="https://att.by/images/news/24341_big.jpg",
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_hard)

# Обучение (ударения)
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
    file = InputMediaPhoto(media="https://i.postimg.cc/XNDZRX7Y/accenrt.jpg",
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_accents)


# Обучение (времена)
@dp.callback_query_handler(lambda c: c.data == 'tenses')
async def learning_tenses(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    text = '''
🕒 выбрана опция: <b>"времена".</b>

🎁 это - емкая шпаргалка по временам. в каждой клетке указана характеристика времени, 
метод образования и маркеры (слова, по которым можно различать времена).
<b>p.s.</b> главное - помнить порядок слов в предложении:
1. <b>утвердительное</b> - подлежащее, сказуемое (возможен вспомогательный глагол), другие члены предложения
2. <b>отрицательное</b> - обстоятельство, подлежащее (возможно с определением), вспомогательный глагол + not,
основной глагол, дополнение (возможно с определением)
3. <b>вопросительное</b> - вспомогательный глагол, подлежащее (возможно с определением), основной глагол,
дополнение (возможно с определением), обстоятельство
    '''
    file = InputMediaPhoto(media="https://i.postimg.cc/gkc7Gb6J/tenses.jpg",
                           caption=text)
    await callback_query.message.edit_media(file, reply_markup=kb.kb_learning_tenses)


# Обучение (подготовка к экзаменам)
@dp.callback_query_handler(lambda c: c.data == 'exams')
async def learning_exams(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '🧠 выбрана опция: <b>"подготовка к экзаменам".</b>')


# Запуск
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
