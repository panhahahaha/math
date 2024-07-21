import sys

import numpy as np
import tqdm
from scipy.optimize import linprog
import pandas as pd
from sklearn.linear_model import LinearRegression

import statsmodels.api as sm
from scipy.stats import norm

from sklearn.preprocessing import OneHotEncoder
import numpy as np
from scipy.optimize import minimize
list_class= ['水生根茎类.xlsx','花叶类.xlsx','花菜类.xlsx','茄类.xlsx','辣椒类.xlsx','食用菌.xlsx']
path_file = '成本加销量汇总.xlsx'
data = pd.read_excel(path_file)[['销售日期', '单品编码', '销售单价(元/千克)', '销量(千克)', '批发价格(元/千克)']]
# 定义数据
# costs = np.array([10, 8, 12, 9, 11, 7])  # 进货成本
# prices = np.array([15, 14, 18, 13, 16, 12])  # 销售价
# demands = np.array([50, 40, 60, 45, 55, 35])  # 预测需求量
# min_display = np.array([2.5, 2.5, 2.5, 2.5, 2.5, 2.5])  # 最小陈列量
# def get_data():
#
# # 计算单位收益
# profits = prices - costs
#
# # 定义目标函数（最大化总收益）
# c = -profits  # linprog求解最小化问题，所以取负号
#
# # 定义不等式约束
# A_ub = np.vstack([
#     -np.eye(len(demands)),  # 每种蔬菜的订货量不能超过需求量
#     np.eye(len(demands))  # 每种蔬菜的订货量至少满足最小陈列量
# ])
# b_ub = np.hstack([
#     -min_display,  # 最小陈列量约束
#     demands  # 需求量约束
# ])
#
# # 定义等式约束
# A_eq = np.ones((1, len(demands)))  # 总订货量约束
# b_eq = [30]  # 假设我们要订货的总量是30公斤，可以根据实际情况调整
#
# # 求解线性规划问题
# result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
#
# # 输出结果
# if result.success:
#     print("最佳订货组合:")
#     for i, x in enumerate(result.x):
#         print(f"蔬菜{i+1} 订货量: {x:.2f} 公斤")
#     print(f"最大总收益: {-result.fun:.2f} 元")
# else:
#     print("无法找到可行的订货组合")
path1 = '附件3.xlsx'  # 成本
path2 = '成本加销量汇总.xlsx'  # 销量
path3 = '附件4.xlsx'


def merge():
    new_path = '优化后成本与销量.xlsx'
    new_path_1 = '成本加销量汇总加损耗率.xlsx'
    table1 = pd.read_excel(path1)
    table2 = pd.read_excel(path2)
    table3 = pd.read_excel(path3)
    merged_df = pd.merge(table2[['销售日期', '单品编码', '销售单价(元/千克)', '销量(千克)']], table3,
                         left_on=['单品编码'],
                         right_on=['单品编码'],
                         how='left')

    # grouped_df = table2.groupby(['销售日期', '单品编码', '销售单价(元/千克)']).agg({'销量(千克)': 'sum'}).reset_index()
    # grouped_df.to_excel(new_path)
    merged_df.to_excel(new_path_1)

def c_Price_elasticity_change(average_price, average_request, dynamic_price, dynamic_request):
    if dynamic_price == 0:
        dynamic_price = 1
    if dynamic_request == 0:
        dynamic_request = 1
    elasticity_change = (average_request / dynamic_request) / (average_price / dynamic_price)
    return elasticity_change
def f_1():
    # path = f'种类数据\\{item}'
    # install_path = f'种类数据1\\{item}'
    for item in range(1,19):
        path = rf'data\data_{item}.xlsx'
        install_path = rf'data\数据分析\data_{item}.xlsx'
        data_0 = pd.read_excel(path)
        df = pd.DataFrame(data_0)


        # 分组聚合
        summary = df.groupby('单品编码').agg({
            '销售单价(元/千克)': lambda x: list(x),
            '销量(千克)': lambda x: list(x),
        }).reset_index()

        # 计算变化率
        summary['销售单价变化率'] = summary['销售单价(元/千克)'].apply(
            lambda x: [(x[i] - x[i - 1]) / x[i - 1] if i > 0 else None for i in range(len(x))]
        )

        summary['销量变化率'] = summary['销量(千克)'].apply(
            lambda x: [(x[i] - x[i - 1]) / x[i - 1] if i > 0 else None for i in range(len(x))]
        )

        # 计算变化率的平均值
        summary['销售单价变化率平均'] = summary['销售单价变化率'].apply(
            lambda x: sum(filter(None, x)) / (len(x) - 1) if len(x) > 1 else 0
        )

        summary['销量变化率平均'] = summary['销量变化率'].apply(
            lambda x: sum(filter(None, x)) / (len(x) - 1) if len(x) > 1 else 0
        )

        # 计算所有单品编码的平均变化率
        总体销售单价变化率平均 = summary.loc[summary['销售单价变化率平均'] != 0, '销售单价变化率平均'].mean()
        总体销量变化率平均 = summary.loc[summary['销量变化率平均'] != 0, '销量变化率平均'].mean()

        # 替换为所有单品编码的平均变化率
        summary['销售单价变化率平均'] = summary['销售单价变化率平均'].replace(0, 总体销售单价变化率平均)
        summary['销量变化率平均'] = summary['销量变化率平均'].replace(0, 总体销量变化率平均)

        print(summary)
        summary.to_excel(install_path)
    sys.exit()
