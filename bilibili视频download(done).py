import requests
import re
import json
import os
import subprocess
from tqdm import tqdm
#导入模块

def input_data():
    BV = input("请输入视频的BV号：")
    video_title = input("请输你想起的名字（注意不要有特殊字符哦）：")
    return BV,video_title
#输入视频名及视频BV

def user_data(BV,video_title):
    url = f'https://www.bilibili.com/video/{BV}'
    headers = {
        'Cookie': 'buvid3=A6DF93F7-96D3-A901-BC95-93771868F34921432infoc; b_nut=1694922421; i-wanna-go-back=-1; b_ut=7; _uuid=25BB10247-D599-F1BD-82D1-F78F84D65AFA52280infoc; buvid4=0C05879D-C9F9-BD09-56E4-0897FD9F4DD622538-023091711-jpYbLRJjQgve7F9uVWHwyA%3D%3D; rpdid=|(k|Rl|~)|~~0J\'uYmRmkkRl~; header_theme_version=CLOSE; buvid_fp_plain=undefined; DedeUserID=412900965; DedeUserID__ckMd5=06c78616ed43ec4c; enable_web_push=DISABLE; is-2022-channel=1; blackside_state=0; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; CURRENT_QUALITY=0; fingerprint=5a200985f6f4a41417525500b40e4c86; buvid_fp=5a200985f6f4a41417525500b40e4c86; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTMxOTU0MDYsImlhdCI6MTcxMjkzNjE0NiwicGx0IjotMX0.OIa2X9h7uMugMkhReJqEoUnjaFz4t2cv4xGxz2Qk8A0; bili_ticket_expires=1713195346; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; SESSDATA=e3e87a04%2C1728530236%2C76f2b%2A42CjA0DhTKS9sFU_9gGorwaq1rH6mwh83KT7Kn81U12xnxwkfsIX8wEmEEQ02n2enxiy8SVnRKeTlkX3h4OHRIY1llaHNNX3hDb3RZM1FKeHVUajRQWjNtQmxsQS14V1F1YllDYkEwSlZEYzh6TE80bmJpUmZKUWo2NnlKeXkwZlo5MUxQb081a0FBIIEC; bili_jct=fd5d6223033f9b6a8bacad576dba027d; bp_video_offset_412900965=919889240723030051; PVID=5; b_lsid=94294BE5_18EDB2E9DB2; bsource=search_baidu; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; home_feed_column=4; browser_resolution=1164-889; sid=4wll2nmx',
        'Referer': f'https://www.bilibili.com/video/{BV}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    }
    return url,headers
#用户数据及请求对象

def request_data(url,headers):
    html_data = requests.get(url=url, headers=headers).text
    video_info = re.findall('<script>window.__playinfo__=(.*?)</script>', html_data)[0]
    json_data = json.loads(video_info)
    video_url = json_data['data']['dash']['video'][0]['baseUrl']
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
    video_data = requests.get(url=video_url, headers=headers).content
    audio_data = requests.get(url=audio_url, headers=headers).content
    return video_data,audio_data,json_data
#获得网页数据并得到视频数据
def write_file(video_title,video_data,audio_data):
    os.makedirs('audio', exist_ok=True)
    os.makedirs('video', exist_ok=True)

    with open(f"video\\{video_title}.mp4", "wb") as video_file:
        video_file.write(video_data)

    with open(f"audio\\{video_title}.mp3", "wb") as audio_file:
        audio_file.write(audio_data)
    print("数据已写入")
#将视频与音频数据写入文件
def combine_file(video_title,json_data):
    ffmpeg_path = "D:\\ffmpeg-7.0-essentials_build\\bin\\ffmpeg.exe"

    final_cmd= f"{ffmpeg_path} -i video\\{video_title}.mp4 -i audio\\{video_title}.mp3 -c:v copy -c:a aac -strict experimental final_video\\{video_title}.mp4"
    # 执行合成命令
    process = subprocess.Popen(
        final_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Read and print ffmpeg process output line by line
    with tqdm(total=json_data['data']['dash']['duration'], desc="合成进度", unit="秒") as pbar:
        for line in process.stdout:
            # Parse ffmpeg output to extract progress information
            if "time=" in line:
                time_info = re.search(r"time=(\d+:\d+:\d+)", line)
                if time_info:
                    time_str = time_info.group(1)
                    hours, minutes, seconds = map(int, time_str.split(":"))
                    total_seconds = hours * 3600 + minutes * 60 + seconds
                    pbar.update(total_seconds - pbar.n)
    # Wait for the process to finish and get the return code
    return_code = process.wait()

    # Check if the process was successful
    if return_code == 0:
        print("合成完成")
        # Delete original video and audio files
        os.remove(f"video\\{video_title}.mp4")
        os.remove(f"audio\\{video_title}.mp3")
        print("原始文件已删除")
    else:
        print("合成过程中出现错误")
#合成视频并删除合成资源


if __name__ == '__main__':
    BV,video_title=input_data()
    url,headers=user_data(BV,video_title)
    video_data,audio_data,json_data=request_data(url,headers)
    write_file(video_title,video_data,audio_data)
    combine_file(video_title,json_data)
