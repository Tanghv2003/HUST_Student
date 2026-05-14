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


class StudySet(BaseModel):
    title: str
    terms: int
    file: str
    words: list[WordPair] = []


class FolderState(rx.State):

    current_folder: str = ""

    current_sets: list[StudySet] = []

    selected_set: StudySet | None = None

    show_set_options: bool = False

    show_flashcards: bool = False

    current_word_index: int = 0

    is_flipped: bool = False

    def open_folder(
        self,
        folder_name: str,
    ):

        data = load_folders()

        self.current_folder = folder_name

        self.current_sets = []

        def find_folder_path(tree, target_name, current_path=""):

            for key, value in tree.items():

                path = f"{current_path}/{key}" if current_path else key

                if key == target_name:
                    return path

                if isinstance(value, dict) and "folders" in value:
                    result = find_folder_path(
                        value["folders"],
                        target_name,
                        path,
                    )
                    if result:
                        return result

            return None

        folder_path = find_folder_path(data, folder_name)

        if folder_path:

            studysets = load_studysets()
            sets_data = studysets.get(
                folder_path,
                [],
            )
            self.current_sets = [
                StudySet(
                    title=item["title"],
                    terms=item["terms"],
                    file=item["file"],
                )
                for item in sets_data
            ]

    def select_set(self, set_title: str):
        """Select a study set and show options"""
        for study_set in self.current_sets:
            if study_set.title == set_title:
                self.selected_set = study_set
                try:
                    detail_data = load_studyset_detail(study_set.file)
                    study_set.words = [
                        WordPair(
                            front=word["foreign"],
                            back=word.get("vietnamese", word.get("japanese", "")),
                        )
                        for word in detail_data
                    ]
                except FileNotFoundError:
                    study_set.words = []
                self.show_set_options = True
                break

    def start_flashcards(self):
        """Open flashcards for the selected study set"""
        if self.selected_set and self.selected_set.words:
            self.show_flashcards = True
            self.show_set_options = False
            self.current_word_index = 0
            self.is_flipped = False

    def flip_card(self):
        """Flip the current flashcard"""
        self.is_flipped = not self.is_flipped

    def next_word(self):
        """Go to the next flashcard"""
        if self.selected_set and self.selected_set.words:
            self.current_word_index = (
                self.current_word_index + 1
            ) % len(self.selected_set.words)
            self.is_flipped = False

    def prev_word(self):
        """Go to the previous flashcard"""
        if self.selected_set and self.selected_set.words:
            self.current_word_index = (
                self.current_word_index - 1
            ) % len(self.selected_set.words)
            self.is_flipped = False

    def close_flashcards(self):
        """Close the flashcard view"""
        self.show_flashcards = False
        self.selected_set = None
        self.current_word_index = 0
        self.is_flipped = False

    def close_set_options(self):
        """Close the study set options modal"""
        self.show_set_options = False
        self.selected_set = None