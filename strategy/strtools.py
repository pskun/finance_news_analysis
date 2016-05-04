import numpy as np


def get_str2pos_dict(strs):
    str2pos = {}
    for i in xrange(len(strs)):
        str2pos[strs[i]] = i
    return str2pos


def get_bstrs_pos_in_astrs(astrs, bstrs, astrs2pos={}):
    if not astrs2pos:
        astrs2pos = get_str2pos_dict(astrs)
    pos = np.zeros(shape=len(bstrs))
    count = 0
    for s in bstrs:
        try:
            pos[count] = astrs2pos[s]
        except Exception:
            pos[count] = np.NAN
        count += 1
    return pos


def get_bstrs_pos_in_astrs_slowly(astrs, bstrs):
    pos = np.zeros(shape=len(bstrs))
    count = 0
    for s in bstrs:
        try:
            pos[count] = np.argwhere([cmp(x, s) == 0 for x in astrs])[0][0]
        except Exception:
            pos[count] = np.NAN
        count += 1
    return pos
