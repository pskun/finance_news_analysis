# -*- coding: utf-8 -*-


def atoi(a):
    ''' 字符串转整型 '''
    try:
        a = int(a)
    except ValueError:
        a = None
    return a
    pass


def atof(f):
    ''' 字符串转浮点数 '''
    try:
        f = float(f)
    except ValueError:
        f = None
    return f
