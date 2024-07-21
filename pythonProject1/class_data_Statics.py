import pandas as pd
path1 = 'class _and_single.xlsx'
path2 = 'detail_single.xlsx'
path3 = 'detail_single_back.xlsx'
category_dict = {}
static_dict = {}
def get_message():
    # 读取第一个表格
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

        category_dict[category_name].append([product_code,[],[]])#第一个id，第二个日期，第三个销量
    for index, row in table1.iterrows():
        # print("index is",index,"row is",row)
        category_name = row['分类名称']
        product_code = row['单品编码']

        if category_name not in static_dict:
            static_dict[category_name] = []

        static_dict[category_name].append(product_code)#第一个id，第二个日期，第三个销量
    print(category_dict)
    print(static_dict)
def math_message():
    table1 = pd.read_excel(path3)
    for index, row in table1.iterrows():
        data = row['销售日期']
        quantify = row['销量(千克)']
        id_num = row['单品编码']
        for key,values in static_dict.items():
            if id_num in values:
                count = static_dict[key].index(id_num)
                category_dict[key][count][1].append(data)
                category_dict[key][count][2].append(quantify)
    print('category_dict is ',category_dict)

# 创建日期范围

get_message()
math_message()