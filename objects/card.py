from importer.gobj import *

class Card(IClickable, Transform):
    paths = {
        'back': "card_back.png",
        'empty': "card_empty.png",
    }

    def __init__(self, role: str = 'back', **kwargs):
        self.role = role
        super().__init__(
            imgpath=Card.paths[self.role], 
            imgsize=vec(200, 300), 
            pos=vec(0, 150),
            pivot=vec(HALF),
            draggable=True, **kwargs)

    def update(self):
        self.iclick_update() # Xử lí click, drag
        #self.spin += 1
        render(self)
        
    def on_startHover(self):
        self.scale = vec(ONE) * 1.4

    def on_clicking(self):
        self.pos = vec(pg.mouse.get_pos()) #- self.global_pos()

    def on_stopClick(self):
        pass
        #self.mark_for_delete = True        

    def on_stopHover(self):
        self.scale = vec(ONE)