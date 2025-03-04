from pytnk.header_pygame import *
from pytnk.world import World

#   _   _        _  _                                  _      _  _ 
#  | | | |      | || |                                | |    | || |
#  | |_| |  ___ | || |  ___     __      __ ___   _ __ | |  __| || |
#  |  _  | / _ \| || | / _ \    \ \ /\ / // _ \ | '__|| | / _` || |
#  | | | ||  __/| || || (_) |_   \ V  V /| (_) || |   | || (_| ||_|
#  \_| |_/ \___||_||_| \___/( )   \_/\_/  \___/ |_|   |_| \__,_|(_)
#                           |/                                     

if __name__ == '__main__': 
    world = Transform("World")
    Image(attach=world, path="woodfloor.jpg", size=NATIVE)
    com_world = World(attach=world)

    if True or not Transform.exist_prefab("DataField"):
        tf = Transform("DataField", pivot=(0, 0.5), 
                            hitbox=(100, 22), simple=True)
        Image(attach=tf, path="white.png", fit=True, standalone=True)
        Text(attach=tf, text="Debug", color=colormap['dark'])
        DataField(attach=tf)
        tf.saveSelf(delete=True) # Lưu bằng pickle

    if True or not Transform.exist_prefab("DataTask"):
        tf2 = Transform("DataTask", pos=(700, 100), pivot=ZERO,
                        hitbox=(300, 26), simple=True)
        Image(attach=tf2, path="white.png", size=(300, 26), standalone=True)
        Text(attach=tf2, color=colormap['dark'])
        DataTask(tf2, "pos", attach=tf2)
        tf2.saveSelf(delete=True)

    if True or not Transform.exist_prefab("ToggleHeader"):
        tf3 = Transform("ToggleHeader", pos=(1000, 100), pivot=ZERO,
                        hitbox=(310, 500), simple=True)
        Image(attach=tf2, path="white.png", size=(310, 500), standalone=True)
        FlexibleMenu(space=2, foldable=False, attach=tf3)
        ToggleHeader(tf3, attach=tf3)
        tf3.saveSelf(delete=True)

    editor = Transform("Editor")
    Editor(attach=editor)
    Transform.getPrefab("ToggleHeader", editor, vec(800, 100))
    #editor.enable = False

    while World.RUNNING:
        world.update_logic()

        # for obj in world:
        #     obj.angle += 1

        world.update_click()
        world.update_render()

        editor.update_logic()
        editor.update_click()
        editor.update_render()
        com_world.windowHandler()

    #world_tf.save()
    pg.quit()
