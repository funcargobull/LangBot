# -*- coding: utf-8 -*-

import logging
import os
import asyncio
from random import choice
from googletrans import Translator
from contextlib import suppress

from aiogram import Bot, types, Dispatcher
from aiogram.types import InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

import base
import functions as fn
import keyboards as kb

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5911147477:AAEsJtQB0A4DQlXPbvdefbQu2EyvYjGGCok", parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
translator = Translator()


@dp.message_handler(text="/start")
async def start_(msg: types.Message):
    # /start
    await bot.send_photo(str(msg.from_user.id),
                         photo="https://i.postimg.cc/WbC1cr9r/file-1-1.jpg",
                         caption="👋 <b>итак</b>, это - <b>главное меню.</b>\n🌍 выбери язык:",
                         reply_markup=kb.kb_main)


@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def start_2(callback_query: types.CallbackQuery):
    # Главное меню
    await bot.answer_callback_query(callback_query.id)
    # await bot.send_photo(callback_query.from_user.id,
    #                      photo="https://i.postimg.cc/WbC1cr9r/file-1-1.jpg",
    #                      caption="👋 <b>итак</b>, это - <b>главное меню.</b>\n🌍 выбери язык:",
    #                      reply_markup=kb.kb_main)
    file = InputMediaPhoto(media="https://i.postimg.cc/WbC1cr9r/file-1-1.jpg",
                           caption="👋 <b>итак</b>, это - <b>главное меню.</b>\n🌍 выбери язык:")
    await callback_query.message.edit_media(file, reply_markup=kb.kb_main)


@dp.callback_query_handler(lambda c: c.data == 'english' or c.data == 'german' or c.data == 'back')
async def start_lang(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # Английский (старт)
    if callback_query.data == "english":
        base.language(str(callback_query.from_user.id), "английский", set=True, get=False)
        file = InputMediaPhoto(media="https://i.postimg.cc/2S4gpjqt/2023-03-21-190241474.png",
                               caption=f"🇬🇧 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыбери опцию:")
        await callback_query.message.edit_media(file, reply_markup=kb.kb_english)


    # Немецкий (старт)
    elif callback_query.data == "german":
        base.language(str(callback_query.from_user.id), "немецкий", set=True, get=False)
        file = InputMediaPhoto(media="https://i.postimg.cc/Dz7vHMzq/2023-03-21-190610782.png",
                               caption=f"🇩🇪 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыбери опцию:")
        await callback_query.message.edit_media(file, reply_markup=kb.kb_english)

    # Назад
    elif callback_query.data == "back":
        if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
            file = InputMediaPhoto(media="https://i.postimg.cc/2S4gpjqt/2023-03-21-190241474.png",
                                   caption=f"🇬🇧 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыбери опцию:")
            await callback_query.message.edit_media(file, reply_markup=kb.kb_english)
        else:
            file = InputMediaPhoto(media="https://i.postimg.cc/Dz7vHMzq/2023-03-21-190610782.png",
                                   caption=f"🇩🇪 язык: <b>{base.language(str(callback_query.from_user.id), '', set=False, get=True)}</b>\nвыбери опцию:")
            await callback_query.message.edit_media(file, reply_markup=kb.kb_english)


# Слово дня
@dp.callback_query_handler(lambda c: c.data == "word_of_day")
async def word_of_the_day(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        text, name, send_pronunciation = fn.parse_english_word_of_the_day()
        file = InputMediaPhoto(media="https://i.postimg.cc/sfHJXFdg/2023-03-21-191014445.png",
                               caption=text)
        await callback_query.message.edit_media(file, reply_markup=kb.kb_word_of_day)
        if send_pronunciation:
            x = await bot.send_audio(str(callback_query.from_user.id), open(f"{name}.mp3", "rb"), title="анг. произношение (удалится через 10 с)")
            asyncio.create_task(delete_message(x, 10))
            os.remove(f"{name}.mp3")
    else:
        text, name = fn.parse_german_word_of_the_day()
        file = InputMediaPhoto(media="https://i.postimg.cc/sfHJXFdg/2023-03-21-191014445.png",
                               caption=text)
        await callback_query.message.edit_media(file, reply_markup=kb.kb_word_of_day)
        x = await bot.send_audio(str(callback_query.from_user.id), open(f"{name}.mp3", "rb"), title="нем. произношение (удалится через 10 с)")
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

    # await bot.send_photo(str(callback_query.from_user.id), photo=photo, caption=fact,
    #                      reply_markup=kb.kb_facts_about_country)
    # file = InputMedia(media=InputFile(photo), caption="Updated caption :)")
    # await callback_query.message.edit_media(file, reply_markup=kb.kb_facts_about_country)

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
        file = InputMediaPhoto(media="https://i.postimg.cc/BvkMv55Y/2023-03-21-203513060.png",
                               caption="📓 чтобы пройти тест, перейди по <b>ссылке:</b>\n💻 https://englishtest.pythonanywhere.com")
        await callback_query.message.edit_media(file, reply_markup=kb.kb_test)
    else:
        file = InputMediaPhoto(media="https://i.postimg.cc/BvkMv55Y/2023-03-21-203513060.png",
                               caption="📓 чтобы пройти тест, перейди по <b>ссылке:</b>\n💻 https://germantest.pythonanywhere.com")
        await callback_query.message.edit_media(file, reply_markup=kb.kb_test)


# Обучение
@dp.callback_query_handler(lambda c: c.data == "learning")
async def learning(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if base.language(str(callback_query.from_user.id), '', set=False, get=True) == "английский":
        file = InputMediaPhoto(
            media="https://деловаясеть.рф/wp-content/uploads/2018/10/1_0_300_business-1_77777777ryeury933339393.jpg",
            caption="🎒 выбери опцию:")
        await callback_query.message.edit_media(file, reply_markup=kb.kb_learning)


@dp.callback_query_handler(lambda c: c.data == 'pronunciation')
async def learning_pronunciation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '🎶 выбрана опция: <b>"основы произношения".</b>')


@dp.callback_query_handler(lambda c: c.data == 'tenses')
async def learning_tenses(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '🕒 выбрана опция: <b>"времена".</b>')


@dp.callback_query_handler(lambda c: c.data == 'exams')
async def learning_exams(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '🧠 выбрана опция: <b>"подготовка к экзаменам".</b>')


# Запуск
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
