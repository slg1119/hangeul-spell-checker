import asyncio
import json
import re
import ssl
import time
from collections import OrderedDict

import aiohttp
import certifi

from hanspell.constants import base_url
from hanspell.response import Checked
from hanspell.utils import remove_tags, process_html_result

ssl_context = ssl.create_default_context(cafile=certifi.where())


async def _get_passport_key_async():
    """
    네이버에서 '네이버 맞춤법 검사기' 페이지에서 passportKey를 비동기로 획득
    """
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=네이버+맞춤법+검사기"

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        async with session.get(url) as response:
            html_text = await response.text()

    match = re.search(r'passportKey=([^&"}]+)', html_text)
    if match:
        passport_key = match.group(1)
        return passport_key
    else:
        assert (
            False
        ), "passportKey를 찾을 수 없습니다. 네이버 맞춤법 검사기 페이지를 확인하세요."


async def check_async(text):
    """
    매개변수로 입력받은 한글 문장의 맞춤법을 비동기로 체크합니다.
    """
    if isinstance(text, list):
        tasks = [check_async(item) for item in text]
        return await asyncio.gather(*tasks)

    # 최대 500자까지 가능.
    if len(text) > 500:
        return Checked(result=False)

    passport_key = await _get_passport_key_async()

    payload = {
        "color_blindness": "0",
        "q": text,
        "passportKey": passport_key,
    }

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "referer": "https://search.naver.com/",
    }

    start_time = time.time()

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        async with session.get(base_url, params=payload, headers=headers) as response:
            response_text = await response.text()

    passed_time = time.time() - start_time

    data = json.loads(response_text)
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
