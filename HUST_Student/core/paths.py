from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PACKAGE_ROOT / "data"
FOLDERS_JSON = DATA_DIR / "folders.json"
STUDYSETS_JSON = DATA_DIR / "studysets.json"
STUDYSETS_DIR = DATA_DIR / "studysets"
