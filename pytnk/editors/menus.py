from ..header_pygame import *

inspector_width = 300
hierarchy_width = 200
assets_height = 200


class MaingameMenu(Menu):
    def onSizeChanged(self):
        '''🟨Size instead of hitbox scaling?'''
        if Window.devMode:
            reduced = vec(inspector_width + hierarchy_width, assets_height + 32)
            self.go.pos = vec(hierarchy_width, 32)
            self.go.anchor = vec(ZERO)
        else: 
            reduced = vec(ZERO)
            self.go.pos = vec(ZERO)
            self.go.anchor = vec(CENTER)
        size = Window.native - reduced
        ratio = size.x / size.y
        if ratio > Window.defRatio:
            size.x = size.y * Window.defRatio
            #self.go.scale = vec(ONE) * (size.y / Window.defNative[1])
        else:
            size.y = size.x / Window.defRatio
            #self.go.scale = vec(ONE) * (size.x / Window.defNative[0])
        self.go.hitbox = size
        super().onSizeChanged()


    @staticmethod
    def create_default():
        mg = GameObject('Maingame', hitbox=Window.native, createScene=True)
        mg += Image(path="woodfloor.jpg", fit=True)
        mg += Text(text="Maingame Window", font=FontPreset.jetbrains_20)
        MaingameMenu(go=mg)()
        return mg
    
    def update_render(self):
        pos = Mouse.pos.elementwise() * self.go.scene.go.global_scale - self.go.scene.go.global_pos
        #off = (Mouse.pos - self.go.pos - self.go.scene.go.global_pos).elementwise() * self.go.scene.go.global_scale
        Window.Scenes['Maingame'].go.getComponent(Text).text = f"Mouse pos: {pos}\n"



