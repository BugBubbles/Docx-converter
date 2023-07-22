import re

suffix = re.compile("(\.[a-zA-Z0-9]+)")
prefix = re.compile("(【题文】)")
dudp_enter = re.compile(r"\n\n+")


def rm_suffix(raw_str: str):
    """
    Use rectification match words `(\.[a-zA-Z0-9]+){1,}$` to remove all the suffix in one filename.
    """
    return suffix.sub(lambda x: "", raw_str)


def rm_prefix(raw_str: str):
    return prefix.sub(lambda x: "", raw_str)


def dedup_enter(raw_str: str):
    """
    replace continuous `\n` to a single one
    """
    return dudp_enter.sub(lambda x: "\n", raw_str)


if __name__ == "__main__":
    test_str = (
        "SYS201801012247174749592066_高中英语_高二_动词的词义辨析,contribute to,result from,语法.docx"
    )
    print(rm_suffix(test_str))
