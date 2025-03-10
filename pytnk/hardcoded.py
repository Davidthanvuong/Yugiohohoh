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
        main = GameObject('Maingame Scene', anchor=TOPLEFT)
        main += Image('background\\woodfloor.jpg', (App.native[0], App.native[1] - 200))

        human1 = GameObject('Human 1', main, pos=(App.center[0], -250), scale=(3, 3), rot=180) + Image("human.png", size=(500, 180))
        human2 = GameObject('Human 2', main, pos=(App.center[0], App.native[1] + 250), scale=(3, 3)) + Image("human.png", size=(500, 180))
        
        plank = GameObject('Board', main, pos=(0, App.native[1] - 200), anchor=TOPLEFT, scale=(1, 0))
        plank += Image('background\\wood.jpg', (App.native[0], 200))

        my_place = GameObject('My Place', main, pos=(100, 200), anchor=TOPLEFT)
        oppo_place = GameObject('Opponent Place', main, pos=(App.native[0] - 100, 200), anchor=TOPRIGHT)

        deck = GameObject('CardDeck', main, pos=(App.center[0], App.native[1] - 100), startEnabled=False) + CardDeck(my_place)
        oppo_deck = GameObject('CardDeck 2', main, pos=(App.center[0], -50), rot=180, startEnabled=False) + CardDeck(oppo_place, opponent=True)

        main += MaingameSeq(plank, deck, oppo_deck)
        main.savePrefab(delete=True)

    @staticmethod
    def create_loadingScene():
        '''Cứ load thôi :v'''
        loading = GameObject('Loading Scene', anchor=TOPLEFT)
        loading += Image('background\\willsmith.png', App.native)
        loading += LoadingSeq(animTime = 1.5)

        loading.savePrefab(delete=True)

    @staticmethod
    def create_cards():
        card = GameObject('Card', pos=(0, 300))
        card += Image(f"card_back.png", (150, 240), overrideHitbox=True)
        card += Card()
        
        card.savePrefab(delete=True)

        slot = GameObject('Card Placeholder')
        slot += Image("card_back.png", (120, 80), overrideHitbox=True)
        slot += CardSpot()

        slot.savePrefab(delete=True)