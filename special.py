## 爬虫练习

#底层逻辑（不建议使用，效率太低）
# from urllib.request import urlopen
#
# url = "https://cn.bing.com/search?q=%E8%8A%92%E6%9E%9C&gs_lcrp=EgZjaHJvbWUqBwgCEEUYwgMyBwgAEEUYwgMyBwgBEEUYwgMyBwgCEEUYwgMyBwgDEEUYwgMyBwgEEEUYwgMyBwgFEEUYwgMyBwgGEEUYwgMyBwgHEEUYwgPSAQsxOTk5NDQ2ajBqMagCCLACAQ&FORM=ANNTA1&adppc=EdgeStart&PC=LCTS"
# respon = urlopen(url)
# result = respon.read()
# print(result.decode("utf-8"))
# import requests
# import lxml
# import requests
# url = 'https://fanyi.baidu.com/sug'
# data={
# 'kw': 'test'
# }
# respon =requests.post(url,data=data)
# import json
# dic = json.loads(respon)
# dic = respon.json()
# print(dic)
import re

obj = re.compile(r"r(?P<id>\d+)g")
result = obj.finditer("adi9qwijf797wqfger541gerqreh7887qhbufw8g4g8")
for num in result:
    print(num.group("id"))

