import requests
import os
import re

url=input("请输入视频的URL：")
video_url="https:"+url
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
}
video_data=requests.get(video_url,headers=headers).content
os.makedirs('douyin', exist_ok=True)
video_title=input("视频名")

with open('douyin\\'+video_title+'.mp4','wb')as douyin:
    douyin.write(video_data)
    print(video_title+"视频已下载")