f_1()
def f_0():
    for item in list_class:
        path = f'种类数据\\{item}'
        install_path = f'种类数据1\\{item}'
        data_0 = pd.read_excel(path)
        df = pd.DataFrame(data_0)

        summary = df.groupby('单品编码').agg({
            '销售单价(元/千克)': lambda x: list(x),
            '销量(千克)': lambda x: list(x),
            '批发价格(元/千克)': lambda x: list(x)
        }).reset_index()

        def average(lst):
            return sum(lst) / len(lst)

        # summary['平均批发价格(元/千克)','平均销售单价(元/千克)','平均销量(千克)'] = [summary['批发价格(元/千克)'].apply(average),summary['销售单价(元/千克)'].apply(average),summary['销量(千克)'].apply(average)]
        # 为每一列计算平均值并赋值
        summary['平均批发价格(元/千克)'] = summary['批发价格(元/千克)'].apply(average)
        summary['平均销售单价(元/千克)'] = summary['销售单价(元/千克)'].apply(average)
        summary['平均销量(千克)'] = summary['销量(千克)'].apply(average)
        summary.to_excel(install_path)
# f_0()
# merge()
def search():
    path_file = '成本加销量汇总.xlsx'
    path_file_1 = '切割实验数据.xlsx'
    path_file_2 = '附件1.xlsx'
    data = pd.read_excel(path_file)[['销售日期', '单品编码', '销售单价(元/千克)', '销量(千克)', '批发价格(元/千克)']]
    data1 = pd.read_excel(path_file_2)

    df1 = pd.DataFrame(data)
    df2 = pd.DataFrame(data1)

    # 将第二个表格数据按分类名称分组
    grouped_df2 = df2.groupby('分类名称')

    # 创建一个字典存储不同分类的数据
    dfs = {name: group for name, group in grouped_df2}

    # 合并数据
    for category, group_df in dfs.items():
        merged_df = pd.merge(group_df, df1, on='单品编码', how='left')
        merged_df.to_excel(f'种类数据\\{category}.xlsx', index=False)
    # 汇总同一单品的销售单价、销量和批发价格
    df = pd.DataFrame(data)

    summary = df.groupby('单品编码').agg({
        '销售单价(元/千克)': lambda x: list(x),
        '销量(千克)': lambda x: list(x),
        '批发价格(元/千克)': lambda x: list(x)
    }).reset_index()
    def average(lst):
        return sum(lst) / len(lst)
    # summary['平均批发价格(元/千克)','平均销售单价(元/千克)','平均销量(千克)'] = [summary['批发价格(元/千克)'].apply(average),summary['销售单价(元/千克)'].apply(average),summary['销量(千克)'].apply(average)]
    # 为每一列计算平均值并赋值
    summary['平均批发价格(元/千克)'] = summary['批发价格(元/千克)'].apply(average)
    summary['平均销售单价(元/千克)'] = summary['销售单价(元/千克)'].apply(average)
    summary['平均销量(千克)'] = summary['销量(千克)'].apply(average)
    for index,row in summary.iterrows():
        price_list = row['销售单价(元/千克)']
        quantity_list = row['销量(千克)']
        average_price = row['平均销售单价(元/千克)']
        average_quantity = row['平均销量(千克)']
        all_thing = list(zip(price_list, quantity_list))
        num = 0
        for price,quanity in all_thing:

            num += c_Price_elasticity_change(average_price, average_quantity, price, quanity)
        num/=len(price_list)

        print(num)
    summary.to_excel('汇总数据——售价成本---实验品.xlsx')

    print(summary)
    # num_list = data['单品编码']
    # num_list = num_list.values.tolist()
    # new_data = pd.DataFrame(
    #     {'单品编码': [], '销售单价(元/千克)': [], '销量(千克)': [], '销售日期': [], '批发价格(元/千克)': []})
    # print(num_list)
    # has_list = []
    # for i in tqdm.tqdm(num_list):
    #     if i in new_data['单品编码']:
    #
    #         row = df[df['单品编码'] == i]
    #         price = df[df['单品编码'] == i]['销售单价(元/千克)'],
    #         quantify = df[df['单品编码'] == i]['销量(千克)'],
    #         data = df[df['单品编码'] == i]['销售日期'],
    #         # new_data.loc[df['单品编码'] == i, ['销量(千克)','售价','日期'] = row['']
    #         new_data.loc[df['单品编码'] == i, '销量(千克)'] = df.loc[df['单品编码'] == i, '销量(千克)'].apply(lambda x: x + [quantify])
    #         new_data.loc[df['单品编码'] == i, '销售单价(元/千克)'] = df.loc[df['单品编码'] == i, '销售单价(元/千克)'].apply(lambda x: x + [price])
    #         new_data.loc[df['单品编码'] == i, '销售日期'] = df.loc[df['单品编码'] == i, '销售日期'].apply(lambda x: x + [data])
    #
    #         # 查看结果
    #     else:
    #         new_row = {
    #             '单品编码': i,
    #             '销售单价(元/千克)': [df[df['单品编码'] == i]['销售单价(元/千克)'],],
    #             '销量(千克)': [df[df['单品编码'] == i]['销量(千克)'],],
    #             '销售日期': [df[df['单品编码'] == i]['销售日期'],],
    #             '批发价格(元/千克)': df[df['单品编码'] == i]['批发价格(元/千克)'],
    #         }
    #         df.loc[len(df)] = new_row
    #
    # print(new_data)
