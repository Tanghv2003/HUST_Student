from pydantic import BaseModel


class MatchTile(BaseModel):
    tile_id: int
    pair_id: int
    text: str
    matched: bool = False


class BlockCard(BaseModel):
    card_id: int
    front: str
    back: str
    is_flipped: bool = False
