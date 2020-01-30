import tkinter as tk
from toolz import identity
from my.utils.utils_3 import MISSING, MissingError

from my.utils.crypto_1 import crypto_manager

########################################################################################################################
# <editor-fold desc="entry box">
# TODO: Move to ?


def get_ui_input(
        label='',
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
        self.entry_value.set('')

        self.entry_wiget = tk.Entry(
            top,
            textvariable=self.entry_value,
            show=show,
            # show='*',
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
########################################################################################################################

HASH_OF_MASTER_KEY = b"ac04333ca6cc57bc985c3f2cbcaa8739e505e454d6cb0aef8dac4c1edcdbbde1"
HASH_OF_SECOND_KEY = b"7f830bd8aff9a334197610798c96b2eef004c87ed020fe2685945820d70c3065"

edata = (
    "b75552442a9db76a20eee6b039b5dbc81798ac35cbdc4e64b26c842f43dab9a6d8703160f1224643a7c564e5ff641e98573b4d57b2d80aee1b"
    "01089c9a44eefbe1848357d065712462fea1ad18362701a1fdbb8379b4c9f803980d08ed0fe0c64f3ddc04881b36e0fe0de5fb90d90adab30f"
    "e95b4e70c480b506f53ca2fde14d3a9d3391d4e91c3fab1e7bd9a36af8e88d3567ec768c693c3f68fa6447f59b2d17c1c4d6"
)


def ui_gey_key(target_hash, n=1, cur=b'', label='', show=None):

    value = cur

    try:

        while crypto_manager.hash(value, n=n).hex().encode() != target_hash:

            value = crypto_manager.hash(
                data=get_ui_input(label=label, show=show, f=str.encode),
                n=n,
            ).hex().encode()

    except MissingError:
        return cur

    else:
        return value


second_key = ui_gey_key(
    target_hash=HASH_OF_SECOND_KEY,
    label='second',
    show=None,
)

assert crypto_manager.hash(second_key, n=1).hex().encode() == HASH_OF_SECOND_KEY


########################################################################################################################
