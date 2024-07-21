from constant import*
import pandas as pd
import os
import tqdm
def merge():
    new_path = os.path.join(base_path,r'问题2新研究\附件2优化数据.xlsx')
    new_path1 = os.path.join(base_path,r'问题2新研究\附件3优化数据.xlsx')
    t6 = pd.read_excel(path3)
    group = t6.groupby(['销售日期','单品编码']).agg({'批发价格(元/千克)':'mean'})
    group.to_excel(new_path1)
    table1 = pd.read_excel(path2)
    grouped_table = table1.groupby(["销售日期", "单品编码"]).agg(
        {'销量(千克)': 'mean', '销售单价(元/千克)': 'mean'}).reset_index()

    grouped_table.to_excel(new_path, index=False)
    table= pd.read_excel(new_path)

    t2 = pd.read_excel(path3)
    group2 = t2.groupby(['单品编码','销售日期']).agg({'批发价格(元/千克)':'mean'}).reset_index()
    group2.to_excel(new_path)
    t3 = pd.read_excel(path1)
    ls = set(t3['分类名称'].values)
    group4 = t3.groupby('分类名称')
    for category, group in group4:
        category_str = str(category).strip("(),'\"")
        # 创建导出路径
        export_path = os.path.join(base_path, f'问题2新研究\分类_{category_str}.xlsx')
        # 保存分组数据到Excel文件
        group.to_excel(export_path, index=False)
    for item in tqdm.tqdm(ls):
        print(item)
        # print(item)
        path6 = f'分类_{item}.xlsx'
        # 读取第一个文件
        df1 = pd.read_excel(path6)

        # 读取第二个文件
        df2 = pd.read_excel(new_path)

        # 合并两个表格
        merged_df = pd.merge(df1, df2, on='单品编码', how='inner')

        # 选择需要的列
        result_df = merged_df[
            ['单品编码', '单品名称', '分类编码', '分类名称', '销售日期', '销量(千克)', '销售单价(元/千克)']]

        # 保存结果到新的Excel文件
        # print(result_df)
        output_path = os.path.join(base_path, f'合并{item}.xlsx')
        result_df.to_excel(output_path, index=False)
    for item in tqdm.tqdm(ls):
        path7 = rf'合并{item}.xlsx'
        t8 = pd.read_excel(path7)
        new_path7 = f'整合各单品{item}.xlsx'
        agg = t8.groupby('销售日期').agg({'销量(千克)':'mean','销售单价(元/千克)':'mean'})
        agg.to_excel(new_path7)
    path7 = '价格弹性系数.xlsx'
    t7 = pd.read_excel(path7)
    agg_t7 = t7.groupby('分类名称').agg({'价格弹性系数':'mean'}).reset_index()
    t9 = pd.read_excel('附件4.xlsx')
    merge_t9 = pd.merge(agg_t7,t9,left_on ='分类名称',right_on='小分类名称')
    merge_t9.to_excel('弹性系数和损耗率.xlsx')
    print(merge_t9)
    # print(t8.head(),'\n',t9)
    # merge_78 = pd.merge(t8,t9,on='单品编码')
    # merge_78.to_excel('损耗率与类.xlsx')
merge()
# a = pd.read_excel('附件4.xlsx')
# print(a)