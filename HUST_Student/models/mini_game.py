from pydantic import BaseModel


class MatchTile(BaseModel):
    tile_id: int
    pair_id: int
    text: str
    matched: bool = False
