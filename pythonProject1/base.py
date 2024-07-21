import copy

import pandas as pd


def main():
    # 读取第一个表格
    table1_path = 'class _and_single.xlsx'
    table1 = pd.read_excel(table1_path)
    category_dict = {}
    modify_dict = {}
    # 遍历每一行，填充字典
    for index, row in table1.iterrows():
        # print("index is",index,"row is",row)
        category_name = row['分类名称']
        product_code = row['单品编码']

        if category_name not in category_dict:
            category_dict[category_name] = []

        category_dict[category_name].append(product_code)
    for index, row in table1.iterrows():
        # print("index is",index,"row is",row)
        category_name = row['分类名称']
        product_code = row['单品编码']

        if category_name not in modify_dict:
            modify_dict[category_name] = []

        modify_dict[category_name].append({"product_code": product_code, "sales": 0, "data": []})

    # 假设编号列名为 'ID'
    id_list = table1['单品编码'].tolist()
    table2_path = 'detail_single_back.xlsx'
    chunksize = 10000  # 每次读取10000行
    print(modify_dict)
    print(category_dict)
    # 初始化一个空的数据框来存储处理后的数据
    filtered_data = pd.DataFrame()
    table2 = pd.read_excel(table2_path)
    for index, row in table2.iterrows():
        # print("index is",index,"row is",row)
        data_message = row["销售日期"]
        id_message = row["单品编码"]
        price = row["销售单价(元/千克)"]
        quantify = row["销量(千克)"]
        # print(data_message,id_message)
        print(data_message, id_message)
        for i in category_dict:
            if id_message in category_dict[i]:
                num = category_dict[i].index(id_message)
                modify_dict[i]["sales"] = quantify
    print(modify_dict)
    # 读取第二个表格
    # print(table2['单品编码'])
    # 根据编号查找对应的数据
    # 假设第二个表格中编号列名也为 'ID'
    matching_data = table2['单品编码'].isin(id_list)

    # 显示结果
    # print(matching_data)

    rows = []

    # 遍历字典，将数据展平
    for category, items in modify_dict.items():
        for item in items:
            row = {'类别': category, 'ID': str(item[0])}
            # 如果有时间戳，则添加到行中
            if len(item) > 1:
                row['时间戳'] = ', '.join(str(ts) for ts in item[1:])
            else:
                row['时间戳'] = None
            rows.append(row)

    # 将行数据转换为DataFrame
    df = pd.DataFrame(rows)

    # 将DataFrame写入Excel文件
    df.to_excel('data_message.xlsx', index=False)


def get_number():
    table1_path = 'class _and_single.xlsx'
    table1 = pd.read_excel(table1_path)
    category_dict = {}
    modify_dict = {}
    # 遍历每一行，填充字典
    for index, row in table1.iterrows():
        # print("index is",index,"row is",row)
        category_name = row['分类名称']
        product_code = row['单品编码']
        if category_name not in category_dict:
            category_dict[category_name] = []

        category_dict[category_name].append(product_code)

    return category_dict


print(get_number())
if __name__ == '__main__':
    main()
