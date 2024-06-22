import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Edge()
driver.get("https://i.njupt.edu.cn/cas/login?service=http%3A%2F%2Fi.njupt.edu.cn%2Fportal%2Fcas%2Fclient%2FvalidateLogin")
driver.find_element(By.NAME,"username").send_keys("Q23010229")
driver.find_element(By.ID,"password").send_keys("36645837!")
driver.find_element(By.XPATH,'//*[@id="loginForm"]/button').click()
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="layui-layer1"]/div[3]/a[2]').click()

input("请输入关闭来关闭浏览器：")