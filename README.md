# COVID-19-2019-nCoV-Infection-Data-cleaning-
针对新冠病毒疫情数据的清洗脚本和清洗后的数据，

# 源数据说明
源数据使用 https://github.com/BlankerL 的 https://github.com/BlankerL/DXY-COVID-19-Data/blob/master/csv/DXYArea.csv
其定时从丁香园网站抓取的原始各地区上报数据

##### 感谢 BlankerL 的工作

原始数据格式如下

provinceName | provinceEnglishName | cityName | cityEnglishName | province_confirmedCount | province_suspectedCount | province_curedCount | province_deadCount | city_confirmedCount | city_suspectedCount | city_curedCount | city_deadCount | updateTime
:-: | :-: | :-: | :-: | :-:| :-: | :-: | :-: | :-:| :-: | :-: | :-: | :-:
河南省 | Henan | 信阳 | Xinyang | 1231 | 0 | 415 | 13 | 261 | 0 | 74 | 2 | 2020-02-16 11:48:34.832|

原始数据有两个不足
1. 原始数据每天都会多次抓取数据，同一个地区每天存在多条记录，因为原始统计数据并不是连续时效性的，各地区并不是按小时的时间段发布，因此每天只需要一条数据
2. 原始数据仅统计省和市的累计数据

针对这两个问题，我做了两个脚本来对数据进行清洗

# 脚本说明
- data_step1.py  第一步处理 本脚本将各省市每天的数据进行去重处理，每个省市只保留最新的一条数据 （也可选择保留当天最大数值）
- data_step2.py  第二步处理 基于data_step1.py的输出文件， 计算每天的新增数据，通过当天数据减去前一天数据的方式，计算出每天新增数据

说明：各地区数据质量不同，同时存在后面修正前期数据，进行核销的处理，因此有时候当天数据会比前一天还少，新增数据为负

# Data说明
data 目录存放了我直接清洗出的数据，方便大家使用，免得大家再配Python环境，去下载数据运行脚本。 源数据不翻墙好像还不能直接下载

里面csv是直接使用脚本导出的数据，后续每天争取更新

excel文件，是对数据源使用了透视图并增加了一些图表分析的结果

![ ]( https://pic1.zhimg.com/80/v2-2dbe34eddb2c6591546498062aec6c6b_hd.png )


2020.2.16 cz
