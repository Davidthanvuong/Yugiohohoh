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
                Monster.create(slot.transf.g_pos, self.data, slot)
                Card.e_placeCard.notify(self)
                self.deck.user.turn_cardPlaceLeft -= 1
                return self.go.destroy()
        else:
            self.oldIndex = -1 # Muốn sắp xếp thì làm vậy
            
        # Undo về deck cũ
        self.inDeck = True
        self.deck.go.insertChildren(self.go, self.oldIndex)
        self.transf.pos -= self.deck.transf.g_pos



class CardSlot(IClickable):
    my_slots  : list['CardSlot'] = []
    oppo_slots: list['CardSlot'] = []

    dragging  : No['CardSlot'] = None
    selecting : No['CardSlot'] = None
    
    @staticmethod
    def getHoveredSlot(isOpponent: bool, bothSide = False) -> 'CardSlot | None':
        select = CardSlot.selecting
        if not select: return None
        if not bothSide and (select.isOpponent != isOpponent): return None
        return select

    @staticmethod
    def getAvailableSlot(mySide: bool, oppoSide: bool, searchOccupied = False) -> 'CardSlot':
        total: list[CardSlot] = []
        if mySide: total += CardSlot.my_slots
        if oppoSide: total += CardSlot.oppo_slots
        shuffle(total)

        print("[WARNING] getAvailableSlot bay game nếu không có slot trống")
        for slot in total:
            occupied = slot.isOccupied()
            if occupied == searchOccupied: return slot
        raise Exception("Full")
    
    @staticmethod
    def getState(allEmpty: bool, isOpponent: bool) -> bool:
        slots = CardSlot.oppo_slots if isOpponent else CardSlot.my_slots

        if allEmpty: # Ngưng khi có 1 cái không rỗng
            for slot in slots:
                if slot.isOccupied(): return False
            return True
        
        # Ngưng khi có 1 cái rỗng
        for slot in slots:
            if not slot.isOccupied(): return False
        return True

    @staticmethod
    def create(slots: 'GameObject', user: 'UserControl', x = 0, y = 0, **kw):
        forward = -1 if user.isOpponent else 1
        slotId = (x * 5 + y) + (user.isOpponent * 100)
        slot = GameObject('Card Slot', slots, pos=(forward * x * 150, y * 120), **kw)
        slot += Image("card_back.png", (120, 80), overrideHitbox=True)
        slot += CardSlot(user, slotId)

    def __init__(self, user: 'UserControl', myId = -1):
        super().__init__(draggable=True)
        self.myId = myId
        self.user = user
        self.isOpponent = user.isOpponent
        self.occupy: No[ref[Monster]] = None
        if self.isOpponent:
              CardSlot.oppo_slots.append(self)
        else: CardSlot.my_slots.append(self)

    def after_init(self):
        self.com_img = self.go.getComponent(Image)

    def update_logic(self):
        selecting = CardSlot.selecting is self
        dragging = CardSlot.dragging is self
        self.com_img.flashing = selecting or dragging
    
    def on_startHover(self):
        CardSlot.selecting = self

    def on_stopHover(self):
        if CardSlot.selecting is self:
            CardSlot.selecting = None

    def on_startDrag(self):
        if CardSlot.dragging is None:
            CardSlot.dragging = self

    def on_dragging(self):
        pass # Đè lên tính năng drag (không cho phép drag vật, chỉ drag mũi tên)

    def on_stopDrag(self):
        drag = CardSlot.dragging
        select = CardSlot.selecting
        if (drag is None) or (select is None):
           CardSlot.dragging = None
           return 
        if (drag is not self): return
        print(f"{drag.myId} --> {select.myId}")
        CardSlot.dragging = None
        CardSlot.selecting = None

        if (self.user.turn_heroActionLeft <= 0) or (not select.isOccupied()): 
            print(f"[{self.myId} {self.user.go.name}] Hết lượt, hết cứu. Khỏi đánh")
            return
        if not self.occupy: return
        mon = self.occupy() # Test weakref và di chuyển monster đến vị trí slot
        if not mon: return

        if mon.isOpponent != select.isOpponent: # Khác phe thì đánh
              mon.trigger_attack(select)
        else: mon.trigger_support(select)

    def update_render(self):
        if (not CardSlot.dragging) or (CardSlot.dragging is not self): return

        pos1 = CardSlot.dragging.transf.g_pos
        select = CardSlot.selecting
        pos2 = select.transf.g_pos if select else Mouse.pos
        pg.draw.line(App.screen, Color.forward, pos1, pos2, 5)

    def getOccupy(self) -> 'Monster':
        '''Dám làm thì cho làm'''
        return self.occupy() # type: ignore
    
    def tryGetOccupy(self) -> 'Monster | None':
        return self.occupy() if self.occupy else None

    def isOccupied(self) -> bool:
        return (self.occupy is not None) and (self.occupy() is not None)

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