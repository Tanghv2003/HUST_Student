import random

import reflex as rx

from HUST_Student.core.folder_tree import find_folder_path
from HUST_Student.models import AnswerRecord, StudySet, WordPair
from HUST_Student.models.mini_game import MatchTile
from HUST_Student.services.folder_service import load_folders
from HUST_Student.services.studyset_service import load_studyset_detail, load_studysets
from HUST_Student.states.learn_state import LearnState


def _word_pair_from_raw(word: dict) -> WordPair:
    return WordPair(
        front=word.get("foreign", word.get("vietnamese", word.get("front", ""))),
        back=word.get("native", word.get("japanese", word.get("back", ""))),
    )


class FolderState(rx.State):

    current_folder: str = ""
    current_sets: list[StudySet] = []
    selected_set: StudySet | None = None

    show_set_options: bool = False
    show_test_options: bool = False
    show_test: bool = False
    show_result: bool = False
    show_flashcards: bool = False

    show_match: bool = False
    show_blast: bool = False
    show_blocks: bool = False
    ui_lang: str = "vi"

    MAX_MATCH_PAIRS: int = 12
    BLAST_CARD_CAP: int = 28
    BLAST_START_LIVES: int = 5

    match_tiles: list[MatchTile] = []
    match_selected_index: int = -1
    match_total_pairs: int = 0
    match_pairs_done: int = 0

    blast_order: list[int] = []
    blast_pos: int = 0
    blast_input: str = ""
    blast_feedback: str = ""
    blast_streak: int = 0
    blast_best_streak: int = 0
    blast_correct: int = 0
    blast_wrong: int = 0
    blast_lives: int = 5
    blast_phase: str = "play"

    blocks_deck: list[int] = []
    blocks_input: str = ""
    blocks_feedback: str = ""
    blocks_cleared: int = 0
    blocks_wrong: int = 0
    blocks_phase: str = "play"

    test_question_count: int = 10
    test_mode: str = "trac_nghiem"
    answer_language: str = "Cả hai"

    current_options: list[str] = []
    correct_answer: str = ""
    selected_answer: str = ""
    dung_sai_candidate: str = ""
    written_answer: str = ""
    check_feedback: str = ""
    hint_text: str = ""
    current_test_index: int = 0
    shuffled_indices: list[int] = []

    answer_records: list[AnswerRecord] = []
    score_correct: int = 0
    score_wrong: int = 0
    show_wrong_only: bool = False

    current_word_index: int = 0
    is_flipped: bool = False

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

    def open_folder(self, folder_name: str):
        data = load_folders()
        self.current_folder = folder_name
        self.current_sets = []

        folder_path = find_folder_path(data, folder_name)
        if not folder_path:
            return

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

    def select_set(self, set_title: str):
        for study_set in self.current_sets:
            if study_set.title == set_title:
                self.selected_set = study_set
                try:
                    detail_data = load_studyset_detail(study_set.file)
                    study_set.words = [_word_pair_from_raw(word) for word in detail_data]
                    study_set.terms = len(detail_data)
                except FileNotFoundError:
                    study_set.words = []
                self.show_set_options = True
                break

    def close_set_options(self):
        self.show_set_options = False
        self.selected_set = None

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

    def set_ui_lang(self, value):
        if value is None:
            return
        self.ui_lang = str(value)

    def _mini_prompt_answer(self, w: WordPair) -> tuple[str, str]:
        if self.answer_language == "Foreign":
            return w.back, w.front
        return w.front, w.back

    def start_match(self):
        if not self.selected_set or not self.selected_set.words:
            return
        words = self.selected_set.words
        n_pairs = min(self.MAX_MATCH_PAIRS, len(words))
        pick = random.sample(range(len(words)), n_pairs)
        tiles: list[MatchTile] = []
        tid = 0
        for pid, wi in enumerate(pick):
            w = words[wi]
            tiles.append(MatchTile(tile_id=tid, pair_id=pid, text=w.front, matched=False))
            tid += 1
            tiles.append(MatchTile(tile_id=tid, pair_id=pid, text=w.back, matched=False))
            tid += 1
        random.shuffle(tiles)
        self.match_tiles = tiles
        self.match_selected_index = -1
        self.match_total_pairs = n_pairs
        self.match_pairs_done = 0
        self.show_match = True
        self.show_set_options = False

    def close_match(self):
        self.show_match = False
        self.match_tiles = []
        self.match_selected_index = -1
        self.match_total_pairs = 0
        self.match_pairs_done = 0
        self.selected_set = None

    def match_pick(self, tile_id: int):
        tlist = list(self.match_tiles)
        index = next((i for i, t in enumerate(tlist) if t.tile_id == tile_id), -1)
        if index < 0:
            return
        tile = tlist[index]
        if tile.matched:
            return
        sel = self.match_selected_index
        if sel < 0:
            self.match_selected_index = index
            return
        if sel == index:
            self.match_selected_index = -1
            return
        other = tlist[sel]
        if other.matched:
            self.match_selected_index = index
            return
        if tile.pair_id == other.pair_id:
            tlist[sel] = MatchTile(
                tile_id=other.tile_id,
                pair_id=other.pair_id,
                text=other.text,
                matched=True,
            )
            tlist[index] = MatchTile(
                tile_id=tile.tile_id,
                pair_id=tile.pair_id,
                text=tile.text,
                matched=True,
            )
            self.match_tiles = tlist
            self.match_pairs_done = self.match_pairs_done + 1
            self.match_selected_index = -1
        else:
            self.match_selected_index = -1

    def restart_match(self):
        if self.selected_set and self.selected_set.words:
            self.start_match()

    def start_blast(self):
        if not self.selected_set or not self.selected_set.words:
            return
        words = self.selected_set.words
        order = list(range(len(words)))
        random.shuffle(order)
        if len(order) > self.BLAST_CARD_CAP:
            order = order[: self.BLAST_CARD_CAP]
        self.blast_order = order
        self.blast_pos = 0
        self.blast_input = ""
        self.blast_feedback = ""
        self.blast_streak = 0
        self.blast_best_streak = 0
        self.blast_correct = 0
        self.blast_wrong = 0
        self.blast_lives = self.BLAST_START_LIVES
        self.blast_phase = "play"
        self.show_blast = True
        self.show_set_options = False

    def close_blast(self):
        self.show_blast = False
        self.blast_order = []
        self.blast_pos = 0
        self.blast_input = ""
        self.blast_feedback = ""
        self.blast_phase = "play"
        self.selected_set = None

    def restart_blast(self):
        if self.selected_set and self.selected_set.words:
            self.start_blast()

    def set_blast_input(self, text: str):
        self.blast_input = str(text) if text is not None else ""

    def submit_blast(self):
        if self.blast_phase != "play" or not self.selected_set or not self.blast_order:
            return
        if self.blast_pos >= len(self.blast_order):
            self.blast_phase = "complete"
            return
        w = self.selected_set.words[self.blast_order[self.blast_pos]]
        _, expected = self._mini_prompt_answer(w)
        user = (self.blast_input or "").strip().lower()
        exp = (expected or "").strip().lower()
        if not user:
            return
        if user == exp:
            self.blast_correct += 1
            self.blast_streak += 1
            if self.blast_streak > self.blast_best_streak:
                self.blast_best_streak = self.blast_streak
            self.blast_input = ""
            self.blast_feedback = ""
            self.blast_pos += 1
            if self.blast_pos >= len(self.blast_order):
                self.blast_phase = "complete"
        else:
            self.blast_wrong += 1
            self.blast_streak = 0
            self.blast_lives -= 1
            self.blast_input = ""
            if self.blast_lives <= 0:
                self.blast_phase = "complete"

    def start_blocks(self):
        if not self.selected_set or not self.selected_set.words:
            return
        words = self.selected_set.words
        deck = list(range(len(words)))
        random.shuffle(deck)
        cap = self.MAX_MATCH_PAIRS * 2
        if len(deck) > cap:
            deck = deck[:cap]
        self.blocks_deck = deck
        self.blocks_input = ""
        self.blocks_feedback = ""
        self.blocks_cleared = 0
        self.blocks_wrong = 0
        self.blocks_phase = "play"
        self.show_blocks = True
        self.show_set_options = False

    def close_blocks(self):
        self.show_blocks = False
        self.blocks_deck = []
        self.blocks_input = ""
        self.blocks_feedback = ""
        self.blocks_phase = "play"
        self.selected_set = None

    def restart_blocks(self):
        if self.selected_set and self.selected_set.words:
            self.start_blocks()

    def set_blocks_input(self, text: str):
        self.blocks_input = str(text) if text is not None else ""

    def submit_blocks(self):
        if self.blocks_phase != "play" or not self.selected_set or not self.blocks_deck:
            if not self.blocks_deck:
                self.blocks_phase = "complete"
            return
        top = self.blocks_deck[0]
        w = self.selected_set.words[top]
        _, expected = self._mini_prompt_answer(w)
        user = (self.blocks_input or "").strip().lower()
        exp = (expected or "").strip().lower()
        if not user:
            return
        deck = list(self.blocks_deck)
        if user == exp:
            deck.pop(0)
            self.blocks_deck = deck
            self.blocks_cleared += 1
            self.blocks_input = ""
            self.blocks_feedback = ""
            if not deck:
                self.blocks_phase = "complete"
        else:
            first = deck.pop(0)
            deck.append(first)
            self.blocks_deck = deck
            self.blocks_wrong += 1
            self.blocks_input = ""
            self.blocks_feedback = "wrong"

    @rx.var
    def blast_prompt_text(self) -> str:
        if (
            not self.selected_set
            or not self.blast_order
            or self.blast_pos >= len(self.blast_order)
            or self.blast_phase != "play"
        ):
            return ""
        w = self.selected_set.words[self.blast_order[self.blast_pos]]
        prompt, _ = self._mini_prompt_answer(w)
        return prompt

    @rx.var
    def blast_progress(self) -> str:
        if not self.blast_order:
            return "0/0"
        n = len(self.blast_order)
        cur = min(self.blast_pos + 1, n) if self.blast_phase == "play" else n
        return f"{cur}/{n}"

    @rx.var
    def blocks_top_prompt(self) -> str:
        if not self.selected_set or not self.blocks_deck or self.blocks_phase != "play":
            return ""
        w = self.selected_set.words[self.blocks_deck[0]]
        prompt, _ = self._mini_prompt_answer(w)
        return prompt

    @rx.var
    def blocks_remaining(self) -> int:
        return len(self.blocks_deck)

    @rx.var
    def match_all_matched(self) -> bool:
        return self.match_total_pairs > 0 and self.match_pairs_done >= self.match_total_pairs

    @rx.var
    def match_selected_tile_id(self) -> int:
        if self.match_selected_index < 0 or self.match_selected_index >= len(self.match_tiles):
            return -1
        return self.match_tiles[self.match_selected_index].tile_id

    @rx.var
    def blast_won(self) -> bool:
        if self.blast_phase != "complete" or not self.blast_order:
            return False
        return self.blast_pos >= len(self.blast_order)

    @rx.var
    def blast_lost(self) -> bool:
        if self.blast_phase != "complete" or not self.blast_order:
            return False
        return self.blast_pos < len(self.blast_order) and self.blast_lives <= 0

    @rx.event
    async def start_learn_mode(self):
        if not self.selected_set or not self.selected_set.words:
            return
        self.show_set_options = False
        words = [{"front": w.front, "back": w.back} for w in self.selected_set.words]
        title = self.selected_set.title
        learn = await self.get_state(LearnState)
        learn.init_learn(words, title)

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
        is_correct = user_ans == correct_ans
        result = "✅ Đúng" if is_correct else "❌ Sai"
        self.check_feedback = (
            f"📖 Đáp án đúng: {self.correct_answer} | Bạn trả lời: {self.written_answer} | {result}"
        )

    def next_test_question(self):
        if not self.selected_set or not self.selected_set.words:
            return

        if self.test_mode == "tu_luan":
            if not self.written_answer:
                self.check_feedback = "❗ Vui lòng nhập câu trả lời trước khi tiếp tục."
                return
        elif self.selected_answer == "":
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
