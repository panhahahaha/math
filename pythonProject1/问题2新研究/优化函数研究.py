import numpy as np
import pandas as pd
from scipy.optimize import minimize
from constant import *
import matplotlib.pyplot as plt
daily_forecast_sales = {}
# 假设的价格弹性系数和初始价格
price_elasticity = {'水生根茎类': -1.2, '茄类': -1.0, '辣椒类': -1.5, '食用菌': -0.8, '花菜类': -1.3, '花叶类': -0.9}
initial_prices = {'水生根茎类': 12, '茄类': 10, '辣椒类': 9, '食用菌': 8, '花菜类': 7, '花叶类': 6}
wholesale_prices = {'水生根茎类': 10, '茄类': 8, '辣椒类': 7, '食用菌': 6, '花菜类': 5, '花叶类': 4}
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
for item in group_name:

    path = rf'C:\Users\17264\Desktop\数学建模\pythonProject1\问题2新研究\数据\{item}预测结果.xlsx'
    t1 = pd.read_excel(path, engine='openpyxl')
    print(t1)
    daily_forecast_sales[item] = np.array(t1['predicted_mean'])
# 未来一周每天的预测销量

print(group_name)

categories = list(price_elasticity.keys())


# 定义单个品类的利润计算函数
def single_category_profit(price, category):
    P = price
    P0 = initial_prices[category]
    Q0_list = daily_forecast_sales[category]
    epsilon = price_elasticity[category]
    total_profit = 0
    for Q0 in Q0_list:
        Q = Q0 * (1 + epsilon * (P - P0) / P0)
        cost = wholesale_prices[category]
        total_profit += (P - cost) * Q
    return -total_profit  # 由于最小化问题，返回负值


# 保存结果的列表
results = []

# 优化每个品类的价格
for category in categories:
    initial_price = initial_prices[category]
    bounds = [(wholesale_prices[category] * 1.1, wholesale_prices[category] * 1.5)]

    result = minimize(single_category_profit, [initial_price], args=(category,), bounds=bounds)
    optimized_price = result.x[0]
    max_profit = -single_category_profit(optimized_price, category)

    results.append({
        '品类': category,
        '预测销量(千克)': daily_forecast_sales[category],
        '初始价格(元)': initial_price,
        '优化价格(元)': optimized_price,
        '最大收益(元)': max_profit
    })

# 转换结果为 DataFrame，并展平预测销量
results_df = pd.DataFrame(results)
results_df = results_df.explode('预测销量(千克)')

# 输出结果
print(results_df)

# 保存结果
results_df.to_excel('每个蔬菜商超的最大获利.xlsx', index=False)

# 绘制结果图表
fig, ax1 = plt.subplots(figsize=(12, 8))

# 设置柱状图的宽度
bar_width = 0.35

# 设置每个类别的位置
index = np.arange(len(categories))

# 绘制初始价格和优化价格的柱状图
bars1 = ax1.bar(index, results_df['初始价格(元)'].unique(), bar_width, label='初始价格')
bars2 = ax1.bar(index + bar_width, results_df['优化价格(元)'].unique(), bar_width, label='优化价格')

# 设置图表的标题和标签
ax1.set_xlabel('品类')
ax1.set_ylabel('价格 (元)')
ax1.set_title('每个品类的初始价格和优化价格')
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels(categories)
ax1.legend()

# 创建第二个 y 轴来绘制最大收益
ax2 = ax1.twinx()
ax2.set_ylabel('最大收益 (元)')
bars3 = ax2.plot(index + bar_width / 2, results_df['最大收益(元)'].unique(), label='最大收益', color='r', marker='o')

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left')

# 保存图表
# plt.savefig('/mnt/data/price_optimization_results.png')
plt.show()