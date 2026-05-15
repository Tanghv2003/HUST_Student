import random
import reflex as rx
from pydantic import BaseModel


class LearnCard(BaseModel):
    front: str
    back: str
    # Trạng thái học của từng thẻ
    stage: int = 0          # 0=chưa học, 1=đã xem, 2=gõ đúng 1 lần, 3=trắc nghiệm đúng, 4=thành thạo
    correct_streak: int = 0 # Số lần đúng liên tiếp
    wrong_count: int = 0    # Số lần sai tổng
    last_wrong: bool = False


class LearnRecord(BaseModel):
    front: str
    back: str
    is_correct: bool
    user_answer: str


class LearnState(rx.State):
    # Dữ liệu
    cards: list[LearnCard] = []
    set_title: str = ""

    # Trạng thái màn hình
    show_learn: bool = False
    phase: str = "preview"   # "preview" | "type" | "choice" | "review" | "complete"

    # Vòng học hiện tại
    current_index: int = 0
    queue: list[int] = []        # index vào cards[], thứ tự học vòng này
    wrong_queue: list[int] = []  # index cần ôn lại sau vòng

    # Trả lời
    typed_answer: str = ""
    selected_answer: str = ""
    choice_options: list[str] = []
    correct_answer: str = ""
    is_preview_flipped: bool = False

    # Feedback
    show_feedback: bool = False
    feedback_correct: bool = False
    feedback_message: str = ""

    # Lịch sử vòng hiện tại
    round_records: list[LearnRecord] = []

    # Thống kê tổng
    total_correct: int = 0
    total_wrong: int = 0
    round_number: int = 1

    # Đếm tiến độ
    mastered_count: int = 0
    learning_count: int = 0
    not_started_count: int = 0

    # ── Setup ─────────────────────────────────────────────────────────────────

    def init_learn(self, words: list[dict], title: str):
        """Khởi động chế độ Học từ danh sách words [{front, back}]."""
        self.set_title = title
        self.cards = [
            LearnCard(front=w["front"], back=w["back"])
            for w in words
        ]
        self.show_learn = True
        self.round_number = 1
        self.total_correct = 0
        self.total_wrong = 0
        self.round_records = []
        self._reset_round()

    def _reset_round(self):
        """Chuẩn bị queue cho vòng học mới."""
        # Ưu tiên: sai nhiều → chưa học → đang học → thành thạo
        not_mastered = [i for i, c in enumerate(self.cards) if c.stage < 4]
        if not not_mastered:
            self._start_complete()
            return

        # Sắp xếp: sai nhiều nhất lên trước
        sorted_q = sorted(not_mastered, key=lambda i: (-self.cards[i].wrong_count, self.cards[i].stage))
        self.queue = sorted_q
        self.wrong_queue = []
        self.current_index = 0
        self._update_counts()
        self._load_current_card()

    def _load_current_card(self):
        """Load câu hỏi cho card hiện tại trong queue."""
        self.typed_answer = ""
        self.selected_answer = ""
        self.show_feedback = False
        self.feedback_message = ""
        self.is_preview_flipped = False

        if self.current_index >= len(self.queue):
            self._finish_round()
            return

        card_idx = self.queue[self.current_index]
        card = self.cards[card_idx]
        self.correct_answer = card.back

        # Chọn phase dựa vào stage của card
        if card.stage == 0:
            self.phase = "preview"
        elif card.stage == 1:
            self.phase = "type"
        elif card.stage == 2:
            self.phase = "choice"
            self._build_choices(card_idx)
        else:
            # stage 3: lại trắc nghiệm hoặc type để củng cố
            if card.wrong_count > 0:
                self.phase = "type"
            else:
                self.phase = "choice"
                self._build_choices(card_idx)

    def _build_choices(self, card_idx: int):
        correct = self.cards[card_idx].back
        others = [c.back for i, c in enumerate(self.cards) if i != card_idx]
        sample = random.sample(others, min(3, len(others)))
        while len(sample) < 3:
            sample.append("—")
        opts = [correct] + sample
        random.shuffle(opts)
        self.choice_options = opts

    def _update_counts(self):
        self.mastered_count = sum(1 for c in self.cards if c.stage >= 4)
        self.learning_count = sum(1 for c in self.cards if 0 < c.stage < 4)
        self.not_started_count = sum(1 for c in self.cards if c.stage == 0)

    # ── Preview phase ─────────────────────────────────────────────────────────

    def flip_preview(self):
        self.is_preview_flipped = not self.is_preview_flipped

    def preview_got_it(self):
        """Người dùng nhấn "Đã biết" ở màn preview."""
        if self.current_index >= len(self.queue):
            return
        card_idx = self.queue[self.current_index]
        card = self.cards[card_idx]
        card.stage = max(card.stage, 1)
        card.correct_streak += 1
        self.cards[card_idx] = card

        record = LearnRecord(
            front=card.front,
            back=card.back,
            is_correct=True,
            user_answer="(xem thẻ)",
        )
        self.round_records = self.round_records + [record]
        self.total_correct += 1
        self._advance()

    def preview_still_learning(self):
        """Người dùng nhấn "Vẫn đang học" ở màn preview."""
        if self.current_index >= len(self.queue):
            return
        card_idx = self.queue[self.current_index]
        card = self.cards[card_idx]
        card.stage = max(card.stage, 1)
        self.cards[card_idx] = card
        self.wrong_queue = self.wrong_queue + [card_idx]
        self._advance()

    # ── Type phase ────────────────────────────────────────────────────────────

    def set_typed_answer(self, text: str):
        self.typed_answer = str(text) if text else ""

    def submit_typed(self):
        if not self.typed_answer.strip():
            return
        if self.current_index >= len(self.queue):
            return
        card_idx = self.queue[self.current_index]
        card = self.cards[card_idx]

        user = self.typed_answer.strip().lower()
        correct = card.back.strip().lower()
        is_correct = (user == correct)

        self.show_feedback = True
        self.feedback_correct = is_correct
        if is_correct:
            self.feedback_message = f"✅ Chính xác! Đáp án: {card.back}"
            card.correct_streak += 1
            card.last_wrong = False
            card.stage = min(card.stage + 1, 4)
            self.total_correct += 1
        else:
            self.feedback_message = f"❌ Đáp án đúng: {card.back}"
            card.wrong_count += 1
            card.correct_streak = 0
            card.last_wrong = True
            card.stage = max(card.stage - 1, 1)
            self.wrong_queue = self.wrong_queue + [card_idx]
            self.total_wrong += 1

        self.cards[card_idx] = card
        record = LearnRecord(
            front=card.front,
            back=card.back,
            is_correct=is_correct,
            user_answer=self.typed_answer.strip(),
        )
        self.round_records = self.round_records + [record]

    def continue_after_type(self):
        self.show_feedback = False
        self._advance()

    # ── Choice phase ──────────────────────────────────────────────────────────

    def select_choice(self, option: str):
        if self.selected_answer != "" or self.current_index >= len(self.queue):
            return
        self.selected_answer = option
        card_idx = self.queue[self.current_index]
        card = self.cards[card_idx]

        is_correct = (option == card.back)
        self.show_feedback = True
        self.feedback_correct = is_correct
        if is_correct:
            self.feedback_message = f"✅ Chính xác!"
            card.correct_streak += 1
            card.last_wrong = False
            card.stage = min(card.stage + 1, 4)
            self.total_correct += 1
        else:
            self.feedback_message = f"❌ Đáp án đúng: {card.back}"
            card.wrong_count += 1
            card.correct_streak = 0
            card.last_wrong = True
            card.stage = max(card.stage - 1, 1)
            self.wrong_queue = self.wrong_queue + [card_idx]
            self.total_wrong += 1

        self.cards[card_idx] = card
        record = LearnRecord(
            front=card.front,
            back=card.back,
            is_correct=is_correct,
            user_answer=option,
        )
        self.round_records = self.round_records + [record]

    def continue_after_choice(self):
        self.show_feedback = False
        self.selected_answer = ""
        self._advance()

    # ── Navigation ────────────────────────────────────────────────────────────

    def _advance(self):
        self.current_index += 1
        self._update_counts()
        if self.current_index >= len(self.queue):
            self._finish_round()
        else:
            self._load_current_card()

    def _finish_round(self):
        """Kết thúc vòng: nếu còn câu sai → vòng mới với câu sai đó."""
        if self.wrong_queue:
            # Có câu sai → ôn lại
            self.queue = list(set(self.wrong_queue))  # deduplicate
            random.shuffle(self.queue)
            self.wrong_queue = []
            self.current_index = 0
            self.round_number += 1
            self.round_records = []
            self.phase = "review"  # Thông báo "Ôn lại" trước
        else:
            # Tất cả đúng → check xem có thẻ nào chưa thành thạo
            not_mastered = [i for i, c in enumerate(self.cards) if c.stage < 4]
            if not_mastered:
                self.queue = not_mastered
                random.shuffle(self.queue)
                self.wrong_queue = []
                self.current_index = 0
                self.round_number += 1
                self.round_records = []
                self.phase = "review"
            else:
                self._start_complete()

    def _start_complete(self):
        self.phase = "complete"
        self._update_counts()

    def continue_review_round(self):
        """Sau màn review summary → tiếp tục vòng mới."""
        self._load_current_card()

    # ── Close ─────────────────────────────────────────────────────────────────

    def close_learn(self):
        self.show_learn = False
        self.cards = []
        self.queue = []
        self.wrong_queue = []
        self.round_records = []
        self.phase = "preview"
        self.typed_answer = ""
        self.selected_answer = ""
        self.show_feedback = False

    # ── Computed vars ─────────────────────────────────────────────────────────

    @rx.var
    def current_card_front(self) -> str:
        if not self.queue or self.current_index >= len(self.queue):
            return ""
        idx = self.queue[self.current_index]
        if idx >= len(self.cards):
            return ""
        return self.cards[idx].front

    @rx.var
    def current_card_back(self) -> str:
        if not self.queue or self.current_index >= len(self.queue):
            return ""
        idx = self.queue[self.current_index]
        if idx >= len(self.cards):
            return ""
        return self.cards[idx].back

    @rx.var
    def current_card_stage(self) -> int:
        if not self.queue or self.current_index >= len(self.queue):
            return 0
        idx = self.queue[self.current_index]
        if idx >= len(self.cards):
            return 0
        return self.cards[idx].stage

    @rx.var
    def progress_pct(self) -> int:
        total = len(self.cards)
        if total == 0:
            return 0
        done = self.current_index
        return min(100, (done * 100) // max(len(self.queue), 1))

    @rx.var
    def queue_progress_label(self) -> str:
        return f"{self.current_index + 1} / {len(self.queue)}"

    @rx.var
    def accuracy_pct(self) -> int:
        total = self.total_correct + self.total_wrong
        if total == 0:
            return 0
        return (self.total_correct * 100) // total