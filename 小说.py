import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://fanqienovel.com/page/7264473116506590243?enter_from=stack-room'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}
page = requests.get(url=url,headers=headers).text
# print(page)
soup = BeautifulSoup(page,'html.parser')
chapter_list = soup.find_all("a",attrs={"class":"chapter-item-title"})
# print(chapter_list)
for chapter in chapter_list:
    href = chapter.get("href")
    chapter_url = urljoin(url,href)
    print(chapter_url)
    chapter_data = requests.get(url=chapter_url,headers=headers).text
    # print(chapter_data)

    chapter_soup = BeautifulSoup(chapter_data,'html.parser')
    word_list = chapter_soup.find_all("div",attrs={"class":"muye-reader-content noselect"})
    print(word_list)
    break

