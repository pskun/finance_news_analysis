import numpy as np


def max_drawdown(prices):
    prevmaxi = 0
    prevmini = 0
    maxi = 0

    for i in range(len(prices))[1:]:
        if prices[i] >= prices[maxi]:
            maxi = i
        else:
            # You can only determine the largest drawdown on a downward price!
            if ((prices[maxi] - prices[i]) / prices[maxi]) > ((prices[prevmaxi] - prices[prevmini]) / prices[prevmaxi]):
                prevmaxi = maxi
                prevmini = i
    maxnegret = (prices[prevmini] - prices[prevmaxi]) / prices[prevmaxi]
    maxdd = abs(maxnegret)
    return maxdd


def win_rate(returns):
    return sum(returns > 0) / float(len(returns))


def ret2value(returns):
    values = np.empty(shape=len(returns) + 1)
    values.fill(np.NAN)
    values[0] = 1
    for i in xrange(len(returns)):
        values[i + 1] = values[i] * (1 + returns[i])
    return values


def retmat2valuemat(retmat):
    valuemat = np.tile(np.NAN, (retmat.shape[0] + 1, retmat.shape[1]))
    for i in xrange(retmat.shape[1]):
        valuemat[:, i] = ret2value(retmat[:, i])
    return valuemat


def value2ret(values):
    if len(values.shape) == 1:
        prevalues = np.append(np.NAN, values[0:-1])
        returns = (values - prevalues) / prevalues
        returns[np.isinf(returns)] = np.NAN
    else:
        prevalues = np.r_[
            np.tile(np.NAN, (1, values.shape[1])), values[0:-1, :]]
        returns = (values - prevalues) / prevalues
        returns[np.isinf(returns)] = np.NAN
    return returns
