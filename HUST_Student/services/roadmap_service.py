"""
roadmap_service.py — CRUD cho roadmaps.json

Thuật toán sinh lịch (4-cycle Spaced Repetition):
  - Mỗi 5 ngày là 1 nhóm, mỗi 4 nhóm là 1 chu kỳ (20 ngày)
  - Ngày milestone (chia hết 5): ôn toàn bộ [1..day-1]
  - Ngày còn lại: ôn theo vị trí trong nhóm và loại chu kỳ
"""
import json
import uuid
from pathlib import Path

from HUST_Student.core.paths import DATA_DIR

ROADMAPS_JSON = DATA_DIR / "roadmaps.json"


def _default_schedule(total_days: int) -> list[dict]:
    """
    Sinh lịch học theo Spaced Repetition 4-cycle.

    Mỗi ngày d có:
      lessons[0] = bài mới (bài d)
      lessons[1:] = các bài ôn lại

    Quy tắc ôn theo nhóm 5 ngày:
      pos 0 (đầu nhóm): không ôn
      pos 4 (milestone): ôn tất cả [1..d-1]
      cycle 0 (group 0,4,8,...): pos1,pos2 ôn từ max(1,pm)→d; pos3 không
      cycle 1 (group 1,5,9,...): pos1,pos2 ôn từ pm→d;        pos3 không
      cycle 2 (group 2,6,10,...): pos1 ôn từ pm-2→d;          pos2 không; pos3 ôn từ gs+1→d
      cycle 3 (group 3,7,11,...): pos1,pos3 ôn từ pm→d;       pos2 không
    """
    schedule = []
    for d in range(1, total_days + 1):
        pos = (d - 1) % 5       # vị trí trong nhóm 5 (0-4)
        group = (d - 1) // 5    # chỉ số nhóm (0-based)
        cycle = group % 4       # loại chu kỳ (0-3)
        pm = group * 5          # bài milestone trước (lesson number)
        gs = pm + 1             # bài đầu của nhóm hiện tại

        reviews: list[int] = []

        if pos == 4:
            # Ngày milestone: ôn toàn bộ
            reviews = list(range(1, d))
        elif pos == 0:
            reviews = []
        elif cycle == 0:
            if pos in (1, 2):
                reviews = list(range(max(1, pm), d))
        elif cycle == 1:
            if pos in (1, 2):
                reviews = list(range(pm, d))
        elif cycle == 2:
            if pos == 1:
                reviews = list(range(max(1, pm - 2), d))
            elif pos == 3:
                reviews = list(range(gs + 1, d))
        elif cycle == 3:
            if pos in (1, 3):
                reviews = list(range(pm, d))

        schedule.append({
            "day": d,
            "lessons": [d] + reviews,
            "completed": False,
        })
    return schedule


# ── I/O ──────────────────────────────────────────────────────────

def load_roadmaps() -> list[dict]:
    try:
        with open(ROADMAPS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_roadmaps(data: list[dict]) -> None:
    ROADMAPS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(ROADMAPS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── CRUD ─────────────────────────────────────────────────────────

def add_roadmap(title: str, total_days: int = 20) -> dict:
    data = load_roadmaps()
    new_id = str(uuid.uuid4())[:8]
    roadmap = {
        "id": new_id,
        "title": title.strip(),
        "protocol": f"Spaced Repetition {total_days}-Day Schedule",
        "total_days": total_days,
        "intervals_used": "milestone-5, 4-cycle pattern",
        "schedule": _default_schedule(total_days),
    }
    data.append(roadmap)
    save_roadmaps(data)
    return roadmap


def update_roadmap_title(roadmap_id: str, new_title: str) -> bool:
    data = load_roadmaps()
    for r in data:
        if r["id"] == roadmap_id:
            r["title"] = new_title.strip()
            save_roadmaps(data)
            return True
    return False


def delete_roadmap(roadmap_id: str) -> bool:
    data = load_roadmaps()
    new_data = [r for r in data if r["id"] != roadmap_id]
    if len(new_data) == len(data):
        return False
    save_roadmaps(new_data)
    return True


def toggle_day_completed(roadmap_id: str, day: int) -> bool:
    data = load_roadmaps()
    for r in data:
        if r["id"] == roadmap_id:
            for s in r["schedule"]:
                if s["day"] == day:
                    s["completed"] = not s["completed"]
                    save_roadmaps(data)
                    return True
    return False