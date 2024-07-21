import basic_method
import tqdm
path1 = "成本一周.xlsx"  ###成本
path2 = ''  ###销量，销售单价
path3 = '附件4.xlsx'  ###损耗率
has_table = basic_method.get_goods_id()

import pandas as pd

# df1 = pd.read_excel(path1, sheet_name='Sheet1')
# df2 = pd.read_excel(path2, sheet_name='Sheet1')
# df3 = pd.read_excel(path3, sheet_name='Sheet1')
# print('df1 is \n', df1, '\n' * 3)
# print('df2 is \n', df2, '\n' * 3)
# print('df3 is \n', df3, '\n' * 3)


def correct(file_path_1,file_path_2,file_path_3):
    df1 = pd.read_excel(file_path_1, sheet_name='Sheet1')
    df2 = pd.read_excel(file_path_2, sheet_name='Sheet1')
    df3 = pd.read_excel(file_path_3, sheet_name='Sheet1')
    number = 1
    for index,row in df2.iterrows():
        a = row['销量(千克)']
        b = row['销售单价(元/千克)']
        number += a*b
    number = df2['']
    print('df1 is \n', df1, '\n' * 3)
    print('df2 is \n', df2, '\n' * 3)
    print('df3 is \n', df3, '\n' * 3)
    # 对 df1 和 df2 进行聚合处理
    df1_agg = df1.groupby('单品编码').agg({
        '日期': 'first',
        '批发价格(元/千克)': 'mean'
    }).reset_index()

    df2_agg = df2.groupby('单品编码').agg({
        '销售日期': 'first',
        '销量(千克)': 'sum',
        '销售单价(元/千克)': 'mean'
    }).reset_index()

    # 打印数据框以确认是否正确
    print(df1_agg)
    print(df2_agg)
    print(df3)

    # 合并数据框
    merged_df1 = pd.merge(df1_agg, df2_agg, on='单品编码', how='left')
    print(merged_df1)

    final_merged_df = pd.merge(merged_df1, df3, on='单品编码', how='left')
    print(final_merged_df)
    count = 1
    for index, row in final_merged_df.iterrows():
        sell_num = row['销量(千克)']
        chengben = row['批发价格(元/千克)']
        sunhao = row['损耗率(%)']
        if sell_num > 0:
            count += (sell_num / (1 - (sunhao / 100))) * chengben
    # final_merged_df.to_excel('正确损耗表.xlsx', index=False)
    # 打印合并后的数据框
    # print(final_merged_df[['单品编码', '单品名称', '损耗率(%)', '销售量', '成本']])
    print(count)
    return (count,number)

# correct()


# def incorrect():
#     merged_df1 = pd.merge(df3, df2, on='单品编码', how='left')
#     print(merged_df1)
#
#     final_merged_df = pd.merge(merged_df1, df2, on='单品编码', how='left')
#     print(final_merged_df)
#     count = 1
#     for index, row in final_merged_df.iterrows():
#         sell_num = row['销售量']
#         chengben = row['成本']
#         sunhao = row['损耗率(%)']
#         if sell_num > 0:
#             count += (sell_num / (1 - (sunhao / 100))) * chengben
#     # final_merged_df.to_excel('损耗表.xlsx', index=False)
#     # 打印合并后的数据框
#     print(final_merged_df[['单品编码', '单品名称', '损耗率(%)', '销售量', '成本']])
#     print(count)
#
#
# incorrect()
def called():
    l = []
    for item in tqdm.tqdm(range(1,18)):

        file_path_1 = f'data\\附件_{item}.xlsx'
        file_path_2 = f'data\\data_{item}.xlsx'
        file_path_3 = f'附件4.xlsx'
        l.append(correct(file_path_1,file_path_2,file_path_3))
    print(l)
called()