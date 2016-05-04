# -*- coding: utf-8 -*-

def set_universe(universe_code):
	universe_code = universe.lower()
	pass


class Account(object):
    # 证券头寸, 表示当前证券头寸中持有的证券，包含停牌证券。
    # 字典，键为证券代码，值为持有的证券数量。
    avail_secpos = None
    # 现金头寸
    cash = None
    # 当前回测日期
    # datetime
    current_date = None
    # 前一交易日
    # datetime
    previous_date = None
    # 使用account.cash，account.referencePrice和account.avail_secpos
    # 计算出的整个策略当前的参考价值
    referencePortfolioValue = None
    # 证券参考价，一般使用的是上一日复权收盘价
    # 字典，键为证券代码，值为价格（浮点）
    referencePrice = None
    # 证券的参考收益率，一般使用的是上一日收益率
    # 字典，键为证券代码，值为收益率（浮点）
    referenceReturn = None
    # 表示当前交易日的证券池
    # 从全局变量universe和当前持有的证券池中，剔除了当天停牌、退市和数据异常证券的证券池
    # list
    universe = None

    def order(self, ticker, amount):
        '''买入（卖出）数量为amount的股票ticker'''
        pass

    def order_to(self, ticker, amount):
        '''买入（卖出）一定量的股票使得股票ticker交易后的数量为amount'''
        pass
