import numpy as np
import utils.strtools as ustr


def fill_symbol_value(symbols, valsyms, vals, fill_value=np.NAN):
    if valsyms.size == 0:
        return np.tile(np.NAN, len(symbols))
    values = np.tile(np.NAN, len(symbols)) if len(vals.shape) == 1 else np.tile(np.NAN, (len(symbols),vals.shape[1]))
    symbol2pos = ustr.get_str2pos_dict(symbols)
    for i in xrange(len(valsyms)):
        try:
            if len(vals.shape) == 1:
                values[symbol2pos[valsyms[i]]] = vals[i]
            else:
                values[symbol2pos[valsyms[i]], :] = vals[i, :]
        except Exception, e:
            pass
    values[np.isnan(values)] = fill_value
    return values


def get_mat_ewma(tsmat, alpha):
    # EWMA(t) = alpha * ts(t) + (1-alpha) * EWMA(t-1)
    ewma = np.tile(np.NAN, tsmat.shape)
    for i in xrange(1, tsmat.shape[0]):
        init_selection = np.isnan(ewma[i-1, :])
        ewma[i-1, init_selection] = tsmat[i-1, init_selection]
        ewma[i, :] = alpha * tsmat[i, :] + (1-alpha) * ewma[i-1, :]
    return ewma


def get_mat_movingstd(tsmat, periods):
    mstd = np.empty(shape = tsmat.shape)
    mstd.fill(np.NAN)
    for i in xrange(tsmat.shape[0]):
        j = i - periods + 1
        if j < 0:
            j = 0
        mstd[i,:] = np.nanstd(tsmat[j:i+1,:], 0)
    return mstd


def get_mat_ma(tsmat, periods):
    ma = np.empty(shape = tsmat.shape)
    ma.fill(np.NAN)
    for i in xrange(tsmat.shape[0]):
        j = i - periods + 1
        if j < 0:
            j = 0
        ma[i,:] = np.nanmean(tsmat[j:i+1,:], 0)
    return ma


def get_array_ma(ts, periods):
    ma = np.empty(shape = len(ts))
    ma.fill(np.NAN)
    for i in xrange(len(ts)):
        j = i - periods + 1
        if j < 0:
            j = 0
        ma[i] = np.nanmean(ts[j:i+1], 0)
    return ma


# 0 for add, 1 for multiply
def get_accum(tsmat, method=0):
    accum_tsmat = np.tile(np.NAN, tsmat.shape)
    if len(tsmat.shape) == 1:
        total = 0 if method==0 else 1
        for i in xrange(len(tsmat)):
            if method == 0: total = total + tsmat[i]
            else: total = total * tsmat[i]
            accum_tsmat[i] = total
    else:
        total = np.zeros(tsmat.shape[1]) if method==0 else np.ones(tsmat.shape[1])
        for i in xrange(tsmat.shape[0]):
            if method == 0: total = total + tsmat[i, :]
            else: total = total * tsmat[i, :]
            accum_tsmat[i, :] = total
    return accum_tsmat



