import random
import time

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tqdm
from django.core.files import temp

# 假设的基准需求量和价格


path = r'C:\Users\17264\Desktop\数学建模\pythonProject1\问题三最后数据.xlsx'
df1 = pd.read_excel(path)

def demand_function(P, Q0, P0, PED):
    return Q0 * (P0 / P) ** PED


def revenue_function(P, Q0, P0, PED):
    return P * demand_function(P, Q0, P0, PED)


def simulated_annealing(Q0, P0, PED, initial_price, min_price, max_price, initial_temp, cooling_rate, max_iter):
    current_price = initial_price
    current_revenue = revenue_function(current_price, Q0, P0, PED)
    temp = initial_temp

    price_history = [current_price]
    revenue_history = [current_revenue]

    for i in range(max_iter):
        new_price = np.random.uniform(min_price, max_price)
        new_revenue = revenue_function(new_price, Q0, P0, PED)

        # 接受新状态的概率
        acceptance_prob = np.exp((new_revenue - current_revenue) / temp)

        if new_revenue > current_revenue or np.random.rand() < acceptance_prob:
            current_price = new_price
            current_revenue = new_revenue

        price_history.append(current_price)
        revenue_history.append(current_revenue)

        temp *= cooling_rate  # 降低温度

    return current_price, current_revenue, price_history, revenue_history

def calculate():
    table = {}
    for index, row in tqdm.tqdm(df1.iterrows()):
        name = row['单品名称']
        id_num = row['单品编码']
        data_agg = list(map(float, row['合并后的数据'].split(' ')))
        eltricity = row['价格弹性系数']
        print(data_agg)
        revenue_get = []
        price_get = [0]
        best_quanity = data_agg[0]
        for index,item in enumerate(data_agg):
            Q0 = item
            P0 = random.randint(8,12)
            PED = -eltricity  # 负值表示需求量随价格增加而减少
            # 参数设置
            initial_price = 10
            min_price = 1
            max_price = 20
            initial_temp = 1000
            cooling_rate = 0.95
            max_iter = 1000

            optimal_price, optimal_revenue, price_history, revenue_history = simulated_annealing(Q0, P0, PED, initial_price,
                                                                                                 min_price, max_price, initial_temp,
                                                                                                 cooling_rate, max_iter)

            # 绘制图表
            plt.figure(figsize=(12, 6))

            # 价格变化图
            plt.subplot(1, 2, 1)
            plt.plot(price_history, label='Price')
            plt.xlabel('Iteration')
            plt.ylabel('Price')
            plt.title('Price Changes During Simulated Annealing')
            plt.legend()


            # 收益变化图
            plt.subplot(1, 2, 2)
            plt.plot(revenue_history, label='Revenue', color='orange')
            plt.xlabel('Iteration')
            plt.ylabel('Revenue')
            plt.title('Revenue Changes During Simulated Annealing')
            plt.legend()

            plt.tight_layout()
            # plt.savefig(rf'C:\Users\17264\Desktop\数学建模\pythonProject1\ 问题三最后数据\{name}单品第{index}预测.png')
            # time.sleep(3)
            print(f"Optimal Price: {optimal_price:.2f}")
            print(f"Optimal Revenue: {optimal_revenue:.2f}")
            if optimal_price>price_get[-1]:
                best_quanity = item
            price_get.append(optimal_price)
            revenue_get.append(optimal_revenue)
        table[name] = [max(price_get),best_quanity,max(revenue_get)]
    print(table)

# calculate()
s ={'海鲜菇(包)': [19.996640234083596, 8.69, 868.0993200455231], '金针菇(盒)': [19.99995713757838, 10.4, 4112.222653483811], '洪湖藕带': [19.99950539588958, 3.82, 558.5480556164141], '红椒(2)': [19.999243442090545, 9.48, 1702.139123208032], '枝江青梗散花': [19.99906930030479, 3.21, 2022.180138138267], '姜蒜小米椒组合装(小份)': [19.999183962229623, 4.0, 382.92961369979054], '七彩椒(2)': [19.997254570792222, 1.72867170344354, 149.66012838318747], '螺丝椒(份)': [19.99771390304413, 8.6031125444041, 3407.5717793131366], '小皱皮(份)': [19.997097698284108, 10.9442168631532, 1726.1299505852855], '小米椒(份)': [19.99777807737518, 16.5511422140881, 5117.033263145325], '云南油麦菜(份)': [19.988669744787064, 14.657320244401, 2758.9559453368465], '云南生菜(份)': [19.994706462021853, 19.2683798865183, 8718.176808703864], '小青菜(1)': [19.996699507791245, 4.15363525456224, 473.14471718808915], '长线茄': [19.99912089831281, 0.874870464144854, 158.18733133721938], '芜湖青椒(1)': [19.999217198596565, 11.3751464677182, 5544.305787865419], '奶白菜': [19.99889917794634, 8.96347990504841, 1421.5358692299762], '菱角': [19.99302848890144, 1.65375637696019, 186.91717900949126], '螺丝椒': [19.9997984501128, 4.6981355229769, 2569.2772781275485], '红薯尖': [19.999733771612995, 3.4365652806873, 3653.0972342651007], '娃娃菜': [19.99807197345987, 9.53801338604256, 904.2371710379736], '净藕(1)': [19.999218567009162, 4.37562438719049, 48701.10667011702], '西兰花': [19.9999341873757, 9.25018961675413, 100608.1979007789], '紫茄子(2)': [19.998840299912885, 15.9290330457876, 3403.7807884995814], '木耳菜': [19.99846612092893, 7.14067983864469, 805.7852360427328], '上海青': [19.997897044341055, 13.7286631331451, 4992.8494058050355], '苋菜': [19.996059079290003, 9.77374642241661, 2399.0359367200344], '西峡花菇(1)': [19.999145657156863, 3.15746788736696, 2548.4238677026124]}
d1 = pd.DataFrame(s)
d1.to_excel('问题三表格.xlsx')