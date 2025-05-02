"""
Python용 한글 맞춤법 검사 모듈
"""

import re
import requests
import json
import time
from collections import OrderedDict

from .response import Checked
from .constants import base_url
from .utils import remove_tags, process_html_result

_agent = requests.Session()
passport_key = ""


def _get_passport_key():
    """
    네이버에서 '네이버 맞춤법 검사기' 페이지에서 passportKey를 획득

    네이버에서 '네이버 맞춤법 검사기'를 띄운 후
    html에서 passportKey를 검색하면 값을 찾을 수 있다.
    """

    global passport_key
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=네이버+맞춤법+검사기"
    res = requests.get(url)

    html_text = res.text

    match = re.search(r'passportKey=([^&"}]+)', html_text)
    if match:
        passport_key = match.group(1)
    return passport_key


def check(text):
    """
    매개변수로 입력받은 한글 문장의 맞춤법을 체크합니다.
    """
    if isinstance(text, list):
        result = []
        for item in text:
            checked = check(item)
            result.append(checked)
        return result

    # 최대 500자까지 가능.
    if len(text) > 300:
        return Checked(result=False)

    payload = {
        "color_blindness": "0",
        "q": text,
        "passportKey": _get_passport_key(),
    }

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "referer": "https://search.naver.com/",
    }

    start_time = time.time()
    r = _agent.get(base_url, params=payload, headers=headers)
    passed_time = time.time() - start_time

    data = json.loads(r.text)
    html = data["message"]["result"]["html"]
    result = {
        "result": True,
        "original": text,
        "checked": remove_tags(html),
        "errors": data["message"]["result"]["errata_count"],
        "time": passed_time,
        "words": OrderedDict(),
    }

    # 결과 처리 로직
    result = process_html_result(html, result)
    return result
