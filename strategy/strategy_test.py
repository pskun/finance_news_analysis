# -*- coding: utf-8 -*-

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
universe = set_universe('ZZ500')
'''
port_dir = ur'D:\dir'

########################
# load and prepare data
########################
### load price data ###
(price_stocks, price_tradingdates, close, adjf) = mydata.get_stock_trading_data(
    begdate, enddate, varnames_tuple=('close', 'adjf'))
price_adj_close = close * adjf
price_ret_mat = utrd.value2ret(price_adj_close)
bench_dates, bench_prices = mydata.get_index_close_prices(
    bench_index, begdate, enddate)
bench_rets = utrd.value2ret(bench_prices)

if True:
    price_ret_mat[np.isnan(price_ret_mat)] = 0
    bench_rets[np.isnan(bench_rets)] = 0

########################
# load portfolio data
########################
port_dates, date2port = pdata.load_dir_of_portfolio_csv_files_with_date_suffix(
    port_dir)

port_rets_dates, port_rets = \
    pdata.get_port_daily_returns(
        date2port, enddate, price_stocks, price_tradingdates, price_ret_mat, cost)

port_bench_rets = bench_rets[np.logical_and(
    bench_dates >= port_rets_dates[0], bench_dates <= port_rets_dates[-1])]

########################
# portfolio strategy
########################
port_rets_act = port_rets - port_bench_rets
port_values_act = utrd.ret2value(port_rets_act)[1:]

port_mean, port_std, port_ir, port_mdd = \
    np.mean(port_rets_act) * 240,
    np.std(port_rets_act) * np.sqrt(240),
    np.mean(port_rets_act) * np.sqrt(240) / np.std(port_rets_act),
    utrd.max_drawdown(port_values_act)
'''


def initialize(account):
    '''调整股票权重，权重列表序号与股票池列表序号对应'''
    weight = [20, 30, 10, 10, 10, 10, 10, ]
    account.avail_secpos = dict(zip(universe, weight))
    pass


def handle_data(account):
    # 本策略将使用account的以下属性：
    # account.referencePortfolioValue表示根据前收计算的当前持有证券市场价值与现金之和。
    # account.universe表示当天，股票池中可以进行交易的证券池，剔除停牌退市等股票。
    # account.referencePrice表示股票的参考价，一般使用的是上一日收盘价。
    # account.valid_secpos字典，键为证券代码，值为虚拟账户中当前所持有该股票的数量。
    pass
