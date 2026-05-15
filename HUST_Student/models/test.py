from pydantic import BaseModel


class AnswerRecord(BaseModel):
    question: str
    correct: str
    chosen: str
    is_correct: bool
