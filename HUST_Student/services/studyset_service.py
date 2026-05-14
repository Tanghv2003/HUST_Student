import json
from pathlib import Path


data_dir = Path(__file__).parent.parent / "data"


def load_studysets():

    file_path = data_dir / "studysets.json"

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_studyset_detail(file_name: str):

    file_path = data_dir / "studysets" / file_name

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)