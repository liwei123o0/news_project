# -*- coding: utf-8 -*-
# ! /usr/bin/env python

"""
@author:LiWei
@license:LiWei
@contact:877129310@qq.com
@version:
@var:
@note:

"""
import pytesseract
from PIL import Image

image = Image.open('D:\\news_project\\6.jpg')
code = pytesseract.image_to_string(image)
print code
