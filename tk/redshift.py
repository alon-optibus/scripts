

import tkinter as tk
import os

########################################################################################################################


def set_redshift(event=None):
    try:
        x = int(1000 * float(v1.get()))
    except (ValueError, TypeError):
        return
    os.system('redshift -O {}'.format(x))


def increase(event):
    try:
        x = str(float(v1.get()) + 0.5)
    except (ValueError, TypeError):
        return
    v1.set(x)
    set_redshift()


def decrease(event):
    try:
        x = str(float(v1.get()) - 0.5)
    except (ValueError, TypeError):
        return
    v1.set(x)
    set_redshift()


########################################################################################################################

master = tk.Tk()

master.bind('<Return>', set_redshift)
master.bind('<Up>', increase)
master.bind('<Down>', decrease)

v1 = tk.StringVar()
v1.set('4')

e1 = tk.Entry(
    master,
    textvariable=v1,
)

e1.grid(row=0, column=0)
e1.focus()

tk.mainloop()

########################################################################################################################
