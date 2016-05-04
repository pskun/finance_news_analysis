# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.dates as plt_dates
import numpy as np
import datetime as dt
import time


def get_datetime_date(curdate):
    '''curdate is integer like: 20090101'''
    return dt.date(curdate/10000, (curdate%10000)/100, curdate%100)


def plot_date_line_and_vline(
        line_values,
        line_dates,
        vline_dates = [],
        line_label = [],
        line_color = []):
    ''' line_values could be 1d or nd arrays '''
    if len(line_label) == 0:
        if len(line_values.shape) == 1:
            line_label = ['line']
        else:
            line_label_coll = ['line1', 'line2', 'line3', 'line4', 'line5', 'line6', 'line7', 'line8']
            line_label = line_label_coll[0:line_values.shape[1]]

    if len(line_color) == 0:
        if len(line_values.shape) == 1:
            line_color = ['CornflowerBlue']
        else:
            line_color_coll = ['Blue', 'Green', 'Red', 'DarkTurquoise', 'Chocolate', 'CadetBlue', 'IndianRed', 'Orange']
            line_color = line_color_coll[0:line_values.shape[1]]

    line_dtdates = [get_datetime_date(x) for x in line_dates]
    vline_dtdates = [get_datetime_date(x) for x in vline_dates]
    (fig, ax) = plt.subplots()
    if len(line_values.shape) == 1:
        ax.plot_date(line_dtdates, line_values, '-', label = line_label[0], color = line_color[0])
    else:
        for i in xrange(line_values.shape[1]):
            ax.plot_date(line_dtdates, line_values[:, i], '-', label = line_label[i], color = line_color[i])
    for vldate in vline_dtdates:
        ax.axvline(vldate)
    ax.xaxis.set_major_formatter(plt_dates.DateFormatter('%Y-%m-%d'))
    def ydata(y): return '$%1.2f'%y
    ax.fmt_xdata = plt_dates.DateFormatter('%Y-%m-%d')
    ax.fmt_ydata = ydata
    ax.grid(True)
    # show
    fig.autofmt_xdate()
    plt.legend()
    plt.show()
