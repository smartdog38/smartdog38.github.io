#examble 1
# heigh = 100
# distance = 0
# for i in range(10):
#     distance = distance + heigh
#     if i == 9:
#         break
#     heigh = heigh / 2
#     distance = distance + heigh
# print(distance)
import re

#examble 2
# for i in range(1,10):
#     for j in range(1,i+1):
#         print(f'{j} * {i} = {i * j}',end='\t')
#     print()

#examble 3
# a = {1,3,2,6,64,4,9}
# if 7 in a:
#     print("true")
# else:
#     print("false")

#examble 4
# import  random
# staff_list = []
# for i in range(1,301):
#     staff_list.append(f"员工{i}")
# list = [3,6,30]
# for i in list:
#     print()
#     third_prize_list = random.sample(staff_list,i)   #remove()#for
#     for i in third_prize_list:
#         print(i,end=" ")

#炸金花
# import random
# player_set = []
# card_set = []
# num = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
# for i in num:
#     card_set.append(f"梅花{i}")
#     card_set.append(f"红桃{i}")
#     card_set.append(f"方片{i}")
#     card_set.append(f"黑桃{i}")
#
# a = int(input("玩家个数（<=17）："))
# for i in range(0,a):
#     player_card = random.sample(card_set,3)
#     player_set.append(player_card)
#     for j in player_card:
#         card_set.remove(j)
# while True:
#     player = int(input("请输入想要查询的玩家序号"))
#     if player > a :
#         print("输入的玩家不存在，请重新输入：")
#         continue
#     print(f"玩家{player}的牌为：{player_set[player-1]}")
#哥ajp

#用.join()来拼接字符串
# set = ['i','love','you','three','thousand']
# result = ' '.join(set)
# print(result)
# import requests
# requests.get(url=url,params=)
# a = "aabcacb1111acbba"
# print(a.strip("abc"))
# print(a.strip("acb"))
# print(a.strip("bac"))
# print(a.strip("bca"))
# print(a.strip("cab"))
# print(a.strip("ca"))

import re
import requests
from lxml import etree
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://www.qixiangwang.cn/guilin30tian.htm'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    content = response.content.decode('utf-8')
    root = etree.HTML(content)
    temperature_elements = root.xpath('//div[@class="tqqk"]/ul/li/text()')
    temperatures = []
    days = []
    for element in temperature_elements:
        day = element.split(',')[0].strip()
        day = re.findall(r"(\d+)",day)
        days.append(day)
        temperature = element.split(',')[1].strip()
        temperature = int(re.findall(r"(\d+)",temperature)[0])
        temperatures.append(temperature)
    July_dates = []
    August_dates = []
for day in days:
    if day[0] == '7':
        July_dates.append(int(day[1]))
    elif day[0] == '8':
        August_dates.append(int(day[1]))
July_temperatures = temperatures[:26]
August_temperatures = temperatures[26:]

df_july = pd.DataFrame({'Date': July_dates, 'Temperature (°C)': July_temperatures})
df_august = pd.DataFrame({'Date': August_dates, 'Temperature (°C)': August_temperatures})
excel_filename = 'Guilin_Temperatures.xlsx'
with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
    if not df_july.empty:
        df_july.to_excel(writer, sheet_name='July', index=False)
    if not df_august.empty:
        df_august.to_excel(writer, sheet_name='August', index=False)
print(f"Excel file '{excel_filename}' has been created successfully.")

plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
plt.plot(July_dates,July_temperatures,'r-',label='July Temperatures')
plt.title("Daily temperature in Guiling")
plt.xlabel('data(July)')
plt.ylabel('temperature(°C)')
plt.grid(True)
plt.legend()
plt.tight_layout()
stride = 1
plt.xticks(July_dates[::stride])

plt.subplot(1,2,2)
plt.plot(August_dates,August_temperatures,'b-',label='August Temperature')
plt.title("Daily temperature in Guiling")
plt.xlabel('data(August)')
plt.ylabel('temperature(°C)')
plt.grid(True)
plt.legend()
plt.tight_layout()
stride = 1
plt.xticks(August_dates[::stride])
plt.savefig('Temperatures.png')

plt.show()