import pandas as pd

# # 创建示例数据框
# df1 = pd.DataFrame({
#     '单品编码': [1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
#     '单品名称': [str(item) for item in range(1, 19)],
# })
#
# df2 = pd.DataFrame({
#     '单品编码': [1, 2, 3, 5],
#     '成本': [3.5, 2.8, 4.1, 1.9]
# })
#
# df3 = pd.DataFrame({
#     '单品编码': [1, 2, 4, 5],
#     '销售量': [100, 150, 200, 130]
# })
# # df1.to_excel('-1-1-1.xlsx')
# merged_df_left = pd.merge(df1, df2, left_on = '单品编码',right_on='单品编码', how='left')
# print(merged_df_left)
# merged_df_inner = pd.merge(merged_df_left, df2, on='单品编码', how='inner')
# print(merged_df_inner)
path = '附件3.xlsx'
table = pd.read_excel(path)
df = pd.DataFrame(table)

# 将销售日期列转换为日期时间类型
df['日期'] = pd.to_datetime(df['日期'])

# 创建一个新的列表示每两个月的时间段
df['两个月期'] = (df['日期'].dt.year * 12 + df['日期'].dt.month - 1) // 2

# 按照每两个月分组并打印每组的内容
grouped = df.groupby('两个月期')
count = 1

for name, group in grouped:
    path_name = f'data\\附件_{count}.xlsx'
    print(f"两个月期: {name}")
    print(group)
    group.to_excel(path_name)
    count+=1
