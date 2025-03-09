from pytnk.engine import *


class Card(IClickable):
    def start(self):
        self.targetPos = vec(ZERO)
        deck = self.go.tryGet_parentComponent(CardDeck)
        self.inDeck = deck is not None
        self.opponent = deck.opponent if deck else False
        self.draggable = self.inDeck and not self.opponent
        self.deck = deck
        
        self.com_img = self.go.getComponent(Image)
        if not self.opponent:
            self.com_img.switchImage(f"card\\{choice(CardDeck.cardImages)}")

    def update_logic(self):
        if self.inDeck:
            self.transf.pos = self.transf.pos.lerp(self.targetPos, 0.2)

    def on_startHover(self):
        self.transf.scale *= 1.1

    def on_stopHover(self):
        self.transf.scale /= 1.1

    def on_startDrag(self):
        self.transf.rot = 0.0
        self.inDeck = False
        self.go.removeParent()
        super().on_startDrag()

    def on_stopDrag(self):
        dist = App.native[1] - self.transf.g_pos.y
        if self.deck and dist <= 200:
            self.inDeck = True
            self.deck.go.addChildren(self.go)
        else:
            burn = GameObject('Burn', pos=self.transf.g_pos)
            burn += Shader_BurningCard(self.com_img.shared.native, self.com_img.imgsize, 
                start_count=rint(5, 20), burn_time=rint(2, 4)*0.5)

            parent = self.deck.getSlotPos() if self.deck else ZERO
            mons = GameObject('Monster', pos=parent, pivot=MIDBOTTOM)
            mons += Image('unknown\\duck.png', (150, 135), overrideHitbox=True)
            mons += Monster()
            self.go.destroy()



class CardPlaceholder(IClickable):
    def start(self):
        self.com_img = self.go.getComponent(Image)
        # flash = GameObject("Flashing", self.go, pivot=self.transf.pivot)
        # size = self.com_render.imgsize
        # img = Image(self.com_render.path, (size.x, size.y), overrideHitbox = True)
        # self.com_flashing = flash.addComponent(img)
        # img.shared.fillColor(Color.white)
        # img.shared.native.set_alpha(100)
        # img.enabled = False
    
    def on_startHover(self):
        self.com_img.flashing = True

    def on_stopHover(self):
        self.com_img.flashing = False




class CardDeck(Component):
    cardImages: list[str] = []

    def __init__(self, slotsGO: GameObject, arc = 50, height = 1200, startCount = 12, opponent = False):
        self.arc = arc
        self.slotsGO = slotsGO
        self.height = height
        self.opponent = opponent
        self.startCount = startCount
        self.slots_empty: list[GameObject] = []
        self.slots_filled: list[GameObject] = []

    def start(self):
        if len(CardDeck.cardImages) == 0: # Chưa khởi tạo
            path = "assets\\images\\card"
            CardDeck.cardImages = [f for f in os.listdir(path) if 
                                   os.path.isfile(os.path.join(path, f))]
            
        for i in range(self.startCount):
            card = GameObject.loadPrefab('Card', parent=self.go)

        for y in range(5):
            for x in range(3):
                inverse = -1 if self.opponent else 1
                pos = vec(x * 150 * inverse, y * 120)
                # slot = GameObject(f"Slot {y*5 + x}", self.slotsGO, pos=pos)
                slot = GameObject.loadPrefab('Card Placeholder', parent=self.slotsGO, pos=pos)
                self.slots_empty.append(slot)

    def getSlotPos(self):
        if len(self.slots_empty) == 0:
            raise Exception("Empty")
        
        slot = choice(self.slots_empty)
        self.slots_empty.remove(slot)
        self.slots_filled.append(slot)
        return slot.transf.g_pos

    def update_logic(self):
        cards = self.go.childs
        n = len(cards)

        center = - UPWARD * self.height
        for i, card in enumerate(cards):
            frac = (i - n / 2 + 0.5) / n * self.arc
            card.getComponent(Card).targetPos = center + (UPWARD * self.height).rotate(frac)
            card.transf.rot = -frac