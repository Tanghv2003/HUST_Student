import random
import reflex as rx

from HUST_Student.models import LearnCard, PracticeItem


class LearnState(rx.State):
    # ── Dữ liệu gốc ───────────────────────────────────────────────
    cards: list[LearnCard] = []
    set_title: str = ""

    # ── Màn hình ──────────────────────────────────────────────────
    show_learn: bool = False
    # phase: "preview" | "practice" | "batch_review" | "round_review" | "complete"
    phase: str = "preview"

    # ── Batch config ───────────────────────────────────────────────
    BATCH_SIZE: int = 5     # số từ MỚI mỗi lô

    # ── Tracking tích lũy ─────────────────────────────────────────
    # Toàn bộ thứ tự đã shuffle một lần, không đổi trong suốt round
    all_indices: list[int] = []
    # Bao nhiêu từ đã được giới thiệu (đã qua preview ít nhất 1 lần)
    introduced_count: int = 0
    # Lô hiện tại
    batch_number: int = 0
    current_new_indices: list[int] = []
    current_old_indices: list[int] = []

    # ── Preview (chỉ từ MỚI) ──────────────────────────────────────
    preview_cards: list[int] = []
    preview_pos: int = 0
    is_preview_flipped: bool = False

    # ── Practice queue ────────────────────────────────────────────
    practice_queue: list[PracticeItem] = []
    practice_pos: int = 0

    # ── Wrong tracking ────────────────────────────────────────────
    batch_wrong: list[int] = []
    round_wrong: list[int] = []

    # ── Trả lời ───────────────────────────────────────────────────
    typed_answer: str = ""
    selected_answer: str = ""
    choice_options: list[str] = []
    correct_answer: str = ""

    # ── Feedback ──────────────────────────────────────────────────
    show_feedback: bool = False
    feedback_correct: bool = False
    feedback_message: str = ""

    # ── Thống kê ──────────────────────────────────────────────────
    total_correct: int = 0
    total_wrong: int = 0
    round_number: int = 1
    mastered_count: int = 0
    learning_count: int = 0
    not_started_count: int = 0

    # ═══════════════════════════════════════════════════════════════
    # SETUP
    # ═══════════════════════════════════════════════════════════════

    def init_learn(self, words: list[dict], title: str):
        self.set_title = title
        self.cards = [LearnCard(front=w["front"], back=w["back"]) for w in words]
        self.show_learn = True
        self.round_number = 1
        self.total_correct = 0
        self.total_wrong = 0
        self.round_wrong = []
        self.batch_number = 0
        self.introduced_count = 0

        indices = list(range(len(self.cards)))
        random.shuffle(indices)
        self.all_indices = indices

        self._load_next_batch()

    # ═══════════════════════════════════════════════════════════════
    # BATCH LOADING
    # ═══════════════════════════════════════════════════════════════

    def _load_next_batch(self):
        """
        Luồng tích lũy:
          Lô 1:  5 từ mới  +  0 từ cũ  → preview 5,  practice 5
          Lô 2:  5 từ mới  +  5 từ cũ  → preview 5,  practice 10
          Lô 3:  5 từ mới  + 10 từ cũ  → preview 5,  practice 15
          Lô N:  5 từ mới  + (N-1)*5 từ cũ
          (Lô cuối có thể ít hơn 5 từ mới nếu không đủ)
        """
        total = len(self.all_indices)
        start = self.introduced_count
        end = min(start + self.BATCH_SIZE, total)
        new_indices = self.all_indices[start:end]

        if not new_indices:
            self._end_round()
            return

        # Từ cũ = tất cả đã giới thiệu trước lô này
        old_indices = self.all_indices[0:start]

        self.current_new_indices = list(new_indices)
        self.current_old_indices = list(old_indices)
        self.batch_number += 1
        self.batch_wrong = []
        self.show_feedback = False
        self.typed_answer = ""
        self.selected_answer = ""

        # Preview chỉ từ mới
        self.preview_cards = list(new_indices)
        self.preview_pos = 0
        self.is_preview_flipped = False

        # Practice: từ mới + từ cũ
        self._build_practice_queue(list(new_indices), list(old_indices))

        self.phase = "preview"
        self._mark_new_cards_seen(list(new_indices))
        self._load_preview_card()
        self._update_counts()

    def _mark_new_cards_seen(self, new_indices: list):
        for idx in new_indices:
            card = self.cards[idx]
            if card.stage == 0:
                card.stage = 1
                self.cards[idx] = card

    def _build_practice_queue(self, new_indices: list, old_indices: list):
        """
        Từ mới  → luôn type (ghi nhớ lần đầu)
        Từ cũ   → mặc định type, chỉ xen kẽ choice khi streak >= 2 VÀ chưa sai lần nào
        Shuffle toàn bộ sau khi tạo.
        """
        practice: list[PracticeItem] = []

        for card_idx in new_indices:
            practice.append(PracticeItem(
                card_index=card_idx,
                mode="type",
                is_new=True,
            ))

        for i, card_idx in enumerate(old_indices):
            card = self.cards[card_idx]
            # Từ cũ: luôn type, chỉ thêm choice xen kẽ khi đã thành thạo tốt (streak >= 2)
            if card.correct_streak >= 2 and card.wrong_count == 0:
                mode = "choice" if i % 2 == 0 else "type"
            else:
                mode = "type"
            practice.append(PracticeItem(
                card_index=card_idx,
                mode=mode,
                is_new=False,
            ))

        random.shuffle(practice)
        self.practice_queue = practice
        self.practice_pos = 0

    # ═══════════════════════════════════════════════════════════════
    # PHASE: PREVIEW
    # ═══════════════════════════════════════════════════════════════

    def _load_preview_card(self):
        if self.preview_pos >= len(self.preview_cards):
            # Hết preview → cập nhật introduced_count rồi sang practice
            self.introduced_count += len(self.current_new_indices)
            self.phase = "practice"
            self._load_practice_item()
            return
        card_idx = self.preview_cards[self.preview_pos]
        self.correct_answer = self.cards[card_idx].back
        self.is_preview_flipped = False

    def flip_preview(self):
        self.is_preview_flipped = not self.is_preview_flipped

    def preview_got_it(self):
        if self.preview_pos >= len(self.preview_cards):
            return
        card_idx = self.preview_cards[self.preview_pos]
        card = self.cards[card_idx]
        card.correct_streak += 1
        self.cards[card_idx] = card
        self.total_correct += 1
        self.preview_pos += 1
        self._update_counts()
        self._load_preview_card()

    def preview_still_learning(self):
        if self.preview_pos >= len(self.preview_cards):
            return
        card_idx = self.preview_cards[self.preview_pos]
        if card_idx not in self.batch_wrong:
            self.batch_wrong = self.batch_wrong + [card_idx]
        self.preview_pos += 1
        self._load_preview_card()

    # ═══════════════════════════════════════════════════════════════
    # PHASE: PRACTICE
    # ═══════════════════════════════════════════════════════════════

    def _load_practice_item(self):
        self.typed_answer = ""
        self.selected_answer = ""
        self.show_feedback = False
        self.feedback_message = ""

        if self.practice_pos >= len(self.practice_queue):
            self._end_batch()
            return

        item = self.practice_queue[self.practice_pos]
        self.correct_answer = self.cards[item.card_index].back
        if item.mode == "choice":
            self._build_choices(item.card_index)

    def _build_choices(self, card_idx: int):
        correct = self.cards[card_idx].back
        others = [c.back for i, c in enumerate(self.cards) if i != card_idx]
        sample = random.sample(others, min(3, len(others)))
        while len(sample) < 3:
            sample.append("—")
        opts = [correct] + sample
        random.shuffle(opts)
        self.choice_options = opts

    def _record_answer(self, card_idx: int, is_correct: bool):
        card = self.cards[card_idx]
        if is_correct:
            card.correct_streak += 1
            card.last_wrong = False
            card.stage = min(card.stage + 1, 4)
            self.total_correct += 1
        else:
            card.wrong_count += 1
            card.correct_streak = 0
            card.last_wrong = True
            card.stage = max(card.stage - 1, 1)
            self.total_wrong += 1
            if card_idx not in self.batch_wrong:
                self.batch_wrong = self.batch_wrong + [card_idx]
            if card_idx not in self.round_wrong:
                self.round_wrong = self.round_wrong + [card_idx]
        self.cards[card_idx] = card
        self._update_counts()

    # ── Type ──────────────────────────────────────────────────────

    def set_typed_answer(self, text: str):
        self.typed_answer = str(text) if text else ""

    def submit_typed(self):
        if not self.typed_answer.strip() or self.show_feedback:
            return
        if self.practice_pos >= len(self.practice_queue):
            return
        item = self.practice_queue[self.practice_pos]
        card = self.cards[item.card_index]
        is_correct = self.typed_answer.strip().lower() == card.back.strip().lower()
        self.show_feedback = True
        self.feedback_correct = is_correct
        self.feedback_message = (
            f"✅ Chính xác! Đáp án: {card.back}" if is_correct
            else f"❌ Đáp án đúng: {card.back}"
        )
        self._record_answer(item.card_index, is_correct)

    def continue_after_type(self):
        self.show_feedback = False
        self.practice_pos += 1
        self._load_practice_item()

    # ── Choice ────────────────────────────────────────────────────

    def select_choice(self, option: str):
        if self.selected_answer != "" or self.show_feedback:
            return
        if self.practice_pos >= len(self.practice_queue):
            return
        item = self.practice_queue[self.practice_pos]
        card = self.cards[item.card_index]
        is_correct = option == card.back
        self.selected_answer = option
        self.show_feedback = True
        self.feedback_correct = is_correct
        self.feedback_message = (
            "✅ Chính xác!" if is_correct
            else f"❌ Đáp án đúng: {card.back}"
        )
        self._record_answer(item.card_index, is_correct)

    def continue_after_choice(self):
        self.show_feedback = False
        self.selected_answer = ""
        self.practice_pos += 1
        self._load_practice_item()

    # ═══════════════════════════════════════════════════════════════
    # BATCH REVIEW
    # ═══════════════════════════════════════════════════════════════

    def _end_batch(self):
        """Hết practice: nếu có sai → batch_review (gõ lại), không thì lô tiếp."""
        wrong = list(set(self.batch_wrong))
        if wrong:
            review: list[PracticeItem] = [
                PracticeItem(card_index=idx, mode="type", is_new=False)
                for idx in wrong
            ]
            random.shuffle(review)
            self.practice_queue = review
            self.practice_pos = 0
            self.batch_wrong = []
            self.phase = "batch_review"
            self._load_practice_item()
        else:
            self._load_next_batch()

    def finish_batch_review(self):
        """Gọi sau khi hết practice trong batch_review → sang lô tiếp."""
        # _end_batch sẽ tự gọi _load_next_batch vì batch_wrong đã rỗng
        self._load_next_batch()

    # ═══════════════════════════════════════════════════════════════
    # ROUND REVIEW / COMPLETE
    # ═══════════════════════════════════════════════════════════════

    def _end_round(self):
        not_mastered = [i for i, c in enumerate(self.cards) if c.stage < 4]
        if not_mastered:
            self.phase = "round_review"
        else:
            self.phase = "complete"
        self._update_counts()

    def continue_round_review(self):
        """Vòng mới: chỉ học lại các thẻ chưa thành thạo, tích lũy lại từ đầu."""
        self.round_number += 1
        not_mastered = [i for i, c in enumerate(self.cards) if c.stage < 4]
        random.shuffle(not_mastered)
        self.all_indices = not_mastered
        self.introduced_count = 0
        self.batch_number = 0
        self.round_wrong = []
        self._load_next_batch()

    # ═══════════════════════════════════════════════════════════════
    # CLOSE
    # ═══════════════════════════════════════════════════════════════

    def close_learn(self):
        self.show_learn = False
        self.cards = []
        self.all_indices = []
        self.practice_queue = []
        self.preview_cards = []
        self.current_new_indices = []
        self.current_old_indices = []
        self.round_wrong = []
        self.batch_wrong = []
        self.phase = "preview"
        self.typed_answer = ""
        self.selected_answer = ""
        self.show_feedback = False
        self.introduced_count = 0
        self.batch_number = 0

    # ═══════════════════════════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════════════════════════

    def _update_counts(self):
        self.mastered_count = sum(1 for c in self.cards if c.stage >= 4)
        self.learning_count = sum(1 for c in self.cards if 0 < c.stage < 4)
        self.not_started_count = sum(1 for c in self.cards if c.stage == 0)

    # ═══════════════════════════════════════════════════════════════
    # COMPUTED VARS
    # ═══════════════════════════════════════════════════════════════

    @rx.var
    def current_card_front(self) -> str:
        if self.phase == "preview":
            if self.preview_pos >= len(self.preview_cards):
                return ""
            idx = self.preview_cards[self.preview_pos]
        elif self.phase in ("practice", "batch_review"):
            if self.practice_pos >= len(self.practice_queue):
                return ""
            idx = self.practice_queue[self.practice_pos].card_index
        else:
            return ""
        return self.cards[idx].front if idx < len(self.cards) else ""

    @rx.var
    def current_card_back(self) -> str:
        if self.phase == "preview":
            if self.preview_pos >= len(self.preview_cards):
                return ""
            idx = self.preview_cards[self.preview_pos]
        elif self.phase in ("practice", "batch_review"):
            if self.practice_pos >= len(self.practice_queue):
                return ""
            idx = self.practice_queue[self.practice_pos].card_index
        else:
            return ""
        return self.cards[idx].back if idx < len(self.cards) else ""

    @rx.var
    def current_practice_mode(self) -> str:
        if self.practice_pos >= len(self.practice_queue):
            return "type"
        return self.practice_queue[self.practice_pos].mode

    @rx.var
    def current_item_is_new(self) -> bool:
        if self.practice_pos >= len(self.practice_queue):
            return False
        return self.practice_queue[self.practice_pos].is_new

    @rx.var
    def batch_label(self) -> str:
        total = len(self.all_indices)
        if total == 0:
            return ""
        total_batches = (total + self.BATCH_SIZE - 1) // self.BATCH_SIZE
        return f"Lô {self.batch_number}/{total_batches}"

    @rx.var
    def batch_composition_label(self) -> str:
        """Ví dụ: '5 từ mới · 10 từ ôn lại'"""
        new_count = len(self.current_new_indices)
        old_count = len(self.current_old_indices)
        if old_count == 0:
            return f"{new_count} từ mới"
        return f"{new_count} từ mới · {old_count} từ ôn lại"

    @rx.var
    def queue_progress_label(self) -> str:
        if self.phase == "preview":
            total = len(self.preview_cards)
            return f"Preview {self.preview_pos + 1}/{total}"
        elif self.phase in ("practice", "batch_review"):
            total = len(self.practice_queue)
            return f"Câu {self.practice_pos + 1}/{total}"
        return ""

    @rx.var
    def batch_progress_pct(self) -> int:
        """% tiến độ trong lô hiện tại."""
        preview_total = len(self.preview_cards)
        practice_total = len(self.practice_queue)
        total_steps = preview_total + practice_total
        if total_steps == 0:
            return 0
        if self.phase == "preview":
            done = self.preview_pos
        elif self.phase in ("practice", "batch_review"):
            done = preview_total + self.practice_pos
        else:
            done = total_steps
        return min(100, (done * 100) // total_steps)

    @rx.var
    def total_progress_pct(self) -> int:
        """% tổng: bao nhiêu từ đã được giới thiệu / tổng số từ."""
        total = len(self.all_indices)
        if total == 0:
            return 0
        return min(100, (self.introduced_count * 100) // total)

    @rx.var
    def accuracy_pct(self) -> int:
        total = self.total_correct + self.total_wrong
        if total == 0:
            return 0
        return (self.total_correct * 100) // total