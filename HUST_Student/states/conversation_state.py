from __future__ import annotations

import reflex as rx

from HUST_Student.models.conversation import ChatLine
from HUST_Student.services.conversation_phrases import (
    STATUS_BAD_JSON,
    STATUS_BAD_SHAPE,
    STATUS_EMPTY,
    STATUS_HTTP,
    STATUS_MISSING_URL,
    STATUS_NETWORK,
    STATUS_OK,
    STATUS_SAME_LANGUAGE,
    STATUS_TIMEOUT,
    get_phrases,
)

LEVEL_BEGINNER = "beginner"
LEVEL_INTERMEDIATE = "intermediate"
LEVEL_ADVANCED = "advanced"


class ConversationState(rx.State):
    native_lang: str = "vi"
    foreign_lang: str = "en"
    native_level: str = LEVEL_BEGINNER
    foreign_level: str = LEVEL_BEGINNER

    phrases: list[dict] = []
    phrase_index: int = 0
    source: str = ""
    loading: bool = False
    error: str = ""

    user_input: str = ""
    chat_rows: list[ChatLine] = []

    def set_native_lang(self, value):
        if value is None:
            return
        self.native_lang = str(value)

    def set_foreign_lang(self, value):
        if value is None:
            return
        self.foreign_lang = str(value)

    def set_native_level(self, value):
        if value is None:
            return
        self.native_level = str(value)

    def set_foreign_level(self, value):
        if value is None:
            return
        self.foreign_level = str(value)

    def set_user_input(self, value):
        self.user_input = str(value) if value is not None else ""

    def _build_tutor_prompt(self, idx: int) -> str:
        if idx < 0 or idx >= len(self.phrases):
            return ""
        p = self.phrases[idx]
        native_text = str(p.get("native", ""))
        topic = p.get("topic")
        lines = [
            f"Người bản xứ ({self.native_lang.upper()}) nói:",
            f"«{native_text}»",
            f"Hãy viết cách diễn đạt tương ứng bằng {self.foreign_lang.upper()}.",
        ]
        if topic:
            lines.insert(2, f"Chủ đề: {topic}")
        return "\n".join(lines)

    def _session_done_message(self) -> str:
        return (
            "🎉 Bạn đã hoàn thành tất cả câu trong bộ này. "
            "Nhấn «Tải câu mới» để lấy thêm hoặc đổi cấp độ / cặp ngôn ngữ."
        )

    @rx.var
    def source_badge(self) -> str:
        if self.source == "api":
            return "Nguồn: API Internet (HUST_CONVERSATION_API_URL)"
        return ""

    @rx.var
    def show_error_banner(self) -> bool:
        return bool(self.error)

    @rx.var
    def show_source_banner(self) -> bool:
        return self.source == "api"

    def load_lesson(self):
        if self.native_lang.strip().lower() == self.foreign_lang.strip().lower():
            self.error = "Chọn hai mã ngôn ngữ khác nhau (ví dụ vi và en)."
            self.phrases = []
            self.chat_rows = []
            self.source = ""
            return

        self.loading = True
        self.error = ""
        self.user_input = ""
        self.source = ""

        err_map = {
            STATUS_SAME_LANGUAGE: "Hai ngôn ngữ phải khác nhau.",
            STATUS_MISSING_URL: (
                "Chưa cấu hình API: đặt biến môi trường HUST_CONVERSATION_API_URL "
                "(base URL, ví dụ https://your-host.com) rồi chạy lại ứng dụng."
            ),
            STATUS_HTTP: (
                "API trả lỗi HTTP. Kiểm tra URL, đường dẫn /phrases và khóa API (nếu có)."
            ),
            STATUS_NETWORK: (
                "Không kết nối được tới máy chủ (mạng, DNS, hoặc URL sai)."
            ),
            STATUS_TIMEOUT: "API phản hồi quá lâu (timeout). Thử lại sau.",
            STATUS_BAD_JSON: "API trả nội dung không phải JSON hợp lệ.",
            STATUS_BAD_SHAPE: (
                "JSON từ API thiếu khóa «phrases» (mảng) hoặc cấu trúc không đúng."
            ),
            STATUS_EMPTY: (
                "API không trả cụm nào. Thử đổi native/foreign hoặc cấp độ (beginner…)."
            ),
        }

        try:
            phrases, status = get_phrases(
                self.native_lang,
                self.foreign_lang,
                self.native_level,
                self.foreign_level,
            )
            self.phrases = phrases
            self.phrase_index = 0

            if status == STATUS_OK and phrases:
                self.source = "api"
                self.chat_rows = [ChatLine(role="tutor", text=self._build_tutor_prompt(0))]
            else:
                self.chat_rows = []
                self.error = err_map.get(status, "Không tải được dữ liệu từ API.")
        finally:
            self.loading = False

    def submit_answer(self):
        if not self.phrases or self.phrase_index >= len(self.phrases):
            return
        user_raw = (self.user_input or "").strip()
        if not user_raw:
            return

        exp = str(self.phrases[self.phrase_index].get("foreign", "")).strip().lower()
        user_norm = user_raw.lower()
        ok = user_norm == exp

        fb = "✅ Khớp với gợi ý mẫu." if ok else f"💡 Gợi ý: {self.phrases[self.phrase_index].get('foreign', '')}"

        self.chat_rows = self.chat_rows + [
            ChatLine(role="user", text=user_raw),
            ChatLine(role="feedback", text=fb),
        ]
        self.user_input = ""
        self.phrase_index += 1

        if self.phrase_index < len(self.phrases):
            self.chat_rows = self.chat_rows + [
                ChatLine(role="tutor", text=self._build_tutor_prompt(self.phrase_index)),
            ]
        else:
            self.chat_rows = self.chat_rows + [
                ChatLine(role="tutor", text=self._session_done_message()),
            ]
