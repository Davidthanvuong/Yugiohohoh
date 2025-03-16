from pytnk.engine import *
from .monster import King

class Controller(Component):
    def build(self, id: int, name: str = ""):
        user = GameObject(name).scope() + self
        slotPosX = (App.native[0] - 100) if self.rightSide else 100
        self.slotsParent = GameObject(pos=(slotPosX, 200))
        self.slots = [CardSlot(self, x*5 + y).build(x, y) for x in range(3) for y in range(5)]
        self.deck = CardDeck(self).build()
        self.myId = id
        [Card(self).build() for _ in range(self.start_cardCount)]

        # slot = self.slots[2]
        # King(card_database['King'], self, slot).build(slot.transf.pos + self.slotsParent.transf.pos) # type: ignore

        return user.unscope().addComponent(self)

    '''Một cách để fix circular import đó là dồn tất cả dependencies vô chung 1 thằng'''
    def __init__(self, main: 'Maingame'):
        self.main = main
        self.slotsParent: GameObject
        self.myId: int
        self.rightSide: bool
        self.isPlayer: bool

        self.opponent: 'Controller'
        self.deck: 'CardDeck'
        self.slots: list['CardSlot']

        self.e_start_drawPhase  : Event = Event(self.hear_start_drawPhase)
        self.e_end_drawPhase    : Event = Event(self.hear_end_drawPhase)
        self.e_start_battlePhase: Event = Event()
        self.e_end_battlePhase  : Event = Event()
        self.e_king_die         : Event = Event()

        self.start_cardCount: int = 8
        self.placeCard_left: int = 0
        self.quickAction_left: int = 0

    def hear_end_drawPhase(self):
        self.placeCard_left = 0
        self.quickAction_left = 0
        self.main.ended ^= (1 << self.myId)
        print(self.main.ended)
        if self.main.ended == (1 << self.main.userCount) - 1:
            self.main.drawCard_time()

        self.opponent.e_start_drawPhase.notify()

    def hear_start_drawPhase(self):
        self.placeCard_left = 3
        self.quickAction_left = 1
        self.main.notif.startNotif(self.rightSide, self.go.name)

    def draw_time(self):
        print("Added card to self")
        Card(self).build()
    

    def get_occupiedSlots(self):
        slots = self.slots
        random.shuffle(slots)
        yield from (slot for slot in slots if (slot.occupy) and (slot.myId >= 5))

    def get_emptySlots(self):
        slots = self.slots
        random.shuffle(slots)
        yield from (slot for slot in slots if (not slot.occupy) and (slot.myId >= 5))

    def getAny_occupiedSlot(self):
        return next(self.get_occupiedSlots())

    def getAny_emptySlot(self):
        return next(self.get_emptySlots())

    def get_frontFirstSlot(self):
        rows = list(range(5))
        random.shuffle(rows)
        slots = (self.slots[row * 3 + col] for col in range(2, -1, -1) for row in rows if self.slots[row * 3 + col].occupy)
        return slots
    
    def getAny_frontFirstSlot(self):
        return next(self.get_frontFirstSlot())
    
    def isEmpty(self):
        return not any(slot.occupy for slot in self.slots)
    
    def isFull(self):
        return all(slot.occupy for slot in self.slots)