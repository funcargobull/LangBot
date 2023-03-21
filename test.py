from requests import get
from bs4 import BeautifulSoup

url = "https://www.lexisrex.com/Немецкий/Слово-Дня"
headers = {
    "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
page = get(url, headers=headers)
soup = BeautifulSoup(page.content, "lxml")
all_ = soup.find('span', style='color:blue;font-size:40px;font-family: "Times New Roman";')
print(all_.text)
