from pytnk.header_pygame import *


# def deadline_demo():
#     '''Chữa cháy demo (do Engine đang làm mà thầy kêu review)'''

#     deck_tf = Transform('Card Deck', pos=(200, Window.native[1]-200), hitbox=(800, 200), pivot=(0, 0.5), parent=Game.maingameTf, rootname='Maingame')
#     #Image(bind=deck_tf, path="white.png", fit=True, standalone=True)
#     FlexArray(interactable=False, bind=deck_tf, axis='x', use_crowding=True)

#     deck = CardDeck(bind=deck_tf)
#     path = "assets\\images\\summoncard"
#     files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#     print(files)
#     for i in range(20):
#         card = Transform.getPrefab('Card', parent=deck_tf)
#         img = card.getComponent(Image)
#         img.cache = SharedImage.fetch(f"summoncard\\{random.choice(files)}")
import os

class Card(IClickable):
    def __call__(self):
        self.com_image = self.go.getComponent(Image)


    def on_startClick(self):
        self.clickDelta = self.go.global_pos - Mouse.pos


    def on_clicking(self):
        if self.go.parent and self.go.parent is not self.go.scene.go: # stupid
            self.go.parent.childs.remove(self.go)
            Window.Scenes['Maingame'].go.addChildren(self.go)
        self.go.pos = Mouse.pos + self.clickDelta

        key = pg.key.get_pressed()
        if key[pg.K_LSHIFT]:
            self.go.rot += 2


    def on_startHover(self):
        self.go.scale *= 1.3


    def on_stopHover(self):
        self.go.scale /= 1.3


path = "assets\\images\\card"
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

class CardDeck(Component):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if False and not GameObject.existPrefab('Card'):
            card = GameObject('Card', ZERO, CENTER, (200, 300), rot=-5)
            card += Image(path="card_empty.png")
            card += Text(text="10", font=FontPreset.jetbrains_60)
            card += Card()
            #Text(bind=card, text="10")

            card.saveSelf(delete=True)

    def __call__(self):
        for i in range(10):
            card = GameObject(hitbox=(100, 150), pivot=CENTER, parent=self.go)
            card += Image(path=f"card\\{choice(files)}", fit=True)
            card += Text(text="10", font=FontPreset.jetbrains_60)
            Card(go=card)()


        
    # spinnies: list[Transform] = []
    # for y in range(100, Window.native[1]-99, 50):
    #     for x in range(400, Window.native[0]-399, 50):
    #         spinny = Transform("Spinny", pos=(x, y), pivot=CENTER, parent=Game.maingameTf)
    #         Image("card_empty.png", size=(100, 150), bind=spinny)
    #         spinnies.append(spinny)