from pytnk.header_pygame import *
import random, os


def deadline_demo():
    '''Chữa cháy demo (do Engine đang làm mà thầy kêu review)'''

    deck_tf = Transform('Card Deck', pos=(200, Window.native[1]-200), hitbox=(800, 200), pivot=(0, 0.5), parent=Game.maingameTf, rootname='Maingame')
    #Image(bind=deck_tf, path="white.png", fit=True, standalone=True)
    FlexArray(interactable=False, bind=deck_tf, axis='x', use_crowding=True)

    deck = CardDeck(bind=deck_tf)
    path = "assets\\images\\summoncard"
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    print(files)
    for i in range(20):
        card = Transform.getPrefab('Card', parent=deck_tf)
        img = card.getComponent(Image)
        img.cache = SharedImage.fetch(f"summoncard\\{random.choice(files)}")

if __name__ == '__main__':
    pg.init()
    screen = Game()
    go = screen.tf
    Maingame()
    if ALLOW_DEVELOPER:
        load_editors()

    deadline_demo()

    while Window.running:

        go.update_logic()   # Cập nhật từng components object
        go.update_click()   # Theo đúng trình tự load
        go.update_render()

        screen.windowHandler()  # Xong mới update và handle màn hình

    pg.quit()