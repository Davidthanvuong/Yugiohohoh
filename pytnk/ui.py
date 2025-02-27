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