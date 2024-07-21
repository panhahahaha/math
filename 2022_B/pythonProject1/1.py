import numpy as np

# 将极坐标转换为笛卡尔坐标
# import numpy as np
#
# # 确定初始点和向量的参数
# P1 = np.array([0, 0])  # 初始点P1
# length_A = 100  # 向量A的长度
# length_B = 100  # 向量B的长度
# angle_between_vectors = 40  # 向量A和B的夹角（度数）
#
# # 确定向量A的角度（假设为0度）
# alpha = 0  # 向量A相对于x轴的角度（度数）
#
# # 计算P2的坐标
# x2 = P1[0] + length_A * np.cos(np.deg2rad(alpha))
# y2 = P1[1] + length_A * np.sin(np.deg2rad(alpha))
# P2 = np.array([x2, y2])
#
# # 确定向量B的角度
# beta = alpha + angle_between_vectors
#
# # 计算P3的坐标
# x3 = P2[0] + length_B * np.cos(np.deg2rad(beta))
# y3 = P2[1] + length_B * np.sin(np.deg2rad(beta))
# P3 = np.array([x3, y3])
#
# print(f'P1的坐标: {P1}')
# print(f'P2的坐标: {P2}')
# print(f'P3的坐标: {P3}')
import numpy as np

import pandas as pd
def calculate():
    # 多维数组示例
    H = np.array([
        [(1, 1, 1), (2, 2, 2), (3, 3, 3)],
        [(4, 4, 4), (5, 5, 5), (6, 6, 6)]
    ])

    # 展平每一列的数组
    column1 = H[:, 0, 0]
    column2 = H[:, 1, 0]
    column3 = H[:, 2, 0]

    data = pd.DataFrame({
        'column1': column1,
        'column2': column2,
        'column3': column3
    })

    print(data)


calculate()
