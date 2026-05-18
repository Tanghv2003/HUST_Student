import reflex as rx

from HUST_Student.states.conversation_state import ConversationState  # noqa: F401
from HUST_Student.states.folder_state import FolderState  # noqa: F401
from HUST_Student.states.kanji_state import ClassesTabState, KanjiState  # noqa: F401
from HUST_Student.states.learn_state import LearnState  # noqa: F401

from .pages.home import home


app = rx.App()

app.add_page(
    home,
    route="/",
    title="HUST Student",
)