from pydantic import BaseModel
from HUST_Student.models.card import WordPair


class StudySet(BaseModel):
    title: str
    file: str
    terms: int = 0
    words: list[WordPair] = []