import reflex as rx

config = rx.Config(
    app_name="HUST_Student",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)