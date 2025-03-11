# from pytnk.engine import *

# class BattleManager(Component):
#     '''Control, liên kết event giữa player với opponent'''

#     # e_playerTurn: Event = Event()
#     # e_opponentTurn: Event = Event()
    
#     def after_init(self):
#         popup = GameObject('Popup', self.go, pos=App.center)
#         popup += Shader_PopupText()
#         self.com_popup = popup.getComponent(Shader_PopupText)
#         Card.e_placeCard += self.on_placeCard

#     def fight(self):        
#         self.com_popup.playText('Battle start!')

#         main = self.go
#         my_place = GameObject('My Place', main, pos=(100, 200), anchor=TOPLEFT)
#         oppo_place = GameObject('Opponent Place', main, pos=(App.native[0] - 100, 200), anchor=TOPRIGHT)

#         deck = GameObject('CardDeck', main, pos=(App.center[0], App.native[1] - 100)) + CardDeck(my_place)
#         oppo_deck = GameObject('CardDeck 2', main, pos=(App.center[0], -50), rot=180) + CardDeck(oppo_place, opponent=True)

#     def on_placeCard(self, card: Card):
#         if not card.opponent:
#             # self.e_opponentTurn.notify()
#             self.com_popup.playText('Opponent turn!')
#         else:
#             # self.e_playerTurn.notify()
#             self.com_popup.playText('Player turn!')