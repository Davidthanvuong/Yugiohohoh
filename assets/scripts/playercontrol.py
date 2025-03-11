from pytnk.engine import *

class UserControl(Component):
    pass

class PlayerControl(UserControl):
    e_playerAction: Event = Event()
    # TODO: Có thể thêm dữ liệu vô event, 
    # hoặc để sang nghe thụ động, lấy dữ liệu chủ độngđộng

    def start(self):
        Card.e_placeCard += self.on_placeCard

    def on_placeCard(self, card: Card):
        if card.opponent:
            print("[Player] My turn!")