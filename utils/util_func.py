# -*- coding: utf-8 -*-

import re


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


def filter_emoji(desstr, restr=''):
    '''
    过滤emoji表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
