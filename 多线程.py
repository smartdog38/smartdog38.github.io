from threading import Thread
import requests
from concurrent.futures import ThreadPoolExecutor
import re

add_url = 'https://play.vplay.life/ts'
url_list = ['https://play.vplay.life/m3/ebacf5f1720327809/76NjY4OTc1YzFmMmEyNSQxNTk3JDEkMTcyMDI4NDYwOQ668975c1f2a23.m3u8','https://play.vplay.life/m3/050c8471720327993/37NjY4OTc2NzlkYTNjOSQxNTk3JDIkMTcyMDI4NDc5Mw66897679da3c7.m3u8','https://play.vplay.life/m3/3d7633e1720328023/36NjY4OTc2OTc1MDlkNyQxNTk3JDMkMTcyMDI4NDgyMw66897697509d5.m3u8','https://play.vplay.life/m3/cc361d41720328057/17NjY4OTc2YjkwM2FkYiQxNTk3JDQkMTcyMDI4NDg1Nw668976b903ad9.m3u8','https://play.vplay.life/m3/a4b84961720328076/49NjY4OTc2Y2M3YTQyMSQxNTk3JDUkMTcyMDI4NDg3Ng668976cc7a41f.m3u8','https://play.vplay.life/m3/06803bb1720328094/80NjY4OTc2ZGUzYmRhZiQxNTk3JDYkMTcyMDI4NDg5NA668976de3bdac.m3u8','https://play.vplay.life/m3/f2567b51720328108/93NjY4OTc2ZWNjYzIyMyQxNTk3JDckMTcyMDI4NDkwOA668976eccc220.m3u8','https://play.vplay.life/m3/3d0b83e1720328126/74NjY4OTc2ZmUwOTE1MCQxNTk3JDgkMTcyMDI4NDkyNg668976fe0914d.m3u8']


def get_video(url):
    respon = requests.get(url=url).text
    ts_urls = re.findall(r"/ts(.*?)\n",respon)
    video_data = b''
    title = re.findall(r"(\d+)",url)[0] + re.findall(r"(\d+)",url)[1] + re.findall(r"(\d+)",url)[2]
    print(f"正在下载{title}.....")
    with open(f"E:\\video\\{title}.mp4","wb")as f:
        for ts_url in ts_urls:
            ts_total_url = add_url + ts_url
            ts_data = requests.get(url=ts_total_url).content
            video_data += ts_data
        f.write(video_data)
        print(f"{title}下载完毕！")
        f.close()

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(get_video, url_list)