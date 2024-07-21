import numpy as np
import itertools, random
from 极坐标绘制 import Draw
import matplotlib.pyplot as plt
import math
print(math.cos((60/180)*math.pi))
class Points:
    def __init__(self, r, d, name=''):
        self.radius = r
        self.d = d
        self.is_shoot = False
        self.signal = []
        self.polar_numpy_list = np.array([self.radius, self.d])
        self.right_angle = self.polar_to_cartesian(self.radius, self.d)
        self.special = False
        self.edge = []
        self.name = name

    def polar_to_cartesian(self, r, theta):
        theta = np.radians(theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.array([x, y])

    def __str__(self, *args, **kwargs):
        return (
            f'name is {self.name}\n'
            f'self.numpy_list is {self.polar_numpy_list}\n'
            f'self.edge is {self.edge[0:10]}\n'
            f'self.signal is {self.signal[0:10]}\n'
            f'self.is_shoot is {self.is_shoot}\n\n\n'

        )


class Coordinates(object):

    def __init__(self,name):
        self.name = name
        self.ob_ls = []
        self.all_ls = []
        self.shoot_ls = []
        self.draw = Draw

    def running(self, show=False):

        self.shoot()
        self.calculate_distance()
        self.calculate_signal()
        if show:
            print('\n' * 3, ''"经过计算完成后的", '\n' * 3)
            self.show_shoot()

    def shoot(self, bound=(0, 0), number=1):
        # for item in self.shoot_ls:
        #     item.is_shoot = True
        for item in self.all_ls:
            if item.is_shoot and item not in self.shoot_ls:
                self.shoot_ls.append(item)
            if not item.is_shoot and item not in self.ob_ls and not item.special:
                # print('进入')
                self.ob_ls.append(item)
            if item in self.shoot_ls and item in self.ob_ls:
                self.ob_ls.remove(item)

        # for item in self.all_ls:
        #     if np.all(item.polar_numpy_list) in bound:
        #         self.shoot_ls.append(item)
        #         item.is_shoot = True
        # while True:
        #     c = random.sample(self.all_ls, 1)
        #     print(c[0])
        #     if len(self.shoot_ls) >= number:
        #         break
        #     if c[0] not in self.shoot_ls:
        #         c[0].is_shoot = True
        #         self.shoot_ls.append(c[0])
        # self.ob_ls = [item for item in self.all_ls if item not in self.shoot_ls]

    def calculate_distance(self):
        for shoot_signal in self.shoot_ls:
            coords = shoot_signal.right_angle
            for receive_signal in self.ob_ls:
                rev = receive_signal.right_angle
                edge = rev - coords

                if np.all(edge[1] != 0):
                    # print('edge is ', edge)
                    shoot_signal.edge.append(edge)
                    receive_signal.edge.append(edge)
                else:
                    print("error")

    def calculate_signal(self):
        def angle_between_vectors(v1, v2):
            dot_product = np.dot(v1, v2)
            norms = np.linalg.norm(v1) * np.linalg.norm(v2)
            cos_theta = dot_product / norms
            angle = np.arccos(cos_theta)
            return np.degrees(angle)

        for item in self.ob_ls:
            polar_coords = item.edge
            print(polar_coords)
            combinations = list(itertools.combinations(polar_coords, 2))
            for item_0 in combinations:
                item.signal.append(angle_between_vectors(item_0[0], item_0[1]))

            # item.signal.append(angle_between_vectors())
    def vector_to_angle(self, vector):

        # 确定初始点和向量的参数
        P1 = np.array([0, 0])  # 初始点P1
        length_A = 100  # 向量A的长度
        length_B = 100  # 向量B的长度
        angle_between_vectors = 40  # 向量A和B的夹角（度数）

        # 确定向量A的角度（假设为0度）
        alpha = 0  # 向量A相对于x轴的角度（度数）

        # 计算P2的坐标
        x2 = P1[0] + length_A * np.cos(np.deg2rad(alpha))
        y2 = P1[1] + length_A * np.sin(np.deg2rad(alpha))
        P2 = np.array([x2, y2])

        # 确定向量B的角度
        beta = alpha + angle_between_vectors

        # 计算P3的坐标
        x3 = P2[0] + length_B * np.cos(np.deg2rad(beta))
        y3 = P2[1] + length_B * np.sin(np.deg2rad(beta))
        P3 = np.array([x3, y3])

        print(f'P1的坐标: {P1}')
        print(f'P2的坐标: {P2}')
        print(f'P3的坐标: {P3}')

    def show_shoot(self):
        print(f"{self.name} is showing")
        print('\n' * 5, '*' * 10, '\n' * 5, 'SHOW_ALL')
        for item in self.all_ls:
            print(item)
        print('\n' * 5, '*' * 10, '\n' * 5, 'SHOW_OB_LS')
        for item in self.ob_ls:
            print(item)
        print('\n' * 5, '*' * 10, '\n' * 5, 'SHOW_SHOOT_LS')
        for item in self.shoot_ls:
            print(item)


class Observation:
    def __init__(self, radius=100):
        self.radius = radius
        self.std_coordinates = [(self.radius, item) for item in range(0, 321, 40)]
        self.std_coordinates.insert(0, (0, 0))
        self.dev_points = [self.polar_to_cartesian(item[0], item[1]) for item in self.std_coordinates]
        self.dev_coordinates_cart = [self.generate_random_points(
            item, 10000, 5) for item in self.dev_points]
        a = self.std_coordinates.pop(2)
        self.dev_points_plor = [[self.cartesian_to_polar(item_0[0], item_0[1]) for item_0 in item] for item in
                                self.dev_coordinates_cart]
        print(self.dev_points_plor)

    def cartesian_to_polar(self, x, y):
        r = np.sqrt(x ** 2 + y ** 2)
        theta = np.arctan2(y, x)  # atan2函数可以处理x为零的情况
        return (r, np.degrees(theta))

    def polar_to_cartesian(self, r, theta):
        theta = np.radians(theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        print('x,y:', x, y)
        return np.array([x, y])

    def generate_random_points(self, center, num_points, radius):
        """
        在给定中心点附近生成随机分布的点。

        参数:
        center (tuple): 中心点的坐标 (x, y)
        num_points (int): 要生成的随机点的数量
        radius (float): 随机点分布的半径

        返回:
        numpy.ndarray: 随机点的数组，形状为 (num_points, 2)
        """
        # 生成随机角度
        angles = np.random.uniform(0, 2 * np.pi, num_points)
        # 生成随机半径
        radii = np.random.uniform(0, radius, num_points)
        # 计算随机点的坐标
        x_points = center[0] + radii * np.cos(angles)
        y_points = center[1] + radii * np.sin(angles)
        return np.vstack((x_points, y_points)).T

    # 示例参数

    # 可视化随机点


def main():
    radius = 100
    coordinates = [(radius, item) for item in range(0, 341, 40)]
    # coordinates = [(0, 0), (radius, 120), (radius, 60), (radius, 340)]
    coordinates.insert(0, (0, 0))
    coor = Coordinates('dev')
    # for index, item in enumerate(coordinates):
    #     name = f'FY0{index}'
    #     c = Points(item[0], item[1], name)
    #     coor.all_ls.append(c)
    # coor.shoot((0, 0), 3)
    # coor.calculate_distance()
    # coor.calculate_signal()
    # coor.show_shoot()
    # coor.draw(coor.all_ls).drawing()
    o = Observation()
    # print(o.dev_coordinates_cart)
    plt.scatter(o.dev_coordinates_cart[:, 0], o.dev_coordinates_cart[:, 1], alpha=0.6)
    plt.scatter(o.dev_points[0], o.dev_points[1], color='red', marker='x')  # 标记中心点
    plt.title('Random Points Around Center')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.show()
    # print(o.dev_points_plor,'\n',o.cartesian_to_polar(o.dev_points[0],o.dev_points[1]))
    for item in o.std_coordinates:
        c1 = Points(item[0], item[1])
        coor.shoot_ls.append(c1)
    for item in o.dev_points_plor:
        c1 = Points(item[0], item[1])
        coor.ob_ls.append(c1)
    coor.shoot()
    coor.calculate_distance()
    coor.calculate_signal()
    coor.show_shoot()
    ls = []
    stand_single = coor.ob_ls[-1].signal
    for item in coor.ob_ls:
        ls.append(item.signal)
    ls.pop()
    import pandas as pd

    table = pd.DataFrame({'∠1': [], '∠2': [], '∠3': [], '∠1偏离值': [], '∠2偏离值': [], '∠3偏离值': []})
    for item in ls:
        new_row = {'∠1': item[0], '∠2': item[1], '∠3': item[2], '∠1偏离值': item[0] - stand_single[0],
                   '∠2偏离值': item[1] - stand_single[1], '∠3偏离值': item[2] - stand_single[2]}
        table = table._append(new_row, ignore_index=True)

    table.to_excel('偏离角度表格.xlsx')
    print(ls)
    print('stand_single', stand_single)
    print(table)


if __name__ == '__main__':
    main()
