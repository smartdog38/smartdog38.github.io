import requests
import os
import re
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

path = "D:/PyCharm Community Edition 2023.3/小爬爬/code"
folder_name = '潮点图片'
folder_path = os.path.join(path, folder_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"文件夹 '{folder_name}' 已创建于路径 '{path}'")
else:
    print(f"文件夹 '{folder_name}' 已经存在于路径 '{path}'")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}

pictures_number = int(input("嘿嘿嘿，想要几张美女照片呢？ "))
page_number = 1
count = 0
while pictures_number > 0:
    url = f'https://shipin520.com/v1/level-search?kid=17&word=%E7%BE%8E%E5%A5%B3&type=tp&order=&filters=&p_page={page_number}&p_limit=100&sale_type='
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode("utf-8")
        id_list = re.findall(r'"id":(\d+),', content)
        for id in id_list:
            if len(id) == 6 and pictures_number > 0:
                html_url = f'https://shipin520.com/tp-{id}.html'
                html_data = requests.get(url=html_url, headers=headers).text
                soup = BeautifulSoup(html_data, 'html.parser')
                pictures_data = soup.find("img", attrs={"class": "full"})
                if pictures_data:
                    pictures_src = pictures_data.get("src")
                    pictures_title = pictures_data.get("alt")
                    pictures_title = f"{id}--" + pictures_title.replace("图片素材免费下载", "")
                    if os.path.exists(os.path.join(folder_path, f"{pictures_title}.jpg")):
                        continue
                    pictures_url = "https:" + pictures_src
                    picture_content = requests.get(url=pictures_url, headers=headers).content
                    with open(os.path.join(folder_path, f"{pictures_title}.jpg"), "wb") as file:
                        file.write(picture_content)
                    file.close()
                    time.sleep(0.1)
                    print(f"已下载：{pictures_title}")
                    pictures_number -= 1
        page_number += 1
    else:
        print(f"Failed to retrieve data from page {page_number}. Status code: {response.status_code}")
        break

print("图片下载完成！")