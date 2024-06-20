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
import random
player_set = []
card_set = []
num = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
for i in num:
    card_set.append(f"梅花{i}")
    card_set.append(f"红桃{i}")
    card_set.append(f"方片{i}")
    card_set.append(f"黑桃{i}")

a = int(input("玩家个数（<=17）："))
for i in range(0,a):
    player_card = random.sample(card_set,3)
    player_set.append(player_card)
    for j in player_card:
        card_set.remove(j)
while True:
    player = int(input("请输入想要查询的玩家序号"))
    if player > a :
        print("输入的玩家不存在，请重新输入：")
        continue
    print(f"玩家{player}的牌为：{player_set[player-1]}")
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
