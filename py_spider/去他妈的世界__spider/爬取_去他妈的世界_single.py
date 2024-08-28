import requests
import re
from tqdm import tqdm
import os
import subprocess

# 第一步：访问视频的网页 -> 返回状态码，200表示允许访问
html_url = 'https://v.ijujitv.cc/play/42405-1-1.html'
respon = requests.get(url=html_url)

# 第二步：请求数据
html_content = respon.text

# 第三步：找到所需的数据
# 视频名
video_title = re.findall(r"<title>(.*?)全集高清在线免费播放_美剧_剧集TV</title>", html_content)[0].replace("《", "").replace("》", "")
folder_path = f"D:\\电视剧\\{video_title}"

# 检查并创建文件夹
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"已创建 {video_title} 文件夹")
else:
    print("文件夹已存在")

# 创建 ts_list.txt 文件
with open(os.path.join(folder_path, "ts_list.txt"), "w",encoding="utf-8") as ff:
    # 视频数据
    index_url = re.findall(r'"url":"(.*?)","url_next"', html_content)[0].replace("\\", "")

    # 找到 ts 文件的存储地址
    mix_url = requests.get(url=index_url).text.splitlines()[2]
    added_url = index_url.replace("index.m3u8", "")
    mixed_url = added_url + mix_url
    added_url2 = mixed_url.replace("mixed.m3u8", "")

    # 请求混合 URL 并获取 TS 列表
    ts_url_list = requests.get(url=mixed_url).text.splitlines()

    if ts_url_list:  # 确保 ts_url_list 不为空
        for i, item in enumerate(tqdm(ts_url_list), start=1):
            if "#" not in item:
                ts_url = added_url2 + item
                try:
                    ts_data = requests.get(url=ts_url).content
                    ts_file_path = os.path.join(folder_path, f"{i}.ts")
                    with open(ts_file_path, "wb") as fff:
                        fff.write(ts_data)
                        # 使用原始字符串，确保写入的路径格式正确
                        ff.write(f"file '{ts_file_path}'\n")
                except Exception as e:
                    print(f"下载 {ts_url} 时出错: {e}")
    else:
        print("没有找到任何 TS 文件")

# 使用 ffmpeg 合并 ts 文件
try:
    output_file_path = os.path.join(folder_path, "final.mp4")
    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", os.path.join(folder_path, "ts_list.txt"),
        "-c", "copy",
        output_file_path
    ], check=True)  # 添加 check=True 来捕获可能的错误
    print("合并完成！")
except subprocess.CalledProcessError as e:
    print(f"合并文件时出错: {e}")

# 删除临时的 .ts 文件
for i, item in enumerate(tqdm(ts_url_list), start=1):
    if "#" not in item:
        try:
            os.remove(os.path.join(folder_path, f"{i}.ts"))
        except Exception as e:
            print(f"删除 {os.path.join(folder_path, f'{i}.ts')} 时出错: {e}")

print("下载和清理工作结束！")