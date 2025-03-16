from pytnk.engine import *
from typing import Generator

class OpponentControl(UserControl):
    '''Có thể được điều khiển bởi network hay bot ngu'''
    
    @staticmethod
    def create(parent: GameObject):
        oppo = GameObject('Opponent', parent)
        user = oppo.addComponent(OpponentControl())
        deck = CardDeck.create(user)

        slots = GameObject('Slot Holder', oppo, pos=(App.native[0] - 100, 200))
        for x in range(3):
            for y in range(5):
                CardSlot.create(slots, user, x, y)

        slots.unscope()
        return oppo
    
    def __init__(self):
        super().__init__(True)
        self.warmup = False
        self.warmup_motion = Motion.linear(0, 1, 1.0) # Cho nó 1 giây để fix lỗi bốc card
        self.attacker: Monster
        self.action: No[Generator] = None

    def update_logic(self):
        if not self.myTurn: return
        if not self.warmup:
            if self.warmup_motion.completed:
                self.warmup = True
            return
        
        if self.action is not None:
            try: next(self.action)
            except StopIteration:
                self.action = None
        else: self.pick_action()

    def endPhase(self):
        self.can_placeCard = False
        self.can_attack = False
        super().endPhase()

    def pick_action(self):
        actions: list[Callable] = []
        weights: list[float] = []

        actions.append(self.act_pickRandomCard)
        weights.append(self.eval_pickRandomCard())

        actions.append(self.act_heroAction)
        weights.append(self.eval_heroAction())

        if sum(weights) == 0:
            print("[Opponent] Hết cứu. Hết nước đi.")
            return self.endPhase()
        
        action = choices(actions, weights, k=1)[0]
        self.action = action()

    def eval_pickRandomCard(self):
        if (self.turn_cardPlaceLeft <= 0) or (len(self.deck.go.childs) == 0):
            return 0
        return 0.8
    
    def act_pickRandomCard(self):
        print("[Opponent] Selecting card...")
        card = choice(self.deck.go.childs).getComponent(Card)
        
        card.on_startDrag(controlled=True)  # Drag nhưng kiểm soát bởi *Artificial Stupidity*
        cardtf = card.transf
        placeSlot = CardSlot.getAny_emptySlot(self.side)
        motion = Motion.ease_in(card.transf.g_pos, placeSlot.transf.g_pos, 0.8)

        while not motion.completed:
            cardtf.pos = motion.value
            yield

        CardSlot.selecting = placeSlot
        card.on_stopDrag()
        CardSlot.selecting = None
        self.turn_cardPlaceLeft -= 1

    def eval_heroAction(self):
        if (self.turn_heroActionLeft <= 0) or CardSlot.isAnySideEmpty():
            return 0
        return 1
    
    def act_heroAction(self):
        print("[Opponent] Selecting attack...")
        atk = CardSlot.getAny_occupiedSlot(self.side).occupy
        targetSlot = CardSlot.getAny_occupiedSlot(not self.side)
        atk.setTarget(targetSlot)
        atk.actions.append(atk.action_attack())
        motion = Motion.linear(0, 1, 2.0)
        while not motion.completed: yield
        self.turn_heroActionLeft -= 1
        print("DONE ATTACKING")