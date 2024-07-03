import requests
from tqdm import tqdm
import os
import time
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}

url = 'https://shipin520.com/sousuo/?word=%E7%BE%8E%E5%A5%B3&type=tp&kid=17&order=&data=&page=1'
respon = requests.get(url=url,headers=headers).text
print(respon)
