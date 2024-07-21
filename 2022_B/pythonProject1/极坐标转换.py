import numpy as np

def polar_angle(r1, theta1, r2, theta2):
    # 将极坐标转换为笛卡尔坐标
    x1, y1 = r1 * np.cos(theta1), r1 * np.sin(theta1)
    x2, y2 = r2 * np.cos(theta2), r2 * np.sin(theta2)

    # 计算向量
    vector1 = np.array([x1, y1])
    vector2 = np.array([x2, y2])

    # 计算向量的点积
    dot_product = np.dot(vector1, vector2)

    # 计算向量的模
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    # 计算夹角的余弦值
    cos_theta = dot_product / (norm1 * norm2)

    # 计算夹角（弧度）
    angle_rad = np.arccos(cos_theta)

    # 将弧度转换为角度
    angle_deg = np.degrees(angle_rad)

    return angle_deg

# 示例：计算极坐标下两个向量之间的角度
r1, theta1 = 5, np.radians(30)  # 向量1的极坐标 (5, 30度)
r2, theta2 = 7, np.radians(65)  # 向量2的极坐标 (7, 60度)

angle = polar_angle(r1, theta1, r2, theta2)
print(f"两个向量之间的夹角为 {angle:.2f} 度")
import numpy as np

# 定义点的坐标
a = np.array([0, 0])
b = np.array([100, 0])
c = np.array([98, 40.10])

# 计算向量ab和cb
ab = b - a
cb = b - c

# 计算向量的点积
dot_product = np.dot(ab, cb)

# 计算向量的模
norm_ab = np.linalg.norm(ab)
norm_cb = np.linalg.norm(cb)

# 计算夹角的余弦值
cos_theta = dot_product / (norm_ab * norm_cb)

# 计算夹角（弧度）
angle_rad = np.arccos(cos_theta)

# 将弧度转换为角度
angle_deg = np.degrees(angle_rad)

print(f"ab与cb连线的夹角为 {angle_deg:.2f} 度")
import numpy as np

# 极坐标列表
polar_coords = [
    np.array([98. , 40.1]),
    np.array([112.  ,  80.21]),
    np.array([105.  , 119.75]),
    np.array([ 98.  , 159.86]),
    np.array([112.  , 199.96]),
    np.array([105.  , 240.07]),
    np.array([ 98.  , 280.17]),
    np.array([112.  , 320.28]),
    np.array([-98. , -40.1])
]

def polar_to_cartesian(r, theta):
    """将极坐标转换为笛卡尔坐标"""
    x = r * np.cos(np.radians(theta))
    y = r * np.sin(np.radians(theta))
    return np.array([x, y])

# 将极坐标转换为笛卡尔坐标
cartesian_coords = [polar_to_cartesian(r, theta) for r, theta in polar_coords]

def calculate_angle(v1, v2):
    """计算两个向量之间的夹角"""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)
    return angle_deg

# 计算每两条边之间的夹角
angles = []
for i in range(len(cartesian_coords) - 1):
    angle = calculate_angle(cartesian_coords[i], cartesian_coords[i + 1])
    angles.append(angle)

# 输出结果
for i, angle in enumerate(angles):
    print(f"边 {i} 与边 {i+1} 之间的夹角为 {angle:.2f} 度")



import numpy as np


def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.array([x, y])


def angle_between_vectors(v1, v2):
    dot_product = np.dot(v1, v2)
    norms = np.linalg.norm(v1) * np.linalg.norm(v2)
    cos_theta = dot_product / norms
    angle = np.arccos(cos_theta)
    return np.degrees(angle)


def main():
    # 给定三个点的极坐标
    r1, theta1 = 3, np.deg2rad(30)
    r2, theta2 = 4, np.deg2rad(45)
    r3, theta3 = 2, np.deg2rad(60)

    # 转换为直角坐标
    p1 = polar_to_cartesian(r1, theta1)
    p2 = polar_to_cartesian(r2, theta2)
    p3 = polar_to_cartesian(r3, theta3)

    # 计算向量
    v1 = p2 - p1
    v2 = p3 - p1
    v3 = p3 - p2

    # 计算两两向量之间的夹角
    angle_1_2 = angle_between_vectors(v1, v2)
    angle_1_3 = angle_between_vectors(v1, -v3)
    angle_2_3 = angle_between_vectors(v2, v3)

    print(f"Angle between p1-p2 and p1-p3: {angle_1_2:.2f} degrees")
    print(f"Angle between p1-p2 and p2-p3: {angle_1_3:.2f} degrees")
    print(f"Angle between p1-p3 and p2-p3: {angle_2_3:.2f} degrees")


if __name__ == "__main__":
    main()
