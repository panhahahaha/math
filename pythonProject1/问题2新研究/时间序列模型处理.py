import time

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from constant import *
# 设置字体为 SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号
# group2.to_excel(new_path)
t3 = pd.read_excel(path1)
ls = set(t3['分类名称'].values)
print(ls)
def function():
    for item in ls:
        ins_path = rf'图片数据\{item}'
        ins_path2 = rf'数据\{item}预测结果.xlsx'
        print(item)
        # 读取数据
        file_path = f'整合各单品{item}.xlsx'  # 修改为实际的文件路径
        # file_path = f'整合各单品花叶类.xlsx'
        sales_data = pd.read_excel(file_path)

        # 转换日期列为 datetime 类型
        sales_data['销售日期'] = pd.to_datetime(sales_data['销售日期'])

        # 按日期排序
        sales_data = sales_data.sort_values('销售日期')

        # 设置日期列为索引，并添加频率信息
        sales_data.set_index('销售日期', inplace=True)
        sales_data = sales_data.asfreq('D')  # 设置为每日频率，根据实际情况修改

        # 选择销量数据进行建模
        sales_volume = sales_data['销量(千克)'].fillna(method='ffill')  # 如果有缺失值，用前向填充

        # 创建并训练 ARIMA 模型
        model = ARIMA(sales_volume, order=(5, 1, 0))
        model_fit = model.fit()

        # 残差分析
        residuals = model_fit.resid

        plt.figure(figsize=(10, 6))
        plt.plot(residuals)
        plt.title('残差图')
        plt.xlabel('日期')
        plt.ylabel('残差')
        plt.savefig(ins_path+'残差图.png')
        plt.show()

        plt.figure(figsize=(10, 6))
        plot_acf(residuals, lags=30)
        plt.title('残差的自相关图')
        plt.savefig(ins_path+'自相关图.png')
        plt.show()

        # 模型评估指标
        aic = model_fit.aic
        bic = model_fit.bic
        print(f"AIC: {aic}")
        print(f"BIC: {bic}")

        # 实际值与预测值对比
        predictions = model_fit.predict(start=0, end=len(sales_volume)-1)
        plt.figure(figsize=(10, 6))
        plt.plot(sales_volume, label='实际值')
        plt.plot(predictions, label='预测值', color='red')
        plt.title('实际值与预测值对比')
        plt.xlabel('日期')
        plt.ylabel('销量(千克)')
        plt.legend()
        plt.savefig(ins_path+'实际与预测')
        plt.show()

        # 进行未来7天的预测
        forecast = model_fit.forecast(steps=7)
        forecast.to_csv(ins_path2)
        # 可视化预测结果
        plt.figure(figsize=(10, 6))
        plt.plot(sales_volume, label='历史销量')
        plt.plot(forecast, label='预测销量', color='red')
        plt.title('销量预测')
        plt.xlabel('日期')
        plt.ylabel('销量(千克)')
        plt.legend()
        plt.xlim(pd.Timestamp('2020-01-01'), pd.Timestamp('2023-01-01'))
        plt.savefig(ins_path+'预测图')
        forecast.to_excel(ins_path2)
        plt.show()
        print(forecast)
        time.sleep(3)
        plt.close()
function()