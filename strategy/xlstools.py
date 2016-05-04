# -*- coding: utf-8 -*-
import numpy as np
import xlwt
import xlrd
import csv

# http://www.crifan.com/python_xlwt_set_cell_background_color/


def gen_format(font_bold=None, pattern_pattern_fore_colour=None, align_horizontal=None):
    ''' excel format '''
    # example is below. (other parameters could be added to parameters if needed in future)
    # EXAMPLE_HEADER = xlwt.easyxf(
    # 'font: bold 1, name Tahoma, height 160;'
    # 'align: vertical center, horizontal center, wrap on;'
    # 'borders: left thin, right thin, top thin, bottom thin;'
    # 'pattern: pattern solid, pattern_fore_colour green, pattern_back_colour green'
    # )
    # color name is listed below
    # Text values for colour indices. "grey" is a synonym of "gray".
    # aqua 0x31
    # black 0x08
    # blue 0x0C
    # blue_gray 0x36
    # bright_green 0x0B
    # brown 0x3C
    # coral 0x1D
    # cyan_ega 0x0F
    # dark_blue 0x12
    # dark_blue_ega 0x12
    # dark_green 0x3A
    # dark_green_ega 0x11
    # dark_purple 0x1C
    # dark_red 0x10
    # dark_red_ega 0x10
    # dark_teal 0x38
    # dark_yellow 0x13
    # gold 0x33
    # gray_ega 0x17
    # gray25 0x16
    # gray40 0x37
    # gray50 0x17
    # gray80 0x3F
    # green 0x11
    # ice_blue 0x1F
    # indigo 0x3E
    # ivory 0x1A
    # lavender 0x2E
    # light_blue 0x30
    # light_green 0x2A
    # light_orange 0x34
    # light_turquoise 0x29
    # light_yellow 0x2B
    # lime 0x32
    # magenta_ega 0x0E
    # ocean_blue 0x1E
    # olive_ega 0x13
    # olive_green 0x3B
    # orange 0x35
    # pale_blue 0x2C
    # periwinkle 0x18
    # pink 0x0E
    # plum 0x3D
    # purple_ega 0x14
    # red 0x0A
    # rose 0x2D
    # sea_green 0x39
    # silver_ega 0x16
    # sky_blue 0x28
    # tan 0x2F
    # teal 0x15
    # teal_ega 0x15
    # turquoise 0x0F
    # violet 0x14
    # white 0x09
    # yellow 0x0D"""

    font_str = 'font:'
    if font_bold is not None:
        font_str = font_str + ' bold ' + str(font_bold) + ','
    if font_str[-1] == ',':
        font_str = font_str[:-1] + ';'

    pattern_str = 'pattern:'
    if pattern_pattern_fore_colour is not None:
        pattern_str = pattern_str + ' pattern solid, pattern_fore_colour ' + \
            pattern_pattern_fore_colour + ','
    if pattern_str[-1] == ',':
        pattern_str = pattern_str[:-1] + ';'

    align_str = 'align:'
    if align_horizontal is not None:
        align_str = align_str + ' horizontal ' + align_horizontal + ','
    if align_str[-1] == ',':
        align_str = align_str[:-1] + ';'

    format_str = ''
    if font_str != 'font:':
        format_str = format_str + font_str
    if pattern_str != 'pattern:':
        format_str = format_str + pattern_str
    if align_str != 'align:':
        format_str = format_str + align_str

    format_object = xlwt.easyxf(format_str)
    return format_object

# csv tools


def read_csv(filename, skip_lines=0):
    csvfile = file(filename, 'rb')
    reader = csv.reader(csvfile)
    data = np.empty(0, dtype=object)
    last_count = np.NAN
    for line in reader:
        if skip_lines > 0:
            skip_lines = skip_lines - 1
            continue
        if data.size > 0:
            if len(line) != last_count:
                raise Exception('unequal columes found')
            data = np.c_[data, line]
            last_count = len(line)
        else:
            data = np.array(line, dtype=object)
            data = data.reshape(len(data), 1)
            last_count = len(line)
    csvfile.close()
    return data.T


def save_dbrst(rst, filename, sheetname='Sheet1'):
    '''save the database returned result (cells of cells) to excel'''
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet(sheetname)
    for i in xrange(len(rst)):
        for j in xrange(len(rst[0])):
            sheet.write(i, j, rst[i][j])
    wbk.save(filename)


def read_sheet_by_index(filename, sheetindex=0, nrows=0, ncols=0, skip_lines=0):
    data = xlrd.open_workbook(filename)
    sheet = data.sheets()[sheetindex]
    if nrows == 0:
        nrows = sheet.nrows
    if ncols == 0:
        ncols = sheet.ncols
    nskip = skip_lines
    data_mat = np.empty(shape=(nrows - nskip, ncols), dtype=object)
    for i in xrange(ncols):
        data_mat[:, i] = sheet.col_values(i)[nskip:]
    return data_mat


def write_sheet(data_mat, filename, sheetname='Sheet1', header=np.empty(0, dtype=object),
                header_format=None, data_format=np.empty(0, dtype=object)):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet(sheetname)
    start_line = 0
    if len(header) == data_mat.shape[1]:
        for j in xrange(data_mat.shape[1]):
            if header_format is None:
                sheet.write(0, j, header[j])
            else:
                sheet.write(0, j, header[j], header_format)
        start_line = 1
    if data_format.size != 0 and len(data_format) != data_mat.shape[0]:
        raise Exception(
            'data_format should be the same length as rows of data_mat')
    for i in xrange(data_mat.shape[0]):
        for j in xrange(data_mat.shape[1]):
            if data_format.size == 0:
                sheet.write(i + start_line, j, data_mat[i][j])
            else:
                sheet.write(i + start_line, j, data_mat[i][j], data_format[i])
    wbk.save(filename)
