import reflex as rx

from .pages.home import home


app = rx.App()


app.add_page(
    home,
    route="/",
    title="QUIZLET - AI",
)