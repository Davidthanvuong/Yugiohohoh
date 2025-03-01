# Chỉnh cài đặt trong settings.py
# Trong edit mode bấm shift để di chuyển vị trí global

from pytnk.header_objects import *
from pytnk.world import World
from pytnk.object_editor import loadAssetsList, createObject, inspectObj
#from pytnk.editor_inspector import InspectorFrame
import time
from random import randint as rint

# Scene cho việc edit sẽ được tạo ở đây
def create_new_editor_scene():
    pass

cnt = 0
# Scene thí nghiệm ở đây
def create_new_scene():
    global cnt
    scene.add(Transform("World", pos=(0, 0), pivot=(0, 0)))
    # for y in range(50, NATIVE[1], 100):
    #     for x in range(50, NATIVE[0], 100):
    #         cnt += 1
    #         parent = None if cnt < 5 else scene.objects[f"Cube {rint(1, cnt-1)}"]
    #         scene.add(Transform(f"Cube {cnt}", pos=(x, y), pivot=(0, 0), parent=parent, rot=x*0.1+y*0.1))
    cube1 = scene.add(Transform("Cube1", pos=(50, 100), rot=260))
    scene.add(Transform("Cube2", pos=(250, 150), pivot=(0, 0), rot=10, parent=cube1))
    scene.add(Transform("Cube3", pos=(350, 250), rot=50, parent=cube1))
    scene.add(Transform("Cube4", pos=(450, 150), rot=140, parent=cube1))

    for obj in scene.objects.values():
        if obj.name == "World": continue
        obj.hitbox = vec(70, 100)
        Image("card_back.png", imgsize=(70, 100), tf=obj)
        ExampleButton("Example button, hello!", clickable=True, tf=obj)
        IRectEditor(tf=obj)


if __name__ == '__main__':
    print("HELLO")
    loadAssetsList()
    clock = pg.time.Clock()
    editor_rect = pg.Rect(NATIVE[0] // 2, 0, NATIVE[0] // 2, NATIVE[1])

    scene = World("pickleball")
    #scene = SceneManager.try_load("pickleball.pkl")
    create_new_scene()
    #insp = InspectorFrame(scene.objects["Cube1"])

    while RUNNING:
        #last_fps_time = time.time()
        for e in pg.event.get():
            if e.type == pg.QUIT:
                RUNNING = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    obj = createObject()
                    if obj:
                        scene.add(obj)
                        obj.hitbox = vec(70, 100)
                        Image("card_back.png", imgsize=(70, 100), tf=obj)
                        ExampleButton("Example button, hello!", clickable=True, tf=obj)
                        IRectEditor(tf=obj)
                        cnt += 1
                if e.key == pg.K_TAB:
                    objname = input("Tên vật:")
                    inspectObj(scene.objects[objname])

        update_mouse()
        for obj in scene.objects.values():
            if obj.name == "World": continue
            obj.rot += 1
        scene.update()

        direct_render(dummy_screen, vec(NATIVE), scene.objects['World'])
        updateDisplay()
        # mspf = time.time() - last_fps_time
        # print(f"Objects: {cnt}, Response time: {mspf*1000:.3f}ms, FPS: {1/mspf:.0f}")
        clock.tick(60)

    #scene.save("pickleball.pkl")
    pg.quit()