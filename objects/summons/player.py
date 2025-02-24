from importer.gobj import *

class Player(Transform):
    def __init__(self, pos = vec(CENTER)):
        super().__init__(pos)
        self.velY = 0
        self.human = Imager("summon\\eldenring.png", pivot=vec(0.5, 1))
        self.selector = Imager("select_circle_dot.png", post_scale=vec(1, 0.4))
        self.selector.shared.replace_color((0, 0, 0), (255, 255, 255))

    def update(self):
        self.input_handler()
        self.velY += 3
        if self.pos[1] > NATIVE[1]:
            self.velY = -40

        self.pos[1] += self.velY
        self.selector.spin += 5

        render(self.human, self.pos)
        render(self.selector, self.pos)

    def input_handler(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                quit()