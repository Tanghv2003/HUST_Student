"""
roadmap_state.py — State quản lý lộ trình học.
Tương thích Reflex 0.9: dùng list[dict] thay vì rx.Base.
"""
import reflex as rx

from HUST_Student.services.roadmap_service import (
    add_roadmap,
    delete_roadmap,
    load_roadmaps,
    toggle_day_completed,
    update_roadmap_title,
)


class RoadmapState(rx.State):

    # list[dict] — mỗi dict là 1 roadmap
    roadmaps: list[dict] = []

    # ── Detail modal ──────────────────────────────────────────────
    show_detail: bool = False
    detail_roadmap: dict = {}

    # ── Add modal ─────────────────────────────────────────────────
    show_add: bool = False
    new_title: str = ""
    new_total_days: int = 20

    # ── Edit modal ────────────────────────────────────────────────
    show_edit: bool = False
    edit_id: str = ""
    edit_title: str = ""

    # ── Delete confirm ────────────────────────────────────────────
    show_delete: bool = False
    delete_id: str = ""
    delete_title: str = ""

    # ── Message ───────────────────────────────────────────────────
    message: str = ""
    message_type: str = ""  # "success" | "error"

    # ── Computed ─────────────────────────────────────────────────

    @rx.var
    def roadmap_count(self) -> int:
        return len(self.roadmaps)

    @rx.var
    def detail_schedule(self) -> list[dict]:
        return self.detail_roadmap.get("schedule", [])

    @rx.var
    def detail_title(self) -> str:
        return self.detail_roadmap.get("title", "")

    @rx.var
    def detail_protocol(self) -> str:
        return self.detail_roadmap.get("protocol", "")

    @rx.var
    def detail_intervals(self) -> str:
        return self.detail_roadmap.get("intervals_used", "")

    @rx.var
    def detail_total_days(self) -> int:
        return self.detail_roadmap.get("total_days", 0)

    @rx.var
    def detail_completed_count(self) -> int:
        return sum(1 for s in self.detail_roadmap.get("schedule", []) if s.get("completed"))

    @rx.var
    def detail_roadmap_id(self) -> str:
        return self.detail_roadmap.get("id", "")

    # ── Load ──────────────────────────────────────────────────────

    def load_roadmaps(self):
        self.roadmaps = load_roadmaps()

    # ── Detail ────────────────────────────────────────────────────

    def open_detail(self, roadmap_id: str):
        for r in self.roadmaps:
            if r.get("id") == roadmap_id:
                self.detail_roadmap = dict(r)
                self.show_detail = True
                return

    def close_detail(self):
        self.show_detail = False
        self.detail_roadmap = {}

    def toggle_day(self, roadmap_id: str, day: int):
        toggle_day_completed(roadmap_id, day)
        self.roadmaps = load_roadmaps()
        # refresh detail
        for r in self.roadmaps:
            if r.get("id") == roadmap_id:
                self.detail_roadmap = dict(r)
                break

    # ── Add ───────────────────────────────────────────────────────

    def open_add(self):
        self.new_title = ""
        self.new_total_days = 20
        self.show_add = True
        self.message = ""

    def close_add(self):
        self.show_add = False

    def set_new_title(self, v: str):
        self.new_title = str(v) if v else ""

    def set_new_total_days(self, v: str):
        try:
            self.new_total_days = max(1, min(int(str(v)), 365))
        except (ValueError, TypeError):
            pass

    def confirm_add(self):
        title = self.new_title.strip()
        if not title:
            self.message = "❌ Tên lộ trình không được để trống."
            self.message_type = "error"
            return
        add_roadmap(title, self.new_total_days)
        self.roadmaps = load_roadmaps()
        self.close_add()
        self.message = f"✅ Đã tạo lộ trình '{title}'"
        self.message_type = "success"

    # ── Edit ──────────────────────────────────────────────────────

    def open_edit(self, roadmap_id: str, current_title: str):
        self.edit_id = roadmap_id
        self.edit_title = current_title
        self.show_edit = True
        self.message = ""

    def close_edit(self):
        self.show_edit = False

    def set_edit_title(self, v: str):
        self.edit_title = str(v) if v else ""

    def confirm_edit(self):
        title = self.edit_title.strip()
        if not title:
            self.message = "❌ Tên không được để trống."
            self.message_type = "error"
            return
        update_roadmap_title(self.edit_id, title)
        self.roadmaps = load_roadmaps()
        self.close_edit()
        self.message = f"✅ Đã đổi tên thành '{title}'"
        self.message_type = "success"

    # ── Delete ────────────────────────────────────────────────────

    def open_delete(self, roadmap_id: str, title: str):
        self.delete_id = roadmap_id
        self.delete_title = title
        self.show_delete = True
        self.message = ""

    def close_delete(self):
        self.show_delete = False

    def confirm_delete(self):
        delete_roadmap(self.delete_id)
        self.roadmaps = load_roadmaps()
        self.close_delete()
        self.message = f"✅ Đã xóa lộ trình '{self.delete_title}'"
        self.message_type = "success"

    def clear_message(self):
        self.message = ""
        self.message_type = ""