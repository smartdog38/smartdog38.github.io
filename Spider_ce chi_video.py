import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import time
from tqdm import tqdm

def extract_valid_number(string):
    number = string.split('/')[-1]
    number = number.lstrip('0')
    if not number:
        return '0'
    elif number[0] == '.':
        return '0' + number
    else:
        return number
#返回找到方法二的最大数字
def method_1(headers,iframe_src):
    video_data = b''
    player_url = re.findall('(.*)&', iframe_src)[0]
    driver = webdriver.Edge()
    driver.get(player_url)
    time.sleep(1)
    video_element = driver.find_element(By.XPATH, '//*[@id="artplayer"]/div/video')
    video_src = video_element.get_attribute("src")
    video_data = requests.get(url=video_src, headers=headers).content
    return video_data
#返回方法一的视频数据
def method_2(common_url,iframe_src,headers):
    video_data = b''
    ts_video_url_head = re.findall('url=(.*)index', iframe_src)[0]
    ts_datas = requests.get(url=common_url, headers=headers).text
    ts_strings = re.findall('(.*).ts', ts_datas)
    large_ts_string = ts_strings[-1]
    large_num = int(extract_valid_number(large_ts_string))
    for i in tqdm(range(0, large_num + 1)):
        ts_video_url = ts_video_url_head + ts_strings[i] + ".ts"
        video_content = requests.get(url=ts_video_url, headers=headers).content
        video_data += video_content
    return video_data
#返回方法二的视频数据
def method_3(common_url,headers):
    video_data = b''
    middle_data = requests.get(url=common_url, headers=headers).text
    add_data = re.findall('(.*)index', middle_data)[0] + "index.m3u8"
    middle_url_head = re.findall('https(.*).com', common_url)[0]
    url_head = "https" + middle_url_head + ".com"
    ts_url = url_head + add_data
    ts_data = requests.get(url=ts_url, headers=headers).text
    ts_file_names = re.findall(r'\/[\w\/]+\.ts', ts_data)
    ts_link_count = len(ts_file_names)
    ts_num = int(ts_link_count)
    for i in tqdm(range(0, ts_num)):
        add_ts_data = re.findall('(.*).ts', ts_data)[i]
        ts_video_url = url_head + add_ts_data + ".ts"
        ts_video_content = requests.get(url=ts_video_url, headers=headers).content
        video_data += ts_video_content
    return video_data
#返回返回方法三的视频数据
def judge_method(headers):
    html_url = input("请输入视频页面的网址：")
    driver = webdriver.Edge()
    driver.get(html_url)
    iframe_element = driver.find_element(By.XPATH, '//*[@id="playleft"]/iframe')
    iframe_src = iframe_element.get_attribute("src")
    common_url = re.findall('url=(.*)&', iframe_src)[0]
    if "index" not in common_url:
        method = 1
    else:
        resp = requests.get(url=common_url, headers=headers).text
        if ".ts" in resp:
            method = 2
        else:
            method = 3
    return method,common_url,html_url,iframe_src
#判断method与返回method、common_url、html_url，iframe_src
def find_video_title(html_url,headers):
    hmtl_data = requests.get(url=html_url, headers=headers).text
    soup = BeautifulSoup(hmtl_data, 'html.parser')
    h3_tags = soup.find_all('h3', class_='title text-fff')
    video_title = ""
    for tag in h3_tags:
        video_title += tag.text
    return video_title
#找到、返回video_title
def write_in_file(video_data,video_title):
    with open(f'E:\\video\\{video_title}.mp4', 'wb') as file:
        file.write(video_data)
        file.close()
#video_data写入文件
def find_next_video_html(html_url,headers):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    }
    driver = webdriver.Edge()
    driver.get(html_url)
    iframe_element = driver.find_element(By.XPATH, '//*[@id="player-left"]/ul/li[7]/a')
    next_video_html = iframe_element.get_attribute("href")
    return next_video_html
