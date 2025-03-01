import pygame as pg

class TextBox:
    def __init__(self, x, y, w, h, font, only_numbers=False):
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.text = ""
        self.active = False
        self.only_numbers = only_numbers
        self.color_active = (0, 200, 0)
        self.color_inactive = (200, 200, 200)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                char = event.unicode
                if not self.only_numbers or char.isdigit():
                    self.text += char

    def render_update(self, screen):
        color = self.color_active if self.active else self.color_inactive
        pg.draw.rect(screen, color, self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
