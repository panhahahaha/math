import pandas as pd
from tqdm import tqdm
path1 = 'class _and_single.xlsx'
match_id = []
match_id_1 = []

def get_match_id():
    table1 = pd.read_excel(path1)
    name_list = ["云南生菜", "上海青", "云南油麦菜", "奶白菜", "黄白菜(2)", "西兰花", "净藕(1)", "紫茄子(2)",
                 "青茄子(1)", "螺丝椒", "芜湖青椒(1)", "西峡香菇(1)"]

    for index, row in table1.iterrows():
        name = row["单品名称"]
        id_number = row["单品编码"]
        if name in name_list:
            match_id.append([id_number,name])
            match_id_1.append(id_number)
    print(len(match_id) == len(name_list))
    print(match_id)
get_match_id()


def get_data():
    sum_dict = [[match,name,[],[]]for match,name in match_id]
    goods_dict = [None, [], []]
    print("sum_dict is ",sum_dict)
    path2 = 'detail_single.xlsx'
    table2 = pd.read_excel(path2)
    for index, row in tqdm(table2.iterrows()):
        data = row["销售日期"]
        quantify = row["销量(千克)"]
        id_num = row["单品编码"]
        # print(data)
        if id_num in match_id_1:
            for item in sum_dict:
                if item[0] == id_num:
                    item[2].append(quantify)
                    item[3].append(data)
    print(sum_dict)
    flattened_data = []
    combined_data = []
    for entry in sum_dict:
        id = entry[0]
        name = entry[1]
        values = entry[2] if isinstance(entry[2], list) else [entry[2]]  # Check if values is a list or string
        timestamps = entry[3]
        combined_values = ", ".join(map(str, values))
        combined_timestamps = ", ".join(map(str, timestamps))
        combined_data.append([id, name, combined_values, combined_timestamps])

    # 创建 DataFrame
    df = pd.DataFrame(combined_data, columns=['ID', 'Name', 'Values', 'Timestamps'])

    # 保存为 Excel 文件并设置列宽
    with pd.ExcelWriter('output_combined.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        worksheet.set_column('C:C', 50)  # 设置Values列的宽度
        worksheet.set_column('D:D', 50)  # 设
get_data()