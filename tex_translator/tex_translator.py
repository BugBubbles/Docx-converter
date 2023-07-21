from .translator import TranslatorBase
from ..utils import (
    TEX_SYMB_PATTERN,
    TEX_SYMB_SUPSUB_PATTERN,
    TEX_SUPSUB_PATTERN,
    NO_TEX_SYMB_PATTERN,
    NO_TEX_SYMB_SUPSUB_PATTERN,
    NO_TEX_SUPSUB_PATTERN,
)
import re
import itertools
from typing import List, Tuple


class TexTranslator(TranslatorBase):
    def __call__(self, raw_str: str, *args, **kwargs) -> str:
        """only match those who lack of `$` with subscripts or supscripts"""
        tex_subsup = ["".join(line) for line in TEX_SUPSUB_PATTERN.findall(raw_str)]

        def __find_hand_in_tex(formu: re.Match) -> str:
            nonlocal tex_subsup
            i = 0
            tex_subsup_copy = tex_subsup.copy()
            for tex in tex_subsup_copy:
                if formu.group() in tex:
                    tex_subsup.pop(i)
                    return f"{formu.group()}"
                else:
                    i += 1
                    continue
            return f"${formu.group()}$"

        # 给特殊符号有上下标的加$$
        tex_symb_supsub = TEX_SYMB_SUPSUB_PATTERN.sub(__find_hand_in_tex, raw_str)
        # 给成单出现的特殊符号加$$
        tex_supsub = TEX_SYMB_PATTERN.sub(__find_hand_in_tex, tex_symb_supsub)
        # 给成单出现的上下标加$$
        return NO_TEX_SUPSUB_PATTERN.sub(__find_hand_in_tex, tex_supsub)

    def _call__2(self, raw_str: str, *args, **kwargs) -> str:
        """only match those who lack of `$` with subscripts or supscripts"""
        # counter = itertools.count(0)
        begin_index = 0

        def __store__(
            flag: re.Pattern, raw_str: str, des: str = ""
        ) -> Tuple[List[str], str]:
            nonlocal begin_index
            split_text = [text for text in flag.split(raw_str) if text]
            output_split_list = split_text[1::2]
            output_header = split_text[0]
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

        # 存放被拿走的带有$$的有上下标的特殊字符
        tex_symb_supsub_list, temp_str = __store__(TEX_SYMB_SUPSUB_PATTERN, raw_str)
        # 存放被拿走的带有$$的特殊字符
        tex_symb_list, temp_str = __store__(TEX_SYMB_PATTERN, temp_str)
        # 存放被拿走的带有$$的上下标字符
        tex_supsub_list, temp_str = __store__(TEX_SUPSUB_PATTERN, temp_str)
        # 存放被拿走的不带有$$的有上下标的特殊字符
        no_tex_symb_supsub_list, temp_str = __store__(
            NO_TEX_SYMB_SUPSUB_PATTERN, temp_str, "$"
        )
        # 存放被拿走的不带有$$的特殊字符
        no_tex_symb_list, temp_str = __store__(NO_TEX_SYMB_PATTERN, temp_str, "$")
        # 存放被拿走的不带有$$的上下标字符
        no_tex_supsub_list, temp_str = __store__(NO_TEX_SUPSUB_PATTERN, temp_str, "$")

        # 恢复被拿走的不带有$$的有上下标的特殊字符
        temp_str = __retrive__(
            list(
                [
                    *tex_symb_supsub_list,
                    *tex_symb_list,
                    *tex_supsub_list,
                    *no_tex_symb_supsub_list,
                    *no_tex_symb_list,
                    *no_tex_supsub_list,
                ]
            ),
            temp_str,
        )
        # # 恢复被拿走的带有$$的特殊字符
        # temp_str = __retrive__(*tex_symb_list, temp_str)
        # # 恢复被拿走的带有$$的上下标字符
        # temp_str = __retrive__(*tex_supsub_list, temp_str)
        # # 恢复被拿走的不带有$$的有上下标的特殊字符
        # temp_str = __retrive__(*no_tex_symb_supsub_list, temp_str)
        # # 恢复被拿走的不带有$$的特殊字符
        # temp_str = __retrive__(*no_tex_symb_list, temp_str)
        # # 恢复被拿走的不带有$$的上下标字符
        # temp_str = __retrive__(*no_tex_supsub_list, temp_str)
        return temp_str
