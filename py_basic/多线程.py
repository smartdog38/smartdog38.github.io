from threading import Thread
import requests
from concurrent.futures import ThreadPoolExecutor
import re
from tqdm import tqdm

add_url = 'https://play.vplay.life/ts'
url_list = ['https://play.vplay.life/m3/3d7633e1720328023/36NjY4OTc2OTc1MDlkNyQxNTk3JDMkMTcyMDI4NDgyMw66897697509d5.m3u8']

def get_video(url):
    respon = requests.get(url=url).text
    ts_urls = re.findall(r"/ts(.*?)\n",respon)
    video_data = b''
    title = re.findall(r"(\d+)",url)[0] + re.findall(r"(\d+)",url)[1] + re.findall(r"(\d+)",url)[2]
    print(f"正在下载{title}.....")
    with open(f"E:\\video\\{title}.mp4","wb")as f:
        for ts_url in tqdm(ts_urls):
            ts_total_url = add_url + ts_url
            ts_data = requests.get(url=ts_total_url).content
            video_data += ts_data
        f.write(video_data)
        print(f"{title}下载完毕！")
        f.close()

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(get_video, url_list)