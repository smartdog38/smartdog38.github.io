# import os
#
# path = "D:/PyCharm Community Edition 2023.3/小爬爬/code"
# folder_name = "AI"
# folder_path = os.path.join(path,folder_name)
# if not os.path.exists(folder_path):
#     os.makedirs(folder_path)
#     print(f"{folder_path}已创建")
# else:
# #     print(f"{folder_path}已存在")
# import numpy as np
# from lxml import etree
# import requests


# url = 'https://www.biqgxs.com/books/63531804/'
# html_string = requests.get(url).text
# html = etree.HTML(text)
# result = etree.tostring(html).decode("utf-8")
#
# html = etree.parse('data.html')
# result = etree.tostring(html).decode("utf-8")

# import pandas
# import numpy
# import matplotlib.pyplot as plt



# df = pandas.Series(data=[44,55,79,66],index=['james','hams','peter','jutty'],dtype=numpy.int64,name='score',copy=False)
# print(df)
# df_2 = pandas.DataFrame(data=[[34,66,89],[78,98,45],[78,44,15]],columns=['maths','Chinese','English'],dtype=numpy.int64,copy=False)
# print(df_2)
# df_3 = pandas.DataFrame(data={'name':['james','hams','peter','jutty'],'age':[99,74,97,78]})
# print(df_3)
# df_4 =pandas.DataFrame(data=[{'name':'hams','score':'78'},{'name':'Tom','score':'74'},{'name':'jams','score':'99'}])
# print(df_4)
# print(df.size,df_2.size,df_3.size,df_4.size)
# print(df.ndim,df_2.ndim,df_3.ndim,df_4.ndim)
# print(df_2.tail(1))
# print(df_2.head(1))
# print(df_2.index)
# print(df_2.columns)
# print(df_2.values)
# print(df_2.info)
# print(df_2.dtypes)
# print(df_2.T)
# result = df_3.loc[df_3['name']=='hams',['name']]
# print(result)
# result = df_4.loc[df_4['name']=='Tom',['score']]
# print(result)
# tip = df_3['name']=='hams'
# result = df_3[tip]['name']
# print(result)
# result = df_3.iloc[:,0]
# print(result)
# df_4['id']=[12,13,15]
# print(df_4)
# df_4.insert(loc=1,column='age',value=[18,77,29])
# print(df_4)
# df_4 = df_4.rename(columns={'id':'student_id'})
# print(df_4)

# city = pandas.DataFrame({'日期': ['2022', '2022', '2024', '2022', '2023', '2024', '2022', '2024', '2024'],
#                      '城市': ['上海', '上海', '上海', '北京', '北京', '北京', '南京', '南京', '南京'],
#                      'GDP(万亿)': [3, 6, 9, 6, 12, 15, 6, 7, 10]})
# city = city.pivot_table(index='日期', columns='城市', values='GDP(万亿)', aggfunc='sum')
# print(city)
# df_5 = pandas.DataFrame(numpy.random.randint(4,20),index=pandas.date_range('2018/9/15',periods=10),columns=list('ABCD'))
# df_5.plot()
# plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


# plt.figure(figsize=(5,5))
# x = np.arange(0,math.pi*2,0.05)
# y = np.sin(x)
# plt.plot(x,y)
# plt.xlabel('angle')
# plt.ylabel('sine')
# plt.title('sin curve')
# plt.grid(True)
# plt.figure(figsize=(5,5))
# np.random.seed(0)
# x1 = np.random.randn(100)
# y1 = np.random.randn(100)
# plt.scatter(x1,y1,s=50,c='r',marker='o',alpha=0.5)

# import matplotlib.pyplot as plt
# import numpy as np
#
# # Generate sample data
# x = np.linspace(0, 10, 100)
# y1 = np.sin(x)
# y2 = np.cos(x)
# y3 = np.tan(x)
# y4 = np.exp(x / 10)
#
# # Create a figure with a 2x2 grid of subplots
# plt.figure(figsize=(10, 10))
#
# # First subplot: Sine Function
# plt.subplot(2,2,1)
# plt.plot(x, y1, 'r-')
# plt.title('Sine Function')
#
# # Second subplot: Cosine Function
# plt.subplot(2, 2, 2)
# plt.plot(x, y2, 'g--')
# plt.title('Cosine Function')
#
# # Third subplot: Tangent Function
# plt.subplot(2, 2, 3)
# plt.plot(x, y3, 'b-')
# plt.title('Tangent Function')
#
# # Fourth subplot: Exponential Function
# plt.subplot(2, 2, 4)
# plt.plot(x, y4, 'm:')
# plt.title('Exponential Function')
#
# # Adjust layout to prevent overlap
# plt.tight_layout()
# plt.show()