# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:李哥工作圈
@QQ:877129310
@VIP交流群:141342076
@version:V1.0
@var:
@note:

"""
import hashlib
import sys
import time

import requests
from faker import Faker
from lxml import etree

from item_fileds import item_fileds

reload(sys)
sys.setdefaultencoding("utf8")
fake = Faker(locale="zh_CN")

keywords = [u"716所", u"73071部队", u"JXUST", u"P3芃w#九淼=", u"七一六", u"万安", u"万年县", u"万载", u"三山区", u"三房巷", u"上上电缆",
            u"上栗", u"上犹", u"上饶", u"上饶县", u"上高", u"不良贷款", u"不良贷款", u"东乡区", u"东台", u"东平", u"东昌府", u"东明", u"东河区",
            u"东海县", u"东港区", u"东湖区", u"东至", u"东营", u"东阿", u"严酷", u"严酷", u"中信", u"中信银行", u"中国石油", u"中国银行", u"中石油",
            u"中行", u"丰县", u"丰城", u"临川", u"临朐", u"临沂", u"临沭", u"临泉", u"临淄", u"临清", u"临邑", u"丹徒", u"丹阳", u"丹阳市",
            u"义安", u"乐安", u"乐平", u"乐陵", u"九原区", u"九江", u"九江县", u"九江财校", u"九江财经职业学院", u"九江财院", u"九里区", u"乳山", u"于都",
            u"云联惠", u"云龙区", u"五段镇", u"五河", u"五莲", u"五邑大学", u"井冈山", u"井冈山干部学院", u"交税", u"交行", u"交行", u"交通银行",
            u"交通银行", u"京口", u"京口区", u"亭湖", u"亳州", u"人寿", u"人民币升值", u"人民币升值", u"人民币贬值", u"人民币贬值", u"人民银行", u"人民银行",
            u"人行", u"人行", u"从化", u"仪征", u"任城", u"伊利谣言", u"伊斯兰教", u"休宁", u"会昌", u"伤残军人", u"伤残军人", u"余干", u"佛教",
            u"供电", u"侯聚森", u"保险", u"信丰", u"信州", u"修宪", u"修改宪法", u"修水", u"假币", u"假币", u"偷税", u"偷税", u"光大银行", u"兖州",
            u"全南", u"全椒", u"八公山", u"六合", u"六安", u"兰山", u"兰陵", u"共青城", u"兴业", u"兴化", u"兴国", u"兴宏", u"农业发展银行",
            u"农业银行", u"农业银行", u"农信社", u"农信社", u"农发行", u"农商行", u"农商行", u"农商银行", u"农商银行", u"农村信用合作社", u"农村信用合作社",
            u"农村信用社", u"农村信用社", u"农村商业银行", u"农村商业银行", u"农行", u"农行", u"冠县", u"凤台", u"凤阳", u"分宜", u"刘国强", u"利津",
            u"利辛", u"包河", u"北塘", u"华夏银行", u"华安证券", u"华尔润", u"华泰", u"华菱", u"华菱星马", u"单县", u"南丰", u"南京", u"南京", u"电信",
            u"南城县", u"南康", u"南昌", u"南昌县", u"南昌大学", u"南昌学院", u"南昌教育学院", u"南昌教院", u"南昌职业学院", u"南沙区", u"南海新区", u"南谯",
            u"南通", u"南通", u"电信", u"南长", u"南陵", u"博兴", u"博山", u"博望区", u"卞平刚", u"印花税", u"即墨", u"历下", u"历城", u"县联社",
            u"句容", u"台儿庄", u"台山", u"叶集", u"合肥", u"吉安", u"吉安县", u"吉州", u"吉水", u"启东", u"吴中", u"吴江", u"周村区", u"周禄宝",
            u"和县", u"响水", u"商河", u"嘉祥", u"固镇", u"固阳", u"国家税务", u"国税", u"国税", u"土地使用税", u"土默特右旗", u"地方债", u"地方债",
            u"地方税务", u"地税", u"地税", u"坊子", u"垦利", u"埇桥", u"城阳", u"基督教", u"增值税", u"增城", u"声援", u"声援", u"夏津", u"大丰",
            u"大余", u"大观区", u"大通区", u"大通县", u"天业股份", u"天主教", u"天宁区", u"天柱山", u"天桥区", u"天河", u"天长市", u"天鹏海鲜",
            u"天鹏菜篮子", u"天鹏集团", u"天鹏食品", u"太仓", u"太和", u"太湖县", u"央行", u"央行", u"奉新", u"奎文", u"契税", u"如东", u"如意科技",
            u"如意集团", u"如皋", u"姑苏", u"姜堰", u"威海", u"婺源", u"存款保险", u"学生跳楼", u"学生跳楼", u"宁国", u"宁波", u"宁津", u"宁都",
            u"宁阳", u"安丘", u"安义", u"安和焦化", u"安庆", u"安源", u"安福", u"安远", u"安邦+吴小晖", u"宏村", u"宗教", u"宗教团体", u"宗教场所",
            u"宗教文化", u"定南", u"定远", u"定陶", u"宜丰", u"宜兴", u"宜春", u"宜秀", u"宜黄", u"宝应", u"宣城", u"宣州", u"宪法修改", u"宿城",
            u"宿州", u"宿松", u"宿豫", u"宿迁", u"宿迁", u"电信", u"寒亭", u"寻乌", u"寿光", u"寿县", u"寿险", u"射阳", u"小尖", u"小尖镇",
            u"少数民族", u"就业保障金", u"屯溪", u"山东大学", u"山亭", u"山大青岛", u"岚山", u"岳西", u"峄城", u"峡江", u"崂山", u"崇义", u"崇仁",
            u"崇安", u"崇川", u"崔爱国", u"巢湖", u"工商银行", u"工商银行", u"工行", u"工行", u"巨野", u"市北", u"市南", u"常州", u"常州", u"电信",
            u"常州大学", u"常州新北", u"常州轻工学院", u"常熟", u"常熟", u"奇瑞捷豹路虎", u"常熟", u"观致", u"常熟", u"通润", u"常熟", u"阿特斯", u"常轻院",
            u"平原县", u"平安保险", u"平度", u"平邑", u"平阴", u"广东发展银行", u"广东商业职业技术学校", u"广东商校", u"广东省商业技工学校", u"广东省商业职业技术学校",
            u"广丰区", u"广发", u"广州", u"广德", u"广昌", u"广陵", u"广饶", u"庆云", u"庐山", u"庐江", u"庐阳", u"庚辰钢铁", u"庚辰铸造", u"建湖",
            u"建行", u"建设税", u"建设银行", u"开平", u"弋江", u"弋阳", u"张家港", u"张店", u"强险", u"当涂", u"彭泽", u"徐加爱", u"徐加爱", u"徐州",
            u"徐州港华", u"微山", u"德兴市", u"德城", u"德安", u"德州", u"德龙镍业", u"徽商银行", u"徽州", u"怀宁", u"怀德学院", u"怀远", u"恒台",
            u"恩平", u"惠山", u"惠民县", u"成武", u"战备状态", u"战备状态", u"戚墅堰", u"房产税", u"所得税", u"打压", u"打压", u"扬中", u"扬州",
            u"扬州", u"电信", u"扬州职业大学", u"扬州职大", u"扬泰机场", u"扬职大", u"抚州", u"招商银行", u"招行", u"招远", u"捷士通", u"捷豹",
            u"文化事业建设费", u"文灿压铸", u"文登", u"新会", u"新余", u"新干", u"新建区", u"新沂", u"新泰", u"新浦", u"新野", u"旌德", u"无为县",
            u"无棣", u"无锡", u"无锡", u"电信", u"无锡天鹏", u"日照", u"昆山", u"昆都仑", u"昌乐", u"昌江区", u"昌邑", u"明光", u"明斯基时刻", u"易纲",
            u"星子县", u"景德镇", u"景焦集团", u"曲阜", u"曹县", u"望江县", u"李沧", u"村镇银行", u"杜集区", u"来安", u"杰瑞股份", u"杰瑞集团", u"枞阳",
            u"枣庄", u"柴桑", u"栖霞市", u"核电", u"桐城", u"梁山", u"梁溪", u"梦兰", u"槐荫", u"樟树", u"樟树市", u"横峰", u"歙县", u"武城",
            u"武宁", u"武进", u"殴打", u"殴打", u"民宗局", u"民族团结进步", u"民族宗教事务局", u"民族宗教局", u"民族艺术团", u"民生信用卡", u"民生银行", u"永丰",
            u"永修", u"永新", u"汝南县", u"江司", u"江海区", u"江理", u"江科大", u"江职院", u"江苏", u"中关村", u"江苏科大", u"江苏科技大学",
            u"江西司法警官职业学院", u"江西师大", u"江西师范大学", u"江西师范学院", u"江西环境工程职业学院", u"江西理工", u"江西科大", u"江西科技师大", u"江西科技师范",
            u"江西财经职业学院", u"江西财院", u"江西青年职业学校", u"江西青院", u"江都", u"江门", u"江阴", u"池州", u"汶上", u"沂南", u"沂水", u"沂源",
            u"沛县", u"沭阳", u"河东区", u"河口区", u"沾化", u"泉山区", u"泗县", u"泗水", u"泗洪", u"泗阳", u"波司登", u"泰兴", u"泰和", u"泰安",
            u"泰州", u"泰州", u"电信", u"泾县", u"洋河新区", u"洪泽县", u"济南", u"济宁", u"济阳", u"浔阳", u"浦东发展", u"浦发", u"浩淼安防", u"浮梁",
            u"海安", u"海州", u"海澜", u"海珠", u"海螺信息", u"海螺国际大酒店", u"海螺型材", u"海螺塑料", u"海螺川崎", u"海螺建材", u"海螺建筑", u"海螺新材料",
            u"海螺暹罗耐火", u"海螺水泥", u"海螺酒店", u"海螺集团", u"海门", u"海阳", u"海陵区", u"涟水", u"涡阳", u"润州", u"淄博", u"淄川", u"淮上",
            u"淮北", u"淮南", u"淮安", u"淮安", u"清河", u"淮安", u"电信", u"淮安区", u"淮安翔宇", u"淮阴", u"清浦", u"清真寺", u"渝水", u"港闸",
            u"湖口", u"湘东", u"湾里", u"溧阳", u"滁州", u"滕州", u"滞纳金", u"滨城", u"滨州", u"滨海", u"滨湖", u"滨湖", u"漏税", u"漏税",
            u"潍坊", u"潍城", u"潘功胜", u"潘集", u"潜山", u"濂溪", u"灌云", u"灌云县", u"灌南", u"灵璧", u"炉桥", u"烈山", u"烟台", u"烟叶税",
            u"牟平", u"牡丹区", u"玉山县", u"王大千", u"环翠", u"珠山", u"琅琊", u"理士", u"瑞年国际", u"瑞年科技", u"瑞昌", u"瑞金", u"瑶海",
            u"田家庵", u"田湾核电", u"申银万国", u"电力", u"电网", u"界首", u"番禺", u"疫苗", u"瘦西湖", u"白云区", u"白云鄂博矿区", u"盐城", u"盐城",
            u"电信", u"盐都", u"盱眙", u"相城", u"相山", u"省联社", u"省联社", u"真正老陆稿荐", u"睢宁", u"石台", u"石城", u"石拐", u"砀山", u"硕项湖",
            u"碧桂园", u"祁门", u"福山", u"禹会", u"禹城", u"税务", u"穆斯林", u"章丘", u"章贡", u"精日", u"繁昌", u"红豆", u"纳吧", u"绍兴",
            u"绩溪", u"罗庄区", u"翔宇教育", u"翔宇集团", u"耕地占用税", u"聊城", u"联勤保障中心", u"联合社", u"肖金学", u"肥东", u"肥城", u"肥西", u"胶州",
            u"舒城", u"芜湖", u"芝罘", u"芦溪", u"花山", u"花都区", u"苏州", u"苏州", u"电信", u"范一飞", u"茌平", u"荔湾", u"荣成", u"莒南",
            u"莒县", u"莘县", u"莱城", u"莱山", u"莱州", u"莱芜", u"莱西", u"莱阳", u"莲花县", u"菏泽", u"萍乡", u"营业税", u"萧县", u"蒙城",
            u"蒙阴", u"蓬江", u"蓬莱", u"薛城", u"蚌埠", u"蚌山", u"蛙宝网", u"蜀山区", u"补税", u"袁州", u"裕安", u"西湖区", u"西递", u"诸城",
            u"诺贝投资", u"诺贝置业", u"调节基金", u"谢家集", u"谯城", u"豫章师范学院", u"豫章师院", u"财险", u"购置税", u"贵池", u"费县", u"贾小涛",
            u"贾汪", u"资源税", u"资溪", u"赣县", u"赣州", u"赣州林校", u"赣榆", u"赣江", u"越秀", u"路虎", u"车船税", u"车险", u"辉强光伏", u"边延风",
            u"达尔罕茂明安联合旗", u"迎江区", u"进贤", u"连云区", u"连云港", u"连云港", u"电信", u"退伍军人", u"退伍军人", u"逃税", u"通商银行", u"遂川",
            u"道教", u"邗江", u"邮储", u"邮政储蓄", u"邮政银行", u"邱亚夫", u"邳州", u"邹城", u"邹平", u"郎溪", u"郑学峰", u"郓城", u"郭主席",
            u"郭主席", u"郭声琨", u"郭树清", u"郭树清", u"郯城", u"都昌", u"鄄城", u"鄱阳", u"金乡", u"金坛", u"金安", u"金寨", u"金峰钢帘", u"金湖",
            u"金溪", u"金融监管局", u"钢城区", u"钱月宝", u"铅山", u"铜官", u"铜山", u"铜陵", u"铜鼓县", u"锡山区", u"镇江", u"镇江", u"电信", u"镜湖",
            u"长丰", u"长岛", u"长江银行", u"长清", u"阜南", u"阜宁", u"阜阳", u"阳信", u"阳谷", u"附加税", u"陆地方舟", u"陈国忠", u"陈家港",
            u"陈港化工", u"陈雨露", u"陵县", u"陵城", u"雅邦", u"雨山", u"雪浪山", u"霍山", u"霍邱", u"青云谱", u"青原", u"青山区", u"青山湖", u"青岛",
            u"青州", u"青阳", u"靖安", u"靖江", u"颍上", u"颍东", u"颍州", u"颍泉", u"风范电力", u"食字路口", u"马俊健", u"马鞍山", u"高唐", u"高安",
            u"高密", u"高港", u"高邮", u"高青", u"鱼台", u"鸠江", u"鹤山", u"黄埔区", u"黄山", u"黄岛", u"黎川", u"黟县", u"齐河", u"龙利得",
            u"龙南", u"龙口", u"龙子湖"]

timeout = 60


def spider_weixin():
    orderno = "ZF20193195158qiaFzt"
    secret = "2dbbf0d00b7242b5ab9f9cd8cf1d1ceb"
    _version = sys.version_info
    is_python3 = (_version[0] == 3)
    ip = "forward.xdaili.cn"
    port = "80"
    ip_port = ip + ":" + port
    timestamp = str(int(time.time()))  # 计算时间戳
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
    if is_python3:
        string = string.encode()
    md5_string = hashlib.md5(string).hexdigest()  # 计算sign
    sign = md5_string.upper()  # 转换成大写
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
    proxy = {"http": "http://" + ip_port}
    for keyword in keywords:
        for i in xrange(1, 10, 1):
            url = "http://weixin.sogou.com/weixin?type=2&ie=utf8&query={}&tsn=1&ft=&et=&interation=&wxid=&usip=&page={}".format(
                keyword, i)
            header = {
                "Host": "weixin.sogou.com",
                "Referer": "http://weixin.sogou.com/weixin?type=2&ie=utf8&query={}&tsn=1&ft=&et=&interation=&wxid=&usip=&page={}".format(
                    keyword, i),
                "User-Agent": fake.user_agent(),
                "Proxy-Authorization": auth
            }
            try:
                txt = requests.post(url, headers=header, proxies=proxy, timeout=timeout, verify=False).content
                dom = etree.HTML(txt)
                sel = dom.xpath("//div[@class='txt-box']")
            except:
                print "#######error#########"
                with open("error.html", "w")as w:
                    w.write(txt)
                continue
            for s in sel:
                item = {}
                try:
                    uri = "https://weixin.sogou.com" + "".join(s.xpath("./h3/a/@href"))
                    pubtime = "".join(s.xpath("./div/@t"))
                    timestruct = time.localtime(int(pubtime))
                    pubdate = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
                    t = requests.get(uri, proxies=proxy,
                                     headers={"Proxy-Authorization": auth, "User-Agent": fake.user_agent()},
                                     timeout=timeout,
                                     verify=True).content
                    sel = etree.HTML(t)
                    item["url"] = uri
                    item["pubtime"] = pubdate
                    item['title'] = "".join(sel.xpath("//h2/text()")).strip()
                    item['content'] = "".join(sel.xpath("//div[@id='js_content']//p//text()")).strip()
                    item['keyword'] = "".join(sel.xpath("//span[@id='profileBt']/a//text()")).strip()
                    item["site_name"] = u"微信公众号"
                    md5 = hashlib.md5()
                    md5.update(uri)
                    url_md5 = md5.hexdigest()
                    item['url_md5'] = url_md5
                    item_fileds(item, "data_wemedia", debug=True)
                except:
                    print "#######error_fileds：%s#########" % uri
                    continue


if __name__ == "__main__":
    spider_weixin()
