import asyncio
import httpx
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import os


# 定义一个获取ts列表的函数，存储 ts 的 URL
async def get_ts_list_url(html_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(html_url) as response:
            html_data = await response.text()
            index_url = re.findall(r'url":"(.*?)","url_next', html_data)[0].replace("\\", "")
            async with session.get(index_url) as response_index:
                mix_url = (await response_index.text()).splitlines()[2]
                mixed_url = urljoin(index_url, mix_url)
                async with session.get(mixed_url) as response_mix:
                    ts_mix_url = (await response_mix.text()).splitlines()
                ts_dict = {}
                i = 1
                if ts_mix_url:
                    for line in ts_mix_url:
                        if "#" not in line:
                            url = urljoin(mixed_url, line)
                            ts_dict[f"{i}"] = url
                            i += 1
                else:
                    print("找不到相应的ts文件")
                return ts_dict, i

# 异步下载单个视频
async def request_respon(ts_url, num, title):
    async with aiohttp.ClientSession() as session:
        async with session.get(ts_url) as response:
            data = await response.read()
            with open(f"{title}/{num}.ts", 'wb') as f:
                f.write(data)

def create_txt(title, num):
    with open("ts_list.txt", "w") as file:
        for i in range(1, num):
            file.write(f"{title}/{str(i)}.ts\n")

async def main(html_url, title):
    ts_dict, num = await get_ts_list_url(html_url)
    create_txt(title, num)
    tasks = []
    for item in ts_dict:
        task = asyncio.create_task(request_respon(ts_dict[item], item, title))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    html_url = 'YOUR_HTML_URL_HERE'
    title = 'YOUR_TITLE_HERE'
    asyncio.run(main(html_url, title))




# 多线程

