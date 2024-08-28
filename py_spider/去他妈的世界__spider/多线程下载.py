import httpx as ht
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import os
import subprocess


def search_html(first_url, retries=3, timeout=10):
    html_dict = {}
    num = re.findall(r"\d+", first_url)[2]
    save_url_dict(first_url, num, html_dict)
    for attempt in range(retries):
        try:
            html_data0 = ht.get(first_url, timeout=timeout).text
            respon = re.findall(r'<a class="playLink" href="(.*?)">', html_data0)
            for url in respon:
                html_url = urljoin(first_url, url)
                num = re.findall(r"\d+", html_url)[2]
                save_url_dict(html_url, num, html_dict)
            return html_dict
        except ht.ReadTimeout:
            print(f"Attempt {attempt + 1} timed out.")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
    print("All attempts failed.")
    return html_dict

def save_url_dict(url, num, html_dict):
    html_dict[f"第{num}集"] = url
def get_title_create_folder(html_url):
    html_data = ht.get(html_url,timeout=10).text
    title = re.findall(r"<title>《(.*?)》.*?<\/title>", html_data)[0]
    folder_name = os.path.join("D:/电视剧", title)
    os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist
    print(f"{folder_name}已创建！")
    return folder_name

def find_ts_url(html_url):
    ts_dict = {}
    html_data = ht.get(html_url,timeout=10).text
    index_url = re.findall(r'url":"(.*?)","url_next', html_data)[0].replace("\\", "")
    mix_url = ht.get(index_url,timeout=10).text.splitlines()[2]
    mixed_url = urljoin(index_url, mix_url)
    ts_mix_url = ht.get(mixed_url,timeout=10).text.splitlines()
    i = 0
    if ts_mix_url:
        for line in ts_mix_url:
            if "#" not in line:
                i += 1
                url = urljoin(mixed_url, line)
                ts_dict[str(i)] = url
    else:
        print("找不到相应的ts文件")
    return ts_dict, i


def create_folder_txt(folder_name, name):
    path = os.path.join(folder_name, name)
    txt_path = os.path.join(path, "list.txt")
    # Create list.txt if it doesn't exist
    if not os.path.exists(txt_path):
        open(txt_path, 'w').close()
    return txt_path



def down_ts_video(folder_name, name, ts_url, episode_num):
    ts_name = os.path.join(folder_name, name, f"{episode_num}.ts")  # Use episode number directly
    try:
        data = ht.get(ts_url, timeout=10).content
        with open(ts_name, "wb") as f:
            f.write(data)
        # Append the ts file path to the corresponding list.txt
        txt_path = os.path.join(folder_name, name, "list.txt")
        with open(txt_path, "a", encoding="utf-8") as f:
            f.write(f"{ts_name}\n")  # Write the .ts file path to the text file
    except Exception as e:
        print(f"Error downloading {ts_url}: {e}")

def merge(txt,folder_path,name):
    try:
        output_file_path = os.path.join(folder_path, f"{name}.mp4")
        subprocess.run([
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", txt,
            "-c", "copy",
            output_file_path
        ], check=True)
        os.rmdir(os.path.join(folder_path,name))
    except subprocess.CalledProcessError as e:
        print(f"合并文件时出错: {e}")


def download(html_url, folder_name, name):
    ts_dict, num = find_ts_url(html_url)
    txt_path = create_folder_txt(folder_name, name, num)
    with ThreadPoolExecutor(max_workers=4) as executor:
        for item in ts_dict:
            executor.submit(down_ts_video, folder_name, name, ts_dict[item], str(num))
    merge(txt_path, folder_name, name)

def main():
    html_url = input("url :")
    html_dict = search_html(html_url)
    folder_name = get_title_create_folder(html_url)
    with ThreadPoolExecutor(max_workers=4) as executor:
        for item in html_dict:
            executor.submit(download(html_dict[item],folder_name,item))


if __name__ == '__main__':
    main()


