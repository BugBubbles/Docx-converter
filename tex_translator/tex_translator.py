from .translator import TranslatorBase
from ..utils import (
    TEX_SYMB_PATTERN,
    TEX_SYMB_SUPSUB_PATTERN,
    TEX_SUPSUB_PATTERN,
    FULL_MATH_PATTERN,
    NO_TEX_SYMB_PATTERN,
    NO_TEX_SYMB_SUPSUB_PATTERN,
    NO_TEX_SUPSUB_PATTERN,
    DISPLAY_PATTERN,
    INLINE_PATTERN,
    full_2_half_formular,
)
import re
import itertools
from typing import List, Tuple


class TexTranslator(TranslatorBase):
    def __call__(self, raw_str: str, *args, **kwargs) -> str:
        """only match those who lack of `$` with subscripts or supscripts"""
        begin_index = 0

        def __store__(
            flag: re.Pattern, raw_str: str, des: str = ""
        ) -> Tuple[List[str], str]:
            nonlocal begin_index
            split_text = [text for text in flag.split(raw_str) if text]
            output_header = split_text[0]
            if flag.fullmatch(output_header):
                output_split_list = split_text[0::2]
                length = len(split_text[1::2])
                output_rm_fotmat_text = "".join(
                    f"{des}" + "{" + f"{cnt}" + "}" + f"{des}" + f"{split_text}"
                    for cnt, split_text in zip(
                        range(begin_index, begin_index + length), split_text[1::2]
                    )
                )
                begin_index += length
                return output_split_list, output_rm_fotmat_text
            else:
                output_split_list = split_text[1::2]
                length = len(split_text[2::2])
                output_rm_fotmat_text = "".join(
                    f"{des}" + "{" + f"{cnt}" + "}" + f"{des}" + f"{split_text}"
                    for cnt, split_text in zip(
                        range(begin_index, begin_index + length), split_text[2::2]
                    )
                )
                begin_index += length
                return output_split_list, output_header + output_rm_fotmat_text

        def __retrive__(split_list: List[str], format_str: str) -> str:
            return format_str.format(*split_list)

        # 存放displaystyle型的latex式子
        temp_str = DISPLAY_PATTERN.sub(
            lambda x: FULL_MATH_PATTERN.sub(
                lambda y: full_2_half_formular[y.group()], x.group()
            ),
            raw_str,
        )
        temp_str = INLINE_PATTERN.sub(
            lambda x: FULL_MATH_PATTERN.sub(
                lambda y: full_2_half_formular[y.group()], x.group()
            ),
            temp_str,
        )
        tex_dis_list, temp_str = __store__(DISPLAY_PATTERN, temp_str)
        # 存放inline型的latex式子
        tex_inl_list, temp_str = __store__(INLINE_PATTERN, temp_str)
        # temp_str = raw_str.replace("$", "")
        # 存放被拿走的不带有$$的有上下标的特殊字符
        no_tex_symb_supsub_list, temp_str = __store__(
            NO_TEX_SYMB_SUPSUB_PATTERN, temp_str, "$"
        )
        # 存放被拿走的不带有$$的特殊字符
        no_tex_symb_list, temp_str = __store__(NO_TEX_SYMB_PATTERN, temp_str, "$")
        # 存放被拿走的不带有$$的上下标字符
        no_tex_supsub_list, temp_str = __store__(NO_TEX_SUPSUB_PATTERN, temp_str, "$")

        # 恢复所有对应位置处的字符串
        temp_str = __retrive__(
            list(
                [
                    *tex_dis_list,
                    *tex_inl_list,
                    *no_tex_symb_supsub_list,
                    *no_tex_symb_list,
                    *no_tex_supsub_list,
                ]
            ),
            temp_str,
        )
        return temp_str
