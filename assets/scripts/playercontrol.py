from pytnk.engine import *

class UserControl(Component):
    e_endPhase: Event['UserControl'] = Event()
    e_startPhase: Event['UserControl'] = Event()

    def __init__(self, isOpponent = False):
        self.turn_cardPlaceLeft = 0
        self.turn_heroActionLeft = 0
        self.myTurn = False
        self.isOpponent = isOpponent
        self.deck: CardDeck
        UserControl.e_endPhase += self.listen_endPhase

    def startPhase(self):
        self.turn_cardPlaceLeft = 3
        self.turn_heroActionLeft = 1
        self.myTurn = True
        UserControl.e_startPhase.notify(self)

    def endPhase(self):
        self.turn_cardPlaceLeft = 0
        self.turn_heroActionLeft = 0
        self.myTurn = False
        UserControl.e_endPhase.notify(self)

    def listen_endPhase(self, user: 'UserControl'):
        if user.isOpponent != self.isOpponent:
            print(f"Someone stopped and {self.go.name} starting")
            self.startPhase()

    def drawPhase(self):
        Card.create(self.deck)
        Card.create(self.deck)

class PlayerControl(UserControl):
    e_playerAction: Event = Event()
    # TODO: Có thể thêm dữ liệu vô event, 
    # hoặc để sang nghe thụ động, lấy dữ liệu chủ độngđộng

    @staticmethod
    def create(parent: GameObject):
        # UserControl
        # - CardDeck
        # - - Cards[]
        # - CardSlot
        # - - Slots[]
        player = GameObject('Player', parent)
        user = player.addComponent(PlayerControl())
        deck = CardDeck.create(user)

        slots = GameObject('Card Slots', player, pos=(100, 200))
        for x in range(3):
            for y in range(5):
                CardSlot.create(slots, user, x, y)

        endphase = EndPhaseButton.create(user)

        return player

    def __init__(self):
        super().__init__(False)

        # Card.e_placeCard += self.on_placeCard
        # Monster.e_attacked += self.on_heroAttack

    # def on_placeCard(self, card: Card):
    #     if not card.isOpponent:
    #         self.turn_cardSummonLeft -= 1
    #         print("[Player] Card Summoned")

    # def on_heroAttack(self, monster: Monster):
    #     if not monster.opponent:
    #         self.turn_heroAttackLeft -= 1
    #         print("[Player] Hero Attacked")

    # def on_spellUsed(self):
    #     # TODO: Spell card
    #     print("[TODO] NOT IMPLEMENTED")
    #     return
    #     self.turn_spellLeft -= 1



class EndPhaseButton(IClickable):
    @staticmethod
    def create(user: UserControl):
        bottom = (App.native[0] - 20, App.native[1] - 50) 

        button = GameObject('End Phase Button', user.go, pos=bottom, anchor=BOTTOMRIGHT, startEnabled=False)
        button += Image("icon\\white.png", (200, 40), overrideHitbox=True)
        button += Text("End", size=20, color=Color.black)
        button += EndPhaseButton(user)
        return button

    def __init__(self, user: UserControl):
        super().__init__()
        self.user = user
        UserControl.e_startPhase += self.reEnable

    def reEnable(self, user: UserControl):
        if isinstance(user, PlayerControl):
            self.go.enabled = True
            print("Bonjour, nút bấm kết thúc lượt đã trở lại")

    def after_init(self):
        self.com_image = self.go.getComponent(Image)
        self.com_text = self.go.getComponent(Text)

    def update_logic(self):
        additional = f"({self.user.turn_cardPlaceLeft}, {self.user.turn_heroActionLeft})"
        self.com_text.text = "End Phase " + additional

    def on_startClick(self):
        self.user.endPhase()
        self.go.enabled = False