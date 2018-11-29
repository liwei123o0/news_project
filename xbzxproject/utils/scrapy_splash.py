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

lua_loadhtml = """
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return {
            html = splash:html(),
    }
end
"""
