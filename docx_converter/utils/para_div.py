"""划分段落的工具"""
import bs4
import os
from ..tex_translator.docx import convert_to_html

QUES_PATTERN = (
    r"[Aa][．.,，、。· ][^Bb]+[Bb][．.,，、。· ][^Cc]+[Cc][．.,，、。· ][^Dd]+[Dd][．.,，、。· ].+"
)
OPTS_PATTERN = r"([ABCDabcd][．.,，、。· ])"
ANSW_PATTERN = r"[ABCDabcd]"
SUBS_PATTERN = r"([\(（\[][0-9]+[\）\)\]])"


def extract_para_html(input_path: os.PathLike) -> str:
    with open(input_path, "r") as f:
        soup = bs4.BeautifulSoup(f, "html.parser")
        paras = soup.find_all("p")
    return "\n".join(para.text for para in paras)


def extract_para_md(input_path: os.PathLike) -> str:
    with open(input_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_para_docx(input_path: os.PathLike, tmp_cache: os.PathLike) -> str:
    try:
        html_str = convert_to_html(input_path, tmp_cache)
        if "<img" in html_str:
            raise Exception
        # soup = bs4.BeautifulSoup(html_str, "html.parser")
        # _paras = soup.find_all("p")
        # paras = "\n".join(
        #     "".join(map(lambda x: "{}".format(x), para.contents)) for para in _paras
        # )
        paras = html_str.replace("<p>", "").replace("</p>", "")
    except:
        raise Exception
    return paras


class QueryType:
    """
    A enumerate class container for "gap-filling", "short-answer" and "multiple-choice"
    """

    @property
    def gap_filling(self):
        return "shiti/gap-filling"

    @property
    def short_answer(self):
        return "shiti/short-answer"

    @property
    def multiple_choice(self):
        return "shiti/multiple-choice"


def categroy_judge(des: str, opts: str, ans: str, nmc: int) -> QueryType:
    """
    roughly judge one problem whether it is a gap-filling or short-answer question
    Output:
     - `arg` : string values, only enumerate in `gap-filling`, `short-answer` and `multiple-choice`
    """
    query_type = QueryType()
    if ans and nmc == 0:
        return query_type.multiple_choice
    else:
        if len(des.strip() + opts.strip()) // len(ans.strip()) > 5:
            return query_type.short_answer
        else:
            return query_type.gap_filling
