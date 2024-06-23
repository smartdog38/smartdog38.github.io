import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import  json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}

#爬取纵横小说网
chapter_url = 'https://bookapi.zongheng.com/api/chapter/getChapterList'
data = {
'bookId': '1322577'#每个书的ID不一样
}
chapter_page = requests.post(url = chapter_url,headers=headers,data=data).json()
# print(chapter_page)
# soup_chapter = BeautifulSoup(chapter_url,'html.parser')

chapter_ID_list = chapter_page['result']['chapterList'][0]['chapterViewList']
# print(chapter_ID_list)
with open("让你下山娶妻，不是让你震惊世界.txt","w",encoding="utf-8") as f:
    for chapter_ID in chapter_ID_list:
        content = ''
        chapterId = chapter_ID['chapterId']
        chapter_url_f = f'https://read.zongheng.com/chapter/1322577/{chapterId}.html'
        # print(chapter_url_f)
        page = requests.get(url=chapter_url_f, headers=headers).text
        # print(page)
        soup = BeautifulSoup(page, 'html.parser')
        # 找到网页的小说内容
        title = soup.find('div', attrs={"class": "title_txtbox"}).get_text()
        print(title)
        f.write(title)
        f.write("\n")
        p_list = soup.find_all('div', attrs={'class': 'content'})
        for p in p_list:
            content += p.get_text()
            # print(content)
        f.write(content)
        f.write("\n")
        print(content)
        time.sleep(1)
    f.close()
