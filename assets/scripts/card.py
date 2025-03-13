from pytnk.engine import *

class Card(IClickable):
    e_placeCard: Event['Card'] = Event()

    @staticmethod
    def create(deck: No['CardDeck'] = None):
        parent = deck.go if deck else None
        card = GameObject('Card', parent, pos=(0, 300))
        card += Image(f"card_back.png", (150, 240), overrideHitbox=True)
        card += Card(deck)

        return card

    def __init__(self, deck: No['CardDeck'] = None):
        self.inDeck = deck is not None
        super().__init__(draggable=self.inDeck) # type: ignore
        self.deck = deck
        self.user = deck.user if deck else None
        self.isOpponent = self.user.isOpponent if self.user else False
        self.glidePos = vec(ZERO)
        self.oldIndex = -1

    def after_init(self):
        self.data = MonsterData.getRandom()

        self.com_img = self.go.getComponent(Image)
        if not self.isOpponent:
            path = f"card\\{self.data.card_path}"
            self.com_img.switchImage(path)

    def update_logic(self):
        self.draggable = (self.user is not None) and self.user.turn_cardPlaceLeft > 0
        if self.inDeck:
            self.transf.pos = self.transf.pos.lerp(self.glidePos, 0.1)

    def on_startHover(self): self.transf.scale *= 1.1
    def on_stopHover(self):  self.transf.scale /= 1.1

    def on_startDrag(self, controlled = False):
        self.transf.rot = 0.0
        self.inDeck = False
        self.oldIndex = self.go.removeParent()
        if not controlled:
            super().on_startDrag()

    def on_stopDrag(self):
        if not self.deck: return
        if self.isOpponent:
              dist = self.transf.g_pos.y + 100
        else: dist = App.native[1] - self.transf.g_pos.y

        if dist > 200:
            slot = CardSlot.getHoveredSlot(self.isOpponent)
            if slot:
                burn = Shader_BurningCard.create(self.transf.g_pos, self.com_img)
                self.data.monster.create(slot.transf.g_pos, self.data, slot)
                Card.e_placeCard.notify(self)
                self.deck.user.turn_cardPlaceLeft -= 1
                return self.go.destroy()
        else:
            self.oldIndex = -1 # Muốn sắp xếp thì làm vậy
            
        # Undo về deck cũ
        self.inDeck = True
        self.deck.go.insertChildren(self.go, self.oldIndex)
        self.transf.pos -= self.deck.transf.g_pos



class CardDeck(Component):
    @staticmethod
    def create(sync: 'UserControl', **kw):
        if sync.isOpponent:
            deck = GameObject('CardDeck', sync.go, pos=(App.center[0], -50), rot=180)
        else: deck = GameObject('CardDeck', sync.go, pos=(App.center[0], App.native[1] - 100))
        deck += CardDeck(sync, **kw)

        return deck
    
    def __init__(self, sync: 'UserControl', arc = 48, height = 1200, maxFrac = 6, initialCount = 8):
        self.user = sync
        self.arc = arc
        self.height = height
        self.user = sync
        self.maxFrac = maxFrac
        self.initialCount = initialCount
        sync.deck = self

    def after_init(self):
        for _ in range(self.initialCount):
            Card.create(self)

    def update_logic(self):
        cards = self.go.childs
        n = len(cards)

        center = - UPWARD * self.height
        spanning = min(self.arc, self.maxFrac * n)
        for i, card in enumerate(cards):
            frac = (i - n / 2 + 0.5) / n * spanning
            card.getComponent(Card).glidePos = center + (UPWARD * self.height).rotate(frac)
            card.transf.rot = -frac