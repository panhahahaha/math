import numpy as np
import matplotlib.pyplot as plt
#
#
# def generate_positions(num_positions, radius):
#     """生成num_positions个在半径为radius的圆周上的点"""
#     angles = np.linspace(0, 2 * np.pi, num_positions, endpoint=False)
#     positions = [(radius * np.cos(angle), radius * np.sin(angle)) for angle in angles]
#     return positions
#
#
# def add_random_noise(positions, noise_level=1):
#     """给位置添加随机噪声，噪声范围在-noise_level到noise_level度之间"""
#     noisy_positions = []
#     for x, y in positions:
#         angle = np.arctan2(y, x)
#         radius = np.hypot(x, y)  # 修正此处使用np.hypot
#         angle += np.deg2rad(np.random.uniform(-noise_level, noise_level))
#         noisy_positions.append((radius * np.cos(angle), radius * np.sin(angle)))
#     return noisy_positions
#
#
# def calculate_angles(positions, center):
#     """计算每个点与中心点连线的角度"""
#     angles = []
#     cx, cy = center
#     for x, y in positions:
#         angle = np.arctan2(y - cy, x - cx)
#         angles.append(np.rad2deg(angle) % 360)
#     return angles
#
#
# def simulate_fy0i_position(alpha_k, lambda_values, center=(0, 0)):
#     """根据仿真模拟算法和角度偏差计算FY0i的位置"""
#     num_positions = 10500
#     radius = 100
#
#     # Step 1: 生成10500组被动接收信号无人机k的实际坐标
#     positions = generate_positions(num_positions, radius)
#     print('positions:', positions[0:10])
#     noisy_positions = add_random_noise(positions)
#     print('noisy_positions:',noisy_positions[0:10])
#
#     # Step 2: 计算每个位置的角度
#     angles = calculate_angles(noisy_positions, center)
#
#     # Step 3: 根据alpha和lambda判断n值
#     alpha_k_rad = np.deg2rad(alpha_k)
#     n_values = []
#     for lambda_value in lambda_values:
#         lambda_rad = np.deg2rad(lambda_value)
#         n = int((180 - 2 * np.rad2deg(alpha_k_rad - lambda_rad)) / 40) - 1
#         n_values.append(n)
#
#     # Step 4: 确定FY0i的位置
#     fy0i_positions = []
#     for i, n in enumerate(n_values):
#         if 0 <= n < num_positions:
#             fy0i_positions.append(noisy_positions[n])
#
#     return fy0i_positions
#
#
# # 示例参数
# alpha_k = 30
# lambda_values = [10, 20, 30]  # 示例lambda值，可以根据具体情况调整
#
# # 计算FY0i位置
# fy0i_positions = simulate_fy0i_position(alpha_k, lambda_values)
#
# # 打印结果
# for i, pos in enumerate(fy0i_positions):
#     print(f"FY0i 位置 {i + 1}: (x, y) = ({pos[0]:.2f}, {pos[1]:.2f})")
