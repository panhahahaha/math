import random

from constant import*
import numpy as np
from scipy.optimize import minimize
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from constant import *
# 设置字体为 SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
forecast_sales = {}
# 假设我们已经有了以下数据
categories = []
wholesale_price = {}
loss_rate = {}
price_elasticity = {}
min_display_qty = 2.5
path_1 = '弹性系数和损耗率.xlsx'
initial_prices = {}
t1 = pd.read_excel(path_1)
for index,row in t1.iterrows():
    elasticity = abs(row['价格弹性系数'])
    loss = abs(row['平均损耗率(%)_小分类编码_不同值']/100)
    name = row['小分类名称']
    loss_rate[name] = loss
    price_elasticity[name] = elasticity
# 初始定价策略和补货量

for item in group_name:
    initial_prices[item] = random.randint(7,13)
    categories.append(item)
    wholesale_price[item] = random.randint(5,10)
    path = rf'C:\Users\17264\Desktop\数学建模\pythonProject1\问题2新研究\数据\{item}预测结果.xlsx'
    t1 = pd.read_excel(path, engine='openpyxl')
    print(t1)
    forecast_sales[item] = np.array(t1['predicted_mean'])
print('forecast_sales is ',forecast_sales)

# print(t1)

replenishment_plan = {category: forecast_sales[category].mean() * (1 + loss_rate[category]) for category in categories}

# 记录优化过程的列表
iter_prices = []
iter_values = []

# 目标函数
# def total_profit(prices):
#     total = 0
#     for category in categories:
#         P = prices[categories.index(category)]
#         P0 = initial_prices[category]
#         Q0 = forecast_sales[category].mean()
#         epsilon = price_elasticity[category]
#         Q = Q0 * (1 + epsilon * (P - P0) / P0)
#         cost = wholesale_price[category] * (1 + loss_rate[category])
#         total += (P - cost) * Q
#     return -total  # 由于最小化问题，返回负值
def total_profit(prices):
    total = 0
    for category in categories:
        P = prices[categories.index(category)]
        P0 = initial_prices[category]
        for item in forecast_sales[category]:
            Q0 = forecast_sales[category][1]
            epsilon = price_elasticity[category]
            Q = item * (1 + epsilon * (P - P0) / P0)
            cost = wholesale_price[category] * (1 + loss_rate[category])
            total += (P - cost) * Q
            return -total  # 由于最小化问题，返回负值
# 回调函数
def callback(xk):
    iter_prices.append(xk)
    iter_values.append(total_profit(xk))

# 约束条件
constraints = [{'type': 'ineq', 'fun': lambda prices: prices[categories.index(category)] - wholesale_price[category] * 1.1} for category in categories] + \
              [{'type': 'ineq', 'fun': lambda prices: wholesale_price[category] * 1.5 - prices[categories.index(category)]} for category in categories]

# 优化
result = minimize(total_profit,
                  list(initial_prices.values()),
                  constraints=constraints,
                  bounds=[(wholesale_price[category] * 1.1, wholesale_price[category] * 1.5) for category in categories],
                  callback=callback,method='BFGS')

# 优化后的价格
optimized_prices = result.x

# 输出优化结果
for category, price in zip(categories, optimized_prices):
    print(f"{category} 的优化价格: {price:.2f}")

# 生成最终的补货和定价策略
final_strategy = pd.DataFrame({
    '品类': categories,
    '补货量': [replenishment_plan[category] for category in categories],
    '优化价格': optimized_prices
})

print(final_strategy)

# 可视化优化过程
iter_values = [-v for v in iter_values]  # 将负值转换为正值以显示实际利润
plt.figure(figsize=(12, 6))
plt.plot(iter_values, marker='o')
plt.title('Optimization Process')
plt.xlabel('Iteration')
plt.ylabel('Total Profit')
plt.grid(True)
plt.show()

# 变量变化情况
iter_prices = np.array(iter_prices)
plt.figure(figsize=(12, 6))
for i, category in enumerate(categories):
    plt.plot(iter_prices[:, i], label=category, marker='o')
plt.title('Price Changes During Optimization')
plt.xlabel('Iteration')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