#寻找、返回next_video_html（若是无则返回""）
def download_video_set(next_video_html):
    driver = webdriver.Edge()
    driver.get(next_video_html)
    iframe_element = driver.find_element(By.XPATH, '//*[@id="playleft"]/iframe')
    iframe_src = iframe_element.get_attribute("src")
    common_url = re.findall('url=(.*)&', iframe_src)[0]
    return common_url, html_url, iframe_src
def create_video_url_list(headers):
    first_video_url = input("请在下面输入系列视频的第一个视频的网址:")
    video_url_list = [first_video_url]
    next_video_url = 0
    while next_video_url != "":
        driver = webdriver.Edge()
        driver.get(video_url_list[-1])
        iframe_element = driver.find_element(By.XPATH, '//*[@id="player-left"]/ul/li[7]/a')
        next_video_url = iframe_element.get_attribute("href")
        video_url_list.append(next_video_url)
        time.sleep(0.1)
    finish_video_url_list = []
    for url in video_url_list:
        if url != "":
            finish_video_url_list.append(url)
    return finish_video_url_list
#返回系列视频列表
def new_judge_method(html_url,headers):
    driver = webdriver.Edge()
    driver.get(html_url)
    iframe_element = driver.find_element(By.XPATH, '//*[@id="playleft"]/iframe')
    iframe_src = iframe_element.get_attribute("src")
    common_url = re.findall('url=(.*)&', iframe_src)[0]
    if "index" not in common_url:
        method = 1
    else:
        resp = requests.get(url=common_url, headers=headers).text
        if ".ts" in resp:
            method = 2
        else:
            method = 3
    return method, common_url, iframe_src
def proce_object():
    print("欢迎运行本程序！！")
    time.sleep(0.5)
    print("您是想要下载单个视频还是下载系列视频：\n1.单个视频\n2.系列视频\n3.方法介绍")
    answer = input("")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
    }
    video_data = b''
    if answer == '1':
        print("正在判断视频的下载方式...")
        method, common_url, html_url, iframe_src = judge_method(headers)
        print(f'该视频的下载方式为：{method}')
        print("正在寻找视频名...")
        video_title = find_video_title(html_url, headers)
        print(f'该视频名字为：{video_title}')
        print("正在寻找视频数据...")
        if method == 1:
            video_data = method_1(headers, iframe_src)
        elif method == 2:
            video_data = method_2(common_url, iframe_src, headers)
        elif method == 3:
            video_data = method_3(common_url, headers)
        print("正在写入文件...")
        write_in_file(video_data, video_title)
    if answer == '2':
        count = 1
        print("正在拉取视频的url列表...")
        finish_video_url_list = create_video_url_list(headers)
        for html_url in finish_video_url_list:
            print(f'正在下载该系列的第{count}个视频')
            method, common_url, iframe_src = new_judge_method(html_url, headers)
            print("正在寻找视频名...")
            video_title = find_video_title(html_url, headers)
            print(f'该视频名字为：{video_title}')
            print("正在寻找视频数据...")
            if method == 1:
                video_data = method_1(headers, iframe_src)
            elif method == 2:
                video_data = method_2(common_url, iframe_src, headers)
            elif method == 3:
                video_data = method_3(common_url, headers)
            print("正在写入文件...")
            write_in_file(video_data, video_title)
            count += 1
        if answer == '3':
            print(
                "方法介绍：\nmethod_1:视频没有分段，找到播放器网址并在播放器页面找到视频的url，访问其数据，全部写入一个二进制文件，转换为MP4格式，并储存\nmethod_2：视频分段，且将url排列，并将排列顺序以网页文本存储，找到网页文本存储位置，找到共有多少个片段，再讲其连接成视频片段的url，访问其数据，全部写入一个二进制文件，转换为MP4格式，并储存\nmethod_3：视频分段，且将url排列，将视频片段的url集合的url的一个片段放到网页的源代码中，进行一系列操作将其补齐，可以得到视频片段的url的集合，访问其数据，全部写入一个二进制文件，转换为MP4格式，并储存")
        print("视频下载完成！")


if __name__ == '__main__':
    proce_object()