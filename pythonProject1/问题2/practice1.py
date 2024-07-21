# import numpy as np
# from scipy.optimize import minimize
import pandas as pd
#
# # 假设我们已经有了以下数据
# categories = ['蔬菜1', '蔬菜2', '蔬菜3', '蔬菜4', '蔬菜5', '蔬菜6']
# forecast_sales = {'蔬菜1': np.array([20, 22, 21, 23, 25, 24, 26]),
#                   '蔬菜2': np.array([30, 31, 29, 28, 30, 32, 31]),
#                   '蔬菜3': np.array([15, 14, 16, 17, 18, 16, 19]),
#                   '蔬菜4': np.array([10, 11, 10, 12, 13, 12, 14]),
#                   '蔬菜5': np.array([5, 6, 5, 7, 6, 7, 8]),
#                   '蔬菜6': np.array([8, 9, 7, 8, 9, 10, 11])}
# wholesale_price = {'蔬菜1': 10, '蔬菜2': 8, '蔬菜3': 7, '蔬菜4': 6, '蔬菜5': 5, '蔬菜6': 4}
# loss_rate = {'蔬菜1': 0.05, '蔬菜2': 0.04, '蔬菜3': 0.03, '蔬菜4': 0.02, '蔬菜5': 0.01, '蔬菜6': 0.05}
# min_display_qty = 2.5
#
# # 初始定价策略和补货量
# initial_prices = {'蔬菜1': 12, '蔬菜2': 10, '蔬菜3': 9, '蔬菜4': 8, '蔬菜5': 7, '蔬菜6': 6}
# replenishment_plan = {category: forecast_sales[category].mean() * (1 + loss_rate[category]) for category in categories}
#
# # 目标函数
# def total_profit(prices):
#     total = 0
#     for category in categories:
#         price = prices[categories.index(category)]
#         cost = wholesale_price[category] * (1 + loss_rate[category])
#         sales = forecast_sales[category].mean()  # 预测的平均销售量
#         total += (price - cost) * sales
#     return -total  # 由于最小化问题，返回负值
#
# # 约束条件
# constraints = [{'type': 'ineq', 'fun': lambda prices: prices[categories.index(category)] - wholesale_price[category] * 1.1} for category in categories] + \
#               [{'type': 'ineq', 'fun': lambda prices: wholesale_price[category] * 1.5 - prices[categories.index(category)]} for category in categories]
#
# # 优化
# result = minimize(total_profit,
#                   list(initial_prices.values()),
#                   constraints=constraints,
#                   bounds=[(wholesale_price[category] * 1.1, wholesale_price[category] * 1.5) for category in categories])
#
# # 优化后的价格
# optimized_prices = result.x
#
# # 输出优化结果
# for category, price in zip(categories, optimized_prices):
#     print(f"{category} 的优化价格: {price:.2f}")
#
# # 生成最终的补货和定价策略
# final_strategy = pd.DataFrame({
#     '品类': categories,
#     '补货量': [replenishment_plan[category] for category in categories],
#     '优化价格': optimized_prices
# })
#
# print(final_strategy)

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 假设我们已经有了以下数据
categories = ['蔬菜1', '蔬菜2', '蔬菜3', '蔬菜4', '蔬菜5', '蔬菜6']
forecast_sales = {'蔬菜1': np.array([20, 22, 21, 23, 25, 24, 26]),
                  '蔬菜2': np.array([30, 31, 29, 28, 30, 32, 31]),
                  '蔬菜3': np.array([15, 14, 16, 17, 18, 16, 19]),
                  '蔬菜4': np.array([10, 11, 10, 12, 13, 12, 14]),
                  '蔬菜5': np.array([5, 6, 5, 7, 6, 7, 8]),
                  '蔬菜6': np.array([8, 9, 7, 8, 9, 10, 11])}
wholesale_price = {'蔬菜1': 10, '蔬菜2': 8, '蔬菜3': 7, '蔬菜4': 6, '蔬菜5': 5, '蔬菜6': 4}
loss_rate = {'蔬菜1': 0.05, '蔬菜2': 0.04, '蔬菜3': 0.03, '蔬菜4': 0.02, '蔬菜5': 0.01, '蔬菜6': 0.05}
min_display_qty = 2.5

# 初始定价策略和补货量
initial_prices = {'蔬菜1': 12, '蔬菜2': 10, '蔬菜3': 9, '蔬菜4': 8, '蔬菜5': 7, '蔬菜6': 6}
replenishment_plan = {category: forecast_sales[category].mean() * (1 + loss_rate[category]) for category in categories}

# 记录优化过程的列表
iter_prices = []
iter_values = []

# 目标函数
def total_profit(prices):
    total = 0
    for category in categories:
        price = prices[categories.index(category)]
        cost = wholesale_price[category] * (1 + loss_rate[category])
        sales = forecast_sales[category].mean()  # 预测的平均销售量
        total += (price - cost) * sales
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
                  callback=callback)

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
