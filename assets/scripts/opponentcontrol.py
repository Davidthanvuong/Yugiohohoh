from pytnk.engine import *

class OpponentControl(Component):
    '''Có thể được điều khiển bởi network hay bot'''
    
    def start(self):
        Card.e_placeCard += self.on_placeCard

    def on_placeCard(self, card: Card):
        if not card.opponent:
            print("[Opponent] My turn!")