class InspectorMenu(Menu):
    ############
    #      [][]#
    #      [][]#
    ############
    def onSizeChanged(self):
        print("TODO: Make this resizable on the X-axis")
        super().onSizeChanged()


    @staticmethod
    def create_default():
        # Inspector
        # - SpecialField
        # - TransformField
        # - ComponentField
        size = (inspector_width, Window.native[1])
        im = GameObject('Inspector', hitbox=size, anchor=(1, 0), 
                        fit=(False, True), enabled=False, createScene=True)
        
        im += Image(path="gray.png", fit=True)
        im += Text("Inspector Window", font=FontPreset.jetbrains_20)
        im += FlexArray()
        InspectorMenu(go=im, editor='Inspector')()


        # ComponentField
        # - Image
        # - Header: FlexArray
        # - - Icon
        # - - Text
        # - - Fold icon
        # - TypeField[]
        for i in range(5):
            cf = GameObject(hitbox=(0, 200), fit=(True, False), parent=im)
            cf += Image("white.png", fit=True)
            cf += FlexArray()

            hd = GameObject(hitbox=(30, 30), parent=cf)
            hd += Image("cube.png", fit=True)

            tx = GameObject(hitbox=(0, 30), pos=(40, 0), parent=cf)
            tx += Text("Hello component", color=Color.dark, font=FontPreset.jetbrains_20)
            # TypeField
            # X Image
            # - StateColor
            # - Text
            # - Field: FlexArray
            # - - DataField[]
            for j in range(4):
                tf = GameObject(hitbox=(0, 30), fit=(True, False), parent=cf)
                tf += Text("Hello params", color=Color.dark, font=FontPreset.jetbrains_16)

                sc = GameObject(hitbox=(20, 20), anchor=TOPRIGHT, parent=tf)
                sc += Image("dot.png", fit=True)

                ff = GameObject(hitbox=(inspector_width-130, 30), anchor=TOPRIGHT, parent=tf)
                ff += FlexArray(flex=(-1, 0))

                # DataField
                # - Image
                # - Text
                for k in range(2):
                    df = GameObject(hitbox=(ff.hitbox.x//2, 30), anchor=TOPRIGHT, parent=ff)
                    #df += Image(path="white.png", fit=True)
                    df += Text("69420", color=Color.black, font=FontPreset.jetbrains_16)

        # Caret (it'll be wandering around)


        return im




class HierarchyMenu(Menu):
    ############
    #[]        #
    #[]        #
    ############
    hier: 'GameObject'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        GameObject.e_onChangedChilds += self.rebuild_hierarchy
        GameObject.e_onCreateGO += self.rebuild_hierarchy


    def onSizeChanged(self):
        print("TODO: Make this resizable on the X-axis")
        super().onSizeChanged()


    def rebuild_hierarchy(self, go: GameObject):
        if go.sceneName in Window.EditorsName:
            return # Tránh đệ quy: spawn rồi thông báo rồi spawn
        print(f"{go} Will rebuild hierarchy")

        HierarchyMenu.hier = Window.Scenes['Hierarchy'].go
        HierarchyMenu.hier.childs.clear()
        self.buildRecursive(go)

    def buildRecursive(self, go: GameObject, depth = 0):
        for c in go.childs:
            te = GameObject(hitbox=(200, 20), parent=HierarchyMenu.hier)
            te += Image(path="white.png", fit=True)

            cube = GameObject(hitbox=(20, 20), pos=(depth * 20, 0), parent=te)
            cube += Image(path="cube.png", size=(20, 20))
            cube += Text(f"{'  '*depth} {c.name}", color=Color.dark, font=FontPreset.jetbrains)
            self.buildRecursive(c, depth + 1)


    @staticmethod
    def create_default():
        # HierarchyMenu + Title
        # - Searchbox
        # - Elements[]

        size = (hierarchy_width, Window.native[1])
        hierarchy = GameObject('Hierarchy', hitbox=size, anchor=(0, 0), 
                        fit=(False, True), enabled=False, createScene=True)
        hierarchy += Image(path="gray.png", fit=True)
        hierarchy += Text("Hierarchy Window", font=FontPreset.jetbrains_20)
        hierarchy += FlexArray()
        HierarchyMenu(go=hierarchy, editor='Hierarchy')()

        # Searchbox
        sbox = GameObject(hitbox=(200, 20), parent=hierarchy)
        sbox += Image(path="white.png", fit=True)
        
        search = GameObject(hitbox=(20, 20), parent=sbox)
        search += Image(path="search_massive.png", fit=True)
        search += Text(text="   Insert text here :)", color=Color.black)

        # Có thể di chuyển sang các file hardcode
        if False and not GameObject.existPrefab("TransformEntry"):
            te = GameObject(hitbox=(200, 20), parent=hierarchy)
            te += Image(path="white.png", fit=True)

            cube = GameObject(hitbox=(20, 20), parent=te)
            cube += Image(path="cube.png", size=(20, 20))
            cube += Text("   The Cube Theorist", color=Color.dark, font=FontPreset.jetbrains)

            te.saveSelf(delete=True)

        # TransformEntry
        # for i in range(10):
        #     # TransformEntry
        #     # - Cube
        #     # - Name
        #     te = GameObject(hitbox=(200, 20), parent=hierarchy)
        #     te += Image(path="white.png", fit=True)

        #     cube = GameObject(hitbox=(20, 20), parent=te)
        #     cube += Image(path="cube.png", size=(20, 20))
        #     cube += Text("   The Cube Theorist", color=Color.dark, font=FontPreset.jetbrains)

        #     indent = rint(0, 3) * 10
        return hierarchy



import os
from random import choice
path = "assets\\images\\card"
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


class AssetsMenu(Menu):
    ############
    #          #
    # [][][]   #
    ############
    def __init__(self, **kwargs):
        self.mgGo = None
        super().__init__(**kwargs)

    def onSizeChanged(self):
        if not self.mgGo:
            self.mgGo = Window.Scenes['Maingame'].go
        if Window.devMode:
            self.go.hitbox.x = Window.native[0] - inspector_width - hierarchy_width
            self.go.hitbox.y = Window.native[1] - self.mgGo.hitbox.y - 32
        super().onSizeChanged()


    @staticmethod
    def create_default():
        # AssetsMenu
        # - Title: FlexArray
        # - - Tab2
        # - - Tab3
        # - - Title path
        # - - Searchbox
        # - Assets: FlexArray
        # - - AssetCell
        size = (Window.native[0] - inspector_width - hierarchy_width, assets_height)
        pos = (hierarchy_width, 0)
        al = GameObject('AssetsLib', pos, hitbox=size, anchor=(0, 1),
                        enabled=False, createScene=True)
        al += Image(path="gray.png", fit=True)
        al += Text("Assetslib Window", font=FontPreset.jetbrains_20)
        AssetsMenu(go=al, editor='AssetsLib')()

        # Title path
        ttp = GameObject(hitbox=(0, 300), pivot=TOPRIGHT, pos=(0, 20), anchor=TOPRIGHT, parent=al)
        ttp += Text("Images/Something/Test", font=FontPreset.jetbrains)
        
        # Searchbox
        sbox = GameObject(hitbox=(200, 20), anchor=TOPRIGHT, parent=al)
        sbox += Image(path="white.png", fit=True)
        
        search = GameObject(hitbox=(20, 20), parent=sbox)
        search += Image(path="search_massive.png", fit=True)
        search += Text(text="   Insert text here :)", color=Color.gray)

        # Assets Array
        asr = GameObject(hitbox=(200, 500), fit=(True, False), pos=(0, 50), parent=al)
        asr += FlexArray(flex=(1, 1), space=10)

        # AssetCell
        # - Image backpane
        # - Image
        # - Text
        # - Version text

        for i in range(20):
            # Backpane
            cell = GameObject(hitbox=(140, 140), parent=asr)
            cell += Image(path="white.png", fit=True)
            #cell.getComponent(Image).cache.texture.set_alpha(150)
            
            # Image
            img = GameObject(hitbox=(80, 120), anchor=CENTER, parent=cell)
            imgpath = f"card\\{choice(files)}"
            img += Image(path=imgpath, fit=True)

            # Version text
            ver = GameObject(hitbox=(0, 20), parent=cell, pivot=TOPRIGHT, anchor=TOPRIGHT)
            ver += Text("x1 ", color=Color.black)

            # Black column
            blc = GameObject(hitbox=(140, 20), anchor=BOTTOMLEFT, parent=cell)
            blc += Image(path="gray.png")
            #gg.cache.texture.set_alpha(100)

            # Bottom text
            btx = GameObject(hitbox=(0, 20), parent=cell, pivot=MIDTOP, anchor=MIDBOTTOM)
            btx += Text("Naming name", color=Color.black)

        return al