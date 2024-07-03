import os
import re
import time
from urllib.parse import urljoin
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


def sanitize_filename(filename):
    """
    Replace or remove characters that are not allowed in filenames.
    Retains Chinese characters and replaces other forbidden characters.
    """
    # Define a regular expression to replace forbidden characters
    forbidden_chars = r'[<>:"/\\|?*]'

    # Substitute forbidden characters with underscores
    filename = re.sub(forbidden_chars, '_', filename)

    return filename


url = 'https://www.ddyueshu.com/0_814/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    html_page = response.content.decode("gbk", 'ignore')
    soup = BeautifulSoup(html_page, 'html.parser')
    url_list = soup.find_all("div", attrs={"class": "box_con"})[1].find_all("a")

    save_folder = r"D:\PyCharm Community Edition 2023.3\小爬爬\code\jingsongleyuan"
    os.makedirs(save_folder, exist_ok=True)

    for a in tqdm(url_list):
        page_url = urljoin(url, a.get("href"))
        title = a.get_text().replace(' ', '').strip()
        filename = sanitize_filename(f"{title}.txt")
        filepath = os.path.join(save_folder, filename)

        with open(filepath, "w", encoding="utf-8") as file:
            try:
                response = requests.get(page_url, headers=headers)
                response.raise_for_status()

                html_content = response.content.decode("gbk", 'ignore')
                soup1 = BeautifulSoup(html_content, 'html.parser')

                content_div = soup1.find('div', id='content')

                if content_div:
                    book_content = content_div.get_text(separator='\n')
                    remove_data = "请记住本书首发域名：ddyueshu.com。顶点小说手机版阅读网址：m2.ddyueshu.com"
                    book_content = book_content.replace(remove_data, '')
                    file.write(book_content.strip())
                else:
                    print(f"Content div not found on the page {page_url}.")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page_url}: {e}")
        time.sleep(0.3)

except requests.exceptions.RequestException as e:
    print(f"Error fetching main URL {url}: {e}")