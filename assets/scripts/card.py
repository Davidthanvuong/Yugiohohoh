from pytnk.header_pygame import *

class Card(IClickable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.com_image = self.tf.getComponent(Image)


    def on_startClick(self):
        self.clickDelta = self.tf.global_pos - mouse.pos

    def on_clicking(self):
        if self.tf.parent:
            self.tf.parent.childrens.remove(self.tf)
            Game.maingameTf.adoptChildren(self.tf)
        self.tf.pos = mouse.pos + self.clickDelta

        key = pg.key.get_pressed()
        if key[pg.K_LSHIFT]:
            self.tf.angle += 2


    def on_startHover(self):
        self.tf.scale *= 1.3


    def on_stopHover(self):
        self.tf.scale /= 1.3


class CardDeck(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if True or not Transform.existPrefab('Card'):
            card = Transform('Card', ZERO, CENTER, (200, 300), angle=-5, parent=self.tf)
            Image(bind=card, path="card_empty.png", standalone=True)
            Card(bind=card)
            #Text(bind=card, text="10")

            card.saveSelf(delete=True)


        
    # spinnies: list[Transform] = []
    # for y in range(100, Window.native[1]-99, 50):
    #     for x in range(400, Window.native[0]-399, 50):
    #         spinny = Transform("Spinny", pos=(x, y), pivot=CENTER, parent=Game.maingameTf)
    #         Image("card_empty.png", size=(100, 150), bind=spinny)
    #         spinnies.append(spinny)