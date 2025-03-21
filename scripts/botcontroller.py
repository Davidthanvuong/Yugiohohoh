from pytnk.engine import *

class BotController(Controller):
    '''Class này để bot (không phải AI) chạy'''
    def build(self, *a):
        return super().build(name="Bot", *a)

    def __init__(self, *a):
        super().__init__(*a)
        self.rightSide = True
        self.isPlayer = False
        self.myTurn = False
        self.action: No[Generator] = None
        self.mainState.e_begin += self.hear_start_drawPhase

    def update_logic(self):
        super().update_logic()
        if not self.myTurn: return
        
        if self.action is not None:
            try: next(self.action)
            except StopIteration:
                self.action = None
        else: self.pick_action()

    def hear_start_drawPhase(self):
        print("[Opponent] MY TURN")
        self.myTurn = True
        self.attacking = False

    
    def pick_action(self):
        actions: list[Callable] = []
        weights: list[float] = []

        actions.append(self.act_pickRandomCard)
        weights.append(self.eval_pickRandomCard())

        actions.append(self.act_quickAttack)
        weights.append(self.eval_quickAttack())

        if sum(weights) == 0:
            # print("[Opponent] Hết cứu. Hết nước đi.")
            self.myTurn = False
            return LinearStateMachine.next_state()
        
        action = random.choices(actions, weights, k=1)[0]
        self.action = action()

    def eval_pickRandomCard(self):
        if (self.placeCard_left < 0) or (len(self.deck.go.childs) == 0):
            return 0
        return 0.8
    
    def act_pickRandomCard(self):
        # print("[Opponent] Selecting card...")
        card = random.choice(self.deck.go.childs).getComponent(Card)
        
        card.on_startDrag(controlled=True)  # Drag nhưng kiểm soát bởi *Artificial Stupidity*
        cardtf = card.transf
        placeSlot = self.choose_frontSlot(EMPTY)
        motion = Motion.ease_in(card.transf.g_pos, placeSlot.transf.g_pos, 0.8)

        while not motion.completed:
            cardtf.pos = motion.value
            yield

        CardSlot.selecting = placeSlot
        if card.on_stopDrag():
            self.placeCard_left -= 1
        CardSlot.selecting = None

    def eval_quickAttack(self):
        anyEmpty = (self.isEmpty(FRONT)) or (self.opponent.isEmpty(FRONT))
        if (self.quickAction_left <= 0) or anyEmpty:
            return 0
        return 1
    
    def act_quickAttack(self):
        # print("[Opponent] Selecting attack...")
        self.attacking = True
        atk = cast(Monster, self.choose_frontSlot(OCCUPIED).occupy)
        targetSlot = self.opponent.choose_frontSlot(OCCUPIED)

        atk.setTarget(targetSlot)
        atk.start_attack()
        atk.e_attackFinished *= self.act_quickFinished

        while not self.attacking: yield
        self.quickAction_left -= 1
        # print("DONE ATTACKING")

    def act_quickFinished(self):
        self.attacking = True