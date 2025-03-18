from pytnk.engine import *
import scripts.carddata_implement as cards
from .custom_monster import King

class MainState(FiniteState):
    def begin(self, user: 'Controller'):
        print("MainState begin")
        user.placeCard_left = 3
        user.quickAction_left = 1
        user.main.notif.startNotif(user.rightSide, user.go.name)

    def end(self, user: 'Controller'):
        print("MainState end")
        user.placeCard_left = 0
        user.quickAction_left = 0



class BattleState(FiniteState):
    def begin(self, user: 'Controller'):
        print(f"{user.go.name}: BattleState begin")
        user.fightTime = Motion.linear(0, 1, 2.0)
        user.wasFighting = False

    def end(self, user: 'Controller'):
        print("BattleState end")



class DrawState(FiniteState):
    def begin(self, user: 'Controller'):
        print("DrawState begin")
        Card(user).build()
        # Card(user).build() # 1 thẻ thôi đủ rồi
        LinearStateMachine.next_state()

    def end(self, user: 'Controller'):
        print("DrawState end")


class Controller(Component):
    def build(self, id: int, name: str = ""):
        user = GameObject(name).scope() + self
        slotPosX = (App.native[0] - 100) if self.rightSide else 100
        self.slotsParent = GameObject(pos=(slotPosX, 200))
        self.slots = [CardSlot(self, x*5 + y).build(x, y) for x in range(3) for y in range(5)]
        self.deck = CardDeck(self).build()
        self.myId = id

        initial_datas = [cards.sung_jin_woo] # Custom here
        for i in range(self.start_cardCount):
            data = initial_datas[i] if (i < len(initial_datas)) else None
            Card(self, data).build()

        slot = self.slots[2]
        kingdata = cast(MonsterData, card_database['King'])
        King(kingdata, self, slot).build(slot.transf.pos + self.slotsParent.transf.pos)

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
        self.fightTime: No[Motion] = None
        self.wasFighting = False

        self.mainState   = MainState  (self, Phase.MAIN)
        self.battleState = BattleState(self, Phase.BATTLE)
        self.drawState   = DrawState  (self, Phase.DRAW)

        # self.e_start_drawPhase  : Event = Event()
        # self.e_end_drawPhase    : Event = Event()
        # self.e_start_battlePhase: Event = Event()
        # self.e_end_battlePhase  : Event = Event()

        self.start_cardCount: int = 8
        self.placeCard_left: int = 0
        self.quickAction_left: int = 0

    def update_logic(self):
        if self.fightTime:
            if not self.wasFighting:
                self.wasFighting = True
                self.main.notif.startNotif(self.rightSide, "Fighting")

            if self.fightTime.completed:
                self.wasFighting = False
                self.fightTime = None
                LinearStateMachine.next_state()
    # def hear_end_drawPhase(self):
    #     self.placeCard_left = 0
    #     self.quickAction_left = 0
    #     self.main.ended ^= (1 << self.myId)
    #     print(self.main.ended)
    #     if self.main.ended == (1 << self.main.userCount) - 1:
    #         self.main.drawCard_time()

    #     self.opponent.e_start_drawPhase.notify()

    # def hear_start_drawPhase(self):
    #     self.placeCard_left = 3
    #     self.quickAction_left = 1

    # def draw_time(self):
    #     print("Added card to self")

    def choose_frontSlot(self, occupied: bool):
        return next(self.get_frontSlots(occupied))

    def get_frontSlots(self, occupied: bool):
        slots = self.slots[5:15]
        random.shuffle(slots)
        for slot in slots:
            if (slot.occupy is not None) == occupied:
                yield slot

    def isEmpty(self, front: bool) -> bool:
        slots = self.slots[5:15] if front else self.slots[0:5]
        return not any(slot.occupy for slot in slots)

    def isFull(self, front: bool) -> bool:
        slots = self.slots[5:15] if front else self.slots[0:5]
        return all(slot.occupy for slot in slots)

    def choose_trapSlot(self, occupied: bool):
        next(self.get_trapSlots(occupied))
    
    def get_trapSlots(self, occupied: bool):
        slots = self.slots[0:5]
        random.shuffle(slots)
        for slot in slots:
            if (slot.occupy is not None) == occupied:
                yield slot