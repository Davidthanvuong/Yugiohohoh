from .header_objects import *

class ExampleButton(IClickable):
    '''Nút bấm'''

    def __init__(self, onClick_phrase: str, spacing: float = 2, **kwargs):
        super().__init__(**kwargs)
        self.onClick_phrase = onClick_phrase
        self.spacing = spacing
        self.texts: list[str] = []
        self.image = self.tf.get(Image) # Lấy ảnh, không thì báo lỗi :v

    def click_update(self):
        super().click_update() # Call hàm kiểm click chuột bên trong
        
    def render_update(self):
        y = 0
        for line in self.texts:
            surface = writer.render(line, True, (0, 0, 0))
            self.image.direct_render(surface, vec(surface.get_size()), vec(0, 0), vec(0, y))
            y += self.spacing * FONT_SIZE # Chỉnh font size trong settings.py

    def on_startClick(self):
        self.texts.append(self.onClick_phrase)
        print("E")

    def on_startHover(self):
        self.tf.scale *= 1.4

    def on_stopHover(self):
        self.tf.scale /= 1.4


# class TextBox:
#     def __init__(self, x, y, w, h, font, only_numbers=False):
#         self.rect = pg.Rect(x, y, w, h)
#         self.font = font
#         self.text = ""
#         self.active = False
#         self.only_numbers = only_numbers
#         self.color_active = (0, 200, 0)
#         self.color_inactive = (200, 200, 200)

#     def handle_event(self, event):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             self.active = self.rect.collidepoint(event.pos)

#         if event.type == pg.KEYDOWN and self.active:
#             if event.key == pg.K_BACKSPACE:
#                 self.text = self.text[:-1]
#             else:
#                 char = event.unicode
#                 if not self.only_numbers or char.isdigit():
#                     self.text += char

#     def render_update(self, screen):
#         color = self.color_active if self.active else self.color_inactive
#         pg.draw.rect(screen, color, self.rect, 2)
#         text_surface = self.font.render(self.text, True, (0, 0, 0))
#         screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

# # Khởi tạo Pygame
# pg.init()
# screen = pg.display.set_mode((500, 500))
# clock = pg.time.Clock()
# font = pg.font.Font(None, 40)
# input_box = TextBox(100, 200, 300, 50, font, only_numbers=True)

# running = True
# while running:
#     screen.fill((255, 255, 255))

#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             running = False
#         input_box.handle_event(event)

#     input_box.render_update(screen)
#     pg.display.flip()
#     clock.tick(30)

# pg.quit()
