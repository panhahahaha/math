import pandas as pd

new_dict = {}


def match():
    df = pd.read_excel('1111.xlsx')

    category_dict = {}
    table1_path = 'class _and_single.xlsx'
    table1 = pd.read_excel(table1_path)

    modify_dict = {}
    # 遍历每一行，填充字典

    for index, row in table1.iterrows():
        # print("index is",index,"row is",row)
        category_name = row['分类名称']
        product_code = row['单品编码']

        if category_name not in category_dict:
            category_dict[category_name] = []
        category_dict[category_name].append(product_code)
    mapping_list = []
    print(category_dict)
    # 遍历category_mapping字典，创建单品编码到大类的映射
    for category, ids in category_dict.items():
        for single_id in ids:
            mapping_list.append({'单品编码': single_id, '大类': category})
    print('mapping_list is', mapping_list)

    # 将映射关系转换为DataFrame
    mapping_df = pd.DataFrame(mapping_list)

    # 合并原始数据和mapping_df
    merged_df = pd.merge(df, mapping_df, on='单品编码', how='left')

    # 按大类和销售日期分组，并求和
    grouped_df = merged_df.groupby(['销售日期', '大类'])['销量(千克)'].sum().reset_index()

    # 计算总日均销售量
    average_sales_per_day = grouped_df.groupby('大类')['销量(千克)'].mean().reset_index()
    average_sales_per_day.columns = ['大类', '日均销量(千克)']

    print(average_sales_per_day)
    output_path = '000.xlsx'  # 输出文件路径
    grouped_df.to_excel(output_path, index=False)


# match()
# # 读取Excel文件
# file_path = 'detail_single_back.xlsx'  # 替换为你的Excel文件路径
# df = pd.read_excel(file_path)
#
# # 将 '销售日期' 转换为日期时间类型（如果尚未转换）
# df['销售日期'] = pd.to_datetime(df['销售日期'])
#
# # 按 '销售日期' 和 '单品编码' 分组，并汇总 '销量(千克)'
# grouped_df = df.groupby(['销售日期', '单品编码'])['销量(千克)'].sum().reset_index()
# for i in grouped_df:
#     print(i)
# print(grouped_df)
# # 将汇总数据保存到新的Excel文件
# output_path = '.xlsx'  # 输出文件路径
# # grouped_df.to_excel(output_path, index=False)
#
# print(f"汇总后的销售数据已保存到 {output_path}")


# 读取Excel文件
file_path = '000.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 重新构建表格
pivot_table = df.pivot_table(index='销售日期', columns='大类', values='销量(千克)', aggfunc='sum').reset_index()
# index='销售日期':
# 透视表按“销售日期”分组。每个不同的日期将作为透视表的行索引。
# columns='大类':
# “大类”列的唯一值将作为透视表的列标题。
# values='销量(千克)':
# “销量(千克)”列中的值将用于聚合操作。
# aggfunc='sum':
# 聚合函数为求和，即将相同“销售日期”和“大类”的销量进行求和。
# fill_value=0:
# 将缺失值填充为0。
# 保存处理后的数据到新的Excel文件
output_file_path = '222.xlsx'  # 替换为你希望保存的Excel文件路径
pivot_table.to_excel(output_file_path, index=False)
