# -*- coding: utf-8 -*-

from collections import Counter


class Account(object):

    def __init__(self):
        # 证券头寸, 表示当前证券头寸中持有的证券，包含停牌证券
        # 字典，键为证券代码，值为持有的证券数量。
        self.avail_secpos = None
        # 现金头寸
        self.cash = None
        # 当前回测日期
        # datetime
        self.current_date = None
        # 前一交易日
        # datetime
        self.previous_date = None
        # 使用account.cash，account.referencePrice和account.avail_secpos
        # 计算出的整个策略当前的参考价值
        self.referencePortfolioValue = None
        # 证券参考价，一般使用的是上一日复权收盘价
        # 字典，键为证券代码，值为价格（浮点）
        self.referencePrice = None
        # 证券的参考收益率，一般使用的是上一日收益率
        # 字典，键为证券代码，值为收益率（浮点）
        self.referenceReturn = None
        # 表示当前交易日的证券池
        # 从全局变量universe和当前持有的证券池中，剔除了当天停牌、退市和数据异常证券的证券池
        # list
        self.universe = None
        # 表示调仓后的新证券头寸
        self.new_avail_secpos = None

    def order(self, ticker, amount):
        '''买入（卖出）数量为amount的股票ticker'''
        pass

    def order_to(self, ticker, amount):
        '''买入（卖出）一定量的股票使得股票ticker交易后的数量为amount'''
        pass

    def order_weight(self, ticker, weight):
        '''买入（卖出）一定量的股票使得股票ticker交易后的权重占比为weight'''
        self.new_avail_secpos[ticker] = weight
        pass

    def before_handle_data(self):
        self.new_avail_secpos = self.avail_secpos.copy()
        pass

    def after_handle_data(self):
        self.avail_secpos = self.new_avail_secpos
        pass

    def calculate_turnover(self):
        weight_sum = sum(self.new_avail_secpos.values())
        for key in self.new_avail_secpos:
            self.new_avail_secpos[key] = self.new_avail_secpos[key] / weight_sum
        avail_secpos_cnt, new_avail_secpos_cnt = Counter(self.avail_secpos), Counter(self.new_avail_secpos)
        turnover_dict = dict(new_avail_secpos_cnt - avail_secpos_cnt)
        turnover = 0.5 * sum([abs(num) for num in turnover_dict.values()])
        return turnover
