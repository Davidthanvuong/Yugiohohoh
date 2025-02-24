import pygame as pg
from settings import *
from manager.objectman import ObjectManager
from engine.abstract_renderer import refresh_display

# Cái này khỏi phải giải thích
class Game:
    def __init__(self):
        pg.display.set_caption("Hierarchy Test: Yugiohohoh @ 24/02/2025")
        self.clock = pg.time.Clock()
        self.objman = ObjectManager()
        self.objman.load_mainGame()

    def bootload(self):
        pass

    def run_game(self):
        self.objman.obj_update()
        refresh_display()
        self.clock.tick(TARGET_FPS)


if __name__ == '__main__':
    g = Game()
    g.bootload()

    while RUNNING: g.run_game()
