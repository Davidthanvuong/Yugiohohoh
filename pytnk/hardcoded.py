from .engine import *

class Hardcoded:
    @staticmethod
    def create_all():
        '''Tạo tất cả các prefab cần thiết'''
        Hardcoded.create_cards()

        Hardcoded.create_introScene()
        Hardcoded.create_loadingScene()
        Hardcoded.create_maingameScene()

    @staticmethod
    def create_introScene():
        '''Intro bao gồm:
        - Chữ nhảy và logo game
        - Danh sách tác giả
        '''
        intro = GameObject('Intro Scene', pos=App.center) + Image('background\\yugioh_bg.jpg', App.native)
        logo = GameObject('Logo', intro) + Image('icon\\pytnk.png', (200, 200))
        brand = GameObject('Text', intro) + Text('PyTNK Game Engine', color=Color.black, size=40)
        intro += IntroSeq(animTime = 1.0)

        author = GameObject('Author', intro) + Text('Author here...', color=Color.black, size=40)
        author.transf.pos.y = 200

        for i in range(4):
            dev = GameObject(f'Dev {i}', author, pos=((i - 1.5) * 160, 100)) + Image("icon\\white.png", size=(128, 128))

        intro.savePrefab(delete=True)

    @staticmethod
    def create_maingameScene():
        '''Maingame (tạm thời):
        - Carddeck của 2 người chơi
        '''
        main = GameObject('Maingame Scene', pivot=TOPLEFT)
        main += Image('background\\woodfloor.jpg', (App.native[0], App.native[1] - 200))
        plank = GameObject('Board', main, pos=(0, App.native[1] - 200), pivot=TOPLEFT)
        plank += Image('background\\wood.jpg', (App.native[0], 200))

        my_place = GameObject('My Place', main, pos=(100, 200), pivot=TOPLEFT)
        oppo_place = GameObject('Opponent Place', main, pos=(App.native[0] - 100, 200), pivot=TOPRIGHT)

        deck = GameObject('CardDeck', main, pos=(App.center[0], App.native[1] - 100)) + CardDeck(my_place)
        oppo_deck = GameObject('CardDeck 2', main, pos=(App.center[0], -50), rot=180) + CardDeck(oppo_place, opponent=True)

        main.savePrefab(delete=True)

    @staticmethod
    def create_loadingScene():
        '''Cứ load thôi :v'''
        loading = GameObject('Loading Scene', pivot=TOPLEFT) + Image('background\\grass2.jpg', App.native) + LoadingSeq(animTime = 1.5)

        loading.savePrefab(delete=True)

    @staticmethod
    def create_cards():
        card = GameObject('Card', pos=(0, 300))
        card += Image(f"card_back.png", (150, 240), overrideHitbox=True)
        card += Card()
        
        card.savePrefab(delete=True)

        slot = GameObject('Card Placeholder')
        slot += Image("card_back.png", (120, 80), overrideHitbox=True)
        slot += CardPlaceholder()

        slot.savePrefab(delete=True)