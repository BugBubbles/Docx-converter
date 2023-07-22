from typing import Tuple, List, Union
import re


class DividerBase:
    """
    using customized divide flags to divid
    """

    def __init__(self, div_str: str) -> None:
        """
        Arguments:
         - `div_str` : this string can be a simple string or a rectified expression.
        """
        assert div_str != None
        if not isinstance(type, re.Pattern):
            if not re.match("\(.+\)", div_str):
                div_str = f"({div_str})"
            self.div_flag = re.compile(div_str)
        else:
            self.div_flag = div_str

    def __call__(self, content: str, *args, **kwargs) -> Tuple[str]:
        raise NotImplementedError


def match_div(content: str, div_flags: List[Union[str, re.Pattern]], **kwargs):
    """
        When first meet a matched string, this functions will memory what style it is in the `div_flags`, then it will divide the remained string according to the chosen style.
        ### Arguments:
         - `content` : the string to be divided.
         - `div_flags` : the potential divident flags
         - `maxsplit` : the maximal divided parts.
        ### Output:
         - `args[0]` : header of the content.
         - `args[1]` : the matched divident flags.
         - `args[2]` : the divided content excluding divident flags.\\
        ### Example:
        python\\
        from docx_converter.formattor import match_div\\
        raw_str = 'I have a dream, a big dream for everyone.'\\
        div_str = 'dream'\\
        header, divider, dividee = match_div(div_str)(raw_str)\\
        >>> header\\
        >>> I have a \\
        >>> divider\\
        >>> ['dream', 'dream']\\
        >>> dividee\\
        >>> [', a big ', ' for everyone.']\\
        raw_str = 'dreaming is a great thing'\\
        header, divider, dividee = match_div(div_str)(raw_str)\\
        >>> header\\
        >>>  \\
        >>> divider\\
        >>> ['dream']\\
        >>> dividee\\
        >>> ['is a great thing']\\
    """
    div_flags = [
        div_flag if isinstance(div_flag, re.Pattern) else re.compile(div_flag)
        for div_flag in div_flags
    ]
    candidates = sorted(
        map(
            lambda div_flag: (
                div_flag,
                div_flag.search(content).start()
                if div_flag.search(content)
                else 10000000,
            ),
            div_flags,
        ),
        key=lambda x: x[1],
    )
    div_flag = candidates[0][0]
    parts = [part for part in div_flag.split(content, **kwargs) if part]
    header = parts[0]
    try:
        if div_flag.fullmatch(header):
            return "", parts[0::2], parts[1::2]
        else:
            return header, parts[1::2], parts[2::2]
    except Exception as exc:
        raise exc


if __name__ == "__main__":
    head, divider, dividee = match_div(
        """【小题2】A.从征鲜卑大战/于临朐累月不决/弥与檀韶等分军自间道攻临朐城/弥擐甲先登/即时溃陷/斩其牙旗/贼遂奔走。\nB.从征鲜卑/大战于临朐/累月不决/弥与檀韶等分军自间道攻临朐城/弥擐甲先登/即时溃陷/斩其牙旗/贼遂奔走。\nC.从征鲜卑/大战于临朐/累月不决/弥与檀韶等分军自间道攻临朐城/弥擐甲/先登即时溃陷/斩其牙旗/贼遂奔走。\nD.从征鲜卑大战/于临朐累月不决/弥与檀韶等分军自间道攻临朐城/弥擐甲/先登即时溃陷/斩其牙旗/贼遂奔走。【小题2】下列对文中加点词语的相关内容的解说，不正确的一项是\nA.“讳”，本意是指违言，不说，避忌。也指不敢直称帝王、尊长或贤才的名字。\nB.“义熙”，东晋司马德宗的年号，汉武帝始建年号，公元前140年为建元元年。\nC.“食邑”，古代君主赐予臣下作为世禄的封地，唐宋时亦作为一种荣誉性加衔。\nD.“侯”，爵名，中国古代皇族、贵族的封号，比上文的“封安南县男”等级低。【小题3】下列对原文有关内容的概括和分析，不正确的一项是\nA.向靖作战冲锋陷阵，勇猛无敌。向靖功高位重，但在作战时仍然能够身先士卒，在关键时刻能够发挥出重要的作用，克敌制胜。\nB.向靖一生南征北战，深受信任。高祖率军南征时，向靖任先锋，取得了重大胜利；高祖北伐时，向靖随从，深得高祖信任器重。\nC.向靖为国鞠躬尽瘁，死而后已。由于连年征战，为国操劳，高祖即位的第二年，向靖死于其任上，年仅五十九岁，时任前将军。\nD.向靖为人克俭自律，颇受称赞。他一贯严格要求自己，生活方面十分节俭，不建造房舍屋宇，也没有园圃田地和货物等产业。【小题4】把文中画横线的句子翻译成现代汉语。（1）子植嗣，多过失，不受母训，夺爵。（2）更以植次弟桢绍封，又坐杀人，国除。""",
        div_flags=[
            r"(\(.{0,2}[0-9]+.{0,2}\))",
            r"(\[.{0,2}[0-9]+.{0,2}\])",
            r"(\{.{0,2}[0-9]+.{0,2}\})",
            r"(【.{0,2}[0-9]+.{0,2}】)",
            r"(（.{0,2}[0-9]+.{0,2}）)",
            r"([ABCD][．.,，、。· ])",
        ],
    )
    print(head)
    print(divider)
    print(dividee)
