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
import datetime
import time
import re

def format_to_date(date):

    return date.format(TODAY=datetime.datetime.now())

    pass

if __name__=="__main__":
    date = "{TODAY}"
    print format_to_date(date)