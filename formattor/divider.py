from typing import Tuple, List
import re


class DividerBase:
    """
    using customized divide flags to divid
    """

    def __init__(self, div_str: str) -> None:
        """
        Arguments:
         - `div_str` : this string can be a simple string or a rectified expression.
        """
        assert div_str != None
        if not re.match("\(.+\)", div_str):
            div_str = f"({div_str})"
        self.div_flag = re.compile(div_str)

    def __call__(self, content: str, *args, **kwars) -> Tuple[str]:
        raise NotImplementedError
