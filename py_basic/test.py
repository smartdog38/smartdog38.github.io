import httpx as ht
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import os
import subprocess


for i in range(3,9):
    with open(f"D:\电视剧\去他妈的世界第一季\第{i}集\list.txt","r+",encoding="utf-8") as f:
        ttt = f.read()
    d = []
    for line in ttt.splitlines():
        r = "file " + f"'{line}'"
        d.append(r)
    f.close()
    with open(f"D:\电视剧\去他妈的世界第一季\第{i}集\list.txt","r+",encoding="utf-8")as f:
        for e in d:
            f.write(e+"\n")


    try:
        subprocess.run([
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", f"D:\电视剧\去他妈的世界第一季\第{i}集\list.txt",
            "-c", "copy",
            f"D:\电视剧\去他妈的世界第一季\第{i}集.mp4"
        ], check=True)  # Adding check=True to catch potential errors
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
