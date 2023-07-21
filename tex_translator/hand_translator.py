from .translator import TranslatorBase
from ..utils import (
    ml2tex,
    SUP_PATTERN,
    SUB_PATTERN,
    uni_2_tex,
    EM_PATTERN,
    SUBSUP_PATTERN,
    FULL_PATTER,
    full_2_half,
    SYMB_PATTERN,
)


class HandTranslator(TranslatorBase):
    def __call__(self, raw_str: str, *args, **kwargs) -> str:
        """
        Warning : the raw_str should only contain necessary formular without any other characters!
        """
        return (
            self._trans_symbol(
                self._trans_subsup(self._rm_emp(self._full2half(raw_str)))
            )
            .replace("<br>", "")
            .replace("</br>", "")
            .replace("<br/>", "\n")
        )

    def _full2half(self, full_raw_str: str):
        """replace fullwidth character with halfwidth character"""
        return FULL_PATTER.sub(lambda x: full_2_half[x.group()], full_raw_str)

    def _trans_symbol(self, symb_str: str):
        """
        translate the string including non ascii character ( for example: `°÷±×αβγδεζηθιλ`) into tex code
        """
        return SYMB_PATTERN.sub(lambda x: uni_2_tex[x.group()], symb_str)

    def _trans_subsup(self, sub_sup_str: str):
        """
        translate the string including `<sup></sup>` and `<sub></sub>` into tex code
        """
        try:
            sub_str = SUP_PATTERN.sub(
                lambda x: "^{" + SUBSUP_PATTERN.sub(lambda y: "", x.group()) + "}",
                sub_sup_str,
            )

        except:
            try:
                return SUB_PATTERN.sub(
                    lambda x: "_{" + SUBSUP_PATTERN.sub(lambda y: "", x.group()) + "}",
                    sub_sup_str,
                )

            except:
                return sub_sup_str
        try:
            output_str = SUB_PATTERN.sub(
                lambda x: "_{" + SUBSUP_PATTERN.sub(lambda y: "", x.group()) + "}",
                sub_str,
            )
        except:
            return sub_str
        return output_str

    def _rm_emp(self, emp_str: str):
        """remove the `<em></em>` index in the raw strings"""
        return EM_PATTERN.sub(lambda x: "", emp_str)


if __name__ == "__main__":
    HandTranslator()(raw_str="")
