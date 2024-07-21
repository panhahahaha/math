import numpy as np
from scipy.optimize import minimize
import pandas as pd
import matplotlib.pyplot as plt

# 价格弹性系数
price_elasticity = {'蔬菜1': -1.2, '蔬菜2': -1.0, '蔬菜3': -1.5, '蔬菜4': -0.8, '蔬菜5': -1.3, '蔬菜6': -0.9}

# 初始定价策略和补货量
initial_prices = {'蔬菜1': 12, '蔬菜2': 10, '蔬菜3': 9, '蔬菜4': 8, '蔬菜5': 7, '蔬菜6': 6}
replenishment_plan = {category: forecast_sales[category].mean() * (1 + loss_rate_data.loc[loss_rate_data['品类'] == category, '损耗率'].values[0]) for category in categories}

# 记录优化过程的列表
iter_prices = []
iter_values = []

# 目标函数
def total_profit(prices):
    total = 0
    for category in categories:
        P = prices[categories.index(category)]
        P0 = initial_prices[category]
        Q0 = forecast_sales[category].mean()
        epsilon = price_elasticity[category]
        Q = Q0 * (1 + epsilon * (P - P0) / P0)
        cost = wholesale_price_data.loc[wholesale_price_data['品类'] == category, '批发价格'].values[0] * (1 + loss_rate_data.loc[loss_rate_data['品类'] == category, '损耗率'].values[0])
        total += (P - cost) * Q
    return -total  # 由于最小化问题，返回负值

# 回调函数
def callback(xk):
    iter_prices.append(xk)
    iter_values.append(total_profit(xk))

# 约束条件
constraints = [{'type': 'ineq', 'fun': lambda prices: prices[categories.index(category)] - wholesale_price_data.loc[wholesale_price_data['品类'] == category, '批发价格'].values[0] * 1.1} for category in categories] + \
              [{'type': 'ineq', 'fun': lambda prices: wholesale_price_data.loc[wholesale_price_data['品类'] == category, '批发价格'].values[0] * 1.5 - prices[categories.index(category)]} for category in categories]

# 优化
result = minimize(total_profit,
                  list(initial_prices.values()),
                  constraints=constraints,
                  bounds=[(wholesale_price_data.loc[wholesale_price_data['品类'] == category, '批发价格'].values[0] * 1.1, wholesale_price_data.loc[wholesale_price_data['品类'] == category, '批发价格'].values[0] * 1.5) for category in categories],
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
