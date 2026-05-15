import random
import reflex as rx
from pydantic import BaseModel

from HUST_Student.services.folder_service import load_folders
from HUST_Student.services.studyset_service import (
    load_studysets,
    load_studyset_detail,
)


# ══════════════════════════════════════════════════════════════════
# MODELS
# ══════════════════════════════════════════════════════════════════

class WordPair(BaseModel):
    front: str
    back: str


class AnswerRecord(BaseModel):
    question: str
    correct: str
    chosen: str
    is_correct: bool


class LearnCard(BaseModel):
    front: str
    back: str
    stage: int = 0           # 0=chưa học, 1=đã xem, 2=gõ đúng, 3=trắc nghiệm đúng, 4=thành thạo
    correct_streak: int = 0
    wrong_count: int = 0


class StudySet(BaseModel):
    title: str
    terms: int = 0
    file: str
    words: list[WordPair] = []


# ══════════════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════════════

class FolderState(rx.State):

    # ── Folder / set data ─────────────────────────────────────────
    current_folder: str = ""
    current_sets: list[StudySet] = []
    selected_set: StudySet | None = None

    # ── Modal visibility ──────────────────────────────────────────
    show_set_options: bool = False
    show_test_options: bool = False
    show_test: bool = False
    show_result: bool = False
    show_flashcards: bool = False
    show_learn: bool = False

    # ── Test config ───────────────────────────────────────────────
    test_question_count: int = 10
    test_mode: str = "trac_nghiem"
    answer_language: str = "Cả hai"

    # ── Test runtime ──────────────────────────────────────────────
    current_options: list[str] = []
    correct_answer: str = ""
    selected_answer: str = ""
    dung_sai_candidate: str = ""
    written_answer: str = ""
    check_feedback: str = ""
    hint_text: str = ""
    current_test_index: int = 0
    shuffled_indices: list[int] = []

    # ── Test results ──────────────────────────────────────────────
    answer_records: list[AnswerRecord] = []
    score_correct: int = 0
    score_wrong: int = 0
    show_wrong_only: bool = False

    # ── Flashcard runtime ─────────────────────────────────────────
    current_word_index: int = 0
    is_flipped: bool = False

    # ── Learn mode runtime ────────────────────────────────────────
    learn_cards: list[LearnCard] = []
    learn_phase: str = "preview"   # preview | type | choice | review | complete
    learn_queue: list[int] = []
    learn_wrong_queue: list[int] = []
    learn_current_index: int = 0
    learn_round: int = 1
    learn_total_correct: int = 0
    learn_total_wrong: int = 0
    learn_correct_answer: str = ""
    learn_choice_options: list[str] = []
    learn_selected_choice: str = ""
    learn_typed_answer: str = ""
    learn_show_feedback: bool = False
    learn_feedback_correct: bool = False
    learn_feedback_message: str = ""
    learn_is_preview_flipped: bool = False

    # ════════════════════════════════════════════════════════════════
    # COMPUTED VARS
    # ════════════════════════════════════════════════════════════════

    @rx.var
    def current_question_display(self) -> str:
        if not self.selected_set or not self.selected_set.words:
            return "—"
        words = self.selected_set.words
        if self.shuffled_indices and self.current_test_index < len(self.shuffled_indices):
            idx = self.shuffled_indices[self.current_test_index]
        else:
            idx = self.current_test_index % len(words)
        current = words[idx]
        if self.answer_language == "Foreign":
            return current.back
        return current.front

    @rx.var
    def current_question_text(self) -> str:
        if not self.selected_set or not self.selected_set.words:
            return ""
        words = self.selected_set.words
        if self.shuffled_indices and self.current_test_index < len(self.shuffled_indices):
            idx = self.shuffled_indices[self.current_test_index]
        else:
            idx = self.current_test_index % len(words)
        current = words[idx]
        if self.answer_language == "Foreign":
            return current.back
        return current.front

    # ── Learn computed vars ───────────────────────────────────────

    @rx.var
    def learn_card_front(self) -> str:
        if not self.learn_queue or self.learn_current_index >= len(self.learn_queue):
            return ""
        idx = self.learn_queue[self.learn_current_index]
        if idx >= len(self.learn_cards):
            return ""
        return self.learn_cards[idx].front

    @rx.var
    def learn_card_back(self) -> str:
        if not self.learn_queue or self.learn_current_index >= len(self.learn_queue):
            return ""
        idx = self.learn_queue[self.learn_current_index]
        if idx >= len(self.learn_cards):
            return ""
        return self.learn_cards[idx].back

    @rx.var
    def learn_queue_label(self) -> str:
        total = len(self.learn_queue)
        if total == 0:
            return "0 / 0"
        return f"{self.learn_current_index + 1} / {total}"

    @rx.var
    def learn_mastered_count(self) -> int:
        return sum(1 for c in self.learn_cards if c.stage >= 4)

    @rx.var
    def learn_learning_count(self) -> int:
        return sum(1 for c in self.learn_cards if 0 < c.stage < 4)

    @rx.var
    def learn_not_started_count(self) -> int:
        return sum(1 for c in self.learn_cards if c.stage == 0)

    @rx.var
    def learn_accuracy_pct(self) -> int:
        total = self.learn_total_correct + self.learn_total_wrong
        if total == 0:
            return 0
        return (self.learn_total_correct * 100) // total

    @rx.var
    def learn_mastered_pct(self) -> int:
        total = len(self.learn_cards)
        if total == 0:
            return 0
        return (self.learn_mastered_count * 100) // total

    # ════════════════════════════════════════════════════════════════
    # FOLDER LOADING
    # ════════════════════════════════════════════════════════════════

    def open_folder(self, folder_name: str):
        data = load_folders()
        self.current_folder = folder_name
        self.current_sets = []

        def find_folder_path(tree, target_name, current_path=""):
            for key, value in tree.items():
                path = f"{current_path}/{key}" if current_path else key
                if key == target_name:
                    return path
                if isinstance(value, dict) and "folders" in value:
                    result = find_folder_path(value["folders"], target_name, path)
                    if result:
                        return result
            return None

        folder_path = find_folder_path(data, folder_name)
        if folder_path:
            studysets = load_studysets()
            sets_data = studysets.get(folder_path, [])
            current_sets = []
            for item in sets_data:
                study_set = StudySet(
                    title=item["title"],
                    terms=item.get("terms", 0),
                    file=item["file"],
                )
                try:
                    detail_data = load_studyset_detail(study_set.file)
                    study_set.terms = len(detail_data)
                except FileNotFoundError:
                    pass
                current_sets.append(study_set)
            self.current_sets = current_sets

    # ════════════════════════════════════════════════════════════════
    # STUDY SET SELECTION
    # ════════════════════════════════════════════════════════════════

    def select_set(self, set_title: str):
        for study_set in self.current_sets:
            if study_set.title == set_title:
                self.selected_set = study_set
                try:
                    detail_data = load_studyset_detail(study_set.file)
                    study_set.words = [
                        WordPair(
                            front=word.get("foreign", word.get("vietnamese", word.get("front", ""))),
                            back=word.get("native", word.get("japanese", word.get("back", ""))),
                        )
                        for word in detail_data
                    ]
                    study_set.terms = len(detail_data)
                except FileNotFoundError:
                    study_set.words = []
                self.show_set_options = True
                break

    def close_set_options(self):
        self.show_set_options = False
        self.selected_set = None

    # ════════════════════════════════════════════════════════════════
    # FLASHCARDS
    # ════════════════════════════════════════════════════════════════

    def start_flashcards(self):
        if self.selected_set and self.selected_set.words:
            self.show_flashcards = True
            self.show_set_options = False
            self.current_word_index = 0
            self.is_flipped = False

    def flip_card(self):
        self.is_flipped = not self.is_flipped

    def next_word(self):
        if self.selected_set and self.selected_set.words:
            self.current_word_index = (self.current_word_index + 1) % len(self.selected_set.words)
            self.is_flipped = False

    def prev_word(self):
        if self.selected_set and self.selected_set.words:
            self.current_word_index = (self.current_word_index - 1) % len(self.selected_set.words)
            self.is_flipped = False

    def close_flashcards(self):
        self.show_flashcards = False
        self.selected_set = None
        self.current_word_index = 0
        self.is_flipped = False

    # ════════════════════════════════════════════════════════════════
    # LEARN MODE
    # ════════════════════════════════════════════════════════════════

    def start_learn_mode(self):
        if not self.selected_set or not self.selected_set.words:
            return
        self.show_set_options = False
        self.show_learn = True
        self.learn_round = 1
        self.learn_total_correct = 0
        self.learn_total_wrong = 0
        self.learn_cards = [
            LearnCard(front=w.front, back=w.back)
            for w in self.selected_set.words
        ]
        self._learn_reset_round()

    def _learn_reset_round(self):
        not_mastered = [i for i, c in enumerate(self.learn_cards) if c.stage < 4]
        if not not_mastered:
            self.learn_phase = "complete"
            return
        sorted_q = sorted(not_mastered, key=lambda i: (-self.learn_cards[i].wrong_count, self.learn_cards[i].stage))
        self.learn_queue = sorted_q
        self.learn_wrong_queue = []
        self.learn_current_index = 0
        self._learn_load_card()

    def _learn_load_card(self):
        self.learn_typed_answer = ""
        self.learn_selected_choice = ""
        self.learn_show_feedback = False
        self.learn_feedback_message = ""
        self.learn_is_preview_flipped = False

        if self.learn_current_index >= len(self.learn_queue):
            self._learn_finish_round()
            return

        card_idx = self.learn_queue[self.learn_current_index]
        card = self.learn_cards[card_idx]
        self.learn_correct_answer = card.back

        if card.stage == 0:
            self.learn_phase = "preview"
        elif card.stage == 1:
            self.learn_phase = "type"
        else:
            if card.wrong_count > 0:
                self.learn_phase = "type"
            else:
                self.learn_phase = "choice"
                self._learn_build_choices(card_idx)

    def _learn_build_choices(self, card_idx: int):
        correct = self.learn_cards[card_idx].back
        others = [c.back for i, c in enumerate(self.learn_cards) if i != card_idx]
        sample = random.sample(others, min(3, len(others)))
        while len(sample) < 3:
            sample.append("—")
        opts = [correct] + sample
        random.shuffle(opts)
        self.learn_choice_options = opts

    def _learn_advance(self):
        self.learn_current_index += 1
        if self.learn_current_index >= len(self.learn_queue):
            self._learn_finish_round()
        else:
            self._learn_load_card()

    def _learn_finish_round(self):
        if self.learn_wrong_queue:
            deduped = list(set(self.learn_wrong_queue))
            random.shuffle(deduped)
            self.learn_queue = deduped
            self.learn_wrong_queue = []
            self.learn_current_index = 0
            self.learn_round += 1
            self.learn_phase = "review"
        else:
            not_mastered = [i for i, c in enumerate(self.learn_cards) if c.stage < 4]
            if not_mastered:
                random.shuffle(not_mastered)
                self.learn_queue = not_mastered
                self.learn_wrong_queue = []
                self.learn_current_index = 0
                self.learn_round += 1
                self.learn_phase = "review"
            else:
                self.learn_phase = "complete"

    # ── Preview actions ───────────────────────────────────────────

    def learn_flip_preview(self):
        self.learn_is_preview_flipped = not self.learn_is_preview_flipped

    def learn_preview_got_it(self):
        if self.learn_current_index >= len(self.learn_queue):
            return
        card_idx = self.learn_queue[self.learn_current_index]
        card = self.learn_cards[card_idx]
        card.stage = max(card.stage, 1)
        card.correct_streak += 1
        self.learn_cards[card_idx] = card
        self.learn_total_correct += 1
        self._learn_advance()

    def learn_preview_still_learning(self):
        if self.learn_current_index >= len(self.learn_queue):
            return
        card_idx = self.learn_queue[self.learn_current_index]
        card = self.learn_cards[card_idx]
        card.stage = max(card.stage, 1)
        self.learn_cards[card_idx] = card
        self.learn_wrong_queue = self.learn_wrong_queue + [card_idx]
        self._learn_advance()

    # ── Type actions ──────────────────────────────────────────────

    def learn_set_typed(self, text: str):
        self.learn_typed_answer = str(text) if text else ""
        if self.learn_feedback_message:
            self.learn_feedback_message = ""

    def learn_submit_typed(self):
        if not self.learn_typed_answer.strip():
            return
        if self.learn_current_index >= len(self.learn_queue):
            return
        card_idx = self.learn_queue[self.learn_current_index]
        card = self.learn_cards[card_idx]

        is_correct = self.learn_typed_answer.strip().lower() == card.back.strip().lower()
        self.learn_show_feedback = True
        self.learn_feedback_correct = is_correct

        if is_correct:
            self.learn_feedback_message = f"✅ Chính xác! Đáp án: {card.back}"
            card.correct_streak += 1
            card.stage = min(card.stage + 1, 4)
            self.learn_total_correct += 1
        else:
            self.learn_feedback_message = f"❌ Đáp án đúng: {card.back}"
            card.wrong_count += 1
            card.correct_streak = 0
            card.stage = max(card.stage - 1, 1)
            self.learn_wrong_queue = self.learn_wrong_queue + [card_idx]
            self.learn_total_wrong += 1

        self.learn_cards[card_idx] = card

    def learn_continue_after_type(self):
        self.learn_show_feedback = False
        self._learn_advance()

    # ── Choice actions ────────────────────────────────────────────

    def learn_select_choice(self, option: str):
        if self.learn_selected_choice != "":
            return
        if self.learn_current_index >= len(self.learn_queue):
            return
        self.learn_selected_choice = option
        card_idx = self.learn_queue[self.learn_current_index]
        card = self.learn_cards[card_idx]

        is_correct = (option == card.back)
        self.learn_show_feedback = True
        self.learn_feedback_correct = is_correct

        if is_correct:
            self.learn_feedback_message = "✅ Chính xác!"
            card.correct_streak += 1
            card.stage = min(card.stage + 1, 4)
            self.learn_total_correct += 1
        else:
            self.learn_feedback_message = f"❌ Đáp án đúng: {card.back}"
            card.wrong_count += 1
            card.correct_streak = 0
            card.stage = max(card.stage - 1, 1)
            self.learn_wrong_queue = self.learn_wrong_queue + [card_idx]
            self.learn_total_wrong += 1

        self.learn_cards[card_idx] = card

    def learn_continue_after_choice(self):
        self.learn_show_feedback = False
        self.learn_selected_choice = ""
        self._learn_advance()

    # ── Round review + complete ───────────────────────────────────

    def learn_continue_review_round(self):
        self._learn_load_card()

    def close_learn(self):
        self.show_learn = False
        self.learn_cards = []
        self.learn_queue = []
        self.learn_wrong_queue = []
        self.learn_phase = "preview"
        self.learn_typed_answer = ""
        self.learn_selected_choice = ""
        self.learn_show_feedback = False
        self.learn_feedback_message = ""
        self.learn_choice_options = []
        self.learn_correct_answer = ""

    # ════════════════════════════════════════════════════════════════
    # TEST OPTIONS
    # ════════════════════════════════════════════════════════════════

    def open_test_options(self):
        if self.selected_set:
            self.show_set_options = False
            self.show_test_options = True
            self.test_question_count = len(self.selected_set.words)
            self.test_mode = "trac_nghiem"

    def close_test_options(self):
        self.show_test_options = False

    def set_test_mode(self, mode: str):
        self.test_mode = mode

    def set_answer_language(self, value):
        if value is None:
            return
        self.answer_language = str(value)

    def set_test_question_count(self, value):
        if value is None:
            return
        value = str(value).strip()
        if value == "":
            self.test_question_count = 1
            return
        try:
            count = int(value)
        except (TypeError, ValueError):
            return
        max_count = len(self.selected_set.words) if self.selected_set else 0
        if max_count <= 0:
            return
        self.test_question_count = min(max(1, count), max_count)

    # ════════════════════════════════════════════════════════════════
    # TEST RUN
    # ════════════════════════════════════════════════════════════════

    def _build_options(self):
        self.hint_text = ""
        if not self.selected_set or not self.selected_set.words:
            self.current_options = []
            self.correct_answer = ""
            self.dung_sai_candidate = ""
            self.check_feedback = ""
            return

        words = self.selected_set.words
        if self.shuffled_indices and self.current_test_index < len(self.shuffled_indices):
            idx = self.shuffled_indices[self.current_test_index]
        else:
            idx = self.current_test_index % len(words)
        current = words[idx]

        if self.answer_language == "Foreign":
            correct = current.front
            get_ans = lambda w: w.front
        else:
            correct = current.back
            get_ans = lambda w: w.back

        if self.test_mode == "dung_sai":
            other_words = [w for i, w in enumerate(words) if i != idx]
            candidate = correct
            if other_words and random.random() < 0.5:
                candidate = get_ans(random.choice(other_words))
            self.dung_sai_candidate = candidate
            self.correct_answer = "Đúng" if candidate == correct else "Sai"
            self.current_options = []
            self.check_feedback = ""
            return

        if self.test_mode == "tu_luan":
            self.correct_answer = correct
            self.current_options = []
            self.dung_sai_candidate = ""
            self.check_feedback = ""
            return

        self.correct_answer = correct
        other_words = [w for i, w in enumerate(words) if i != idx]
        sample_count = min(3, len(other_words))
        distractors_words = random.sample(other_words, sample_count)
        distractors = [get_ans(w) for w in distractors_words]
        while len(distractors) < 3:
            distractors.append("—")
        options = [correct] + distractors
        random.shuffle(options)
        self.current_options = options
        self.check_feedback = ""

    def start_test(self):
        if self.selected_set and self.selected_set.words:
            self.show_test_options = False
            self.show_test = True
            self.show_result = False
            self.current_test_index = 0
            self.selected_answer = ""
            self.written_answer = ""
            self.check_feedback = ""
            self.hint_text = ""
            self.test_question_count = len(self.selected_set.words)
            self.answer_records = []
            self.score_correct = 0
            self.score_wrong = 0
            self.show_wrong_only = False
            indices = list(range(self.test_question_count))
            random.shuffle(indices)
            self.shuffled_indices = indices
            self._build_options()

    def close_test(self):
        self.show_test = False
        self.show_result = False
        self.current_test_index = 0
        self.selected_answer = ""
        self.written_answer = ""
        self.check_feedback = ""
        self.hint_text = ""
        self.current_options = []
        self.correct_answer = ""
        self.dung_sai_candidate = ""
        self.answer_records = []
        self.shuffled_indices = []

    def show_hint(self):
        if self.correct_answer:
            self.hint_text = f"📖 Đáp án đúng: {self.correct_answer}"
        else:
            self.hint_text = ""

    def check_current_answer(self):
        if self.test_mode != "tu_luan":
            return
        if not self.written_answer:
            self.check_feedback = "❗ Vui lòng nhập câu trả lời."
            return
        user_ans = self.written_answer.strip().lower()
        correct_ans = self.correct_answer.strip().lower()
        is_correct = (user_ans == correct_ans)
        result = "✅ Đúng" if is_correct else "❌ Sai"
        self.check_feedback = f"📖 Đáp án đúng: {self.correct_answer} | Bạn trả lời: {self.written_answer} | {result}"

    def next_test_question(self):
        if not self.selected_set or not self.selected_set.words:
            return

        if self.test_mode == "tu_luan":
            if not self.written_answer:
                self.check_feedback = "❗ Vui lòng nhập câu trả lời trước khi tiếp tục."
                return
        else:
            if self.selected_answer == "":
                return

        question_text = self.current_question_text

        if self.test_mode == "tu_luan":
            is_correct = self.written_answer.strip().lower() == self.correct_answer.strip().lower()
            record = AnswerRecord(
                question=question_text,
                correct=self.correct_answer,
                chosen=self.written_answer,
                is_correct=is_correct,
            )
        else:
            is_correct = (self.selected_answer == self.correct_answer)
            record = AnswerRecord(
                question=question_text,
                correct=self.correct_answer,
                chosen=self.selected_answer,
                is_correct=is_correct,
            )

        self.answer_records = self.answer_records + [record]
        if is_correct:
            self.score_correct += 1
        else:
            self.score_wrong += 1

        next_index = self.current_test_index + 1
        if next_index >= self.test_question_count:
            self.show_test = False
            self.show_result = True
            self.check_feedback = ""
            self.hint_text = ""
            return

        self.current_test_index = next_index
        self.selected_answer = ""
        self.written_answer = ""
        self.check_feedback = ""
        self.hint_text = ""
        self._build_options()

    def set_selected_answer(self, answer: str):
        if self.selected_answer != "":
            return
        self.selected_answer = str(answer) if answer is not None else ""
        if self.hint_text:
            self.hint_text = ""

    def set_written_answer(self, text: str):
        self.written_answer = str(text) if text is not None else ""
        if self.check_feedback:
            self.check_feedback = ""

    def retry_wrong_only(self):
        if not self.selected_set:
            return
        wrong_records = [r for r in self.answer_records if not r.is_correct]
        if not wrong_records:
            return
        wrong_fronts = {r.question for r in wrong_records}
        if self.answer_language == "Foreign":
            wrong_words = [w for w in self.selected_set.words if w.back in wrong_fronts]
        else:
            wrong_words = [w for w in self.selected_set.words if w.front in wrong_fronts]

        self.selected_set.words = wrong_words if wrong_words else self.selected_set.words
        self.show_result = False
        self.show_test = True
        self.current_test_index = 0
        self.selected_answer = ""
        self.written_answer = ""
        self.check_feedback = ""
        self.hint_text = ""
        self.test_question_count = len(self.selected_set.words)
        self.answer_records = []
        self.score_correct = 0
        self.score_wrong = 0
        indices = list(range(self.test_question_count))
        random.shuffle(indices)
        self.shuffled_indices = indices
        self._build_options()

    def retry_all(self):
        self.show_result = False
        self.show_test = True
        self.current_test_index = 0
        self.selected_answer = ""
        self.written_answer = ""
        self.check_feedback = ""
        self.hint_text = ""
        self.answer_records = []
        self.score_correct = 0
        self.score_wrong = 0
        indices = list(range(self.test_question_count))
        random.shuffle(indices)
        self.shuffled_indices = indices
        self._build_options()

    def set_show_wrong_only(self, value: bool):
        self.show_wrong_only = value