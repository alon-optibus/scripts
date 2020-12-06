from my.utils.bash_1 import shell_lines
from collections import namedtuple
from dataclasses import dataclass

WMCTRL = 'wmctrl'


@dataclass
class WinInfo:
    wid: int
    pid: int
    desktop: int
    client: str
    title: str

    def is_hidden(self):
        return self.desktop < 0

    pass




def iter_all_windows():
    for line in shell_lines([WMCTRL, '-p', '-l']):
        wid, desktop, pid, client, title = line.split(maxsplit=4)

        yield WinInfo(
            wid=int(wid, 16),
            pid=int(pid),
            desktop=int(desktop),
            client=client,
            title=title,
        )


def iter_real_windows():
    for winfo in iter_all_windows():
        if winfo.desktop >= 0:
            yield winfo


def test():

    print(*iter_all_windows(), sep='\n')

    pass


if __name__ == '__main__':
    test()
