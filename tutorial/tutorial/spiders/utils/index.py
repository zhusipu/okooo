# -*- coding: utf-8 -*-
def resultToFormat(result):
    if result == u"胜":
        result = 1
    if result == u"平":
        result = 2
    if result == u"负":
        result = 3
    return result