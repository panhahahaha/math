import pandas as pd

path = r'data\data_1.xlsx'
table = pd.read_excel(path)
print(table['销量(千克)'] * table['销售单价(元/千克)'].values)
t1 = pd.DataFrame(
    {'sno': [11, 11, 12, 12, 12],
     '爱好': ['篮球', '羽毛球', '乒乓球', '篮球', '足球']}
)
t2 = pd.DataFrame(
    {'sno': [11, 11,11, 12, 12, 13],
     'grade': ['语文88', '数学90', '英语75', '语文66', '数学55', '英语29']}
)
t3 = pd.merge(t1, t2, on='sno')
print(t3)
