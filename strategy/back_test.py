# -*- coding: utf-8 -*-

import os
from datetime import datetime
import pandas as pd

from account import Account
from strategy_test import *

PRICES_COL_NAME = ['tradedate', 'ticker', 'adjpreclose', 'adjopen', 'adjclose', 'adjfactor', 'tradestatus']
PRICES_DATA_TYPE = {
    'ticker': str,
    'adjpreclose': float,
    'adjopen': float,
    'adjclose': float,
    'adjfactor': float,
    'tradestatus': str
}

account = Account()

# 市场交易日期
trading_dates = []
# 股票价格
ticker_prices = None
# 股票停复牌信息
ticker_suspend_info = None
# 基准股票价格
benchmark_prices = None


def load_trading_dates():
    trading_dates_file = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], 'data/trading_days.csv')
    for line in open(trading_dates_file):
        date = datetime.strptime(line.strip(), '%Y%m%d')
        trading_dates.append(date)
    pass


def load_ticker_prices():
    ticker_prices_file = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], 'data/prices.csv')
    ticker_prices = pd.read_csv(
        ticker_prices_file,
        header=None, names=PRICES_COL_NAME, dtype=PRICES_DATA_TYPE)
    ticker_prices['tradedate'] = pd.to_datetime(ticker_prices['tradedate'], format='%Y%m%d')
    ticker_prices.set_index('tradedate', inplace=True)
    ticker_prices = ticker_prices[begdate: enddate]
    ticker_prices['return'] = ticker_prices['adjclose'] / ticker_prices['adjpreclose']
    ticker_prices = ticker_prices[['ticker', 'return']]
    pass


def load_bench_mark():
    if bench_index != 'ALL':
        # 某一个指数作为benchmark
        benchmark_prices_file = os.path.join(
            os.path.split(os.path.realpath(__file__))[0], 'data/%s.csv' % bench_index)
        benchmark_prices = pd.read_csv(
            benchmark_prices_file,
            header=None, names=['tradedate', 'close', 'pctchange'])
        benchmark_prices['tradedate'] = pd.to_datetime(benchmark_prices['tradedate'], format='%Y%m%d')
        benchmark_prices.set_index('tradedate', inplace=True)
        benchmark_prices = benchmark_prices[begdate: enddate]
        benchmark_prices['pctchange'] = (1 + benchmark_prices['pctchange'] / 100)
    else:
        # 全市场股票作为benchmark
        ticker_prices.reset_index('tradedate', inplace=True)
        group_by_date = ticker_prices.groupby('tradedate')
        benchmark_prices['pctchange'] = group_by_date['return'].mean()
    benchmark_prices['cumchange'] = benchmark_prices['pctchange'].cumprod()
    pass


def load_ticker_suspend_info():
    pass


def initialize_back_test():
    load_trading_dates()
    load_ticker_prices()
    load_bench_mark()
    initialize(account)
    pass


def back_test():
    begdate_datetime = datetime.strptime(begdate, '%Y%m%d')
    enddate_datetime = datetime.strptime(enddate, '%Y%m%d')
    cur_datetime = begdate_datetime
    while cur_datetime < begdate_datetime:
        temp_end_datetime = cur_datetime + refresh_rate
        period_prices = ticker_prices[[cur_datetime, temp_end_datetime]]
        
    pass


def main():
    load_ticker_prices()
    pass


if __name__ == '__main__':
    main()
