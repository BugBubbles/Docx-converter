import os
from typing import Callable, Tuple
from .converter import ConverterBase
from ..formattor import bi_part_div, part_div, fir_mat_div
from ..utils import (
    extract_para_html,
    OPTS_PATTERN,
    SUBS_PATTERN,
    ANSW_PATTERN,
)
from ..utils import NoSplitError
import itertools


class HtmlConverter(ConverterBase):
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
        # Main Features
        Extract the query and answer, as well as resolution if it has. It can process the single one multiple choice or more formatted text. Here are two examples:
        # Examples
        `file_path` file single one multiple choice example: \\
        【题文】下列各项中，哪种说法是正确的（  ）：\\
         A. 地球上的太阳从西边升起，东边落下； \\
         B. 一年的四季是由地球自转产生的； \\
         C. 当北半球处于冬季时，南半球正好处于夏季； \\
         D. 地球的公转面称为赤道平面。 \\
        【答案】 C 【解析】 A.地球自西向东自转，太阳东升西落；B.地球自转决定白昼黑夜，四季由地球公转产生；D.地球的公转面称为黄道面；北半球和南半球同时接收到太阳的光照时，太阳直射南回归线时南半球处于夏季，此时北半球正好处于冬季。

        expecting output:
        - `arg[0]`: \\
         下列各项中，哪种说法是正确的（  ）：
        - `arg[1]`: \\
         A. 地球上的太阳从西边升起，东边落下； \\
         B. 一年的四季是由地球自转产生的； \\
         C. 当北半球处于冬季时，南半球正好处于夏季； \\
         D. 地球的公转面称为黄道平面。
        - `arg[2]`: \\
         C
        - `arg[3]`: \\
         A.地球自西向东自转，太阳东升西落；B.地球自转决定白昼黑夜，四季由地球公转产生；D.地球的公转面称为黄道面；北半球和南半球同时接收到太阳的光照时，太阳直射南回归线时南半球处于夏季，此时北半球正好处于冬季。
        - `arg[4]`: \\
         4 \\
         ---------------------------------------------------------------------------
        `file_path` file more than one multiple choice example: \\
        阅读以下题目，按要求完成解答：\\
        (1)下列各项中，哪种说法是正确的（  ）： \\
         A. 地球上的太阳从西边升起，东边落下； \\
         B. 一年的四季是由地球自转产生的； \\
         C. 当北半球处于冬季时，南半球正好处于夏季； \\
         D. 地球的公转面称为赤道平面。 \\
        （2） \\
        下列各项中，哪种说法是不正确的（  ）： \\
         A. 地球上的太阳从东边升起，西边落下； \\
         B. 一年的四季是由地球公转产生的； \\
         C. 当北半球处于冬季时，南半球正好处于夏季； \\
         D. 地球的地轴倾角约为66.4度。 \\
        【答案】 C D【解析】 (1) A.地球自西向东自转，太阳东升西落；B.地球自转决定白昼黑夜，四季由地球公转产生；D.地球的公转面称为黄道面；北半球和南半球同时接收到太阳的光照时，太阳直射南回归线时南半球处于夏季，此时北半球正好处于冬季。（2）前三个同（1），最后一个，地轴倾角定义为地球自转轴与地理南北极连线的夹角，约为23.6度。
        expecting output:
        - `arg[0]`: \\
         阅读以下题目，按要求完成解答：
        - `arg[1]`: \\
        (1)下列各项中，哪种说法是正确的（  ）：
         A. 地球上的太阳从西边升起，东边落下；\\
         B. 一年的四季是由地球自转产生的；\\
         C. 当北半球处于冬季时，南半球正好处于夏季；\\
         D. 地球的公转面称为黄道平面。\\
        (2)下列各项中，哪种说法是不正确的（  ）：\\
         A. 地球上的太阳从东边升起，西边落下；\\
         B. 一年的四季是由地球公转产生的；\\
         C. 当北半球处于冬季时，南半球正好处于夏季；\\
         D. 地球的公转面称为赤道平面。
        - `arg[2]`: \\
         (1) C; (2) D;
        - `arg[3]`: \\
         (1) A.地球自西向东自转，太阳东升西落；B.地球自转决定白昼黑夜，四季由地球公转产生；D.地球的公转面称为黄道面；北半球和南半球同时接收到太阳的光照时，太阳直射南回归线时南半球处于夏季，此时北半球正好处于冬季。（2）前三个同（1），最后一个，地轴倾角定义为地球自转轴与地理南北极连线的夹角，约为23.6度。
        - `arg[4]`: \\
        2
        """
        passage = extract_para_html(file_path)
        query, _, answer = bi_part_div("【答案】")(passage)
        # divide the query part into desc(if it has) and options
        try:
            desc, _, options = fir_mat_div(OPTS_PATTERN)(query)
        except NoSplitError:
            desc = None
            options = query
        except Exception as exc:
            print(exc)
            raise Exception
        # divide the options into split option list.
        opt_list = []
        non_multiple_choice_num = 0
        try:
            # multiple choices
            for sub_option in part_div(SUBS_PATTERN)(
                options, schema="({}) {};", ind=itertools.count(1)
            ):
                try:
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
                    part_div(OPTS_PATTERN)(
                        options, schema="{}. {}\n", ind="ABCDEFGHIJK"
                    )
                )
            except NoSplitError:
                # Non multiple choice problem.
                opt_list = options
                non_multiple_choice_num += 1
            except Exception as exc:
                print(exc)
                raise Exception
            ans, _, res = bi_part_div("【解析】")(answer)
            return (
                desc,
                opt_list,
                ans,
                res,
                non_multiple_choice_num,
            )
