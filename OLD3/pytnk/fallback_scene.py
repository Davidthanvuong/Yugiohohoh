from .header_pygame import *
from .world import World

# def new_world_spinning() -> Transform:
#     world_tf = Transform("World")
#     dist = 20
#     angle = 0
#     for y in range(0, NATIVE[1] - 50, dist):
#         for x in range(50, NATIVE[0] - 50, dist):
#             card = Transform(parent=world_tf, pos=(x, y), hitbox=(70, 100), angle=angle, pivot=CENTER)
#             Image("card_empty.png", fit=True, attach=card)
#             IClickable(attach=card)
#             #card.make(Text("Hello", colormap['dark']))
            
#     return world_tf



#     # for y in range(200, NATIVE[1] - 200, 28):
#     #     dt = Transform.prefab("DataTask", world_tf, vec(200, y))
#     #     dt.get(Image).cache.native.fill(colormap['relation'])
#     Transform.prefab("ToggleHeader", world_tf, vec(800, 100))

#     return world_tf, com, editor_tf