# search()
def f_1():
    def average(lst):
        return sum(lst) / len(lst)
    ever_goods = pd.DataFrame({'单品编号':[],'价格弹性系数':[]})
    class_dict = {}
    for item in tqdm.tqdm(list_class):
        road1 = f'种类数据1\\{item}'
        summary = pd.read_excel(road1)
        class_dict[item] = []
        for index,row in summary.iterrows():
            id_num = row['单品编码']
            price_list = row['销售单价(元/千克)']
            price_list = eval(price_list)
            quantity_list = row['销量(千克)']
            quantity_list = eval(quantity_list)
            average_price = row['平均销售单价(元/千克)']
            average_quantity = row['平均销量(千克)']
            all_thing = list(zip(price_list, quantity_list))
            num = 0
            for price,quanity in all_thing:

                num += c_Price_elasticity_change(average_price, average_quantity, price, quanity)
            num/=len(price_list)
            ever_goods.loc[len(ever_goods)] = [id_num, num]



            class_dict[item].append(num)
    print(class_dict)
    ever_goods.to_excel("---单品弹性系数---.xlsx")
    for value,keys in class_dict.items():
        print('key is',keys,'and value is',value)
        print(f"{value} 的弹性系数为",average(class_dict[value]))
f_1()
def split_function():
    path_file = '成本加销量汇总.xlsx'
    data = pd.read_excel(path_file)[['销售日期', '单品编码', '销售单价(元/千克)', '销量(千克)', '批发价格(元/千克)']]
    start_date = pd.to_datetime('2020-07-01')
    end_date = pd.to_datetime('2020-07-06')

    # 获取日期范围内的数据
    filtered_df = data[(data['销售日期'] >= start_date) & (data['销售日期'] <= end_date)]
    filtered_df.to_excel('切割实验数据.xlsx', index=False)

    print(filtered_df)
# split_function()
def calculate1():
    df = pd.DataFrame(data)

    # 将销售日期列转换为日期时间类型
    df['销售日期'] = pd.to_datetime(df['销售日期'])

    # 检查并删除可能的重复行
    df = df.drop_duplicates()

    # 去除销售单价或销量为零或负数的行
    df = df[(df['销售单价(元/千克)'] > 0) & (df['销量(千克)'] > 0)]

    # 计算需求价格弹性
    df['log_销量'] = np.log(df['销量(千克)'])
    df['log_销售单价'] = np.log(df['销售单价(元/千克)'])

    X = sm.add_constant(df['log_销售单价'])
    y = df['log_销量']

    model = sm.OLS(y, X).fit()
    elasticity = model.params['log_销售单价']

    print(f'需求价格弹性: {elasticity}')

    # 设置参数
    价格 = 10  # 销售价格
    成本 = 7  # 采购成本
    剩余成本 = 3  # 库存剩余成本
    期望需求 = df['销量(千克)'].mean()
    需求标准差 = df['销量(千克)'].std()

    # 计算临界比率
    临界比率 = (价格 - 成本) / (价格 - 成本 + 剩余成本)

    # 计算最佳订购量
    最佳订购量 = norm.ppf(临界比率, loc=期望需求, scale=需求标准差)

    print(f'最佳订购量: {最佳订购量}')

    # 假设调整价格后
    调整后的销售单价 = df['销售单价(元/千克)'] * 1.1  # 增加10%的价格

    # 根据需求价格弹性计算新的需求量
    调整后的需求量 = df['销量(千克)'] * (调整后的销售单价 / df['销售单价(元/千克)']) ** elasticity

    # 计算调整后的收益
    调整后的收益 = 调整后的需求量 * 调整后的销售单价

    # 计算收益增量
    收益增量 = 调整后的收益.sum() - (df['销量(千克)'] * df['销售单价(元/千克)']).sum()

    print(f'收益增量: {收益增量}')


