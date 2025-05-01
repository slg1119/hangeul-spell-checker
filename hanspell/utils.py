import xml.etree.ElementTree as ET

from hanspell.constants import CheckResult
from hanspell.response import Checked


def remove_tags(text):
    text = "<content>{}</content>".format(text).replace("<br>", "")
    result = "".join(ET.fromstring(text).itertext())

    return result


def process_html_result(html, result):
    """
    HTML 결과를 처리하는 공통 함수
    """
    # 띄어쓰기로 구분하기 위해 태그는 일단 보기 쉽게 바꿔둠.
    html = (
        html.replace("<em class='green_text'>", "<green>")
        .replace("<em class='red_text'>", "<red>")
        .replace("<em class='violet_text'>", "<violet>")
        .replace("<em class='blue_text'>", "<blue>")
        .replace("</em>", "<end>")
    )
    items = html.split(" ")
    words = []
    tmp = ""
    for word in items:
        if tmp == "" and word[:1] == "<":
            pos = word.find(">") + 1
            tmp = word[:pos]
        elif tmp != "":
            word = "{}{}".format(tmp, word)

        if word[-5:] == "<end>":
            word = word.replace("<end>", "")
            tmp = ""

        words.append(word)

    for word in words:
        check_result = CheckResult.PASSED
        if word[:5] == "<red>":
            check_result = CheckResult.WRONG_SPELLING
            word = word.replace("<red>", "")
        elif word[:7] == "<green>":
            check_result = CheckResult.WRONG_SPACING
            word = word.replace("<green>", "")
        elif word[:8] == "<violet>":
            check_result = CheckResult.AMBIGUOUS
            word = word.replace("<violet>", "")
        elif word[:6] == "<blue>":
            check_result = CheckResult.STATISTICAL_CORRECTION
            word = word.replace("<blue>", "")
        result["words"][word] = check_result

    return Checked(**result)
