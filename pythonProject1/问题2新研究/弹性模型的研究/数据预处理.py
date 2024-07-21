import os
import pandas as pd
base_path = r'C:\Users\17264\Desktop\数学建模\pythonProject1'
path1 = os.path.join(base_path, '附件1.xlsx')
path2 = os.path.join(base_path, '附件2.xlsx')
path3 = os.path.join(base_path, '附件3.xlsx')
path4= os.path.join(base_path, '附件4.xlsx')
path5 = os.path.join(base_path, r'\问题2数据\分类_加_弹性系数_加平均成本与销量.xlsx')
def merge():
    t1 = pd.read_excel(r'C:\Users\17264\Desktop\数学建模\pythonProject1\问题2数据\分类_加_弹性系数_加平均成本与销量.xlsx')
    new_path = os.path.join(base_path,r'问题2新研究\弹性模型的研究\品类弹性系数.xlsx')
    group = t1.groupby(['分类名称']).agg({'价格弹性系数':'mean','平均销售单价(元/千克)':'mean','平均销量(千克)':'mean'}).reset_index()
    group.to_excel(new_path, index=False)
merge()