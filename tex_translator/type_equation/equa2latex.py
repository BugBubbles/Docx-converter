import os
from lxml import etree
import re

inline_pattern = re.compile(
    "^\$\S+\$$|^(\\\()\S+(\\\))$", flags=re.ASCII
)  # 匹配以 $ $ 或者 \( \)开头的字符串，作为latex行内公式
display_pattern = re.compile(
    "^\$\$\S+\$\$$|^(\\\[)\S+(\\\])$", flags=re.ASCII
)  # 匹配以 $$ $$ 或者 \[ \]开头的字符串，作为latex行间公式

zh_cn_pattern = re.compile("[（）【】——·！，。？：；]")

uni_2_tex = {
    "（": '<mo stretchy="false">(</mo>',
    "）": '<mo stretchy="false">)</mo>',
    "【": '<mo stretchy="false">[</mo>',
    "】": '<mo stretchy="false">]</mo>',
    "——": "<mo>&#x2212;</mo>",
    "·": "<mo>&#x22C5;</mo>",
    "！": "<mo>!</mo>",
    "，": "<mo>,</mo>",
    "。": "<mo>.</mo>",
    "？": "<mo>?</mo>",
    "：": "<mo>:</mo>",
    "；": "<mo>;</mo>",
    "*": "<mo>&#xD7;</mo>",
    "": "",
}
label_2_tex = {
    "sup": re.compile("<sup>\S+</sup>", flags=re.ASCII),  # 上标
    "sub": re.compile("<sub>\S+</sub>", flags=re.ASCII),  # 下标
}


def is_latex_str(formular: str):
    """
    Test whether a string is latex str or not.
    """
    pass


def mathml2latex_yarosh(equation):
    """MathML to LaTeX conversion with XSLT from Vasil Yaroshevich"""
    xslt_file = os.path.join("xsl_yarosh", "mmltex.xsl")
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return newdom


if __name__ == "__main__":
    mathml = """<mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML"><mml:mtable><mml:mtr><mml:mtd></mml:mtd><mml:mtd><mml:mrow><mml:munder><mml:mo stretchy="true">∑</mml:mo><mml:mrow><mml:mo>(</mml:mo><mml:mi>i</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi><mml:mo>)</mml:mo><mml:mo>∈</mml:mo><mml:mi>A</mml:mi></mml:mrow></mml:munder><mml:mrow><mml:msubsup><mml:mrow><mml:mi>x</mml:mi></mml:mrow><mml:mrow><mml:mi>i</mml:mi><mml:mi>j</mml:mi></mml:mrow><mml:mrow><mml:mi>k</mml:mi></mml:mrow></mml:msubsup></mml:mrow></mml:mrow><mml:mo>-</mml:mo><mml:mrow><mml:munder><mml:mo stretchy="true">∑</mml:mo><mml:mrow><mml:mfenced separators="|"><mml:mrow><mml:mi>n</mml:mi><mml:mo>+</mml:mo><mml:mi>i</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi></mml:mrow></mml:mfenced><mml:mo>∈</mml:mo><mml:mi>A</mml:mi></mml:mrow></mml:munder><mml:mrow><mml:msubsup><mml:mrow><mml:mi>x</mml:mi></mml:mrow><mml:mrow><mml:mi>n</mml:mi><mml:mo>+</mml:mo><mml:mi>i</mml:mi><mml:mo>,</mml:mo><mml:mi>j</mml:mi></mml:mrow><mml:mrow><mml:mi>k</mml:mi></mml:mrow></mml:msubsup></mml:mrow></mml:mrow><mml:mo>=</mml:mo><mml:mn>0</mml:mn><mml:mo>,</mml:mo><mml:mo>∀</mml:mo><mml:mi>i</mml:mi><mml:mo>∈</mml:mo><mml:mi>P</mml:mi><mml:mo>,</mml:mo><mml:mo>∀</mml:mo><mml:mi>k</mml:mi><mml:mo>∈</mml:mo><mml:mi>K</mml:mi><mml:mo>,</mml:mo></mml:mtd></mml:mtr></mml:mtable></mml:math>"""
    mathml = """<math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  − 3<em>a</em><em>b</em><sup>2</sup> + 3
  </math>"""
    tex = mathml2latex_yarosh(mathml)
    print(tex)
