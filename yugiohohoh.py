# Chỉnh cài đặt trong settings.py
# Trong edit mode bấm shift để di chuyển vị trí global

from pytnk.header_objects import *
from pytnk.scene import Scene

# Scene cho việc edit sẽ được tạo ở đây
def create_new_editor_scene():
    pass

# Scene thí nghiệm ở đây
def create_new_scene():
    cube1 = scene.add("Cube1", Translite(pos=(50, 100), pivot=(0, 0), rot=260))
    scene.add("Cube2", Translite(pos=(250, 150), rot=10, parent=cube1))
    scene.add("Cube3", Translite(pos=(350, 250), rot=50, parent=cube1))
    scene.add("Cube4", Translite(pos=(450, 150), rot=140, parent=cube1))

    for obj in scene.objects.values():
        obj.hitbox = vec(70, 100)
        Image("card_back.png", imgsize=(70, 100), tf=obj)
        ExampleButton("Example button, hello!", clickable=True, tf=obj)
        IRectEditor(tf=obj)


if __name__ == '__main__':
    print("HELLO")
    clock = pg.time.Clock()

    scene = Scene()
    #scene.try_load("pickleball.pkl")
    create_new_scene()
    #scene.save("pickleball.pkl")

    while RUNNING:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                RUNNING = False

        screen.fill((60, 60, 60))
        update_mouse()
        scene.update()


        pg.display.update()
        clock.tick(60)

    pg.quit()