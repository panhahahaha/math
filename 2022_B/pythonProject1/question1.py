import random

import numpy as np
import itertools
from 极坐标绘制 import Draw

radius = 100
coordinates = [(radius, item) for item in range(0, 341, 40)]
# coordinates = [(0, 0), (radius, 120), (radius, 60), (radius, 340)]
coordinates.insert(0, (0, 0))
print(coordinates)


class Coordinates(object):

    def __init__(self):
        self.ob_ls = []
        self.all_ls = []
        self.shoot_ls = []

    def polar_to_cartesian(self, r, theta):
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.array([x, y])

    def shoot(self, bound, number=1):

        for item in self.all_ls:
            if np.all(item.polar_numpy_list) in bound:
                self.shoot_ls.append(item)
                item.is_shoot = True
        while True:
            c = random.sample(self.all_ls, 1)
            print(c[0])
            if len(self.shoot_ls) >= number:
                break
            if c[0] not in self.shoot_ls:
                c[0].is_shoot = True
                self.shoot_ls.append(c[0])
        self.ob_ls = [item for item in self.all_ls if item not in self.shoot_ls]

    def calculate_distance(self):
        for shoot_signal in self.shoot_ls:
            coords = shoot_signal.right_angle
            for receive_signal in self.ob_ls:
                rev = receive_signal.right_angle
                edge = rev - coords

                if np.all(edge[1] != 0):
                    print('edge is ', edge)
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

    def show_shoot(self):
        print('SHOW_SHOOT')
        for item in self.shoot_ls:
            print(item)


l = ['0', 'm', 'i', 'j']
for index, item in enumerate(coordinates):
    name = f'FY0{index}'
    c = Coordinates(item[0], item[1], name)
    Coordinates.all_ls.append(c)
# for index, item in enumerate(coordinates[0:4]):
#     print(index, item)
#     name = f'FY0{l[index]}'
#     c = Coordinates(item[0], item[1], name)
#     Coordinates.all_ls.append(c)
Coordinates.shoot((0, 0), 3)
print(len(Coordinates.ob_ls))
print(len(Coordinates.shoot_ls))
print("all")
for item in Coordinates.all_ls:
    print(item)
Coordinates.show_shoot()
Coordinates.calculate_distance()
Coordinates.calculate_signal()
# for item in Coordinates.ob_ls:
#     print(item)
# print('信号为', item.signal)
d = Draw(Coordinates.all_ls)
d.drawing()
# Coordinates.drawing.drawing()
