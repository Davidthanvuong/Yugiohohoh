from pytnk.engine import *

class UserControl(Component):
    pass

class PlayerControl(UserControl):
    e_playerAction: Event = Event()
    # TODO: Có thể thêm dữ liệu vô event, 
    # hoặc để sang nghe thụ động, lấy dữ liệu chủ độngđộng

    @staticmethod
    def create_default():
        player = GameObject('Player')
        deck = CardDeck.create_default()

        slots = GameObject('Slot Holder', player, pos=(100, 200))
        for y in range(5):
            for x in range(3):
                CardSlot.create_default(slots, x, y)

        player += PlayerControl()
        slots.unscope()
        return player

    def after_init(self):
        Card.e_placeCard += self.on_placeCard
        Monster.e_attacked += self.on_attack

    def on_placeCard(self, card: Card):
        if card.opponent:
            print("[Player] My turn!")

    def on_attack(self, monster: Monster):
        if monster.opponent:
            print(f"[Player] You attacked me! {monster.go.name}")