from pytnk.engine import *


class Card(IClickable):
    e_placeCard: Event['Card'] = Event()

    @staticmethod
    def create_default(parent: No[GameObject] = None, opponent = False):
        card = GameObject('Card', parent, pos=(0, 300))
        card += Image(f"card_back.png", (150, 240), overrideHitbox=True)
        card += Card(opponent)

    def __init__(self, opponent = False, **kw):
        super().__init__(draggable=True, **kw)
        self.opponent = opponent

    def after_init(self):
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

    def on_startDrag(self, controlled = False):
        self.transf.rot = 0.0
        self.inDeck = False
        self.go.removeParent()
        if not controlled:
            super().on_startDrag()

    def on_stopDrag(self):
        if self.opponent:
            dist = self.transf.g_pos.y
        else: dist = App.native[1] - self.transf.g_pos.y
        if self.deck and dist <= 200:
            self.inDeck = True
            self.deck.go.addChildren(self.go)
        else:
            burn = Shader_BurningCard.create_default(self.transf.g_pos, self.com_img)
            slot = CardSlot.ownHoveredSlot(self.opponent)
            mon = Monster.create_default(slot.transf.g_pos, slot)

            # slot = self.deck.getSlot() if self.deck else None
            # pos = slot.transf.g_pos if slot else ZERO

            # mons = GameObject('Monster', pos=pos, anchor=MIDBOTTOM)

            # newpath = os.path.join(
            #     "monster", os.path.splitext(os.path.basename(self.com_img.path))[0] + ".png"
            # )

            # mons += Image(newpath, (150, 135), overrideHitbox=True)
            # com_mon = mons.addComponent(Monster)

            # GameObject.loadPrefab('Monster UI', mons)

            # if slot: slot.getComponent(CardSlot).bind = ref(com_mon)
            Card.e_placeCard.notify(self)
            self.go.destroy()



class CardSlot(IClickable):
    rt_dragId: tuple[No['CardSlot'], int] = (None, -1)
    rt_selectId: tuple[No['CardSlot'], int] = (None, -1)
    slots_empty: list['CardSlot'] = []
    slots_filled: list['CardSlot'] = []
    free_count: list[int] = [0, 0]

    @staticmethod
    def create_default(parent: No['GameObject'] = None, x = 0, y = 0, opponent = False, **kw):
        forward = -1 if opponent else 1
        slot = GameObject('Card Slot', parent, pos=(forward * x * 150, y * 120), **kw)
        slot += Image("card_back.png", (120, 80), overrideHitbox=True)
        slot += CardSlot(x + y * 5, opponent)

    @staticmethod
    def ownHoveredSlot(opponent = False, includeOpposite = False):
        select = CardSlot.rt_selectId[0]
        if select is not None and select.side == opponent and not select.occupied:
            slot = select
        elif CardSlot.free_count[opponent] != 0:
            slot = CardSlot.slots_empty[0]
            # Chỉ search có trùng phe hay không khi includeOpposite = True
            while (not includeOpposite) and (slot.side != opponent):
                slot = choice(CardSlot.slots_empty)
        else:
            raise ValueError("Không chỗ nào phù hợp cả")

        CardSlot.slots_empty.remove(slot)
        CardSlot.slots_filled.append(slot)
        CardSlot.free_count[opponent] -= 1
        slot.occupied = True
        return slot

    def __init__(self, startId = -1, opponent = False, **kwargs):
        super().__init__(draggable=True, **kwargs)
        self.startId = startId
        self.side = opponent
        self.occupied = False
        self.bind: No[ref[Monster]] = None
        CardSlot.free_count[opponent] += 1
        CardSlot.slots_empty.append(self)

    def after_init(self):
        self.com_img = self.go.getComponent(Image)

    def update_logic(self):
        selecting = CardSlot.rt_selectId[0] is self
        dragging = CardSlot.rt_dragId[0] is self
        self.com_img.flashing = selecting or dragging
    
    def on_startHover(self):
        # if CardSlot.rt_dragId[0] is not self:
        CardSlot.rt_selectId = (self, self.startId)

    def on_stopHover(self):
        if CardSlot.rt_selectId[0] is self:
            CardSlot.rt_selectId = (None, -2)

    def on_startDrag(self):
        if CardSlot.rt_dragId[0] is None:
            CardSlot.rt_dragId = (self, self.startId)

    def on_dragging(self):
        # Đè lên tính năng drag (không cho phép drag vật, chỉ drag mũi tên)
        pass

    def on_stopDrag(self):
        # Check trước khi hủy, tạm thời chỉ in
        if CardSlot.rt_dragId[0] is self and CardSlot.rt_selectId[0] is not None:
            print(f"{CardSlot.rt_dragId[1]} --> {CardSlot.rt_selectId[1]}")
            if self.bind:
                mons = self.bind()
                if mons:
                    mons.moving = True
                    mons.targetPos = CardSlot.rt_selectId[0].transf.g_pos
            CardSlot.rt_dragId = (None, -1)
            CardSlot.rt_selectId = (None, -2)

    def update_render(self):
        if CardSlot.rt_dragId[0] is not self: return
        assert CardSlot.rt_dragId[0] is not None # Chắc chắn không thể xảy ra

        pos1 = CardSlot.rt_dragId[0].transf.g_pos
        if CardSlot.rt_selectId[0] is not None:
            pos2 = CardSlot.rt_selectId[0].transf.g_pos
        else: pos2 = Mouse.pos
        pg.draw.line(App.screen, Color.forward, pos1, pos2, 5)


class CardDeck(Component):
    cardImages: list[str] = []

    @staticmethod
    def create_default(parent: No[GameObject] = None, opponent = False, **kw):
        if opponent:
            deck = GameObject('CardDeck', parent, pos=(App.center[0], 0), rot=180)
        else: deck = GameObject('CardDeck', parent, pos=(App.center[0], App.native[1] - 100))
        deck += CardDeck(deck, opponent, **kw)

        for i in range(8): # TODO: Start count
            Card.create_default(deck, opponent)
        return deck

    def __init__(self, slotsGO: GameObject, opponent = False, arc = 50, height = 1200, startCount = 12):
        self.arc = arc
        self.slotsGO = slotsGO
        self.height = height
        self.opponent = opponent
        self.startCount = startCount
        # self.slots_empty: list[GameObject] = []
        # self.slots_filled: list[GameObject] = []

    # def after_init(self):
        
            # card = GameObject.loadPrefab('Card', parent=self.go)

    #     for y in range(5):
    #         for x in range(3):
    #             inverse = -1 if self.opponent else 1
    #             pos = vec(x * 150 * inverse, y * 120)
    #             # slot = GameObject(f"Slot {y*5 + x}", self.slotsGO, pos=pos)
    #             slot = GameObject.loadPrefab('Card Placeholder', parent=self.slotsGO, pos=pos)
    #             slot.getComponent(CardSlot).startId = y * 5 + x
    #             self.slots_empty.append(slot)

    def update_logic(self):
        cards = self.go.childs
        n = len(cards)

        center = - UPWARD * self.height
        for i, card in enumerate(cards):
            frac = (i - n / 2 + 0.5) / n * self.arc
            card.getComponent(Card).targetPos = center + (UPWARD * self.height).rotate(frac)
            card.transf.rot = -frac