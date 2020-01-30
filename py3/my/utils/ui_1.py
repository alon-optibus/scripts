from __future__ import print_function, division

import tkinter as tk

from toolz import identity

from my.utils.utils_3 import MISSING, MissingError

########################################################################################################################
# <editor-fold desc="entry box">


def get_ui_input(
        label='',
        value='',
        show=None,
        default=MISSING,
        missing=MISSING,
        f=identity,
        raise_=MissingError,
):

    return TkEntryBox(
        label=label,
        show=show,
    ).get(
        default=default,
        missing=missing,
        f=f,
        raise_=raise_,
    )


class TkEntryBox:
    __slots__ = (
        'top',
        'entry_wiget',
        'entry_value',
        'label_wiget',
        'submit_flag',
    )

    def __init__(
            self,
            top=None,
            label='',
            value='',
            show=None,
    ):

        self.submit_flag = False

        self.top = top = tk.Tk() if top is None else top

        top.bind('<Return>', self.key_enter)
        top.bind('<Escape>', self.key_esc)

        self.label_wiget = tk.Label(
            top,
            text=label,
        )

        self.entry_value = tk.StringVar()
        self.entry_value.set(value)

        self.entry_wiget = tk.Entry(
            top,
            textvariable=self.entry_value,
            show=show,
        )

        self.label_wiget.grid(row=0, column=0)
        self.entry_wiget.grid(row=1, column=0)
        self.entry_wiget.focus()

    def key_enter(self, event=None):
        return self.submit()

    def key_esc(self, event=None):
        return self.cancel()

    def submit(self):
        self.submit_flag = True
        self.top.destroy()

    def cancel(self):
        self.submit_flag = False
        self.top.destroy()

    def get(
            self,
            default=MISSING,
            missing=MISSING,
            f=identity,
            raise_=MissingError,
    ):

        tk.mainloop()

        value = self.entry_value.get()

        if self.submit_flag:
            return f(value)

        if default is missing:
            raise raise_(value)

        return default

    pass


# </editor-fold>
# <editor-fold desc="msgbox">


def msgbox(
        msg='',
        title='',
):
    return TkMsgBox(
        msg=msg,
    ).show()


class TkMsgBox:
    __slots__ = (
        'top',
        'label_wiget',
    )

    def __init__(
            self,
            top=None,
            msg='',
    ):

        self.top = top = tk.Tk() if top is None else top

        top.bind('<Return>', self.key_enter)
        top.bind('<Escape>', self.key_esc)

        self.label_wiget = tk.Label(
            top,
            text=msg,
        )

        self.label_wiget.grid(row=0, column=0)
        self.label_wiget.focus()

    def key_enter(self, event=None):
        return self.close()

    def key_esc(self, event=None):
        return self.close()

    def close(self):
        self.top.destroy()

    def show(self):
        tk.mainloop()
        return

    pass


# </editor-fold>
########################################################################################################################
