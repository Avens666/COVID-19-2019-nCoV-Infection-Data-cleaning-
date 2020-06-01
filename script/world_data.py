# 本脚本是针对全球各个国家历史发病数据的清洗工具
# 作者 https://github.com/tiffanyXiaoqing  mail: tiffany_xiqoing@foxmail.com
# 源数据来自 https://github.com/BlankerL/DXY-COVID-19-Data/blob/master/csv/DXYArea.csv
# 用户通过修改 inputfile 和  utputfile 定义源数据文件和输出文件

import pandas
from datetime import timedelta
from datetime import datetime

input_file = "data3.13.csv"  # "data3.13.csv"
output_file = "testOut2.csv"

date_start = datetime(2020, 1, 24, 0, 0)

# 显示所有列
pandas.set_option('display.max_columns', None)
# 显示所有行
pandas.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pandas.set_option('max_colwidth', 200)

try:
    dataf = pandas.read_csv(input_file, encoding='UTF-8')
except:
    dataf = pandas.read_csv(input_file, encoding='gb2312')

#dataf = dataf[0:58]   #截取100行测试
dataf['updateTime'] = pandas.to_datetime(dataf['updateTime'])
dataf['date'] = dataf['updateTime'].apply(lambda x: x.strftime('%Y-%m-%d'))  #返回以可读字符串表示的当地时间
dataf['date'] = pandas.to_datetime(dataf['date'])

# 提取国家列表，包括中国和外国
df_c = dataf['countryName']
df_country = df_c.drop_duplicates()  # 去重 这个返回Series对象
# 提取省份列表，包括中国和外国
df_province = dataf['provinceName']
df_province = df_province.drop_duplicates()  # 去重 这个返回Series对象

df = pandas.DataFrame(index=None) #最后的结果

df_t = dataf['date']
df_date = df_t.drop_duplicates()  # 去重 返回Series对象
df_date = df_date.sort_values()

NewList = []
#中国和外国分开计算，如果是中国，那么则统计所有城市相加结果
for date_t in df_date:
    for name in df_country:
        print(date_t.strftime('%Y-%m-%d') + name)  # 输出处理进度
        if name == '中国':
            china_confirmedCount = 0
            china_curedCount = 0
            china_deadCount = 0
            for province in df_province:
                df2 = dataf.loc[(dataf['countryName'].str.contains(name)) & (dataf['provinceName'].str.contains(province)) & (dataf['date'] == date_t),:]  # 通过索引标签来筛选数据
                if df2.empty:
                    continue
                df2 = df2.loc[(df2['updateTime'] == df2['updateTime'].max()), ['province_confirmedCount', 'province_curedCount', 'province_deadCount']]  # 筛出时间上的最后数据
                df2 = df2.drop_duplicates()
                print(df2)
                # 将所有省份数据求和即得到整个中国得数据
                china_confirmedCount += df2['province_confirmedCount'].values
                china_curedCount += df2['province_curedCount'].values
                china_deadCount += df2['province_deadCount'].values

            new = pandas.DataFrame({'国家': name,
                                    '确诊': china_confirmedCount.astype(int),
                                    '治愈': china_curedCount.astype(int),
                                    '死亡': china_deadCount.astype(int),
                                    '日期': date_t},
                                   pandas.Index(range(1))
                                   )
            NewList.append(new)

        else:
            df1 = dataf.loc[(dataf['countryName'].str.contains(name)) & (dataf['date'] == date_t), :]  # 通过索引标签来筛选数据
            if df1.empty:
                continue
            df1 = df1.loc[(df1['updateTime'] == df1['updateTime'].max()), :]  # 筛出国家的最后数据

            # 数据当中的国家确诊人数仍然是用province表示的
            province_confirmedCount = df1['province_confirmedCount'].max()
            province_curedCount = df1['province_curedCount'].max()
            province_deadCount = df1['province_deadCount'].max()

            new = pandas.DataFrame({'国家': name,
                                    '确诊': province_confirmedCount.astype(int),
                                    '治愈': province_curedCount.astype(int),
                                    '死亡': province_deadCount.astype(int),
                                    '日期': date_t},
                                   pandas.Index(range(1))
                                   )
            NewList.append(new)

df = df.append(NewList)
df = df.dropna()
df.to_csv(output_file, encoding="utf_8_sig", index=False)  # 为保证excel打开兼容，输出为UTF8带签名格式