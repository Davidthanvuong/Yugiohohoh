from .engine import *

class Maingame(Component):
    @staticmethod
    def create_default(opponent_startFirst = False, **kw):
        game = GameObject('Maingame Scene', toScope=True)
        game += Maingame(**kw)

        player = PlayerControl.create_default()
        oppon = OpponentControl.create_default(opponent_startFirst)
                            
        game.unscope()
        return game