from pytnk.engine import *

class BattleController(Component):
    '''Control, liên kết event giữa player với opponent'''

    e_playerTurn: Event = Event()
    e_opponentTurn: Event = Event()
    
    def __init__(self):
        pass

    def start(self):
        pass