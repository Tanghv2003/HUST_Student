from __future__ import annotations

import os
import reflex as rx

from HUST_Student.models.conversation import ChatLine

LEVEL_BEGINNER = "beginner"
LEVEL_INTERMEDIATE = "intermediate"
LEVEL_ADVANCED = "advanced"

_LANG_NAMES = {
    "vi": "Tiếng Việt",
    "en": "Tiếng Anh",
    "ja": "Tiếng Nhật",
    "ko": "Tiếng Hàn",
    "zh": "Tiếng Trung",
    "fr": "Tiếng Pháp",
    "de": "Tiếng Đức",
}

_LEVEL_NAMES = {
    "beginner": "cơ bản (A1-A2)",
    "intermediate": "trung cấp (B1-B2)",
    "advanced": "nâng cao (C1-C2)",
}


def _get_api_key() -> str:
    """Ưu tiên: rxconfig.gemini_api_key → env GEMINI_API_KEY"""
    try:
        cfg = rx.config.get_config()
        key = str(getattr(cfg, "gemini_api_key", "") or "").strip()
        if key and not key.startswith("AIza..."):
            return key
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "").strip()


def _build_system_prompt(native: str, foreign: str, foreign_level: str) -> str:
    native_name = _LANG_NAMES.get(native, native.upper())
    foreign_name = _LANG_NAMES.get(foreign, foreign.upper())
    foreign_lvl = _LEVEL_NAMES.get(foreign_level, foreign_level)

    return f"""Bạn là gia sư hội thoại AI thân thiện, chuyên luyện {foreign_name} cho học viên người {native_name}.

## Nhiệm vụ
- Tạo tình huống giao tiếp thực tế phù hợp cấp độ {foreign_lvl} (mua sắm, hỏi đường, đặt món, giới thiệu bản thân…)
- Đóng vai nhân vật trong tình huống, nói chuyện tự nhiên bằng {foreign_name}
- Sau mỗi câu học viên gửi: nhận xét ngắn bằng {native_name}, sửa lỗi nếu có, rồi tiếp tục hội thoại
- Giữ mỗi lượt ngắn gọn (2-3 câu)

## Định dạng phản hồi
🗣️ **[Nhân vật]**: <câu thoại bằng {foreign_name}>
💡 **Nhận xét**: <giải thích ngắn bằng {native_name} — chỉ khi cần sửa lỗi>

Bắt đầu bằng cách giới thiệu tình huống và nói câu đầu tiên bằng {foreign_name}."""


async def _call_gemini(
    history: list[dict],
    system_prompt: str,
    api_key: str,
) -> str:
    """
    Gọi Gemini API (gemini-2.0-flash — miễn phí 1500 req/ngày).
    Tích hợp vòng lặp tự động thử lại khi gặp lỗi nghẽn hoặc Rate Limit (429).
    history: [{"role": "user"|"model", "parts": [{"text": "..."}]}]
    """
    import httpx
    import asyncio

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models"
        f"/gemini-2.0-flash:generateContent?key={api_key}"
    )

    payload = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": history,
        "generationConfig": {
            "maxOutputTokens": 800,
            "temperature": 0.85,
        },
    }

    max_retries = 3
    async with httpx.AsyncClient(timeout=30) as client:
        for attempt in range(max_retries):
            try:
                resp = await client.post(url, json=payload)
                
                # Nếu dính giới hạn 429 (Too Many Requests) từ Google
                if resp.status_code == 429:
                    if attempt < max_retries - 1:
                        # Chờ thời gian tăng dần: Lần 1 chờ 2s, Lần 2 chờ 4s... sau đó thử lại
                        await asyncio.sleep((attempt + 1) * 2)
                        continue
                    else:
                        raise ValueError("Hệ thống AI đang quá tải lượt yêu cầu (Lỗi 429). Vui lòng đợi khoảng 1 phút rồi nhấn gửi lại.")
                
                resp.raise_for_status()
                data = resp.json()
                break
            except httpx.RequestError as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                    continue
                raise e

    # Trích text từ response
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Gemini trả về định dạng lạ: {data}") from e


