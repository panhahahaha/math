import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np
# x = [1, 2, 3, 4, 5]
# y1 = [2, 3, 5, 7, 11]
# y2 = [1, 4, 6, 8, 10]
#
# plt.plot(x, y1, label='Prime Numbers', linestyle='-', marker='o')
# plt.plot(x, y2, label='Other Numbers', linestyle='--', marker='x')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Comprehensive Legend Example')
#
# # 设置图例
# plt.legend(
#     loc='upper right',      # 位置
#     fontsize='large',       # 字体大小
#     title='Legend Title',   # 图例标题
#     shadow=True,            # 阴影
#     ncol=2,                 # 列数
#     bbox_to_anchor=(1.05, 1) # 自定义位置
# )
#
# plt.show()
# temperature = [20, 25, 30, 35, 40]  # 温度
# humidity = [30, 45, 50, 55, 60]  # 湿度
#
# plt.scatter(temperature, humidity, label='City Data', color='red', marker='x')
# plt.xlabel('Temperature (°C)')
# plt.ylabel('Humidity (%)')
# plt.title('Temperature vs Humidity')
# plt.legend()
# plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 创建数据框
data = {
    '无人机编号': range(10),
    '极坐标': [
        (0, 0), (100, 0), (98, 40.10), (112, 80.21),
        (105, 119.75), (98, 159.86), (112, 199.96),
        (105, 240.07), (98, 280.17), (112, 320.28)
    ]
}

df = pd.DataFrame(data)

# 将极坐标转换为直角坐标
df['r'] = df['极坐标'].apply(lambda x: x[0])
df['theta'] = df['极坐标'].apply(lambda x: np.deg2rad(x[1]))
df['x'] = df['r'] * np.cos(df['theta'])
df['y'] = df['r'] * np.sin(df['theta'])

# 绘制图表
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# 绘制无人机位置
ax.scatter(df['theta'], df['r'])

# 标注无人机编号
for i in range(len(df)):
    ax.annotate(df['无人机编号'][i], (df['theta'][i], df['r'][i]), textcoords="offset points", xytext=(0,10), ha='center')

# 添加半径为100的圆形
circle = plt.Circle((0, 0), 100, transform=ax.transData._b, color='blue', fill=False, linestyle='--')
ax.add_artist(circle)

# 设置标题
plt.title('无人机的初始位置')

# 设置极坐标图的最大半径
ax.set_ylim(0, max(df['r']) + 20)

plt.show()
