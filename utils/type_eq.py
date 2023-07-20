import re
import os
from lxml import etree

INLINE_PATTERN = re.compile(
    "^\$\S+\$$|^(\\\()\S+(\\\))$", flags=re.ASCII
)  # 匹配以 $ $ 或者 \( \)开头的字符串，作为latex行内公式
DISPLAY_PATTERN = re.compile(
    "^\$\$\S+\$\$$|^(\\\[)\S+(\\\])$", flags=re.ASCII
)  # 匹配以 $$ $$ 或者 \[ \]开头的字符串，作为latex行间公式

EM_PATTERN = re.compile("(</?em>)")
SUP_PATTERN = re.compile("(<sup>\S{1,10}</sup>)")  # 上标
SUB_PATTERN = re.compile("(<sub>\S{1,10}</sub>)")  # 下标
SUBSUP_PATTERN = re.compile("(</?sup?b?>)")
FULL_PATTER = re.compile("[＋－＊／＝＾＞＜．＇＂～…（）【】——·！，。？：；｛｝［］％＆＃＠｀＄｜＼]")
full_2_half = {
    "＋": "+",
    "｜": "|",
    "＼": "\\",
    "＄": "$",
    "－": "-",
    "＊": "*",
    "／": "/",
    "＝": "=",
    "＾": "^",
    "＞": ">",
    "＜": "<",
    "．": ".",
    "＇": "'",
    "＂": '"',
    "～": "~",
    "…": "\codts",
    "（": "(",
    "）": ")",
    "【": "[",
    "】": "]",
    "——": "-",
    "·": "\cdot",
    "！": "!",
    "，": ",",
    "。": ".",
    "？": "?",
    "：": ":",
    "；": ";",
    "｛": "{",
    "｝": "}",
    "［": "[",
    "］": "]",
    "％": "%",
    "＆": "&",
    "＃": "#",
    "＠": "@",
    "｀": "`",
}
ZH_PATTERN = re.compile(
    "[＋－＊／＝＾＞＜．＇＂～…（）【】——·！，。？：；*°÷±×αβγδεζηθιλκμνξορπσςτυφχψωϕϑΘΔΓΛΞΠΣΦΨΩ•∂∈√∞∠∟∥∧∨∩∪∴∵≈≌≠≤≥⊙⊕⊥ø→←↑↓∀∃]"
)

uni_2_tex = {
    "＋": "<mo>+</mo>",
    "－": "<mo>&#x2212;</mo>",
    "＊": "<mo>&#x2217;</mo>",
    "／": "<mo>/</mo>",
    "＝": "<mo>=</mo>",
    "＾": "<mtext>\^</mtext>",
    "＞": "<mo>&gt;</mo>",
    "＜": "<mo>&lt;</mo>",
    "．": "<msup><mo>.</mo></msup>",
    "＇": """<msup><mo data-mjx-alternate="1">&#x2032;</mo></msup>""",
    "＂": """<mrow data-mjx-texclass="ORD"><mo data-mjx-pseudoscript="true">&quot;</mo>
  </mrow>""",
    "～": "<mtext>&#xA0;</mtext>",
    "…": "<mo>&#x22EF;</mo>",
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
    "°": "<mo>&#xB0;</mo>",
    "÷": "<mi>&#xF7;</mi>",
    "±": "<mo>&#xB1;</mo>",
    "×": "<mi>&#xD7;</mi>",
    "α": "<mi>&#x3B1;</mi>",
    "β": "<mi>&#x3B2;</mi>",
    "γ": "<mi>&#x3B3;</mi>",
    "δ": "<mi>&#x3B4;</mi>",
    "ε": "<mi>&#x3B5;</mi>",
    "ζ": "<mi>&#x3B6;</mi>",
    "η": "<mi>&#x3B7;</mi>",
    "θ": "<mi>&#x3B8;</mi>",
    "ι": "<mi>&#x3B9;</mi>",
    "λ": "<mi>&#x3BB;</mi>",
    "κ": "<mi>&#x3BA;</mi>",
    "μ": "<mi>&#x3BC;</mi>",
    "ν": "<mi>&#x3BD;</mi>",
    "ξ": "<mi>&#x3BE;</mi>",
    "ο": "<mi>&#x3BF;</mi>",
    "ρ": "<mi>&#x3C1;</mi>",
    "π": "<mi>&#x3C0;</mi>",
    "σ": "<mi>&#x3C3;</mi>",
    "ς": "<mi>&#x3C2;</mi>",
    "τ": "<mi>&#x3C4;</mi>",
    "υ": "<mi>&#x3C5;</mi>",
    "φ": "<mi>&#x3C6;</mi>",
    "χ": "<mi>&#x3C7;</mi>",
    "ψ": "<mi>&#x3C8;</mi>",
    "ω": "<mi>&#x3C9;</mi>",
    "ϕ": "<mi>&#x3D5;</mi>",
    "ϑ": "<mi>&#x3D1;</mi>",
    "Θ": "<mi>&#x398;</mi>",
    "Δ": "<mi>&#x394;</mi>",
    "Γ": "<mi>&#x393;</mi>",
    "Λ": "<mi>&#x39B;</mi>",
    "Ξ": "<mi>&#x39E;</mi>",
    "Π": "<mi>&#x3A0;</mi>",
    "Σ": "<mi>&#x3A3;</mi>",
    "Φ": "<mi>&#x3A6;</mi>",
    "Ψ": "<mi>&#x3A8;</mi>",
    "Ω": "<mi>&#x3A9;</mi>",
    "•": "<mo>&#x2022;</mo>",
    "∂": "<mo>&#x2202;</mo>",
    "∈": "<mo>&#x2208;</mo>",
    "√": "<mo>&#x221A;</mo>",
    "∞": "<mo>&#x222E;</mo>",
    "∠": "<mo>&#x2220;</mo>",
    "∟": "<mo>&#x221F;</mo>",
    "∥": "<mo>&#x2225;</mo>",
    "∧": "<mo>&#x2227;</mo>",
    "∨": "<mo>&#x2228;</mo>",
    "∩": "<mo>&#x2229;</mo>",
    "∪": "<mo>&#x222A;</mo>",
    "∴": "<mo>&#x2234;</mo>",
    "∵": "<mo>&#x2235;</mo>",
    "≈": "<mo>&#x2248;</mo>",
    "≌": "<mo>&#x224C;</mo>",
    "≠": "<mo>&#x2260;</mo>",
    "≤": "<mo>&#x2264;</mo>",
    "≥": "<mo>&#x2265;</mo>",
    "⊙": "<mo>&#x2299;</mo>",
    "⊕": "<mo>&#x2295;</mo>",
    "⊥": "<mo>&#x22A5;</mo>",
    "ø": "<mi>&#xF8;</mi>",
    "→": "<mo>&#x2192;</mo>",
    "←": "<mo>&#x2190;</mo>",
    "↑": "<mo>&#x2191;</mo>",
    "↓": "<mo>&#x2193;</mo>",
    "∀": "<mo>&#x2200;</mo>",
    "∃": "<mo>&#x2203;</mo>",
}


def mathml2latex_yarosh(equation: str) -> str:
    """MathML to LaTeX conversion with XSLT from Vasil Yaroshevich"""
    xslt_file = os.path.join("xsl_yarosh", "mmltex.xsl")
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return newdom
