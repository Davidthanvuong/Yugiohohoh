from pytnk.engine import *

class Card(IClickable):
    e_placeCard: Event['Card'] = Event()
    sfx_picking: pg.mixer.Sound
    sfx_placing: pg.mixer.Sound

    @staticmethod
    def create(deck: No['CardDeck'] = None):
        parent = deck.go if deck else None
        card = GameObject('Card', parent, pos=(0, 300))
        card += Image(f"card_back.png", (150, 240), support_overlay=True, overrideHitbox=True)
        card += Card(deck)

        return card
    
    @staticmethod
    def load_sound():
        Card.sfx_picking = get_sound("picking")
        Card.sfx_placing = get_sound("placing")

    def __init__(self, deck: No['CardDeck'] = None):
        self.inDeck = deck is not None
        super().__init__(draggable=self.inDeck) # type: ignore
        self.deck = deck
        self.user = deck.user if deck else None
        self.isOpponent = self.user.side if self.user else False
        self.glidePos = vec(ZERO)
        self.oldIndex = -1
        self.selectMotion = Motion.linear(0, 150, 0.3, True, True)

    def after_init(self):
        self.data = MonsterData.getRandom()

        self.com_img = self.go.getComponent(Image)
        self.com_img.overlay_color = Color.pivot

        if not self.isOpponent:
            path = f"card\\{self.data.img_path}"
            self.com_img.switchImage(path)

    def changed_childs(self):
        self.draggable = (self.user is not None) and self.user.turn_cardPlaceLeft > 0
        if self.inDeck:
            self.transf.pos = self.transf.pos.lerp(self.glidePos, 0.5)

    def on_startHover(self):
        self.transf.scale *= 1.1
        self.selectMotion.start()

    def on_hovering(self):
        k = 0 if self.dragging else self.selectMotion.value
        self.com_img.overlay_opacity = k

    def on_stopHover(self):  
        self.transf.scale /= 1.1
        self.com_img.overlay_opacity = 0

    def on_startDrag(self, controlled = False):
        self.transf.rot = 0.0
        self.inDeck = False
        self.oldIndex = self.go.removeParent()
        Card.sfx_picking.play()
        # GameObject.root.insertChildren(self.go)
        if not controlled:
            super().on_startDrag()

    def on_stopDrag(self):
        if not self.deck: return
        if self.isOpponent:
              dist = self.transf.g_pos.y + 100
        else: dist = App.native[1] - self.transf.g_pos.y

        if dist > 200:
            slot = CardSlot.get_hoveredSlot(self.isOpponent)
            if slot and self.try_placeCard(slot):
                self.deck.user.turn_cardPlaceLeft -= 1
                Card.sfx_placing.play()
                return self.go.destroy()
        else:
            self.oldIndex = -1 # Muốn sắp xếp thì làm vậy
            
        # Undo về deck cũ
        self.inDeck = True
        self.go.removeParent(reroot=False)
        self.deck.go.insertChildren(self.go, self.oldIndex)
        self.transf.pos -= self.deck.transf.g_pos

    def try_placeCard(self, slot: 'CardSlot') -> bool:
        assert self.user is not None
        if isinstance(self.data, MonsterData):
            if slot.isOccupied(): return False
            self.data.monster.create(slot.transf.g_pos, self.data, self.user, slot)
        elif isinstance(self.data, TrapData):
            self.data.trap.create(slot.transf.g_pos, self.data, slot)
        elif isinstance(self.data, SpellData):
            if CardSlot.isEmpty(not self.isOpponent): return False # Không thể dùng spell khi không có monster
            self.data.spell.create(slot.transf.g_pos, self.data, slot, self.isOpponent)

        burn = Shader_BurningCard.create(self.transf.g_pos, self.com_img)
        Card.e_placeCard.notify(self)
        return True


class CardDeck(Component):
    @staticmethod
    def build(sync: 'UserControl', **kw):
        if sync.side:
            deck = GameObject('CardDeck', sync.go, pos=(App.center[0], -50), rot=180)
        else: deck = GameObject('CardDeck', sync.go, pos=(App.center[0], App.native[1] - 100))
        deck += CardDeck(sync, **kw)

        return deck
    
    def __init__(self, user: 'UserControl', arc = 48, height = 1200, maxFrac = 6, initialCount = 8):
        self.user = user
        self.arc = arc
        self.height = height
        self.maxFrac = maxFrac
        self.initialCount = initialCount
        user.deck = self

    def after_init(self):
        for _ in range(self.initialCount):
            Card.create(self)

    def changed_childs(self):
        cards = self.go.childs
        n = len(cards)

        center = - UPWARD * self.height
        spanning = min(self.arc, self.maxFrac * n)
        for i, card in enumerate(cards):
            frac = (i - n / 2 + 0.5) / n * spanning
            card.getComponent(Card).glidePos = center + (UPWARD * self.height).rotate(frac)
            card.transf.rot = -frac