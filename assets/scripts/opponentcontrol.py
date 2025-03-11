from pytnk.engine import *

class OpponentControl(Component):
    '''Có thể được điều khiển bởi network hay bot'''
    
    @staticmethod
    def create_default(headStart = False):
        oppon = GameObject('Opponent')
        deck = CardDeck.create_default(oppon, True)

        slots = GameObject('Slot Holder', oppon, pos=(App.native[0] - 100, 200))
        for y in range(5):
            for x in range(3):
                CardSlot.create_default(slots, x, y, True)

        oppon += OpponentControl(deck.getComponent(CardDeck), headStart)
        slots.unscope()
        return oppon
    
    def __init__(self, deck: CardDeck, headStart = False):
        Card.e_placeCard += self.on_placeCard
        Monster.e_attacked += self.on_attack
        self.selecting: No[Card] = None
        self.selMotion: Motion
        self.myTurn = headStart
        self.deck = deck

    def pick_algorithm(self):
        '''Tạm thời bốc ngẫu nhiên, sorry :D'''
        thought = choice(self.deck.go.childs)
        return thought.getComponent(Card)

    def update_logic(self):
        if self.myTurn and self.selecting is None:
            print("[Opponent] Selecting card...")
            card = self.pick_algorithm()
            card.on_startDrag(controlled=True)  # Drag nhưng kiểm soát bởi *Artificial Stupidity*
            self.selecting = card
            rand_pos = (rint(App.center[0] + 100, App.native[0] - 100), rint(300, App.native[1] - 300))
            self.selMotion = Motion.ease_in(card.transf.g_pos, rand_pos, 0.6)
        elif self.selecting is None: return

        self.selecting.transf.pos = self.selMotion.value
        if self.selMotion.completed:
            self.selecting.on_stopDrag()
            self.selecting = None
            self.myTurn = False

    def on_placeCard(self, card: Card):
        if not card.opponent:
            print("[Opponent] My turn!")
            self.myTurn = True

    def on_attack(self, mon: Monster):
        if not mon.opponent:
            print(f"[Opponent] You attacked me! {mon.go.name}")
            self.myTurn = True