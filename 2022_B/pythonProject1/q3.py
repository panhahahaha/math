import numpy
import pandas as pd
from typing import List
from q1 import Points, Coordinates
import numpy as np

data = {
    '无人机编号': range(10),
    '极坐标': [
        (0, 0), (100, 0), (98, 40.10), (112, 80.21),
        (105, 119.75), (98, 159.86), (112, 199.96),
        (105, 240.07), (98, 280.17), (112, 320.28)
    ]
}
# 标准坐标
std_ls = [(100, item) for item in range(0, 341, 40)]
std_ls.insert(0, (0, 0))

std_points = {
    '无人机编号': range(10),
    '极坐标': std_ls
}
coord_dev = Coordinates('有偏差')
coord_std = Coordinates('无偏差')
for index, item in enumerate(data['极坐标']):
    name = f'FY0{index}'
    c = Points(item[0], item[1], name=name)
    coord_dev.all_ls.append(c)
for index, item in enumerate(std_points['极坐标']):
    name = f'FY0{index}'
    c = Points(item[0], item[1], name=name)
    coord_std.all_ls.append(c)
# coord_dev.running()
# coord_std.running()
# coord_dev.show_shoot()
# coord_std.show_shoot()

# data_message.to_excel('标准与实际.xlsx')
modify = []
modify_angle = []
name = [f'FY0{_}' for _ in range(10)]
locate = pd.DataFrame({'无人机编号': name,
                       '第一次矫正坐标': [0 for item in range(len(name))],
                       '第一次矫正方向角(°)': [0 for item in range(len(name))]})


class Handle_angle():
    def __init__(self, dev: Coordinates, std: Coordinates):
        """
        specoal_number：将特殊编号标记出，方便替换非标准数据与标准数据
        :param dev:
        :param std:
        """
        self.std, self.dev = std, dev
        self.special_number_angle, self.special_angle = self.find_special_angle()
        print(self.special_angle, self.special_number_angle)
        self.dev_signal = []
        self.std_signal = []
        self.car_gap = []  # 存放与标准值的坐标差
        self.angle_gap = []  # 存放与标准值的角度差
        self.special_number_angle_1, self.special_angle_1, self.std_special_angle_1 = None, None, None

    def collect_signal(self):
        self.dev_signal = np.array([item.signal for item in self.dev.ob_ls])
        self.std_signal = np.array([item.signal for item in self.std.ob_ls])

    def compare(self):
        ls = []
        for a, b in zip(self.dev_signal, self.std_signal):
            result = abs(a - b)
            ls.append(result)
        self.angle_gap.extend([(round(item[0], 2), round(item[1], 2), round(item[2], 2)) for item in ls])
        gap = [item[0] + item[1] + item[2] for item in ls]
        print(gap)
        index = gap.index(min(gap)) + 2
        self.special_number_angle_1, self.special_angle_1, self.std_special_angle_1 = index, self.dev.all_ls[index], \
        self.std.all_ls[index]

    def handle_shoot_received(self):
        '''
        先替换标准数据与非标准数据
        :return:
        '''
        std_data = self.std.all_ls[self.special_number_angle]
        # 设置有偏差的coor对象的发射
        self.dev.all_ls[self.special_number_angle] = std_data
        self.dev.all_ls[self.special_number_angle].is_shoot = True
        self.dev.all_ls[0].is_shoot, self.dev.all_ls[1].is_shoot = True, True
        self.dev.running(show=True)
        # 设置无偏差的coor对象的发射
        self.std.all_ls[self.special_number_angle].is_shoot = True
        self.std.all_ls[0].is_shoot, self.std.all_ls[1].is_shoot = True, True
        self.std.running(show=True)

    def find_special_angle(self):
        std_car = [item.right_angle for item in self.std.all_ls]
        dev_car = [item.right_angle for item in self.dev.all_ls]
        gap = []
        for a, b in zip(std_car, dev_car):
            result = abs(a - b)
            gap.append(numpy.sqrt(result[0] ** 2 + result[1] ** 2))
        new_gap = [item for item in gap if item != 0]
        min_object, index = min(new_gap), new_gap.index(min(new_gap)) + 2
        # print(new_gap)
        return index, self.dev.all_ls[index]

    def __str__(self):
        return (f'{self.special_angle}'
                f'{self.special_angle_1}'
                f'{self.std_special_angle_1}')


def calculate():
    H = Handle_angle(coord_dev, coord_std)
    H.find_special_angle()
    H.handle_shoot_received()
    H.collect_signal()
    H.compare()
    print(H)
    # H.angle_gap.insert(0,(0,0,0))
    # H.angle_gap.insert(0,(0,0,0))
    # H.dev_signal.insert(0,(0,0,0))
    # H.dev_signal.insert(0,(0,0,0))
    # H.std_signal.insert(0,(0,0,0))
    # H.std_signal.insert(0,(0,0,0))

    print(len(H.dev_signal), len(H.std_signal), len(H.angle_gap))
    data = pd.DataFrame({

        '无人机编号': range(3, 10),
        '极坐标': [
            (112, 80.21),
            (105, 119.75), (98, 159.86), (112, 199.96),
            (105, 240.07), (98, 280.17), (112, 320.28),
        ],
        '实际方位角度':
            [(np.round(item[0], 2), np.round(item[1], 2), np.round(item[2], 2)) for item in H.dev_signal]
        ,
        '理想方位角度':
            [(np.round(item[0], 2), np.round(item[1], 2), np.round(item[2], 2)) for item in H.std_signal]
        ,
        '角度差值':
            H.angle_gap

    })
    # key_point = coord_std.all_ls[index]
    # key_point.is_shoot = True
    # key_point_1 = coord_dev.all_ls[index]
    # key_point_1.special = True
    # # 添加特殊点
    # coord_dev.shoot_ls.append(key_point)
    #
    # coord_dev.shoot()
    # coord_dev.ob_ls = [item for item in coord_dev.all_ls if item not in coord_dev.shoot_ls and not item.special]
    # coord_dev.show_shoot()
    # coord_std.running(show=True)
    # print(key_point)
    # coord_dev.running(show=True)
    # h = Handle_angle(coord_dev.ob_ls, coord_std.ob_ls)
    # h.compare()
    data.to_excel("第二次.xlsx")


calculate()
