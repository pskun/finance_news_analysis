# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import pandas as pd

from account import Account
from strategy_test import *

PRICES_COL_NAME = ['tradedate', 'ticker', 'adjpreclose',
                   'adjopen', 'adjclose', 'adjfactor', 'tradestatus']
PRICES_DATA_TYPE = {
    'ticker': str,
    'adjpreclose': float,
    'adjopen': float,
    'adjclose': float,
    'adjfactor': float,
    'tradestatus': str
}

# 市场交易日期
trading_dates = []
# 股票价格
ticker_prices = None
# 股票停复牌信息
ticker_suspend_info = None
# 基准股票价格
benchmark_prices = None
# 策略每日收益率
strategy_daily_return = []


def set_universe(universe_code):
    universe = []
    universe_code = universe_code.lower()
    universe_file = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], 'data/%s_tickers.csv' % universe_code)
    for line in open(universe_file):
        universe.append(line.strip())
    return universe


def load_trading_dates():
    global trade_dates
    trading_dates_file = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], 'data/trade_days.csv')
    for line in open(trading_dates_file):
        date = datetime.strptime(line.strip(), '%Y%m%d')
        trading_dates.append(date)
    pass


def load_ticker_prices():
    global ticker_prices
    ticker_prices_file = os.path.join(
        os.path.split(os.path.realpath(__file__))[0], 'data/prices.csv')
    ticker_prices = pd.read_csv(
        ticker_prices_file,
        header=None, names=PRICES_COL_NAME, dtype=PRICES_DATA_TYPE)
    ticker_prices['tradedate'] = pd.to_datetime(
        ticker_prices['tradedate'], format='%Y%m%d')
    ticker_prices.set_index('tradedate', inplace=True)
    ticker_prices = ticker_prices[begdate: enddate]
    ticker_prices['return'] = ticker_prices[
        'adjclose'] / ticker_prices['adjpreclose']
    ticker_prices = ticker_prices[['ticker', 'return', 'tradestatus']]
    pass


def load_bench_mark():
    global benchmark_prices
    if bench_index != 'ALL':
        # 某一个指数作为benchmark
        benchmark_prices_file = os.path.join(
            os.path.split(os.path.realpath(__file__))[0], 'data/%s.csv' % bench_index)
        benchmark_prices = pd.read_csv(
            benchmark_prices_file,
            header=None, names=['tradedate', 'close', 'pctchange'])
        benchmark_prices['tradedate'] = pd.to_datetime(
            benchmark_prices['tradedate'], format='%Y%m%d')
        benchmark_prices.set_index('tradedate', inplace=True)
        benchmark_prices = benchmark_prices[begdate: enddate]
        benchmark_prices['pctchange'] = (
            1 + benchmark_prices['pctchange'] / 100)
    else:
        # 全市场股票作为benchmark
        ticker_prices.reset_index('tradedate', inplace=True)
        group_by_date = ticker_prices.groupby('tradedate')
        benchmark_prices['pctchange'] = group_by_date['return'].mean()
    benchmark_prices['cumchange'] = benchmark_prices['pctchange'].cumprod()
    pass


def load_ticker_suspend_info():
    pass


def initialize_back_test(account):
    load_trading_dates()
    load_ticker_prices()
    load_bench_mark()
    account.universe = universe
    initialize(account)
    pass


def back_test(account):
    global ticker_prices, strategy_daily_return
    begdate_datetime = datetime.strptime(begdate, '%Y%m%d')
    enddate_datetime = datetime.strptime(enddate, '%Y%m%d')
    cur_datetime = begdate_datetime
    while cur_datetime <= enddate_datetime:
        temp_end_datetime = cur_datetime + timedelta(days=refresh_rate)
        period_prices = ticker_prices[cur_datetime: temp_end_datetime]
        period_prices.reset_index('tradedate', inplace=True)
        group_by_date = period_prices.groupby('tradedate')
        # 按天计算
        day_count = 0
        for tradedate, grouped in group_by_date:
            day_count += 1
            if day_count == 1:
                universe = grouped[grouped['tradestatus'] == '1'][
                    'ticker'].values.to_list()
                account.universe = universe
                account.previous_date = account.current_date
                account.current_date = cur_datetime
                account.before_handle_data()
                handle_data(account)
                turnover = account.calculate_turnover()
                account.after_handle_data()
                ticker_weight_df = pd.DataFrame(
                    account.new_avail_secpos.items(),
                    columns=['ticker', 'weight'])
            grouped = pd.merge(grouped, ticker_weight_df, on='ticker')
            grouped['weight_return'] = grouped['return'] * grouped['weight']
            daily_return = grouped['weight_return'].sum()
            print daily_return
            if day_count == 1:
                daily_return -= cost * turnover
            strategy_daily_return.append(
                {'tradedate': tradedate, 'return': daily_return})
        cur_datetime = temp_end_datetime
    strategy_daily_return = pd.DataFrame(strategy_daily_return)
    pass


def summary_back_test(account):
    pass


def main():
    account = Account()
    initialize_back_test(account)
    back_test(account)
    summary_back_test(account)
    pass


if __name__ == '__main__':
    main()
