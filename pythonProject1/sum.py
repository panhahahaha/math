import pandas as pd
from base import get_number
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
path = "new_output.xlsx"
sum_dict_0 = pd.read_excel(path)
sum_dict = {}
save_dict = get_number()
for index, row in sum_dict_0.iterrows():
    id_0 = row["Key"]
    value = row["Value"]
    sum_dict[id_0] = value
print("sum_dict is", sum_dict)
table1 = pd.read_excel(path)
# id_num = set(table1["单品编码"])
# sum_dict = {key: 0 for key in id_num}


# print(id_num)
# for index, row in table1.iterrows():
#     price = row['销售单价(元/千克)']
#     goods = row['单品编码']
#     if goods in sum_dict:
#         sum_dict[goods] += price
# print(sum_dict)
# df = pd.DataFrame(list(sum_dict.items()), columns=['Key', 'Value'])
# df.to_excel('new_output.xlsx', index=False)
# class DRAW:
#     def __init__(self):
#         self.
def draw(data,cls,number_key):
    keys = list(data.keys())
    values = list(data.values())
    # 创建柱状图
    plt.figure(figsize=(12, 8))  # 设置图形大小
    # plt.bar(keys, values, color='blue')
    plt.bar(range(len(keys)),values, width=0.5, color='blue')  # 使用指定的宽度
    plt.xticks(ticks=range(len(keys)),labels=number_key)
    plt.tight_layout()  # 调整布局以避免标签重叠
    # 添加标题和标签
    plt.title(cls,fontsize=20)
    plt.xlabel('Keys')
    plt.ylabel('Values')

    # 显示图形
    plt.show()


# for cls, i in save_dict.items():
#     new_dict = {}
#     number_key=[]
#     num = 0
#     for (key, items) in sum_dict.items():
#         key = int(key)
#         if key in i:
#             id_num = str(key)
#             number_key.append(id_num[-1])
#             num += 1
#             new_dict[num] = sum_dict[key]
#     print("new dict is", new_dict)
#     print("len",len(number_key),len(new_dict.keys()))
#     draw(new_dict,cls,number_key)
new_dict = {}
for cls, i in save_dict.items():
    print("cls is ",cls)
    new_dict[cls] = {}
    number_key=[]
    num = 0
    for (key, items) in sum_dict.items():
        key = int(key)
        if key in i:
            id_num = str(key)
            number_key.append(id_num[-1])
            num += 1
            new_dict[cls][key] = sum_dict[key]
    # print("new dict is", new_dict)
    print("len",len(number_key),len(new_dict.keys()))
    # draw(new_dict,cls,number_key)
print("new_dict is ",new_dict)

# 将字典转换为DataFrame
data_list = [
    (category, id_, value)
    for category, id_values in new_dict.items()
    for id_, value in id_values.items()
]

# 重命名列
print(data_list)
df = pd.DataFrame(data_list, columns=['Category', 'ID', 'Value'])

# 输出DataFrame
print(df)

# 将DataFrame保存为Excel文件
df.to_excel('data.xlsx', index=False)
# 将DataFrame保存为CSV文件（可选）
# 输出DataFrame
# import unittest
# class A(unittest.TestCase):
#     def test_sum(self):
#         draw({2:3,4:5})
# df = pd.DataFrame(list(new_dict.items()), columns=['name','id'])

import pandas as pd

# Data provided by the user
