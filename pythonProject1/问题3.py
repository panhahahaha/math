import pandas as pd

path1 = '附件2.xlsx'
path2 = '附件3.xlsx'


def search():
    df = pd.read_excel(path1)
    df1 = pd.read_excel(path2)
    start_date = '2023-6-24'
    end_date = '2023-6-30'
    cost_df = df1[(df1['销售日期'] >= start_date) & (df1['销售日期'] <= end_date)]

    filtered_df = df[(df['销售日期'] >= start_date) & (df['销售日期'] <= end_date)]
    agg_df = filtered_df.groupby('单品编码', as_index=False).agg({
        '销量(千克)': 'sum',
        '销售单价(元/千克)': 'mean'
    })
    print(agg_df)
    # 过滤掉销量低于 2.5 的记录
    filtered_agg_df = agg_df[agg_df['销量(千克)'] >= 2.5]
    filtered_agg_df.to_excel('问题3.xlsx', index=False)
    # print(filtered_agg_df)
    # # 合并原始数据和过滤后的聚合数据，保留其它列
    # merged_df = pd.merge(filtered_df.drop(columns='销量(千克)'), filtered_agg_df, on='单品编码', how='inner')
    #
    #
    # # 保存结果到新的 Excel 文件
    # output_file_path = '问题3.xlsx'
    # merged_df.to_excel(output_file_path, index=False)
    #
    # print("处理完成，结果已保存到:", output_file_path)
    #
    # # 保存结果到新的 Excel 文件
    # # output_file_path = '/mnt/data/aggregated_data.xlsx'
    # # final_df.to_excel(output_file_path, index=False)
    #
    # # print("处理完成，结果已保存到:", output_file_path)
    # print(final_df)


# search()


def merge():
    new_path = '问题3.xlsx'
    df1 = pd.read_excel(path2)
    df2 = pd.read_excel(new_path)
    start_date = '2023-6-24'
    end_date = '2023-6-30'
    cost_df = df1[(df1['销售日期'] >= start_date) & (df1['销售日期'] <= end_date)]
    print('cost_df is', cost_df)
    print('df2 is ', df2)
    merge_table = pd.merge(cost_df, df2, left_on=['单品编码'], right_on=['单品编码'])
    grou = merge_table.groupby('单品编码').agg({'批发价格(元/千克)': 'mean'})
    grou = pd.merge(grou,df2,on='单品编码')
    grou.to_excel(r'test_file\cost.xlsx')
    print(merge_table)
# merge()
def a():
    df = pd.read_excel(path1)
    start_date = '2023-6-24'
    end_date = '2023-6-30'
    cost_df = df[(df['销售日期'] >= start_date) & (df['销售日期'] <= end_date)]
    dict_a = {}
    new_path = r'test_file\cost.xlsx'
    df1 = pd.read_excel(new_path)
    for index, row in df1.iterrows():
        a1 = row['批发价格(元/千克)']
        a2 = row['销量(千克)']
        a3 = row['销售单价(元/千克)']
        a4 = row['单品编码']
        b = a3*a2-a2*a1
        dict_a[a4] = b
    sorted_dict = dict(sorted(dict_a.items(), key=lambda item: item[1], reverse=True))
    list_number = []

    print("按值降序排序后的字典:")
    for k, v in sorted_dict.items():
        list_number.append(int(k))
        print(f"{k}: {v}")
    print(list_number)
    list_number = list_number[0:30]
    # for i in list_number:
    #     result = cost_df[cost_df['单品编码']==i]
    #     print('result is',result)
    #     result.to_excel(r'问题三文件\商品：{}.xlsx'.format(i))
    for item in list_number:
        path = rf'问题三文件\商品：{item}.xlsx'
        df = pd.read_excel(path)
        result = df.groupby('销售日期').agg({'销量(千克)': 'sum', '销售单价(元/千克)': 'mean'}).reset_index()
        path3 = rf'问题三备份\{item}.xlsx'
        result.to_excel(path3)
a()
# merge()