def _to_gemini_history(messages: list[dict]) -> list[dict]:
    """Chuyển history dạng {role, content} → Gemini {role, parts}."""
    result = []
    for m in messages:
        role = "model" if m["role"] == "assistant" else "user"
        result.append({"role": role, "parts": [{"text": m["content"]}]})
    return result


class ConversationState(rx.State):
    native_lang: str = "vi"
    foreign_lang: str = "en"
    native_level: str = LEVEL_BEGINNER
    foreign_level: str = LEVEL_BEGINNER

    loading: bool = False
    error: str = ""

    user_input: str = ""
    chat_rows: list[ChatLine] = []
    _message_history: list[dict] = []  # {role: user|assistant, content: str}

    # ── Setters ──────────────────────────────────────────────────

    def set_native_lang(self, v):
        if v:
            self.native_lang = str(v)

    def set_foreign_lang(self, v):
        if v:
            self.foreign_lang = str(v)

    def set_native_level(self, v):
        if v:
            self.native_level = str(v)

    def set_foreign_level(self, v):
        if v:
            self.foreign_level = str(v)

    def set_user_input(self, v):
        self.user_input = str(v) if v is not None else ""

    def handle_key_press(self, key: str):
        if key == "Enter" and self.user_input.strip():
            return ConversationState.submit_answer

    # ── Computed ─────────────────────────────────────────────────

    @rx.var
    def show_error_banner(self) -> bool:
        return bool(self.error)

    # ── Actions ──────────────────────────────────────────────────

    @rx.event(background=True)
    async def load_lesson(self):
        async with self:
            if self.native_lang == self.foreign_lang:
                self.error = "Chọn hai ngôn ngữ khác nhau."
                return

            api_key = _get_api_key()
            if not api_key:
                self.error = (
                    "Chưa có Gemini API key. "
                    "Mở rxconfig.py → điền gemini_api_key='AIza...' "
                    "rồi restart reflex run."
                )
                return

            self.loading = True
            self.error = ""
            self.chat_rows = []
            self._message_history = []
            self.user_input = ""

        system = _build_system_prompt(
            self.native_lang, self.foreign_lang, self.foreign_level,
        )
        first_msg = {"role": "user", "content": "Bắt đầu phiên học!"}

        try:
            ai_text = await _call_gemini(
                _to_gemini_history([first_msg]), system, _get_api_key()
            )
            async with self:
                self._message_history = [
                    first_msg,
                    {"role": "assistant", "content": ai_text},
                ]
                self.chat_rows = [ChatLine(role="tutor", text=ai_text)]
                self.loading = False
        except Exception as e:
            async with self:
                self.error = f"Lỗi Gemini API: {str(e)[:200]}"
                self.loading = False

    @rx.event(background=True)
    async def submit_answer(self):
        async with self:
            user_text = self.user_input.strip()
            if not user_text or self.loading:
                return
            if not self._message_history:
                self.error = "Nhấn «Bắt đầu phiên học» trước!"
                return

            self.loading = True
            self.error = ""
            self.user_input = ""
            self.chat_rows = list(self.chat_rows) + [
                ChatLine(role="user", text=user_text)
            ]
            new_history = list(self._message_history) + [
                {"role": "user", "content": user_text}
            ]

        system = _build_system_prompt(
            self.native_lang, self.foreign_lang, self.foreign_level,
        )

        try:
            ai_text = await _call_gemini(
                _to_gemini_history(new_history), system, _get_api_key()
            )
            async with self:
                self._message_history = new_history + [
                    {"role": "assistant", "content": ai_text}
                ]
                self.chat_rows = list(self.chat_rows) + [
                    ChatLine(role="tutor", text=ai_text)
                ]
                self.loading = False
        except Exception as e:
            async with self:
                self.error = f"Lỗi Gemini API: {str(e)[:200]}"
                self.loading = False