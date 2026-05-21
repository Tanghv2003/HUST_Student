import reflex as rx

from HUST_Student.states.class_manager_state import ClassManagerState  # noqa: F401
from HUST_Student.states.conversation_state import ConversationState  # noqa: F401
from HUST_Student.states.folder_manager_state import FolderManagerState  # noqa: F401
from HUST_Student.states.folder_state import FolderState  # noqa: F401
from HUST_Student.states.kanji_state import ClassesTabState, ClassTreeState, KanjiState  # noqa: F401
from HUST_Student.states.learn_state import LearnState  # noqa: F401
from HUST_Student.states.tree_state import TreeState  # noqa: F401

from .pages.home import home


app = rx.App()

app.add_page(
    home,
    route="/",
    title="HUST Student",
)