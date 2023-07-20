from typing import Any, List, Tuple


class TranslatorBase:
    """
    translate a html or other format math formular into tex format code.
    """

    def __init__(self) -> None:
        pass

    def __call__(self, raw_str:str, *args, **kwargs) -> str:
        raise NotImplementedError
