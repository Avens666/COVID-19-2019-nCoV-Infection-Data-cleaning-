# 本脚本是针对中国新冠病毒各省市历史发病数据的清洗工具
# 作者 https://github.com/Avens666  mail: cz_666@qq.com
# 数据源使用 https://github.com/BlankerL/DXY-COVID-19-Data/blob/master/csv/DXYArea.csv
# 输入源数据来自 data_step1.py 的输出文件
# 本脚本基于data_step1.py的输出 计算每天的新增数据，源数据只有每天的累计确诊数据，本脚本通过当天数据减去前一天数据的方式，计算出每天新增数据
# 用户通过修改 inputfile  和  outputfile 定义源数据文件和输出文件

from datetime import timedelta

import pandas

inputfile = "out1.csv"
outputfile = "out_2_18.csv"
# 显示所有列
pandas.set_option('display.max_columns', None)
# 显示所有行
pandas.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pandas.set_option('max_colwidth', 200)

# ！！！ 根据需要选择合适的字符集
try:
    dataf = pandas.read_csv(inputfile, encoding='UTF-8')
except:
    dataf = pandas.read_csv(inputfile, encoding='gb2312')

# 计算增量 根据日期间隔计算

dataf['日期'] = pandas.to_datetime(dataf['日期'], format='%Y-%m-%d')  # 1900 -> 2020

df_t = dataf['日期']
df_date = df_t.drop_duplicates()  # 去重 这个返回Series对象

# dataf['新增确诊'] = dataf['确诊']
dataf.insert(loc=6, column='新增确诊', value=0)
dataf.insert(loc=7, column='新增治愈', value=0)
dataf.insert(loc=8, column='新增死亡', value=0)

# df_date = df_date.sort_values(ascending=False)
min_date = df_date.min()
cur_date = df_date.max()

df_t = pandas.DataFrame()

for index, data in dataf.iterrows():
    # if data['日期'] != min_date:
        data2 = dataf.loc[
                (dataf['省'] == data['省']) & (dataf['市'] == data['市']) & (dataf['日期'] == data['日期'] - timedelta(days=1)),
                :]
        # 判断后一天是否存在
        data3 = dataf.loc[
                (dataf['省'] == data['省']) & (dataf['市'] == data['市']) & (dataf['日期'] == data['日期'] + timedelta(days=1)),
                :]

        if data2.shape[0] > 0:
            dataf.loc[index, '新增确诊'] = data['确诊'] - data2.iloc[0, :]['确诊']
            dataf.loc[index, '新增治愈'] = data['治愈'] - data2.iloc[0, :]['治愈']
            dataf.loc[index, '新增死亡'] = data['死亡'] - data2.iloc[0, :]['死亡']
        else:
            dataf.loc[index, '新增确诊'] = data['确诊']
            dataf.loc[index, '新增治愈'] = data['治愈']
            dataf.loc[index, '新增死亡'] = data['死亡']

        if (data['日期'] != cur_date) & (data3.shape[0] == 0):  # 后一天如果没有数据，加一条冲抵数据
            new = pandas.DataFrame({'省': data['省'],
                                    '省确诊': data['省确诊'],
                                    '省治愈': data['省治愈'],
                                    '省死亡': data['省死亡'],
                                    '市': data['市'],
                                    '新增确诊': 0 - data['确诊'],
                                    '新增治愈': 0 - data['治愈'],
                                    '新增死亡': 0 - data['死亡'],
                                    '确诊': 0,
                                    '治愈': 0,
                                    '死亡': 0,
                                    '日期': data['日期'] + timedelta(days=1)},
                                   pandas.Index(range(1)))
            #            print(new.head())
            df_t = df_t.append(new)
    # else:
    #     dataf.loc[index, '新增确诊'] = data['确诊']
    #     dataf.loc[index, '新增治愈'] = data['治愈']
    #     dataf.loc[index, '新增死亡'] = data['死亡']
#    print(data['日期'])  # 输出处理进度

out = dataf.append(df_t, sort=False)

out.to_csv(outputfile, encoding="utf_8_sig")  # 为保证excel打开兼容，输出为UTF8带签名格式
