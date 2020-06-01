# COVID-19-2019-nCoV-Infection-Data-cleaning-
针对新冠病毒疫情数据的清洗脚本和清洗后的数据。
在原有基础上增加对全世界各国的数据处理。

# 源数据说明
源数据使用 https://github.com/BlankerL 的 https://github.com/BlankerL/DXY-COVID-19-Data/blob/master/csv/DXYArea.csv
其定时从丁香园网站抓取的原始各地区上报数据

##### 感谢 BlankerL 的工作

原始数据格式如下<br/>
continentName | continentEnglishName | countryName | ountryEnglishName | provinceName | provinceEnglishName | province_zipCode | province_confirmedCount | province_suspectedCount | province_curedCount | province_deadCount | updateTime | cityName | cityEnglishName | city_zipCode | city_confirmedCount | city_suspectedCount | city_curedCount | city_deadCount
:-: | :-: | :-: | :-: | :-:| :-: | :-: | :-: | :-:| :-: | :-: | :-: | :-:| :-:| :-: | :-: | :-: | :-: | :-:
亚洲 | Asia | 中国 | China | 重庆市 | Chongqing | 500000 | 573 | 0 | 328 | 6 | 2020-02-23 07:18:21| 渝中区 | Yuzhong District|500103|20|0|15|0
欧洲 | Europe | 卢森堡 | Luxembourg | 卢森堡 | Luxembourg | 961004 | 335 | 0 | 0 | 4 | 2020-03-20 12:33:45 | NA | NA | NA | NA | NA | NA | NA


针对数据的改进：<br/>
1.原始数据每天都会多次抓取数据，同一个地区每天存在多条记录，因为原始统计数据并不是连续时效性的，各地区并不是按小时的时间段发布，因此每天只需要一条数据<br/>
2.源数据不能直观的看出中国的累计数量，只能看出各个省份的信息。
因此需要对中国与其他国家数据分开处理，通过累加各个省份的人数来得到中国的累计信息。其中境外输入数据也包含在中国的累计信息当中。<br/>


# 脚本说明
- world_data.py  对于中国，统计每个城市的信息和；对于其他国家，保留各个国家每天最新的一条数据
- data_step1.py  第一步处理 本脚本将各省市每天的数据进行去重处理，每个省市只保留最新的一条数据 （也可选择保留当天最大数值）
- data_step2.py  第二步处理 基于data_step1.py的输出文件， 计算每天的新增数据，通过当天数据减去前一天数据的方式，计算出每天新增数据

说明：各地区数据质量不同，同时存在后面修正前期数据，进行核销的处理，因此有时候当天数据会比前一天还少，新增数据为负

# Data说明
data 目录存放了清洗出的数据。<br/>
nCov_china_0312 是3月12日中国的数据。<br/>
nCov_world_0516 是5月16日全世界的数据。<br/>
输出数据格式如下
国家 | 确诊 | 治愈 | 死亡 | 日期
:-: | :-: | :-: | :-: | :-:
阿曼 | 19 | 2 | 0 | 2020-03-13

# 数据下载说明
由于raw.githubusercontent.com 被DNS污染，部分地区不能下载。大家可以试试我的百度云链接，数据更新到5月16号。
链接：https://pan.baidu.com/s/1QRaTV1OCTDDpLtuZ3JDtBA 
提取码：u2d1

# 缅怀
很难以想象冷冰冰的ASCII码代表了几百万鲜活的生命，我真是无比心痛。愿逝者安息，生者珍惜当下。
