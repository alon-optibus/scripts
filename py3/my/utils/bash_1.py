from functools import lru_cache

########################################################################################################################


@lru_cache(100)
def termfmt(i):
    return f"\033[{i}m{{}}\033[00m".format


termfmt_u = termfmt(21)

termfmt_rf = termfmt(91)
termfmt_bf = termfmt(94)
termfmt_pf = termfmt(95)
termfmt_cf = termfmt(96)
termfmt_gf = termfmt(92)
termfmt_yf = termfmt(93)
termfmt_grf = termfmt(37)
termfmt_kf = termfmt(38)

termfmt_rb = termfmt(41)
termfmt_gb = termfmt(42)
termfmt_yb = termfmt(43)
termfmt_grb = termfmt(100)

########################################################################################################################
if __name__ == '__main__':

    for i in range(200):
        print(f'{i}: ', termfmt(i)('wwwwwww'))
        pass

    pass
########################################################################################################################
