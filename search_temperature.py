import requests
import pandas as pd
import numpy as np
import os
import re
import time
import matplotlib.pyplot as plt
from lxml import etree


city = input("请输入你想要查询的城市：")
url = f'https://www.qixiangwang.cn/{city}.htm'
respon = requests.get(url=url)
respon_content =respon.content.decode("utf-8")
root = etree.HTML(respon_content)
total_temperatures = root.xpath('//div[@class="tqqk"]/ul/li/text()')

morning_temperqtures = []
night_temperatures = []
months = []
days = []

for temperatures in total_temperatures:
    date = temperatures .split("：")[0]
    date = re.findall(r"(\d+)",date)
    month = date[0]
    months.append(int(month))
    day = date[1]
    days.append(int(day))
    morning_temperqture = temperatures.split(",")[1].strip()
    night_temperature = temperatures.split("；")[1].strip()
    morning_temperqture = re.findall(r"(\d+)",morning_temperqture)[0]
    night_temperature = re.findall(r"(\d+)", night_temperature)[0]
    # print(morning_temperqture,night_temperature)
    morning_temperqtures.append(int(morning_temperqture))
    night_temperatures.append(int(night_temperature))


print(morning_temperqtures,night_temperatures,months,days)




# 创建列表以存储每个月的早晚温度
monthly_morning_temperatures = [[] for _ in range(12)]
monthly_night_temperatures = [[] for _ in range(12)]

# 用每个月的温度填充列表
for i, month in enumerate(months):
    index = month - 1  # Adjust index since months are 1-based
    monthly_morning_temperatures[index].append(morning_temperqtures[i])
    monthly_night_temperatures[index].append(night_temperatures[i])

# Plotting temperatures for each month
fig, ax = plt.subplots(figsize=(10, 6))


for month in range(12):
    if len(monthly_morning_temperatures[month]) > 0:
        days_in_month = range(1, len(monthly_morning_temperatures[month]) + 1)
        ax.plot(days_in_month, monthly_morning_temperatures[month], marker='o', linestyle='-', label=f'Morning Temp Month {month+1}')
        ax.plot(days_in_month, monthly_night_temperatures[month], marker='x', linestyle='--', label=f'Night Temp Month {month+1}')

ax.set_xlabel('Days')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Monthly Temperature Variation')
ax.legend()
plt.grid(True)
plt.tight_layout()
plt.show()








