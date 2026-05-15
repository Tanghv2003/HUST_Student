from pydantic import BaseModel


class WordPair(BaseModel):
    front: str
    back: str


class LearnCard(BaseModel):
    front: str
    back: str
    stage: int = 0
    correct_streak: int = 0
    wrong_count: int = 0
    last_wrong: bool = False


class PracticeItem(BaseModel):
    card_index: int
    mode: str
    is_new: bool = True
