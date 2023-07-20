from .translator import TranslatorBase
from ..utils import (
    ml2tex,
    SUP_PATTERN,
    SUB_PATTERN,
    ZH_PATTERN,
    uni_2_tex,
    FULL_PATTER,
    full_2_half,
)


class HandTranslator(TranslatorBase):
    def __call__(self, raw_str: str, *args, **kwargs) -> str:
        """
        Warning : the raw_str should only contain necessary formular without any other characters!
        """
        # replace fullwidth character with halfwidth character

    def _full2half(self, full_raw_str: str):
        return FULL_PATTER.sub(lambda x: full_2_half[x], full_raw_str)


if __name__ == "__main__":
    HandTranslator()(raw_str="")
