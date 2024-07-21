import os
import pandas as pd
base_path = r'C:\Users\17264\Desktop\数学建模\pythonProject1'
path1 = os.path.join(base_path, '附件1.xlsx')
path2 = os.path.join(base_path, '附件2.xlsx')
path3 = os.path.join(base_path, '附件3.xlsx')
path4= os.path.join(base_path, '附件4.xlsx')
group_name = set(pd.read_excel(path1)['分类名称'].values)
