from typing import Callable
import warnings


class BadFormatWarning(Warning):
    pass


class SmallBatchWarning(Warning):
    pass


class NoSplitError(BaseException):
    pass


def bi_div_num(func):
    """
    divide into 2 parts.
    """

    def warp(*args, **kwargs):
        splits = func(*args, **kwargs)

        try:
            if len(splits) < 3:
                raise NoSplitError("No divident flags was found in this text!")
            elif len(splits) > 3:
                warnings.warn(
                    "This text was going to be divided more than two parts, we only reserve the first two items. Here is the raw text:\n----------------->>>>>\n{}\n<<<<<<<<--------------".format(
                        "\n".join(splits)
                    ),
                    BadFormatWarning,
                )
        except Exception as exc:
            print(exc)
            raise Exception

        return splits

    return warp


def div_num(func):
    """
    divide into 2 or more parts
    """

    def warp(*args, **kwargs):
        splits = func(*args, **kwargs)
        try:
            if len(splits) < 2:
                raise NoSplitError("No divident flags was found in this text!")
        except Exception as exc:
            print(exc)
            raise Exception
        return splits

    return warp


def input_func(func):
    def warp(arg_func: Callable, *fn_args, **fn_kwargs):
        output = func(arg_func, *fn_args, **fn_kwargs)
        return output

    return warp


def input_class(func):
    def warp(arg_class, *init_args, **init_kwargs):
        output = func(arg_class, *init_args, **init_kwargs)
        return output

    return warp
