from random import choice

from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from requests import get
from unicodedata import category
from contextlib import suppress


def remove_control_characters(s):
    return "".join(ch for ch in s if category(ch)[0] != "C")


def parse_english_word_of_the_day():
    send_pronunciation = True
    url = "https://dictionary.cambridge.org/ru/"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    page = get(url, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    all_ = soup.findAll('p', class_='fs36 lmt-5 feature-w-big wotd-hw')

    for data in all_:
        if data.find("a") is not None:
            word = remove_control_characters(data.text)

    translation = GoogleTranslator(source='en', target='ru').translate(word)
    text = f'''
<b>слово:</b> {word}
<b>перевод:</b> {translation}'''

    with suppress(Exception):
        transcript = f'/{soup.find("span", class_="ipa dipa lpr-2 lpl-1").text}/'
        text += f'''
<b>транскрипция:</b> {transcript}
'''

    name = "".join([choice("qwertyuiopasdfghjklzxcvbnm") for _ in range(9)])

    try:
        doc = get(
            "https://dictionary.cambridge.org" + soup.find("source", type="audio/mpeg")["src"], headers=headers)
        with open(f'{name}.mp3', 'wb') as f:
            f.write(doc.content)
    except:
        send_pronunciation = False

    return text, name, send_pronunciation


def parse_german_word_of_the_day():
    url = "https://www.lexisrex.com/Немецкий/Слово-Дня"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    page = get(url, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    all_ = soup.find('span', style='color:blue;font-size:40px;font-family: "Times New Roman";')
    word = all_.text
    translation = soup.find("font", color="green").text.lower()

    name = "".join([choice("qwertyuiopasdfghjklzxcvbnm") for _ in range(9)])

    doc = get(
        "https://www.lexisrex.com" + soup.find("img", id="play_img_1")["onclick"].split("'")[1], headers=headers)
    with open(f'{name}.mp3', 'wb') as f:
        f.write(doc.content)

    text = f'''
<b>слово:</b> {word}
<b>перевод:</b> {translation}'''

    with suppress(AttributeError):
        example = soup.find("table", width="95%").text.split("\n")[0]
        translation_of_example = GoogleTranslator(source='de', target='ru').translate(example)
        text += f'''
<b>пример предложения:</b> {example}'''
        text += f'''
<b>перевод предложения:</b> {translation_of_example}'''

    return text, name


def process_word_marathon(url, is_noun=False):
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    page = get(url, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    word = soup.find('span', class_="eng").text
    translated = soup.find('span', class_="rus").text
    transcript = soup.find('span', class_="no-mobile transcript").text
    image = "https://www.kreekly.com" + soup.findAll("img")[1]["src"]
    if is_noun:
        word = GoogleTranslator(source='en', target='de').translate(word)
        page = get("https://www.translate.ru/спряжение%20и%20склонение/немецкий/" + word, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")
        try:
            article = soup.find('a', id="fwi1-tab").text[:3]
            return word, article, translated, transcript, image
        except AttributeError:
            return word, translated, transcript, image

    return word, translated, transcript, image