def calculate2():
    path_file = '成本加销量汇总.xlsx'
    data = pd.read_excel(path_file)

    df = pd.DataFrame(data)

    # 计算加成率
    df['加成率'] = (df['销售单价(元/千克)'] - df['批发价格(元/千克)']) / df['批发价格(元/千克)']

    # 定义自变量和因变量
    X = df['加成率']
    y = df['销量(千克)']

    # 添加常数项
    X = sm.add_constant(X)

    # 拟合回归模型
    model = sm.OLS(y, X).fit()

    # 查看模型摘要
    print(model.summary())

    # 定义未来一周的加成率
    future_markup = [0.3, 0.4, 0.5, 0.35, 0.45, 0.55, 0.5]  # 示例值

    # 创建未来一周的数据框架
    future_df = pd.DataFrame({'加成率': future_markup})

    # 添加常数项
    future_df = sm.add_constant(future_df)

    # 预测未来一周的销售量
    future_sales = model.predict(future_df)
    print(future_sales)

    # 计算未来一周的补货量（假设库存为0）
    future_stock = future_sales

    # 计算未来一周的定价（假设批发价格不变）
    future_pricing = (df['批发价格(元/千克)'][:len(future_markup)] * (1 + pd.Series(future_markup))).tolist()

    # 生成补货和定价策略表
    strategy = pd.DataFrame({
        '单品编码': df['单品编码'].unique()[:len(future_markup)],
        '补货量(千克)': future_stock,
        '定价(元/千克)': future_pricing
    })

    print(strategy)


def calculate3():
    path_file = '成本加销量汇总.xlsx'
    data = pd.read_excel(path_file)

    df = pd.DataFrame(data)

    # 计算加成率
    df['加成率'] = (df['销售单价(元/千克)'] - df['批发价格(元/千克)']) / df['批发价格(元/千克)']

    # 提取月份信息
    df['销售日期'] = pd.to_datetime(df['销售日期'])
    df['月份'] = df['销售日期'].dt.month

    # One-hot编码月份
    encoder = OneHotEncoder()
    months_encoded = encoder.fit_transform(df[['月份']]).toarray()
    months_encoded_df = pd.DataFrame(months_encoded, columns=[f'月份_{i}' for i in range(1, 13)])

    # 合并编码后的月份信息
    df = pd.concat([df, months_encoded_df], axis=1)

    # 分品类回归分析
    unique_items = df['单品编码'].unique()
    results = {}
    for item in unique_items:
        df_item = df[df['单品编码'] == item]
        X = df_item[['加成率'] + [f'月份_{i}' for i in range(1, 13)]]
        y = df_item['销量(千克)']

        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        results[item] = model
        print(f"单品编码 {item} 的回归模型结果：")
        print(model.summary())
        print("\n")

    # 预测未来一周的销售量
    future_markup = [0.3, 0.4, 0.5, 0.35, 0.45, 0.55, 0.5]  # 示例值
    future_month = 7  # 假设未来一周在7月

    future_data = {
        '加成率': future_markup,
        '月份': [future_month] * 7
    }

    future_df = pd.DataFrame(future_data)
    future_months_encoded = encoder.transform(future_df[['月份']]).toarray()
    future_months_encoded_df = pd.DataFrame(future_months_encoded, columns=[f'月份_{i}' for i in range(1, 13)])
    future_df = pd.concat([future_df, future_months_encoded_df], axis=1)
    future_df = sm.add_constant(future_df)

    future_stock = []
    future_pricing = []

    for item in unique_items[:len(future_markup)]:  # 这里假设unique_items数量和future_markup数量一致
        model = results[item]
        future_sales = model.predict(future_df)
        future_stock.append(future_sales)

        # 计算定价
        wholesale_price = df[df['单品编码'] == item]['批发价格(元/千克)'].iloc[0]
        pricing = wholesale_price * (1 + np.array(future_markup))
        future_pricing.append(pricing)

    # 生成补货和定价策略表
    strategy = pd.DataFrame({
        '单品编码': unique_items[:len(future_markup)],
        '补货量(千克)': np.mean(future_stock, axis=1),
        '定价(元/千克)': np.mean(future_pricing, axis=1)
    })

    print(strategy)


