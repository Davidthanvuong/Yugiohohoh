from importer.gobj import *

class Card(Transform, IClickable):
    paths = {
        'back': "card_back.png",
        'empty': "card_empty.png",
    }

    def __init__(self, pos = vec(CENTER), back: bool = False, **kwargs):
        self.role = 'back' if back else 'empty'
        super().__init__(
            imgpath=Card.paths[self.role], 
            imgsize=vec(200, 300), spin=-5, 
            pos=pos, host=self, 
            draggable=True, **kwargs)

    def update(self):
        self.iclick_update() # Xử lí click, drag
        render(self)
        
    def on_startHover(self):
        print("Hello")