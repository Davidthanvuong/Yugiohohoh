from pygame import font
from .settings import screen

class TextEngine:
    def __init__(self):
        self.game_font = font.Font('Comic.ttf', 20)

    def write(self, txt: str, pos):
        img = self.game_font.render(txt, True, (255, 255, 255))
        rect = img.get_rect(topleft = pos)
        screen.blit(img, rect)