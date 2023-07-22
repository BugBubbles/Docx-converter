"""划分段落的工具"""
import bs4
import os
from ..tex_translator.docx import convert_to_html

QUES_PATTERN = (
    r"[Aa][．.,，、。· ][^Bb]+[Bb][．.,，、。· ][^Cc]+[Cc][．.,，、。· ][^Dd]+[Dd][．.,，、。· ].+"
)
OPTS_PATTERN = r"([ABCD][．.,，、。· ])"
ANSW_PATTERN = r"[ABCD]"
SUBS_PATTERN = r"(\(.{0,2}[0-9]+.{0,2}\))|(\[.{0,2}[0-9]+.{0,2}\])|(\{.{0,2}[0-9]+.{0,2}\})|(【.{0,2}[0-9]+.{0,2}】)|(（.{0,2}[0-9]+.{0,2}）)"  # |([\(（\[【[0-9]+】\）\)\]])
DES_OPTS_PATTERNS = r"(\(.{0,2}[0-9]+.{0,2}\))|(\[.{0,2}[0-9]+.{0,2}\])|(\{.{0,2}[0-9]+.{0,2}\})|(【.{0,2}[0-9]+.{0,2}】)|(（.{0,2}[0-9]+.{0,2}）)|([ABCD][．.,，、。· ])"


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

    @property
    def mixed(self):
        return "shiti/mixed"


def categroy_judge(des: str, opts: str, ans: str, nmc: int) -> QueryType:
    """
    roughly judge one problem whether it is a gap-filling or short-answer question
    Output:
     - `des` : description part, when there is a single problem without sub questions, it will be the whole part of problem.
     - `opts` : options, not empty only when there are more than one sub questions.
     - `ans` : answers.
     - `nmc` : the number of non-multiple-choice sub question.
    """
    query_type = QueryType()
    if ans and nmc == 0:
        return query_type.multiple_choice
    elif len(opts.strip()) > 2 and nmc == 0:
        return query_type.mixed
    else:
        if len(des.strip() + opts.strip()) // len(ans.strip()) > 5:
            return query_type.gap_filling
        else:
            return query_type.short_answer
