import os

path = "D:/PyCharm Community Edition 2023.3/小爬爬/code"
folder_name = "AI"
folder_path = os.path.join(path,folder_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"{folder_path}已创建")
else:
    print(f"{folder_path}已存在")
