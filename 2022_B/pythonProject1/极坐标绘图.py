import numpy as np
import matplotlib.pyplot as plt

# 定义极坐标点
points = [(3, np.deg2rad(30)), (4, np.deg2rad(60))]

# 提取 r 和 theta
r = [p[0] for p in points]
theta = [p[1] for p in points]

# 创建一个极坐标子图
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# 绘制极坐标点
ax.plot(theta, r, 'bo', label='Points')

# 绘制两点之间的连线
ax.plot([theta[0], theta[1]], [r[0], r[1]], 'r-', label='Line between points')

# 添加标题和图例
ax.set_title('Polar Coordinates Plot')
ax.legend()

# 显示图表
plt.show()
