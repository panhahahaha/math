import pandas as pd
def get_goods_id():
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