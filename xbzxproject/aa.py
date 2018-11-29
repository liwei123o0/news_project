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
import re

p=re.compile(r'[-,$()#+&*]')
str="asdasdfasd123123asd123-0asdafa&#009$dddy*h(iasdh), 78dhfasfi ,goodhi123fsdsdfasda"

#查找特定单个字符
m = re.findall(p, str)
print(m)

#分割。如果一篇文章当中，要一次去掉某些特定的符号，这句很有效率
subs = re.split(p, str)
print(" ".join(subs))
print str
#替换
print(re.sub(p, "替换内容", str))
