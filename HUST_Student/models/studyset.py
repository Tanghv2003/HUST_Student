from pydantic import BaseModel

from HUST_Student.models.card import WordPair


class StudySet(BaseModel):
    title: str
    terms: int = 0
    file: str
    words: list[WordPair] = []
