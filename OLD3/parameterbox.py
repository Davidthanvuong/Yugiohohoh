import pygame as pg
from textbox import TextBox

class ParameterBox:
    def __init__(self, x, y, w, h, name, font, func=None, only_numbers=False):
        """
        x, y, w, h: Tọa độ và kích thước khung lớn.
        name: tên hiển thị (label).
        font: font để render chữ.
        func: hàm callback (nếu có) sẽ được gọi khi text X, Y thay đổi.
        only_numbers: True nếu chỉ cho nhập số.
        """
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.name = name
        self.func = func
        self.only_numbers = only_numbers

        # Tạo surface để vẽ tên
        self.name_surface = self.font.render(self.name, True, (0, 0, 0))
        self.name_rect = self.name_surface.get_rect(topleft=(x + 5, y + 5))

        # Tạo 2 TextBox cho X, Y. Bạn có thể chỉnh toạ độ, kích thước theo ý.
        # Ví dụ: Đặt text box X cách nhãn 10px, text box Y cách X 10px
        textbox_width = 60
        textbox_height = 30

        self.textbox_x = TextBox(
            self.name_rect.right + 10,
            y + 5,
            textbox_width,
            textbox_height,
            self.font,
            only_numbers=self.only_numbers
        )
        self.textbox_y = TextBox(
            self.textbox_x.rect.right + 10,
            y + 5,
            textbox_width,
            textbox_height,
            self.font,
            only_numbers=self.only_numbers
        )

    def handle_event(self, event):
        # Truyền event cho từng TextBox
        old_x = self.textbox_x.text
        old_y = self.textbox_y.text

        self.textbox_x.handle_event(event)
        self.textbox_y.handle_event(event)

        # Kiểm tra nếu text X hoặc Y thay đổi => gọi func (nếu có)
        new_x = self.textbox_x.text
        new_y = self.textbox_y.text

        if self.func and (new_x != old_x or new_y != old_y):
            self.func(new_x, new_y)

    def render_update(self, screen):
        # Vẽ khung lớn (có thể vẽ đậm hay nhạt, tuỳ thích)
        pg.draw.rect(screen, (150, 150, 150), self.rect, 2)

        # Vẽ label name
        screen.blit(self.name_surface, self.name_rect)

        # Vẽ 2 text box
        self.textbox_x.render_update(screen)
        self.textbox_y.render_update(screen)
