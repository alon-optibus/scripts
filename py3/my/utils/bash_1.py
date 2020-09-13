from pathlib import Path
from functools import lru_cache
from subprocess import PIPE
from subprocess import Popen


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


def shell_process(cmd, cwd=None):

    if not isinstance(cmd, str):
        cmd = ' '.join(cmd)

    return Popen(
        cmd,
        shell=True,
        cwd=None if cwd is None else Path(cwd).resolve(strict=True),
        stdout=PIPE,
    )

def shell_lines(cmd, cwd=None):
    for line in shell_process(cmd=cmd, cwd=cwd).stdout:
        yield line.decode()[:-1]


########################################################################################################################
if __name__ == '__main__':

    for i in range(200):
        print(f'{i}: ', termfmt(i)('wwwwwww'))
        pass

    pass
########################################################################################################################
