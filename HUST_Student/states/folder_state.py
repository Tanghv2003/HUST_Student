import random
import reflex as rx
from pydantic import BaseModel

from HUST_Student.services.folder_service import load_folders
from HUST_Student.services.studyset_service import (
    load_studysets,
    load_studyset_detail,
)


class WordPair(BaseModel):
    front: str
    back: str


class AnswerRecord(BaseModel):
    question: str       # nội dung câu hỏi
    correct: str        # đáp án đúng
    chosen: str         # đáp án user chọn
    is_correct: bool    # đúng hay sai


class StudySet(BaseModel):
    title: str
    terms: int = 0
    file: str
    words: list[WordPair] = []


class FolderState(rx.State):

    current_folder: str = ""
    current_sets: list[StudySet] = []
    selected_set: StudySet | None = None

    show_set_options: bool = False
    show_test_options: bool = False
    show_test: bool = False
    show_result: bool = False
    show_flashcards: bool = False

    test_question_count: int = 10
    test_mode: str = "trac_nghiem"
    answer_language: str = "Cả hai"

    # Trắc nghiệm: 4 đáp án được tính sẵn phía server
    current_options: list[str] = []
    correct_answer: str = ""
    selected_answer: str = ""

    current_test_index: int = 0
    current_word_index: int = 0
    is_flipped: bool = False

    # Kết quả bài kiểm tra
    answer_records: list[AnswerRecord] = []
    score_correct: int = 0
    score_wrong: int = 0
    show_wrong_only: bool = False

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _build_options(self):
        """Build 4 shuffled answer options for current test question."""
        if not self.selected_set or not self.selected_set.words:
            self.current_options = []
            self.correct_answer = ""
            return

        words = self.selected_set.words
        idx = self.current_test_index % len(words)
        current = words[idx]

        # front = nghĩa (foreign/english) — dùng làm câu hỏi mặc định
        # back  = chữ Nhật (native)       — dùng làm đáp án mặc định
        # "Cả hai"/"Native": hỏi front → đáp án back
        # "Foreign":  hỏi back  → đáp án front
        if self.answer_language == "Foreign":
            correct = current.front
            get_ans = lambda w: w.front
        else:
            correct = current.back
            get_ans = lambda w: w.back

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

    def _get_question_text(self) -> str:
        """Get the question text for the current index."""
        if not self.selected_set or not self.selected_set.words:
            return ""
        words = self.selected_set.words
        idx = self.current_test_index % len(words)
        current = words[idx]
        if self.answer_language == "Foreign":
            return current.back
        return current.front

    # ── Folder loading ────────────────────────────────────────────────────────

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

    # ── Study set selection ───────────────────────────────────────────────────

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

    # ── Test options ──────────────────────────────────────────────────────────

    def open_test_options(self):
        if self.selected_set:
            self.show_set_options = False
            self.show_test_options = True
            self.test_question_count = len(self.selected_set.words)
            self.test_mode = "trac_nghiem"

    def close_test_options(self):
        self.show_test_options = False

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

    def set_test_mode(self, mode: str):
        self.test_mode = mode

    def set_answer_language(self, value):
        if value is None:
            return
        self.answer_language = str(value)

    # ── Test run ──────────────────────────────────────────────────────────────

    def start_test(self):
        if self.selected_set and self.selected_set.words:
            self.show_test_options = False
            self.show_test = True
            self.show_result = False
            self.current_test_index = 0
            self.selected_answer = ""
            self.test_question_count = len(self.selected_set.words)
            self.answer_records = []
            self.score_correct = 0
            self.score_wrong = 0
            self.show_wrong_only = False
            self._build_options()

    def close_test(self):
        self.show_test = False
        self.show_result = False
        self.current_test_index = 0
        self.selected_answer = ""
        self.current_options = []
        self.correct_answer = ""
        self.answer_records = []

    def next_test_question(self):
        if not self.selected_set or not self.selected_set.words:
            return
        if self.selected_answer == "":
            return

        # Lưu kết quả câu hiện tại
        question_text = self._get_question_text()
        is_correct = self.selected_answer == self.correct_answer
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

        # Kiểm tra đã hết câu chưa
        next_index = self.current_test_index + 1
        if next_index >= self.test_question_count:
            # Hiện màn hình kết quả
            self.show_test = False
            self.show_result = True
            return

        self.current_test_index = next_index
        self.selected_answer = ""
        self._build_options()

    def set_selected_answer(self, answer: str):
        if self.selected_answer != "":
            return
        self.selected_answer = str(answer) if answer is not None else ""

    def retry_wrong_only(self):
        """Làm lại chỉ các câu sai."""
        if not self.selected_set:
            return
        wrong_records = [r for r in self.answer_records if not r.is_correct]
        if not wrong_records:
            return
        # Tạo lại word list chỉ từ các câu sai
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
        self.test_question_count = len(self.selected_set.words)
        self.answer_records = []
        self.score_correct = 0
        self.score_wrong = 0
        self._build_options()

    def retry_all(self):
        """Làm lại toàn bộ bài."""
        self.show_result = False
        self.show_test = True
        self.current_test_index = 0
        self.selected_answer = ""
        self.answer_records = []
        self.score_correct = 0
        self.score_wrong = 0
        self._build_options()

    def set_show_wrong_only(self, value: bool):
        self.show_wrong_only = value

    # ── Flashcards ────────────────────────────────────────────────────────────

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
            self.current_word_index = (
                self.current_word_index + 1
            ) % len(self.selected_set.words)
            self.is_flipped = False

    def prev_word(self):
        if self.selected_set and self.selected_set.words:
            self.current_word_index = (
                self.current_word_index - 1
            ) % len(self.selected_set.words)
            self.is_flipped = False

    def close_flashcards(self):
        self.show_flashcards = False
        self.selected_set = None
        self.current_word_index = 0
        self.is_flipped = False

    # ── Modals ────────────────────────────────────────────────────────────────

    def close_set_options(self):
        self.show_set_options = False
        self.selected_set = None