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

    # ── Hướng hỏi-đáp ─────────────────────────────────────────────
    answer_language: str = "native_to_foreign"

    # ── Batch config ───────────────────────────────────────────────
    BATCH_SIZE: int = 5
    SESSION_SRS_GAP: int = 3

    # ── Tracking tích lũy ─────────────────────────────────────────
    all_indices: list[int] = []
    introduced_count: int = 0
    batch_number: int = 0
    current_new_indices: list[int] = []
    current_old_indices: list[int] = []

    # ── Preview ──────────────────────────────────────────────────
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
    user_answer: str = ""
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

    # ── Âm thanh ──────────────────────────────────────────────────
    # Tốc độ: 0.5 | 0.7 | 1.0 | 1.3 | 1.6
    speech_rate: float = 1.0
    # Âm lượng: 0.0 → 1.0 (0%, 25%, 50%, 75%, 100%)
    speech_volume: float = 1.0

    # ═══════════════════════════════════════════════════════════════
    # SETUP
    # ═══════════════════════════════════════════════════════════════

    def init_learn(self, words: list[dict], title: str, answer_language: str = "native_to_foreign"):
        self.set_title = title
        self.answer_language = answer_language
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

        return self._load_next_batch()

    def set_answer_language(self, value: str):
        if value in ("native_to_foreign", "foreign_to_native"):
            self.answer_language = value

    def set_speech_rate(self, value: float):
        self.speech_rate = float(value)

    def set_speech_volume(self, value: float):
        self.speech_volume = max(0.0, min(1.0, float(value)))

    # ── Helpers ──────────────────────────────────────────────────

    def _get_prompt(self, card: LearnCard) -> str:
        if self.answer_language == "foreign_to_native":
            return card.back
        return card.front

    def _get_answer(self, card: LearnCard) -> str:
        if self.answer_language == "foreign_to_native":
            return card.front
        return card.back

    # ═══════════════════════════════════════════════════════════════
    # BATCH LOADING
    # ═══════════════════════════════════════════════════════════════

    def _load_next_batch(self):
        total = len(self.all_indices)
        start = self.introduced_count
        end = min(start + self.BATCH_SIZE, total)
        new_indices = self.all_indices[start:end]

        if not new_indices:
            self._end_round()
            return

        old_indices = self.all_indices[0:start]

        self.current_new_indices = list(new_indices)
        self.current_old_indices = list(old_indices)
        self.batch_number += 1
        self.batch_wrong = []
        self.show_feedback = False
        self.typed_answer = ""
        self.user_answer = ""
        self.selected_answer = ""

        self.preview_cards = list(new_indices)
        self.preview_pos = 0
        self.is_preview_flipped = False

        self._build_practice_queue(list(new_indices), list(old_indices))

        self.phase = "preview"
        self._mark_new_cards_seen(list(new_indices))
        self._update_counts()
        return self._load_preview_card()

    def _mark_new_cards_seen(self, new_indices: list):
        for idx in new_indices:
            card = self.cards[idx]
            if card.stage == 0:
                card.stage = 1
                self.cards[idx] = card

    def _build_practice_queue(self, new_indices: list, old_indices: list):
        practice_new: list[PracticeItem] = [
            PracticeItem(card_index=idx, mode="type", is_new=True)
            for idx in new_indices
        ]
        practice_old: list[PracticeItem] = []
        for i, card_idx in enumerate(old_indices):
            card = self.cards[card_idx]
            if card.correct_streak >= 2 and card.wrong_count == 0:
                mode = "choice" if i % 2 == 0 else "type"
            else:
                mode = "type"
            practice_old.append(
                PracticeItem(card_index=card_idx, mode=mode, is_new=False)
            )

        random.shuffle(practice_new)
        practice_old.sort(
            key=lambda it: (
                -self.cards[it.card_index].wrong_count,
                self.cards[it.card_index].stage,
            )
        )

        merged: list[PracticeItem] = []
        i, j = 0, 0
        while i < len(practice_new) or j < len(practice_old):
            if i < len(practice_new):
                merged.append(practice_new[i])
                i += 1
            if j < len(practice_old):
                merged.append(practice_old[j])
                j += 1

        chunk_size = 4
        chunks = [merged[k: k + chunk_size] for k in range(0, len(merged), chunk_size)]
        random.shuffle(chunks)
        merged = [item for ch in chunks for item in ch]

        self.practice_queue = merged
        self.practice_pos = 0

    def _insert_spaced_review(self, card_idx: int):
        repeat = PracticeItem(card_index=card_idx, mode="type", is_new=False)
        q = list(self.practice_queue)
        insert_at = min(self.practice_pos + self.SESSION_SRS_GAP, len(q))
        q.insert(insert_at, repeat)
        self.practice_queue = q

    def _continue_after_answer(self):
        if not self.show_feedback:
            return
        if self.practice_pos >= len(self.practice_queue):
            return
        item = self.practice_queue[self.practice_pos]
        was_wrong = not self.feedback_correct
        self.show_feedback = False
        self.typed_answer = ""
        self.user_answer = ""
        self.selected_answer = ""
        self.practice_pos += 1
        if was_wrong:
            self._insert_spaced_review(item.card_index)
        return self._load_practice_item()

    # ═══════════════════════════════════════════════════════════════
    # PHASE: PREVIEW
    # ═══════════════════════════════════════════════════════════════

    def _load_preview_card(self):
        if self.preview_pos >= len(self.preview_cards):
            self.introduced_count += len(self.current_new_indices)
            self.phase = "practice"
            return self._load_practice_item()
        card_idx = self.preview_cards[self.preview_pos]
        self.correct_answer = self._get_answer(self.cards[card_idx])
        self.is_preview_flipped = False
        return self.speak_current_word()

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
        return self._load_preview_card()

    def preview_still_learning(self):
        if self.preview_pos >= len(self.preview_cards):
            return
        card_idx = self.preview_cards[self.preview_pos]
        if card_idx not in self.batch_wrong:
            self.batch_wrong = self.batch_wrong + [card_idx]
        self.preview_pos += 1
        return self._load_preview_card()

    def handle_preview_key(self, key: str):
        if key != "Enter":
            return
        if not self.is_preview_flipped:
            self.flip_preview()
        else:
            return self.preview_got_it()

    # ═══════════════════════════════════════════════════════════════
    # PHASE: PRACTICE
    # ═══════════════════════════════════════════════════════════════

    def _load_practice_item(self):
        self.typed_answer = ""
        self.user_answer = ""
        self.selected_answer = ""
        self.show_feedback = False
        self.feedback_message = ""

        if self.practice_pos >= len(self.practice_queue):
            return self._end_batch()

        item = self.practice_queue[self.practice_pos]
        self.correct_answer = self._get_answer(self.cards[item.card_index])
        if item.mode == "choice":
            self._build_choices(item.card_index)

        if self.answer_language == "native_to_foreign":
            return self.speak_current_word()

    def _build_choices(self, card_idx: int):
        correct = self._get_answer(self.cards[card_idx])
        others = [self._get_answer(c) for i, c in enumerate(self.cards) if i != card_idx]
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

    def handle_type_key(self, key: str):
        if key != "Enter":
            return
        if self.show_feedback:
            return self._continue_after_answer()
        else:
            return self._do_submit_typed()

    def _do_submit_typed(self):
        if not self.typed_answer.strip() or self.show_feedback:
            return
        if self.practice_pos >= len(self.practice_queue):
            return
        item = self.practice_queue[self.practice_pos]
        card = self.cards[item.card_index]
        correct = self._get_answer(card)
        is_correct = self.typed_answer.strip().lower() == correct.strip().lower()
        self.user_answer = self.typed_answer.strip()
        self.show_feedback = True
        self.feedback_correct = is_correct
        self.feedback_message = (
            f"✅ Chính xác! Đáp án: {correct}" if is_correct
            else f"❌ Đáp án đúng: {correct}"
        )
        self._record_answer(item.card_index, is_correct)
        if self.answer_language == "foreign_to_native":
            return self.speak_current_word()

    def submit_typed(self):
        return self._do_submit_typed()

    def continue_after_type(self):
        return self._continue_after_answer()

    # ── Choice ────────────────────────────────────────────────────

    def select_choice(self, option: str):
        if self.selected_answer != "" or self.show_feedback:
            return
        if self.practice_pos >= len(self.practice_queue):
            return
        item = self.practice_queue[self.practice_pos]
        card = self.cards[item.card_index]
        correct = self._get_answer(card)
        is_correct = option == correct
        self.selected_answer = option
        self.show_feedback = True
        self.feedback_correct = is_correct
        self.feedback_message = (
            "✅ Chính xác!" if is_correct
            else f"❌ Đáp án đúng: {correct}"
        )
        self._record_answer(item.card_index, is_correct)
        if self.answer_language == "foreign_to_native":
            return self.speak_current_word()

    def continue_after_choice(self):
        return self._continue_after_answer()

    def handle_choice_key(self, key: str):
        if key != "Enter":
            return
        if self.show_feedback:
            return self._continue_after_answer()

    def handle_batch_review_key(self, key: str):
        if key != "Enter":
            return
        if self.show_feedback:
            return self._continue_after_answer()
        else:
            return self._do_submit_typed()

    # ═══════════════════════════════════════════════════════════════
    # BATCH REVIEW
    # ═══════════════════════════════════════════════════════════════

    def _end_batch(self):
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
            return self._load_practice_item()
        else:
            return self._load_next_batch()

    def finish_batch_review(self):
        return self._load_next_batch()

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
        self.user_answer = ""
        self.selected_answer = ""
        self.show_feedback = False
        self.introduced_count = 0
        self.batch_number = 0
        self.answer_language = "native_to_foreign"

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
    def session_srs_hint(self) -> str:
        if self.phase not in ("practice", "batch_review"):
            return ""
        return (
            f"Lặp ngắt quãng: sai một thẻ → gặp lại sau {self.SESSION_SRS_GAP} thẻ khác · "
            "thẻ mới và ôn xen kẽ theo độ khó."
        )

    @rx.var
    def prompt_label(self) -> str:
        if self.answer_language == "foreign_to_native":
            return "Thuật ngữ"
        return "Nghĩa"

    @rx.var
    def answer_label(self) -> str:
        if self.answer_language == "foreign_to_native":
            return "Nghĩa"
        return "Thuật ngữ"

    @rx.var
    def current_card_prompt(self) -> str:
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
        if idx >= len(self.cards):
            return ""
        card = self.cards[idx]
        return self._get_prompt(card)

    @rx.var
    def current_card_answer_text(self) -> str:
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
        if idx >= len(self.cards):
            return ""
        card = self.cards[idx]
        return self._get_answer(card)

    @rx.var
    def current_card_front(self) -> str:
        return self.current_card_prompt

    @rx.var
    def current_card_back(self) -> str:
        return self.current_card_answer_text

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

    @rx.var
    def current_foreign_word(self) -> str:
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
        if idx >= len(self.cards):
            return ""
        return self.cards[idx].front

    # ── Computed: icon âm lượng ───────────────────────────────────
    @rx.var
    def volume_icon(self) -> str:
        if self.speech_volume == 0.0:
            return "volume-x"
        elif self.speech_volume <= 0.4:
            return "volume-1"
        elif self.speech_volume <= 0.7:
            return "volume-2"
        else:
            return "volume-2"

    @rx.var
    def volume_pct_label(self) -> str:
        return f"{int(self.speech_volume * 100)}%"

    @rx.var
    def rate_label(self) -> str:
        mapping = {0.5: "x0.5", 0.7: "x0.7", 1.0: "Thường", 1.3: "x1.3", 1.6: "x1.6"}
        return mapping.get(self.speech_rate, f"x{self.speech_rate}")

    def speak_word(self, word_text: str):
        if not word_text:
            return

        is_japanese = any(
            0x3040 <= ord(c) <= 0x309F or
            0x30A0 <= ord(c) <= 0x30FF or
            0x4E00 <= ord(c) <= 0x9FAF
            for c in word_text
        )
        lang = "ja-JP" if is_japanese else "en-US"

        js_code = f"""
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance({repr(word_text)});
                utterance.lang = '{lang}';
                utterance.rate = {self.speech_rate};
                utterance.volume = {self.speech_volume};
                var voices = window.speechSynthesis.getVoices();
                if (voices && voices.length > 0) {{
                    var matchingVoice = voices.find(v => v.lang.startsWith('{lang.split("-")[0]}'));
                    if (matchingVoice) utterance.voice = matchingVoice;
                }}
                window.speechSynthesis.speak(utterance);
            }}
        }})()
        """
        return rx.call_script(js_code)

    def speak_current_word(self):
        return self.speak_word(self.current_foreign_word)