from pydantic import BaseModel


class ChatLine(BaseModel):
    role: str
    text: str
    dialogue: str = ""
    feedback: str = ""
    context: str = ""
