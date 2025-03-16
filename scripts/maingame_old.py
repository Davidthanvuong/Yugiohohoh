from pytnk.engine import *

class Controller:
    '''Một cách để fix circular import đó là dồn tất cả dependencies vô chung 1 thằng'''
    def __init__(self, rightSide: bool, isPlayer: bool):
        self.rightSide = rightSide                  # Container \/
        self.isPlayer = isPlayer
        self.root: GameObject
        self.opponent: 'Controller'
        self.controller: 'Controller'
        self.cardDeck: 'CardDeck'
        self.slots: list['CardSlot']
        self.mons: list['Monster']
        self.king: 'Monster'

        self.turn_placeLeft: int = 3                # Runtime \/
        self.turn_specialLeft: int = 1
        self.hovering_slot: No['CardSlot'] = None
        self.dragging_slot: No['CardSlot'] = None
        



# class CardSlot(IClickable):
#     def build(self, side: int, x: int, y: int):
#         forward = -1 if self. else 1
#         slot = Image("card_back.png", (120, 80), True).build(parent=self.user.go,
#                 pos=(forward * x * 150, y * 120))
#         return slot.addComponent(self)

#     def __init__(self, user: UserState, myId: int):
#         super().__init__(draggable=True)
#         self.user = user
#         self.myId = myId
#         self.state = user.state


# class Monster(Component):
#     pass


class Maingame(Component):
    def build(self):
        mg = Image('background\\woodfloor.jpg', (App.native[0], App.native[1] - 200)).build(anchor=TOPLEFT).scope()
        plank = Image('background\\wood.jpg', (App.native[0], 200)).build(pos=(0, App.center[1] - 100))

        self.user1 = PlayerController().build()
        self.user2 = EnemyController().build()

        return mg.unscope() + self # Nên unscope không?

    @classmethod
    def endPhase(cls, user: 'Controller'):
        pass



class Controller(Component):
    def __init__(self):
        self.side: int
        self.state = Controller()

    def endPhase(self):
        self.state.turn_placeLeft = 0
        self.state.turn_specialLeft = 0
        


class PlayerController(Controller):
    def build(self):
        player = GameObject('Player').scope()
        self.state.slots = [CardSlot(self, x*5 + y).build(PLAYER, x, y) for x in range(3) for y in range(5)]

        player.unscope()
        return player + PlayerController()

    def __init__(self):
        self.side: int = PLAYER


class EnemyController(Controller):
    def build(self):
        oppo = GameObject('Opponent').scope()
        self.state.slots = [CardSlot(self, x*5 + y).build(OPPONENT, x, y) for x in range(3) for y in range(5)]

        oppo.unscope()
        return oppo + EnemyController()
    
    def __init__(self):
        self.side: int = OPPONENT