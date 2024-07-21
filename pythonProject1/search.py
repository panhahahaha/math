import pandas as pd
path = '附件2.xlsx'
static_dict = {}
def get_id():
    table1_path = 'class _and_single.xlsx'
    table1 = pd.read_excel(table1_path)
    for index, row in table1.iterrows():
        # print("index is",index,"row is",row)
        category_name = row['分类名称']
        product_code = row['单品编码']

        if category_name not in static_dict:
            static_dict[category_name] = []

        static_dict[category_name].append(product_code)#第一个id，第二个日期，第三个销量
def search():
    dis_count_table = []
    table1 = pd.read_excel(path)
    for index, row in table1.iterrows():
        discount = row['是否打折销售']
        id_num = row['单品编码']
        quantify = row['销量(千克)']
        price = row['销售单价(元/千克)']
        data = row['销售日期']
        if discount == '是':
            dis_count_table.append([id_num, quantify, price,data])
    dp = pd.DataFrame(dis_count_table, columns=['单品编码','销量(千克)','销售单价(元/千克)','销售日期'])
    dp.to_excel('打折蔬菜详细信息.xlsx')
# search()