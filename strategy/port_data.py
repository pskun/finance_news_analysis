# -*- coding: utf-8 -*-
import os
import numpy as np
import xlstools as uxls
import tradetools as utrd
import mattools as umat


class WgtEntry:
    def __init__(self):
        self.date = 0
        self.stocks = np.empty(0)
        self.wgts = np.empty(0)


def load_dir_of_portfolio_csv_files_with_date_suffix(dir):
    date2port = {}
    files = os.listdir(dir)
    for f in files:
        filename = dir + '\\' + f
        if filename[-4:] == '.csv' and filename[-13] == '_' and filename[-12:-4].isdigit():
            data = uxls.read_csv(filename)
            date = int(filename[-12:-4])
            date2port[date] = WgtEntry()
            date2port[date].date = date
            date2port[date].stocks = data[:, 0]
            date2port[date].wgts = data[:, 1].astype(float)
    return np.sort(date2port.keys()), date2port

# NOTICE: portfolio on date D means we complete the portfolio on the end of date D,
# so it can be used to calculate the return next day.
# parameters
# enddate: the last date you want to get daily return
# price_codes, price_dates, price_ret_mat: the price ret matrix(value on
# date D mean (priceD-priceD-1)/priceD-1) and it's rows(price_dates) and
# columns(price_codes)


def get_port_daily_returns(date2port, enddate, price_codes, price_dates, price_ret_mat, rebalance_cost=0):
    port_dates = np.sort(date2port.keys())
    if enddate <= port_dates[0]:
        raise Exception(
            'enddate should be greater than the first portfolio date')
    if price_dates[0] > port_dates[0] or price_dates[-1] < enddate:
        raise Exception('more price data needed')

    last_codes = np.empty(0, dtype=object)
    last_wgts = np.empty(0)
    last_port_date_index = 0
    daily_returns = np.zeros(len(price_dates))
    for i in xrange(len(price_dates)):
        if price_dates[i] <= port_dates[0]:
            continue
        if price_dates[i] > enddate:
            continue
        last_date = price_dates[i - 1]
        turnover = 0
        if last_port_date_index < len(port_dates) and last_date == port_dates[last_port_date_index]:
            wgts1 = umat.fill_symbol_value(
                price_codes, date2port[last_date].stocks, date2port[last_date].wgts, fill_value=0)
            wgts2 = umat.fill_symbol_value(
                price_codes, last_codes, last_wgts, fill_value=0) if last_codes.size > 0 else np.zeros(len(wgts1))
            buy = np.maximum(0, wgts1 - wgts2)
            sell = np.maximum(0, wgts2 - wgts1)
            turnover = 0.5 * (sum(buy) + sum(sell))

            # print '%d-%.2f' % (last_date,turnover)

            last_codes = date2port[last_date].stocks
            last_wgts = date2port[last_date].wgts
            last_port_date_index += 1
        if last_codes.size > 0:
            code_ret = umat.fill_symbol_value(
                last_codes, price_codes, price_ret_mat[i, :], fill_value=0)
            daily_returns[i] = last_wgts.dot(code_ret)

            if turnover > 0 and rebalance_cost > 0:
                daily_returns[i] = daily_returns[i] - rebalance_cost * turnover

            tmp_last_wgts = last_wgts * (1 + code_ret)
            last_wgts = tmp_last_wgts / np.sum(tmp_last_wgts)
    returns_dates = price_dates[
        np.logical_and(price_dates > port_dates[0], price_dates <= enddate)]
    final_daily_returns = daily_returns[
        np.logical_and(price_dates > port_dates[0], price_dates <= enddate)]
    return returns_dates, final_daily_returns
