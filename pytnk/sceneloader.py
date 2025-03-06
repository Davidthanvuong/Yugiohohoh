from .header_pygame import *

class SceneLoader:
    '''Dùng trong việc tạo các scene cần thiết
    🟨 Sau này có thể sẽ dời qua làm Scene thẳng trong PyTNK luôn
    '''
    
    @staticmethod
    def create_introScene():
        '''Hiện logo và sản phẩm trên intro'''
        print("Intro")

    
    @staticmethod
    def create_startScene():
        '''Màn hình bắt đầu game'''
        print("Start Screen")


    @staticmethod
    def create_loadingScene():
        '''Load game ngầu tí'''
        print("Loading screen")
        

    @staticmethod
    def create_maingameScene():
        MaingameMenu.create_default()

        deck = GameObject(anchor=BOTTOMLEFT, pos=(50, 0), hitbox=(600, 200))
        deck += Image("white.png", fit=True)
        deck += FlexArray(flex=(1, 0))
        CardDeck(go=deck)()

        print(deck.parent)


    @staticmethod
    def create_editorScenes():
        '''✅Todo: điều chỉnh theo anchor'''
        InspectorMenu.create_default()
        AssetsMenu.create_default()
        HierarchyMenu.create_default()


        # mg_size = vec(0.66, 0.66).elementwise() * vec(Window.native)
        # mg_pos = vec(200, 32)
        # hierarchy_width = 200
        # inspector_width = 400

        # def inspectorMenu():
        #     ############
        #     #      [][]#
        #     #      [][]#
        #     ############
        #     size = (inspector_width, Window.native[1])
        #     #pos = (Window.native[0] - size[0], 0)
        #     im = GameObject('Inspector', hitbox=size, anchor=(1, 0), 
        #                     fit=(False, True), enabled=False, createScene=True)
        #     im += Image(path="grass.jpg", fit=True)
        #     im += Text("Inspector Window", font=FontPreset.jetbrains_big)

        #     #im += FlexArray(interactable=False)
        #     Window.EditorsName.append('Inspector')

        # def assetMenu():
        #     ############
        #     #          #
        #     # [][][]   #
        #     ############
        #     size = (Window.native[0] - hierarchy_width - inspector_width, Window.native[1] - inspector_width)
        #     pos = (hierarchy_width, 0)
        #     al = GameObject('AssetsLib', pos, hitbox=size, anchor=(0, 1), parent=Window.Scenes['MiddleEditor'].go,
        #                     fit=(True, False), enabled=False, createScene=True)
        #     al += Image(path="grass2.jpg", fit=True)
        #     al += Text("Assetslib Window", font=FontPreset.jetbrains_big)
        #     Window.EditorsName.append('AssetsLib')

        # def hierarchyMenu():
        #     ############
        #     #[]        #
        #     #[]        #
        #     ############
        #     size = (hierarchy_width, Window.native[1])
        #     hm = GameObject('Hierarchy', hitbox=size, anchor=(0, 0), 
        #                     fit=(False, True), enabled=False, createScene=True)
        #     hm += Image(path="grass.jpg", fit=True)
        #     hm += Text("Hierarchy Window", font=FontPreset.jetbrains_big)
        #     Window.EditorsName.append('Hierarchy')

        
        # assetMenu()
        # hierarchyMenu()
        # inspectorMenu()