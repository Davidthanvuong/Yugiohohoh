import pygame as pg
from settings import *
from manager.objectman import ObjectManager
from engine.abstract_renderer import refresh_display

# Cái này khỏi phải giải thích
class Game:
    def __init__(self):
        pg.display.set_caption("Transform + Interactive Test: Yugiohohoh @ 25/02/2025")
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
    print('hello')

    while RUNNING: g.run_game()

# 25/02 Focus:
# All
# - Group syncing (Python, libs, Github & push pull)
# - Ideas for Summons

# Davich
# - Split update to logic_update (top down), render_update (down up)
# Then commit to github
# - QUICK Document important code and make examples for Summon
# - QUICK Scene Loader -- Array of Scene (renamed from GOMan)
# - QUICK Game --> Editor mode --> Transform test scene


# DONE QUICK Split, no more second Inheritant. All are binded to a parent (engine/)
# DONE QUICK Merge, all Transform have an optional ImageCache
# DONE QUICK 9 screenpivot as main Transform (.children \[Transform])



# HazzyQuan
# - QUICK Loading screen scene (Insert loading scene on bootload)
# - Transform & Parent stacking
# - Draggable objects
# - Card picking and dragging test
# - Health bar (2 images: outline, and fill)
# - Health on Summon
# - Textwriter (font, text, pivot?)

# Itsrandomizable
# - Summons modelling & skills, attacks,...
# DuckMinh
# - Description, modelling, summons skill,..