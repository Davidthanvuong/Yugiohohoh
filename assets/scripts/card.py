from pytnk.engine import *


class Card(IClickable):
    e_placeCard: Event['Card'] = Event()

    def start(self):
        self.targetPos = vec(ZERO)
        deck = self.go.tryGet_parentComponent(CardDeck)
        self.inDeck = deck is not None
        self.opponent = deck.opponent if deck else False
        self.draggable = self.inDeck# and not self.opponent
        self.deck = deck
        
        self.com_img = self.go.getComponent(Image)
        if not self.opponent:
            path = f"card\\{choice(CardDeck.cardImages)}"
            self.com_img.switchImage(path)

    def update_logic(self):
        # print(self.go.parent, self.transf.g_pos, self.inDeck)
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
            burn = GameObject.loadPrefab("Burning Card", pos=self.transf.g_pos, edit=True)
            burn.getComponent(Shader_BurningCard).bind(self.com_img)
            burn.restart()

            slot = self.deck.getSlot() if self.deck else None
            pos = slot.transf.g_pos if slot else ZERO

            mons = GameObject('Monster', pos=pos, anchor=MIDBOTTOM)

            newpath = os.path.join(
                "monster", os.path.splitext(os.path.basename(self.com_img.path))[0] + ".png"
            )

            mons += Image(newpath, (150, 135), overrideHitbox=True)
            com_mon = mons.addComponent(Monster)

            GameObject.loadPrefab('Monster UI', mons)

            if slot: slot.getComponent(CardSpot).bind = ref(com_mon)
            Card.e_placeCard.notify(self)
            self.go.destroy()



class CardSpot(IClickable):
    rt_dragId: tuple[No['CardSpot'], int] = (None, -1)
    rt_selectId: tuple[No['CardSpot'], int] = (None, -1)

    def __init__(self, startId = -1, **kwargs):
        super().__init__(draggable=True, **kwargs)
        self.startId = startId
        self.bind: No[ref[Monster]] = None

    def start(self):
        self.com_img = self.go.getComponent(Image)

    def update_logic(self):
        selecting = CardSpot.rt_selectId[0] is self
        dragging = CardSpot.rt_dragId[0] is self
        self.com_img.flashing = selecting or dragging
    
    def on_startHover(self):
        # if CardSpot.rt_dragId[0] is not self:
        CardSpot.rt_selectId = (self, self.startId)

    def on_stopHover(self):
        if CardSpot.rt_selectId[0] is self:
            CardSpot.rt_selectId = (None, -2)

    def on_startDrag(self):
        if CardSpot.rt_dragId[0] is None:
            CardSpot.rt_dragId = (self, self.startId)

    def on_dragging(self):
        # Đè lên tính năng drag (không cho phép drag vật, chỉ drag mũi tên)
        pass

    def on_stopDrag(self):
        # Check trước khi hủy, tạm thời chỉ in
        if CardSpot.rt_dragId[0] is self and CardSpot.rt_selectId[0] is not None:
            print(f"{CardSpot.rt_dragId[1]} --> {CardSpot.rt_selectId[1]}")
            if self.bind:
                mons = self.bind()
                if mons:
                    mons.moving = True
                    mons.targetPos = CardSpot.rt_selectId[0].transf.g_pos
            CardSpot.rt_dragId = (None, -1)
            CardSpot.rt_selectId = (None, -2)

    def update_render(self):
        if CardSpot.rt_dragId[0] is not self: return
        assert CardSpot.rt_dragId[0] is not None # Chắc chắn không thể xảy ra

        pos1 = CardSpot.rt_dragId[0].transf.g_pos
        if CardSpot.rt_selectId[0] is not None:
            pos2 = CardSpot.rt_selectId[0].transf.g_pos
        else: pos2 = Mouse.pos
        pg.draw.line(App.display, Color.forward, pos1, pos2, 5)


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
        print(self.go.coms)
        for i in range(self.startCount):
            card = GameObject.loadPrefab('Card', parent=self.go)

        for y in range(5):
            for x in range(3):
                inverse = -1 if self.opponent else 1
                pos = vec(x * 150 * inverse, y * 120)
                # slot = GameObject(f"Slot {y*5 + x}", self.slotsGO, pos=pos)
                slot = GameObject.loadPrefab('Card Placeholder', parent=self.slotsGO, pos=pos)
                slot.getComponent(CardSpot).startId = y * 5 + x
                self.slots_empty.append(slot)

    def getSlot(self) -> GameObject:
        if CardSpot.rt_selectId[0] is not None:
            slot = CardSpot.rt_selectId[0].go
        else:
            slot = choice(self.slots_empty)
        
        self.slots_empty.remove(slot)
        self.slots_filled.append(slot)
        return slot

    def update_logic(self):
        cards = self.go.childs
        n = len(cards)

        center = - UPWARD * self.height
        for i, card in enumerate(cards):
            frac = (i - n / 2 + 0.5) / n * self.arc
            card.getComponent(Card).targetPos = center + (UPWARD * self.height).rotate(frac)
            card.transf.rot = -frac