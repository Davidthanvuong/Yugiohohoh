from pytnk.engine import *

class OpponentControl(UserControl):
    '''Có thể được điều khiển bởi network hay bot ngu'''
    
    @staticmethod
    def create(parent: GameObject):
        oppo = GameObject('Opponent', parent)
        user = oppo.addComponent(OpponentControl())
        deck = CardDeck.create(user)

        slots = GameObject('Slot Holder', oppo, pos=(App.native[0] - 100, 200))
        for y in range(5):
            for x in range(3):
                CardSlot.create(slots, user, x, y)

        slots.unscope()
        return oppo
    
    def __init__(self):
        super().__init__(True)
        self.selecting = None
        self.placingSlot = None
        self.attacker: Monster
        self.inAction: No[Callable] = None

    def update_logic(self):
        if not self.myTurn: return
        if not self.inAction:
            self.pick_action()
        else: self.inAction()

    def endPhase(self):
        self.can_placeCard = False
        self.can_attack = False
        super().endPhase()

    def pick_action(self):
        '''Sử dụng AI ngu ngu'''
        actions: list[tuple[Callable, Callable]] = []
        minmax: list[float] = []
        if (self.turn_cardPlaceLeft > 0) and (len(self.deck.go.childs) != 0):
            actions.append((self.act_start_pickCard, self.act_doing_pickCard))
            minmax.append(self.act_point_pickCard())
            print("[Opponent] Pick card có khả năng")

        if (self.turn_heroActionLeft > 0):
            attackSide_notEmpty = not CardSlot.getState(allEmpty=True, isOpponent=True)
            defendSide_notEmpty = not CardSlot.getState(allEmpty=True, isOpponent=False)
            if attackSide_notEmpty and defendSide_notEmpty:
                actions.append((self.act_start_heroAction, self.act_doing_heroAction))
                minmax.append(self.act_point_heroAction())
                print("[Opponent] Hero attack có khả năng")

        if len(actions) == 0:
            print("[Opponent] Hết cứu. Hết nước đi. T thua mày")
            self.endPhase()
            return
        
        group = choices(actions, minmax, k=1)[0]
        group[0]()  # Chạy action bắt đầu
        self.inAction = group[1]

    def act_point_pickCard(self) -> float:
        '''Suy nghĩ (tạm thời bị ngu)'''
        return 1

    def act_start_pickCard(self):
        '''Tạm thời bốc ngẫu nhiên D:'''
        card = choice(self.deck.go.childs).getComponent(Card)
        
        print("[Opponent] Selecting card...")
        card.on_startDrag(controlled=True)  # Drag nhưng kiểm soát bởi *Artificial Stupidity*
        self.slot = CardSlot.getAvailableSlot(False, True, False)
        slot_pos = self.slot.transf.g_pos

        self.selecting = card
        self.selMotion = Motion.ease_in(card.transf.g_pos, slot_pos, 0.6)

    def act_doing_pickCard(self):
        assert self.selecting is not None

        self.selecting.transf.pos = self.selMotion.value
        CardSlot.selecting = self.slot
        if self.selMotion.completed:
            self.selecting.on_stopDrag()
            self.selecting = None
            self.inAction = None
            CardSlot.selecting = None

    def act_point_heroAction(self) -> float:
        '''Suy nghĩ (tạm thời bị ngu)'''
        return 1

    def act_start_heroAction(self):
        print("[Opponent] Selecting attack...")
        self.attacker = CardSlot.getAvailableSlot(False, True, True).getOccupy()
        targetSlot = CardSlot.getAvailableSlot(True, False, True)
        self.attacker.trigger_attack(targetSlot)

    def act_doing_heroAction(self):
        if not self.attacker.attacking:
            self.inAction = None