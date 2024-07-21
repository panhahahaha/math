import numpy as np
import matplotlib.pyplot as plt
from typing import List

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
# Set the font properties
font_properties = FontProperties(fname='/path/to/your/SimHei.ttf')  # Update with the correct path to the SimHei font
class Draw(object):
    def __init__(self, points: List):
        print('points is ',np.all(points))
        for item in points:
            print(item)
        self.points = [(item.radius,item.d,item.is_shoot,item.name) for item in points]
        self.rad_points = []
        self.plot = []
        self.degree_to_rad()

    def degree_to_rad(self):
        for item in self.points:
            rad = np.deg2rad(item[1])
            self.rad_points.append((item[0], rad))

    # def degree_to_rad(self):
    #     self.rad_points = [(r, np.deg2rad(theta), is_special, name) for r, theta, is_special, name in self.points]
    def calculate_angle(self, p1, p2):
        # 计算从p1到p2的直线方位角
        delta_theta = p2[1] - p1[1]
        angle = np.arctan2(np.sin(delta_theta), np.cos(delta_theta))
        return np.rad2deg(angle)

    def drawing(self):
        print(self.rad_points)
        # 提取 r 和 theta
        r = [p[0] for p in self.rad_points]
        theta = [p[1] for p in self.rad_points]
        # 创建一个极坐标子图
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # 绘制点并确保每种颜色的点在图例中只出现一次
        red_label_added = False
        blue_label_added = False

        for i, item in enumerate(self.points):
            if item[2] is True:
                if not red_label_added:
                    ax.plot(theta[i], r[i], 'o', color='red', label='发射点')
                    red_label_added = True
                else:
                    ax.plot(theta[i], r[i], 'o', color='red')
            else:
                if not blue_label_added:
                    ax.plot(theta[i], r[i], 'o', color='blue', label='接收点')
                    blue_label_added = True
                else:
                    ax.plot(theta[i], r[i], 'o', color='blue')

        # 添加每个点的名字
        for i, name in enumerate(self.points):
            ax.annotate(name[3], (theta[i], r[i]), textcoords="offset points", xytext=(5, 5), ha='center')

        # 绘制点之间的连线
        # 根据需要取消注释以下代码
        # for index, item in enumerate(self.points):
        #     if item[2] is True:
        #         for j in range(index + 1, len(self.points)):
        #             ax.plot([theta[index], theta[j]], [r[index], r[j]], 'r-')
        #     else:
        #         continue
            # 绘制点之间的连线并标注代号
        # angle_counter = 1
        # for i in range(len(self.rad_points)):
        #     for j in range(i + 1, len(self.rad_points)):
        #         ax.plot([theta[i], theta[j]], [r[i], r[j]], 'r-')
        #         # 标注代号
        #         mid_theta = (theta[i] + theta[j]) / 2
        #         mid_r = (r[i] + r[j]) / 2
        #         ax.annotate(f'$\\alpha_{{{angle_counter}}}$', (mid_theta, mid_r), textcoords="offset points",
        #                     xytext=(0, 10), ha='center')
        #         angle_counter += 1
        # 添加标题和图例
        ax.set_title('Polar Coordinates Plot')
        ax.legend()

        # 显示图表
        plt.show()
def main():
    points = [(3, 30), (4, 60)]
    d = Draw(points)
    d.drawing()
    print(d.rad_points)
if __name__ == '__main__':
    main()