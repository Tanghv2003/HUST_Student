import reflex as rx

class ClassState(rx.State):
    def handle_class_click(self, class_type: str):
        """Xử lý khi click vào mục trong lớp học"""
        print(f"Clicked on: {class_type}")
        # Thêm logic chuyển trang hoặc xử lý khác
        # Ví dụ: return rx.redirect(f"/{class_type}")