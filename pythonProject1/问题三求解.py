import numpy as np
import pandas as pd
path1 = '销量数据预测处理汇总.xlsx'
path2 = r'问题2数据\分类_加_弹性系数.xlsx'
df1 = pd.read_excel(path1)
df2 = pd.read_excel(path2)
# 定义一个函数，用于合并行中的多个列
def combine_columns(row):
    return ' '.join(row.dropna().astype(str))

# 对数据框进行操作
df1['合并后的数据'] = df1.apply(lambda row: combine_columns(row[1:]), axis=1)

# 只保留需要的列
result_df = df1[['单品编码', '合并后的数据']]
print(df2)
merge_df = pd.merge(df1, df2[['单品编码','价格弹性系数','单品名称']],on='单品编码')
print(merge_df.head())
merge_df.to_excel('问题三最后数据.xlsx')