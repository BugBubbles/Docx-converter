import os
from typing import Callable, Tuple
from .converter import ConverterBase
from ..formattor import bi_part_div, part_div, fir_mat_div, match_div
from ..utils import (
    extract_para_md,
    OPTS_PATTERN,
    SUBS_PATTERN,
    DES_OPTS_PATTERNS,
)
from ..utils import NoSplitError
import itertools


class MdConverter(ConverterBase):
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
            passage = extract_para_md(file_path, self.tmp_cache)
            query, _, answer = bi_part_div(r"(【答案】)|(解[：: ])")(passage)
            # divide the query part into desc(if it has) and options
            desc, _, options = fir_mat_div(SUBS_PATTERN)(query)
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
            for sub_option in match_div(DES_OPTS_PATTERNS)(
                options, schema="{}. {}", ind=itertools.count(1)
            ):
                try:
                    if sub_option == "\n":
                        continue
                    opt_list.append(
                        "".join(
                            part_div(OPTS_PATTERN)(
                                sub_option, schema="{}. {}\n", ind="ABCDEFGHIJK"
                            )
                        )
                    )
                except NoSplitError:
                    # 当前为非选择题的时候
                    opt_list.append(sub_option)
                    non_multiple_choice_num += 1
                except IndexError:
                    # 当前为非选择题的时候
                    opt_list.append(sub_option)
                    non_multiple_choice_num += 1
                except Exception as exc:
                    print(exc)
                    raise Exception
            ans, _, res = bi_part_div(r"(【解析】)")(answer)
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
                desc = "".join(
                    match_div(OPTS_PATTERN)(desc, schema="{}. {}\n", ind="ABCDEFGHIJK")
                )
            except NoSplitError:
                # Non multiple choice problem.
                # desc = desc
                non_multiple_choice_num += 1
            except Exception as exc:
                print(exc)
                raise Exception
            try:
                ans, _, res = bi_part_div(r"(【解析】)")(answer)
            except NoSplitError:
                # Non multiple choice problem.
                ans = answer
                res = answer

            return (
                desc,
                "".join(opt_list),
                ans,
                res,
                non_multiple_choice_num,
            )
