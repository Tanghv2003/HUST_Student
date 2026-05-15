"""Lấy cụm giao tiếp chỉ qua API Internet (không có dữ liệu offline).

Biến môi trường bắt buộc: HUST_CONVERSATION_API_URL — base URL, ví dụ https://api.example.com/

Endpoint (GET):
  {BASE}/phrases?native=vi&foreign=en&native_level=beginner&foreign_level=beginner

Response JSON:
  {"phrases": [{"native": "...", "foreign": "...", "topic": "..."}]}

Các khóa câu được chấp nhận cho mỗi phần tử: native/source; foreign/target/translation.
"""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

_DEFAULT_TIMEOUT = 20

STATUS_OK = "ok"
STATUS_SAME_LANGUAGE = "same_language"
STATUS_MISSING_URL = "missing_api_url"
STATUS_HTTP = "http_error"
STATUS_NETWORK = "network_error"
STATUS_TIMEOUT = "timeout"
STATUS_BAD_JSON = "bad_json"
STATUS_BAD_SHAPE = "bad_response"
STATUS_EMPTY = "empty_phrases"


def get_phrases(
    native: str,
    foreign: str,
    native_level: str,
    foreign_level: str,
) -> tuple[list[dict], str]:
    """
    Trả về (danh_sách_cụm, trạng_thái).

    Trạng thái: ok | same_language | missing_api_url | http_error | network_error |
    timeout | bad_json | bad_response | empty_phrases
    """
    if native.strip().lower() == foreign.strip().lower():
        return [], STATUS_SAME_LANGUAGE

    base = (os.environ.get("HUST_CONVERSATION_API_URL") or "").strip()
    if not base:
        return [], STATUS_MISSING_URL

    qs = urlencode(
        {
            "native": native,
            "foreign": foreign,
            "native_level": native_level,
            "foreign_level": foreign_level,
        }
    )
    url = f"{base.rstrip('/')}/phrases?{qs}"
    req = Request(url, headers={"Accept": "application/json"})

    try:
        with urlopen(req, timeout=_DEFAULT_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except HTTPError:
        return [], STATUS_HTTP
    except URLError:
        return [], STATUS_NETWORK
    except TimeoutError:
        return [], STATUS_TIMEOUT
    except (json.JSONDecodeError, UnicodeDecodeError):
        return [], STATUS_BAD_JSON

    if not isinstance(payload, dict):
        return [], STATUS_BAD_SHAPE
    raw = payload.get("phrases")
    if not isinstance(raw, list):
        return [], STATUS_BAD_SHAPE

    out: list[dict] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        n = item.get("native") or item.get("source") or ""
        f = item.get("foreign") or item.get("target") or item.get("translation") or ""
        if n and f:
            row = {"native": str(n).strip(), "foreign": str(f).strip()}
            if item.get("topic"):
                row["topic"] = str(item["topic"])
            if item.get("hint"):
                row["hint"] = str(item["hint"])
            out.append(row)

    if not out:
        return [], STATUS_EMPTY
    return out, STATUS_OK
