import os
from typing import Callable, Tuple
from .converter import ConverterBase
from ..formattor import bi_part_div, part_div, fir_mat_div
from ..utils import (
    extract_para_docx,
    OPTS_PATTERN,
    SUBS_PATTERN,
    QUES_PATTERN,
)
from ..utils import NoSplitError
import itertools


class DocxConverter(ConverterBase):
    def _main_process(
        self,
        file_path: os.PathLike,
        text_extract_fun: Callable[[str], Tuple[str, str, str, str, int]] = None,
        **dump_kwargs
    ) -> str:
        return super()._main_process(
            file_path, self._text_extract_multiple_choice, **dump_kwargs
        )

    def _text_extract_multiple_choice(
        self, file_path: os.PathLike
    ) -> Tuple[str, str, str, str, int]:
        """
        extract the query and answer, as well as desolution if it is.
        """
        try:
            passage = extract_para_docx(file_path, self.tmp_cache)
            query, _, answer = bi_part_div("(【答案】)|(解：)")(passage)
            # divide the query part into desc(if it has) and options
            desc, _, options = fir_mat_div(OPTS_PATTERN)(query)
        except NoSplitError:
            desc = None
            options = query
        except:
            raise Exception
        # divide the options into split option list.
        opt_list = []
        non_multiple_choice_num = 0
        try:
            # multiple choices
            for sub_option in part_div(SUBS_PATTERN)(
                options, schema="({}){};", ind=itertools.count(1)
            ):
                try:
                    opt_list.append(
                        "".join(
                            part_div(OPTS_PATTERN)(
                                sub_option, schema="{}.{}\n", ind="ABCDEFGHIJK"
                            )
                        )
                    )
                except NoSplitError:
                    # 当前为非选择题的时候
                    opt_list.append(sub_option)
                    non_multiple_choice_num += 1
                except Exception as exc:
                    print(exc)
                    raise Exception
            ans, _, res = bi_part_div("【解析】")(answer)
            return (
                desc,
                "".join(opt_list),
                ans,
                res,
                non_multiple_choice_num,
            )
        except:
            # only one multiple choice problem
            try:
                opt_list = "".join(
                    part_div(OPTS_PATTERN)(options, schema="{}.{}\n", ind="ABCDEFGHIJK")
                )
            except NoSplitError:
                # Non multiple choice problem.
                opt_list = options
                non_multiple_choice_num += 1
            except Exception as exc:
                print(exc)
                raise Exception
            try:
                ans, _, res = bi_part_div("【解析】")(answer)
            except NoSplitError:
                # Non multiple choice problem.
                ans = answer
                res = answer

            return (
                desc,
                opt_list,
                ans,
                res,
                non_multiple_choice_num,
            )
