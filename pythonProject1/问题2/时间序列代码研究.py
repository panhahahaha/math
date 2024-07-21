import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# 读取数据
sales_data = pd.read_excel('附件2 销售流水明细数据.xlsx')
wholesale_price_data = pd.read_excel('附件3 蔬菜类商品的批发价格.xlsx')
loss_rate_data = pd.read_excel('附件4 蔬菜类商品的近期损耗率.xlsx')

# 数据预处理
sales_data['date'] = pd.to_datetime(sales_data['date'])
sales_data = sales_data.sort_values('date')

# 对于每个品类进行时间序列分析
categories = sales_data['品类'].unique()
forecast_sales = {}

for category in categories:
    category_data = sales_data[sales_data['品类'] == category].set_index('date')

    # 创建并训练ARIMA模型
    model = ARIMA(category_data['销售量'], order=(5, 1, 0))
    model_fit = model.fit()

    # 进行未来7天的预测
    forecast = model_fit.forecast(steps=7)
    forecast_sales[category] = forecast

    # 可视化预测结果
    plt.figure(figsize=(10, 6))
    plt.plot(category_data['销售量'], label='历史销售量')
    plt.plot(forecast, label='预测销售量', color='red')
    plt.title(f'{category} 销售量预测')
    plt.xlabel('日期')
    plt.ylabel('销售量')
    plt.legend()
    plt.show()


# 补货量计算函数
def calculate_replenishment(forecast_sales, loss_rate_data, min_display_qty):
    replenishment = {}
    for category, sales in forecast_sales.items():
        loss = loss_rate_data[loss_rate_data['品类'] == category]['损耗率'].values[0]
        replenishment_qty = sales * (1 + loss)
        replenishment[category] = np.maximum(replenishment_qty, min_display_qty)
    return replenishment


min_display_qty = 2.5  # 每个单品的最小陈列量
replenishment_plan = calculate_replenishment(forecast_sales, loss_rate_data, min_display_qty)

# 定价策略制定和优化步骤同前面给出的示例代码
# ...
