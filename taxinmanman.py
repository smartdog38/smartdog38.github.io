
import requests
import re
import os
from bs4 import BeautifulSoup
import time

path = r"D:\PyCharm Community Edition 2023.3\小爬爬\code"
folder_name = "taxinmanman"
folder_path = os.path.join(path, folder_name)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("已创建文件夹！")
else:
    print("文件夹已存在！")

url = 'https://www.biqgxs.com/books/63531804/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
chapter_list = soup.find_all("div", class_="02e03 panel panel-default")[2].find_all("a")

for chapter_data in chapter_list:
    chapter_href = chapter_data.get("href")
    chapter_title = chapter_data.get_text()
    chapter_url = "https://www.biqgxs.com" + chapter_href
    try:
        chapter_page = requests.get(url=chapter_url).text
        chapter_soup = BeautifulSoup(chapter_page, "html.parser")
        chapter_content = chapter_soup.find("div", id="rtext").get_text()
        cleaned_content = re.search(r'最新章节！(.*?)本章未完', chapter_content, re.DOTALL).group(1).strip()
        with open(os.path.join(folder_path, f"{chapter_title}.txt"), "w", encoding="utf-8") as file:
            file.write(cleaned_content)
        print(f"已下载并保存章节：{chapter_title}")
        time.sleep(0.1)  # Adding a small delay to be polite to the server
    except Exception as e:
        print(f"下载章节 {chapter_title} 时出错：{e}")

print("下载完成")


