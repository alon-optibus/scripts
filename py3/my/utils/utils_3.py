
########################################################################################################################
# <editor-fold desc="missing">
# TODO: missing type


MISSING = object()


class MissingError (ValueError):
    pass


def unmissing(*values, missing=MISSING, e=MissingError()):

    for value in values:
        if value is not missing:
            return value

    raise e


# </editor-fold>
########################################################################################################################
