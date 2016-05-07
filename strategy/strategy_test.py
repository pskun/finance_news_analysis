# -*- coding: utf-8 -*-

import random

from back_test import set_universe

BENCH_INDEX = ['000300.SH', 'ALL']

# 回测起始日期
begdate = '20110101'
# 回测结束日期
enddate = '20160224'
# 调仓频率
refresh_rate = 30
# 基准股票池
bench_index = '000001.SH'
# 交易费率
cost = 0.0050

# 设置股票池
universe = set_universe('all')


def initialize(account):
    '''调整股票权重'''
    account.avail_secpos = dict(
        zip(account.universe, [0] * len(account.universe)))
    pass


def handle_data(account):
    # 本策略将使用account的以下属性：
    # account.referencePortfolioValue表示根据前收计算的当前持有证券市场价值与现金之和。
    # account.universe表示当天，股票池中可以进行交易的证券池，剔除停牌退市等股票。
    # account.referencePrice表示股票的参考价，一般使用的是上一日收盘价。
    # account.valid_secpos字典，键为证券代码，值为虚拟账户中当前所持有该股票的数量。
    for ticker in account.universe:
        account.order_weight(ticker, random.random())
    pass
