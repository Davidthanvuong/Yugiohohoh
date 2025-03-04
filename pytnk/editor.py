from .header_pygame import *

mg_size = vec(0.66, 0.66).elementwise() * vec(Window.native)
mg_pos = vec(250, 32)

def load_editors():
    #mg = Transform.roots['Maingame'][0]
    InspectorMenu() 
    HierarchyMenu()
    AssetsMenu()

#todo: EditorMenu base class



class ComponentField(FlexArray):
    '''Hiển thị danh sách các TypeField - Dữ liệu trong Component'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.com_text = self.tf.getComponent(Text)

    
    def on_startClick(self):
        print(f"I am {self.tf.name}")



class InspectorMenu(Component):
    inst: 'InspectorMenu'

    def __init__(self, **kwargs):
        InspectorMenu.inst = self
        size = (Window.native[0] - mg_size.x - mg_pos.x, Window.native[1])

        tf = Transform('Inspector',
                pos=(Window.native[0] - size[0], 0), 
                hitbox=size, 
                parent=Game.inst.tf, 
                enabled=False, 
                rootname='Inspector')
        tf.root = Transform.roots['Inspector'] = (tf, pg.Surface(tf.hitbox, pg.SRCALPHA))
        img = Image(bind=tf, path="white.png", fit=True, standalone=True)
        FlexArray(interactable=False, bind=tf)
        img.cache.texture.fill(colormap['dark'])
        Game.editorsTf.append(tf)

        txt = Transform('Text', hitbox=(size[0], 50), parent=tf)
        Text(bind=txt, text="Inspector", preset='jetbrains_big')


        # Chữa cháy start cũ do start mới clean hơn mà chưa kịp implement
        if True or not Transform.existPrefab('Input Field'):
            ipf = Transform('Input Field', ZERO, ZERO, (100, 22), parent=tf)
            Image(bind=ipf, path="white.png", fit=True, standalone=True)
            Text(bind=ipf, text="69420", color=(0, 0, 0))
            InputField(bind=ipf, value=69420)

            ipf.saveSelf(delete=True)


        if True or not Transform.existPrefab('Type Field'):
            df = Transform('Type Field', ZERO, ZERO, (size[0], 22), parent=tf)
            Image(bind=df, path="white.png", fit=True, standalone=True)
            #ComponentField(bind=df)
            FlexArray(interactable=False, bind=df, use_crowding=True, axis='x')

            tt = Transform('Text', ZERO, ZERO, (150, 22), parent=df)
            Text(bind=tt, text='Data example', color=(0, 0, 0))
            for i in range(3):
                Transform.getPrefab('Input Field', parent=df)

            df.saveSelf(delete=True)


        if True or not Transform.existPrefab('Component Field'):
            cf = Transform('Component Field', ZERO, ZERO, (size[0], 35), parent=tf)
            img = Image(bind=cf, path="white.png", fit=True, standalone=True, indent=0)
            Text(bind=cf, text='Hello, world! I am Component Field', color=(0, 0, 0))

            #arr = Transform('Type Array', (0, 30), ZERO, (0, 0), cf)
            FlexArray(bind=cf, includeSelf=True, foldable=True)
            for i in range(12):
                Transform.getPrefab('Type Field', parent=cf)
            cf.saveSelf(delete=True)


        for i in range(3):
            Transform.getPrefab('Component Field', parent=tf)
            img.cache.texture.fill(colormap['gray'])

        super().__init__(bind=tf, **kwargs)




class HierarchyMenu(Component):
    inst: 'HierarchyMenu'

    def __init__(self, **kwargs):
        HierarchyMenu.inst = self
        size = (mg_pos.x, Window.native[1])

        tf = Transform('Hierarchy', (0, 0), (0, 0), size, Game.inst.tf, enabled=False)
        tf.root = Transform.roots['Hierarchy'] = (tf, pg.Surface(tf.hitbox, pg.SRCALPHA))
        img = Image(bind=tf, path="white.png", fit=True, standalone=True)
        img.cache.texture.fill(colormap['dark'])

        txt = Transform('Text', hitbox=(size[0], 50), parent=tf)
        Text(bind=txt, text="Hierarchy", preset='jetbrains_big')

        Game.editorsTf.append(tf)

        super().__init__(bind=tf, **kwargs)




class AssetsMenu(Component):
    inst: 'AssetsMenu'

    def __init__(self, **kwargs):
        AssetsMenu.inst = self
        size = (mg_size.x, Window.native[1] - mg_size.y)

        tf = Transform('Assets', (mg_pos.x, mg_pos.y + mg_size.y), (0, 0), size, Game.inst.tf, enabled=False)
        tf.root = Transform.roots['Assets'] = (tf, pg.Surface(tf.hitbox, pg.SRCALPHA))
        img = Image(bind=tf, path="white.png", fit=True, standalone=True)
        img.cache.texture.fill(colormap['dark'])

        txt = Transform('Text', hitbox=(size[0], 50), parent=tf)
        Text(bind=txt, text="Assetslib", preset='jetbrains_big')

        Game.editorsTf.append(tf)

        super().__init__(bind=tf, **kwargs)