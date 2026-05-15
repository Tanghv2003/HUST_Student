import reflex as rx

# Đăng ký state với Reflex (tránh context null trên một số nhánh UI)
from HUST_Student.states.conversation_state import ConversationState  # noqa: F401
from HUST_Student.states.folder_state import FolderState  # noqa: F401
from HUST_Student.states.learn_state import LearnState  # noqa: F401

from .pages.home import home


app = rx.App()


app.add_page(
    home,
    route="/",
    title="QUIZLET - AI",
)