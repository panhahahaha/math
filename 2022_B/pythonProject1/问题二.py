import numpy as np
import matplotlib.pyplot as plt

# 设置无人机初始位置和偏差
def generate_initial_positions(num_drones, radius, center=(0, 0), deviation=5):
    angles = np.linspace(0, 2 * np.pi, num_drones, endpoint=False)
    positions = [(center[0] + radius * np.cos(angle) + np.random.uniform(-deviation, deviation),
                  center[1] + radius * np.sin(angle) + np.random.uniform(-deviation, deviation)) for angle in angles]
    return positions

# 三点定位法计算理想位置
def calculate_ideal_position(num_drones, radius, center=(0, 0)):
    angles = np.linspace(0, 2 * np.pi, num_drones, endpoint=False)
    ideal_positions = [(center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle)) for angle in angles]
    return ideal_positions

# 迭代调整无人机位置
def adjust_positions(positions, ideal_positions, learning_rate=0.1, iterations=10):
    adjusted_positions = positions.copy()
    for _ in range(iterations):
        new_positions = []
        for pos, ideal_pos in zip(adjusted_positions, ideal_positions):
            adjusted_x = pos[0] + learning_rate * (ideal_pos[0] - pos[0])
            adjusted_y = pos[1] + learning_rate * (ideal_pos[1] - pos[1])
            new_positions.append((adjusted_x, adjusted_y))
        adjusted_positions = new_positions
    return adjusted_positions

# 绘制无人机位置
def plot_positions(initial_positions, adjusted_positions, ideal_positions):
    fig, ax = plt.subplots()

    # 初始位置
    initial_x, initial_y = zip(*initial_positions)
    ax.scatter(initial_x, initial_y, color='red', label='Initial Positions')

    # 调整后位置
    adjusted_x, adjusted_y = zip(*adjusted_positions)
    ax.scatter(adjusted_x, adjusted_y, color='blue', label='Adjusted Positions')

    # 理想位置
    ideal_x, ideal_y = zip(*ideal_positions)
    ax.scatter(ideal_x, ideal_y, color='green', label='Ideal Positions')

    for i in range(len(initial_positions)):
        ax.plot([initial_x[i], adjusted_x[i]], [initial_y[i], adjusted_y[i]], 'k--')
        ax.plot([adjusted_x[i], ideal_x[i]], [adjusted_y[i], ideal_y[i]], 'k--')

    ax.set_aspect('equal')
    plt.legend()
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('UAV Formation Adjustment')
    plt.show()

# 参数设置
num_drones = 10
radius = 100
center = (0, 0)

# 生成初始位置
initial_positions = generate_initial_positions(num_drones, radius, center)

# 计算理想位置
ideal_positions = calculate_ideal_position(num_drones, radius, center)

# 迭代调整
adjusted_positions = adjust_positions(initial_positions, ideal_positions)

# 绘制结果
plot_positions(initial_positions, adjusted_positions, ideal_positions)
