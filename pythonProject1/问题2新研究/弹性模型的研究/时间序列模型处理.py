import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# 读取数据
sales_data = pd.read_excel('合并水生根茎类.xlsx')
# wholesale_price_data = pd.read_excel('附件3 蔬菜类商品的批发价格.xlsx')
# loss_rate_data = pd.read_excel('附件4 蔬菜类商品的近期损耗率.xlsx')

# 数据预处理
sales_data['销售日期'] = pd.to_datetime(sales_data['销售日期'])
sales_data = sales_data.sort_values('销售日期')

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