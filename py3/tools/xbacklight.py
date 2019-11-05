

import tkinter as tk
import os

########################################################################################################################


def set_level(event=None):
    try:
        x = int(v1.get())
    except (ValueError, TypeError):
        return
    os.system('xbacklight -set {}'.format(x))


def increase(event):
    try:
        x = int(v1.get())
        y = min(100, x + (1 if x < 10 else 10))
    except (ValueError, TypeError):
        return
    v1.set(y)
    set_level()


def decrease(event):
    try:
        x = int(v1.get())
        y = max(1, x - (1 if x <= 10 else 10))
    except (ValueError, TypeError):
        return
    v1.set(y)
    set_level()


########################################################################################################################

master = tk.Tk()

master.bind('<Return>', set_level)
master.bind('<Up>', increase)
master.bind('<Down>', decrease)

v1 = tk.StringVar()
v1.set(int(float(os.popen('xbacklight -get').read())))

e1 = tk.Entry(
    master,
    textvariable=v1,
)

e1.grid(row=0, column=0)
e1.focus()

tk.mainloop()

########################################################################################################################
