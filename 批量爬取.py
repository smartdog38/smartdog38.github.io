import requests
import  re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import  json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}
url = 'https://www.ddyueshu.com/0_814/62091756.html'
respon = requests.get(url=url,headers=headers).content.decode("gbk",'ignore')
# print(respon)
soup = BeautifulSoup(respon,'html.parser')
book_content = soup.find("div",attrs={"id":"content"}).get_text()
print(book_content)