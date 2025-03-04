from pytnk.header_pygame import *
import math

if __name__ == '__main__':
    pg.init()
    screen = Game()
    go = screen.tf
    Maingame()
    if ALLOW_DEVELOPER:
        load_editors()

    # Chữa cháy demo (do Engine đang làm)
    deck_tf = Transform('Card Deck', pos=(200, Window.native[1]-200), hitbox=(600, 200), pivot=(0, 0.5), parent=Game.maingameTf, rootname='Maingame')
    Image(bind=deck_tf, path="white.png", fit=True, standalone=True)
    FlexArray(interactable=False, bind=deck_tf, axis='x', use_crowding=True)

    deck = CardDeck(bind=deck_tf)
    for i in range(10):
        Transform.getPrefab('Card', parent=deck_tf)

    while Window.running:

        go.update_logic()   # Cập nhật từng components object
        go.update_click()   # Theo đúng trình tự load
        go.update_render()

        screen.windowHandler()  # Xong mới update và handle màn hình

    pg.quit()