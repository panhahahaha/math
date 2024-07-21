# import numpy as np
# from scipy.optimize import fsolve
#
# # 定义信号源的位置（已知）
# signal_sources = [
#     (0, 0),  # FY00
#     (100, 0),  # FY01
#     (100, 70)   # FY02, 假设一个位置
# ]
# def polar_to_cartesian(var,method):
#     if method == "cartesian":
#         r = var[0]  # 极径
#         theta = var[1]  # 极角（弧度）
#         x = r * np.cos(theta)
#         y = r * np.sin(theta)
#         return x,y
#     else:
#         r = np.sqrt(var[0]**2 + var[1]**2)
#         theta = np.arctan2(var[0], var[1])  # 使用 arctan2 处理四象限的情况
#         return r, theta
#
# cartesian_sources = [polar_to_cartesian(item,'cartesian') for item in signal_sources]
# print(cartesian_sources)
# # 定义接收机接收到的方向信息（角度，以度为单位）
# angles = [45, 60, 30]  # 假设一些方向角度
#
# # 将角度转换为弧度
# angles_rad = np.radians(angles)
#
# # 定义方程组
# def equations(vars):
#     x, y = vars
#     eq1 = y - np.tan(angles_rad[0]) * x
#     eq2 = y - np.tan(angles_rad[1]) * (x - cartesian_sources[1][0])
#     eq3 = y - np.tan(angles_rad[2]) * (x - cartesian_sources[2][0]) - cartesian_sources[2][1]
#     return [eq1, eq2]
#
# # 初始猜测
# initial_guess = (50, 50)
#
# # 使用 fsolve 求解方程组
# solution = fsolve(equations, initial_guess)
# solution = polar_to_cartesian(solution,'')
# # 输出接收机的位置
# print(f"接收机的位置: x = {solution[0]:.2f}, y = {solution[1]:.2f}")
#
import numpy as np
import matplotlib.pyplot as plt
from question1 import Coordinates

# # 已知条件
# FY00 = (0, 0)
# FY01 = (100, 0)
#
# # 无人机接收到的角度信息（单位：度）
# alpha_k = 30  # 例如 α_k = 30度
#
#
# # 无人机的位置（极坐标）
# def polar_to_cartesian(r, theta):
#     """极坐标转换为直角坐标"""
#     theta_rad = np.deg2rad(theta)
#     x = r * np.cos(theta_rad)
#     y = r * np.sin(theta_rad)
#     return x, y
#
#
# def calculate_position(alpha_k, FY00, FY01):
#     """根据接收到的角度信息计算无人机位置"""
#     # α_k 转换为弧度
#     alpha_k_rad = np.deg2rad(alpha_k)
#
#     # 计算 n 值
#     n = (180 - 2 * alpha_k) / 40 - 1
#     n = int(np.round(n))  # 四舍五入为整数
#
#     # 假设 k = 2, 计算θ
#     if n == 0:
#         theta = alpha_k
#     else:
#         theta = alpha_k / n
#
#     # 无人机相对位置坐标
#     r = 100  # 假设半径为100
#     x, y = polar_to_cartesian(r, theta)
#
#     return x, y, n
#
#
# # 计算无人机位置
# x, y, n = calculate_position(alpha_k, FY00, FY01)
# print(f"无人机的相对位置: (x, y) = ({x:.2f}, {y:.2f}), n = {n}")
#
#
# # 可视化无人机位置
# def plot_positions(FY00, FY01, drone_positions):
#     plt.figure(figsize=(8, 8))
#     plt.plot(FY00[0], FY00[1], 'ro', label='FY00')
#     plt.plot(FY01[0], FY01[1], 'bo', label='FY01')
#     for pos in drone_positions:
#         plt.plot(pos[0], pos[1], 'go')
#     plt.legend()
#     plt.xlabel('X 坐标')
#     plt.ylabel('Y 坐标')
#     plt.title('无人机位置')
#     plt.grid(True)
#     plt.show()
#
#
# # 无人机位置列表
# drone_positions = [(x, y)]
#
# # 绘制无人机位置
# plot_positions(FY00, FY01, drone_positions)
