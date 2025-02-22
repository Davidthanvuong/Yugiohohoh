from .image_processor import *

RES = (1600, 1000)
pg.init()
pg.display.set_caption('Yugiohohoh: Summons demo @ 22/02/2025 11:30')
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()

background = scale(load("fs_woodfloor_seemless.jpg"), RES)
background.set_alpha(200)

card = {
    'front': scale(load("card_front_empty.png"), (200, 300)),
    'back': scale(load("card_back.png"), (200, 300))
}
player      = scale(load("eldenring.png", Path.summon), (200, 350))
stickman    = scale(load("stickman.png", Path.summon), (100, 200))
warrior     = scale(load("warrior.png", Path.summon), (200, 200)) 
duck        = scale(load("duck.png", Path.summon), (200, 200))
guard       = scale(load("guard.png", Path.summon), (100, 220))
vignette    = scale(load("vignette.png"), (RES[0] * 2.5, RES[1]))

my_select   = recolor(load("select_circle_dot.png"), (0, 0, 0), (255, 255, 255))
ty_select   = recolor(load("select_circle_dot.png"), (0, 0, 0), (255, 0, 0))