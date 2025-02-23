from script import *

# Cái này khỏi phải giải thích
class Game:
    def __init__(self):
        pg.display.set_caption("OOP + OpenGL Test: Yugiohohoh @ 23/02/2025. Session 08:29 - 20:37")
        self.clock = pg.time.Clock()
        self.goman = GOManager()
        self.goman.load_mainGame()

    def bootload(self):
        pass

    def run_game(self):
        self.goman.obj_update()
        refresh_display()
        self.clock.tick(TARGET_FPS)


if __name__ == '__main__':
    g = Game()
    g.bootload()

    while RUNNING: g.run_game()