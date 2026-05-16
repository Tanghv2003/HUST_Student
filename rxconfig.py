import reflex as rx
 
config = rx.Config(
    app_name="HUST_Student",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    gemini_api_key="AIza...",  # Thay bằng key thật từ aistudio.google.com
)
 