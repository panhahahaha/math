import random
import sys

import pandas as pd
path_elasticity = r'C:\Users\17264\Desktop\数学建模\pythonProject1\单品弹性系数.xlsx'
path_detail = r'C:\Users\17264\Desktop\数学建模\pythonProject1\附件2.xlsx'
list_class= ['水生根茎类','花叶类','花菜类','茄类','辣椒类','食用菌']
def f0():
    pd2 = pd.read_excel(path_elasticity)
    for item in range(1,19):
        path_cost = rf'C:\Users\17264\Desktop\数学建模\pythonProject1\data\数据分析\data_{item}.xlsx'
        ins_path = rf'C:\Users\17264\Desktop\数学建模\pythonProject1\data\实验\结合弹性系数data_{item}.xlsx'
        pd1 = pd.read_excel(path_cost)
        merge_table = pd.merge(pd1,pd2,on='单品编码')
        merge_table.to_excel(ins_path)
def calculate():
    def average(lst):
        return sum(lst)/len(lst)

    for item in range(1,19):
        ins_path = rf'C:\Users\17264\Desktop\数学建模\pythonProject1\data\实验\结合弹性系数data_{item}.xlsx'
        # print('-'*10)
        pd1 = pd.read_excel(ins_path)
        price_list = []
        quantify_list = []
        for index,item in enumerate(pd1['销售单价(元/千克)']):
            # print('item is',item)
            item = eval(item)
            price_list.append(average(item))
        for item in pd1['销量(千克)']:
            item = eval(item)
            quantify_list.append(average(item))
        pd1['平均销售价格'] = price_list
        pd1['平均销售量'] = quantify_list
        print(pd1)
        calculate2(pd1)
def calculate2(table):
    earnings_list = []
    for index, row in table.iterrows():
        base_price = row['平均销售价格']
        base_quantify = row['平均销售量']
        elasticity = row['价格弹性系数']
        the_best_price = (base_price*(elasticity-1))/(2*elasticity)
        provide = base_quantify*(1+elasticity*((the_best_price-base_price)/base_price))
        earnings = abs(the_best_price*provide)
        print(the_best_price,provide)
        earnings_list.append(earnings)
    print(earnings_list)
def merge():
    path1 = r'C:\Users\17264\Desktop\数学建模\pythonProject1\附件1.xlsx'
    elasticity = pd.read_excel(path_elasticity)
    table_class = pd.read_excel(path1)
    merge_class = pd.merge(elasticity, table_class,on='单品编码')
    # merge_class.to_excel(r'C:\Users\17264\Desktop\数学建模\pythonProject1\问题2数据\分类_加_弹性系数.xlsx',index=False)
    table = pd.read_excel(path_detail)
    merge_class['平均销量'] = 0
    merge_class['平均定价'] = 0
    id_num = merge_class['单品编码'].values
    for num in id_num:
        table[table['单品编码']==num].agg({})
def f1():
    def average(lst):
        return sum(lst)/len(lst)
    # path = r'C:\Users\17264\Desktop\数学建模\pythonProject1\优化后成本与销量.xlsx'
    # df = pd.read_excel(path)
    # aggre = df.groupby(['单品编码']).agg({'销售单价(元/千克)':'mean','销量(千克)':"mean"}).reset_index()
    # ins = r'C:\Users\17264\Desktop\数学建模\pythonProject1\优化后成本与销量(更加精细的).xlsx'
    # aggre.to_excel(ins)
    ins = r'C:\Users\17264\Desktop\数学建模\pythonProject1\优化后成本与销量(更加精细的).xlsx'
    path = r'C:\Users\17264\Desktop\数学建模\pythonProject1\问题2数据\分类_加_弹性系数.xlsx'
    ins_path = r'C:\Users\17264\Desktop\数学建模\pythonProject1\问题2数据\分类_加_弹性系数_加平均成本与销量.xlsx'
    # df = pd.read_excel(ins)
    # df1 = pd.read_excel(path)
    # merge_data = pd.merge(df, df1,on='单品编码')
    # merge_data.to_excel(ins_path)
    df2 = pd.read_excel(ins_path)

    for item in list_class:
        goods_path = rf'C:\Users\17264\Desktop\数学建模\pythonProject1\问题2数据\{item}.xlsx'
        # class_goods = df2[df2['分类名称']==item]
        # class_goods.to_excel(goods_path)
        df3 = pd.read_excel(goods_path)

        class_dict = {'天数':[],'最大收益':[],'最佳订货量':[],'最佳价格':[]}
        for i in range(1,8):
            earnings_list = []
            price_list = []
            quanity_list = []
            for index, row in df3.iterrows():
                base_price = row['平均销售单价(元/千克)']
                base_quantify = row['平均销量(千克)']
                elasticity = row['价格弹性系数']
                base_price *=random.randint(1,2)
                base_quantify *=random.randint(1,2)
                elasticity *=random.randint(1,2)
                the_best_price = (base_price * (elasticity - 1)) / (2 * elasticity)
                provide = base_quantify * (1 + elasticity * ((the_best_price - base_price) / base_price))
                earnings = abs(the_best_price * provide)
                price_list.append(the_best_price)
                quanity_list.append(provide)
                earnings_list.append(earnings)
                print(the_best_price, provide)
            class_dict['最大收益'].append(abs(average(earnings_list)))
            class_dict['最佳订货量'].append(abs(average(quanity_list)))
            class_dict['最佳价格'].append(abs(average(price_list)))
            class_dict['天数'].append(i)
            dp = pd.DataFrame(class_dict)
            dp.to_excel(f'{item}.xlsx')
        print(class_dict)
f1()

# merge()
def c_average():
    pass




