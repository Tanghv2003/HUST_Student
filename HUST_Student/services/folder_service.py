import json
from pathlib import Path


DATA_PATH = (
    Path(__file__)
    .resolve()
    .parent.parent
    / "data"
    / "folders.json"
)


def load_folders():

    with open(
        DATA_PATH,
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


def save_folders(data):

    with open(
        DATA_PATH,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )