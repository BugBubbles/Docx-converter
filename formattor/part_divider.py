from typing import List, Tuple, Iterable
from .divider import DividerBase
from ..utils import bi_div_num, div_num


class BiPartDivider(DividerBase):
    """
    divide the whole passage into query and answer parts.\\
    output:
     - a list for three items including.
    """

    @bi_div_num
    def __call__(self, content: str):
        parts = self.div_flag.split(content)
        return tuple(part for part in parts)


class PartDivider(DividerBase):
    """
    divide the whole passage into several parts, reserve the divident flags.
    """

    @div_num
    def __call__(
        self,
        content: str,
        schema: str = None,
        ind: Iterable = None,
        res_flag: bool = False,
    ):
        """
        Argument:
         - schema:
        """
        parts = self.div_flag.split(content)
        try:
            assert schema and ind
            if res_flag:
                return tuple(
                    schema.format(index, flag + cnt)
                    for index, flag, cnt in zip(ind, parts[1::2], parts[2::2])
                )
            else:
                return tuple(
                    schema.format(index, cnt) for index, cnt in zip(ind, parts[2::2])
                )
        except AssertionError:
            # No customized schema input
            return tuple(
                f"{index} {cnt}\n" for index, cnt in zip(parts[1::2], parts[2::2])
            )
        except:
            # No splits is found
            return parts


class FirstMatchDivider(DividerBase):
    """
    divide the whole passage into 2 parts when first meeting the divident flags.
    """

    @bi_div_num
    def __call__(self, content: str):
        parts = self.div_flag.split(content)

        return (
            parts[0],
            "",
            "\n".join(f"{index} {cnt}" for index, cnt in zip(parts[1::2], parts[2::2])),
        )
