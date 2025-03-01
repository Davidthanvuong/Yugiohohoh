from pytnk.header_pygame import *
from pytnk.world import World
import time

def new_world_spinning() -> Transform:
    world_tf = Transform("World")
    dist = 200
    World(attach=world_tf)
    for y in range(0, NATIVE[1] - 50, dist):
        for x in range(50, NATIVE[0] - 50, dist):
            card = Transform(parent=world_tf, pos=(x, y), pivot=(0, 0))
            Image(attach=card, path="card_back.png", size=(70, 100))
            #IClickable(attach=card, clickable=True)
            #Text(attach=card, text="Hello")
    return world_tf

def new_world_inspector() -> Transform:
    world_tf = Transform("World", pos=(0, 0))

    if True or not Transform.exist_prefab("Datafield"):
        print("Not exist")
        field = Transform("Datafield", pos=(100, 22), pivot=(0, 1), 
                            hitbox=(100, 22), simple=True)
        Image(attach=field, path="white.png", size=(100, 22), standalone=True)
        Text(attach=field, text="69.42", color=colormap['dark'])
        DataField(None, "int", attach=field)
        field.save()

    for y in range(200, NATIVE[1] - 200, 28):
        f = Transform.prefab("Datafield", world_tf)
        f.pos = vec(200, y)

    return world_tf

def new_world_empty() -> Transform:
    world_tf = Transform("World")
    World(attach=world_tf)
    return world_tf


if __name__ == '__main__':
    last_time = time.time()
    frame = 0
 
    world_tf = new_world_inspector()
    world = World(attach=world_tf)

    while World.RUNNING:
        world_tf.update_logic()
        world_tf.update_click()
        world_tf.update_render()

        delta = time.time() - last_time
        frame += 1
        #print(f"Response: {delta*1000:.2f}ms, FPS: {1/delta:.0f}")
        world.windowHandler()
        last_time = time.time()

    #world_tf.save()
    pg.quit()