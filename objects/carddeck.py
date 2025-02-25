from importer.gobj import *
from objects.card import Card

class CardDeck(Transform):
    def __init__(self, deck_width: float = 1000, back: bool = False, **kwargs):
        super().__init__(
            imgpath="white.png", imgsize=vec(deck_width, 300), **kwargs)
        self.back = back
        self.cards: list[Card] = []
        self.amount = 0
        self.deck_width = deck_width
        for _ in range(10):
            self.insertCard()

    def insertCard(self, index = 0):
        self.cards.insert(index, Card(parent=self, role=('back' if self.back else 'empty')))
        self.amount += 1

    def deployCard(self, index):
        self.cards.pop(index)

    def update(self):
        render(self)
        
        space = self.deck_width / (self.amount + 1)
        i, back = 0, 0
        while i < self.amount: # Vector xóa phần tử trong O(1) :)
            card = self.cards[i]
            if card.mark_for_delete:
                self.amount -= 1
                back += 1
                space = self.deck_width / (self.amount + 1)
            if back != 0 and i + back < self.amount:
                self.cards[i] = self.cards[i+back]

            card.pos.x = space * i + self.cards[0].imgsize.x / 2
            card.update()
            i += 1