def check():
    for index, row in data.iterrows():
        a, b, c, d, e = row[['销售日期', '单品编码', '销售单价(元/千克)', '销量(千克)', '批发价格(元/千克)']]
        if not (d > 0):
            print(a, b, c, d, e)


# check()
def calculate4():
    df = pd.DataFrame(data)
    df['销售日期'] = pd.to_datetime(df['销售日期'])
    # 示例数据，确保没有缺失值
    X = df[['销售单价(元/千克)', '批发价格(元/千克)']]
    y = df['销量(千克)']

    # 删除包含 NaN 或无效值的行
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    y.replace([np.inf, -np.inf], np.nan, inplace=True)

    # 删除包含 NaN 的行
    X.dropna(inplace=True)
    y.dropna(inplace=True)

    # 确保 X 和 y 的行数匹配
    X = X.loc[y.index]

    # 转换为对数
    X_log = np.log(X)
    y_log = np.log(y)

    # 检查是否有无效值
    X_log.replace([np.inf, -np.inf], np.nan, inplace=True)
    y_log.replace([np.inf, -np.inf], np.nan, inplace=True)

    # 删除包含 NaN 的行
    X_log.dropna(inplace=True)
    y_log.dropna(inplace=True)

    # 确保 X_log 和 y_log 的行数匹配
    X_log = X_log.loc[y_log.index]

    # 回归分析
    reg = LinearRegression().fit(X_log, y_log)

    # 打印回归结果
    print("回归系数：", reg.coef_)
    print("截距：", reg.intercept_)

    # 预测函数
    # def predict_sales(price, base_price, base_quantity, elasticity):
    #     return base_quantity * (price / base_price) ** elasticity
    #
    # # 基准价格和销售量
    # base_price = df['销售单价(元/千克)'].mean()
    # base_quantity = df['销量(千克)'].mean()
    #
    # # 未来一周的销售量预测
    # predicted_sales = []
    # future_dates = pd.date_range(start='2023-07-01', end='2023-07-07')
    #
    # for date in future_dates:
    #     for product_id in df['单品编码'].unique():
    #         price = base_price  # 初始价格，可以根据策略调整
    #         quantity = predict_sales(price, base_price, base_quantity, price_elasticity)
    #         predicted_sales.append([date, product_id, price, quantity])
    #
    # predicted_sales_df = pd.DataFrame(predicted_sales, columns=['date', 'product_id', 'price', 'quantity'])
    #
    # # 优化定价策略
    # def revenue_function(prices, base_price, base_quantity, elasticity, costs):
    #     total_revenue = 0
    #     for i, price in enumerate(prices):
    #         quantity = predict_sales(price, base_price, base_quantity, elasticity)
    #         total_revenue += price * quantity - costs[i]
    #     return -total_revenue  # 取负值进行最小化
    #
    # # 初始价格
    # initial_prices = [base_price] * len(df['单品编码'].unique())
    # costs = df['批发价格(元/千克)'].mean()  # 平均成本，实际情况需要具体数据
    #
    # # 优化
    # result = minimize(revenue_function, initial_prices, args=(base_price, base_quantity, price_elasticity, costs),
    #                   bounds=[(cost, 2 * cost) for cost in df['批发价格(元/千克)']])
    #
    # optimal_prices = result.x
    #
    # # 计算最优补货总量
    # optimal_predicted_sales = []
    #
    # for i, product_id in enumerate(df['单品编码'].unique()):
    #     price = optimal_prices[i]
    #     quantity = predict_sales(price, base_price, base_quantity, price_elasticity)
    #     for date in future_dates:
    #         optimal_predicted_sales.append([date, product_id, price, quantity])
    #
    # optimal_predicted_sales_df = pd.DataFrame(optimal_predicted_sales,
    #                                           columns=['date', 'product_id', 'price', 'quantity'])
    #
    # # 计算每个蔬菜品类的日补货总量
    # daily_restock = optimal_predicted_sales_df.groupby(['date', 'product_id'])['quantity'].sum().reset_index()
    #
    # print(daily_restock)


calculate2()
calculate1()
calculate3()
calculate4()
