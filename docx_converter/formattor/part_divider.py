from typing import List, Tuple, Iterable
from .divider import DividerBase, match_div
from ..utils import bi_div_num, div_num, DES_OPTS_PATTERNS


class BiPartDivider(DividerBase):
    """
    divide the whole passage into query and answer parts.\\
    output:
     - a list for three items including.
    """

    @bi_div_num
    def __call__(self, content: str):
        parts = self.div_flag.split(content, maxsplit=1)
        return tuple(part for part in parts if part)


class PartDivider(DividerBase):
    """
    divide the whole passage into several parts, reserve the divident flags.
    """

    @div_num
    def __call__(
        self,
        content: str,
        schema: str = "{}. {}\n",
        ind: Iterable = "ABCD",
        res_flag: bool = False,
    ):
        """
        ### Argument:
        - `content` : the string to be divided.
         - `schema` : The output schema, default is "A.The desc".
         - `ind` : the index label to name the list of splits.
        """
        try:
            header, divider, dividee = match_div(content, [self.div_flag])
        except Exception as exc:
            raise exc
        try:
            if res_flag:
                splits = [
                    schema.format(index, flag + cnt)
                    for index, flag, cnt in zip(ind, divider, dividee)
                ]
                splits.insert(0, header + "\n")
            else:
                splits = [schema.format(index, cnt) for index, cnt in zip(ind, dividee)]
                splits.insert(0, header + "\n")
                return splits
        except:
            # No splits is found
            return content


class FirstMatchDivider(DividerBase):
    """
    divide the whole passage into 2 parts when first meeting the divident flags.
    """

    @bi_div_num
    def __call__(self, content: str):
        parts = [part for part in self.div_flag.split(content) if part]

        return (
            parts[0],
            "",
            "\n".join(f"{index}{cnt}" for index, cnt in zip(parts[1::2], parts[2::2])),
        )


class MatchPartDivider(DividerBase):
    """
    using the first matched style to divide the whole string
    """

    def __init__(self, div_str: str) -> None:
        self.div_flag = div_str

    def __call__(
        self,
        content: str,
        schema: str = "{}. {}\n",
        ind: Iterable = "ABCD",
        res_flag: bool = False,
    ) -> Tuple[str, List[str], List[str]]:
        """
        ### Argument:
        - `content` : the string to be divided.
         - `schema` : The output schema, default is "A.The desc".
         - `ind` : the index label to name the list of splits.
        """
        try:
            header, divider, dividee = match_div(
                content, self.div_flag.split("|")
            )
        except Exception as exc:
            raise exc
        try:
            if res_flag:
                splits = [
                    schema.format(index, flag + cnt)
                    for index, flag, cnt in zip(ind, divider, dividee)
                ]
                splits.insert(0, header + "\n")
            else:
                splits = [schema.format(index, cnt) for index, cnt in zip(ind, dividee)]
                splits.insert(0, header + "\n")
                return splits
        except:
            # No splits is found
            return content
