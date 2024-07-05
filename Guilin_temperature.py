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