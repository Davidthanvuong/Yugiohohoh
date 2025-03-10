import pygame as pg
from PIL import Image, ImageSequence

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

aura_path = "D:/GAMEYUGI/Yugiohohoh/assets/Animations/rias/rias_aura.gif"
aura_gif = Image.open(aura_path)
aura_frames = [
    pg.image.fromstring(frame.convert("RGBA").tobytes(), frame.size, "RGBA") 
    for frame in ImageSequence.Iterator(aura_gif)
]
aura_size = (300, 300)
aura_frames = [pg.transform.scale(frame, aura_size) for frame in aura_frames]

skill_path = "D:/GAMEYUGI/Yugiohohoh/assets/Animations/rias/rias_skill.gif"
skill_gif = Image.open(skill_path)
skill_frames = [
    pg.image.fromstring(frame.convert("RGBA").tobytes(), frame.size, "RGBA") 
    for frame in ImageSequence.Iterator(skill_gif)
]
skill_size = (350, 100)
skill_frames = [pg.transform.scale(frame, skill_size) for frame in skill_frames]

x_aura = 50  
y_aura = 250  
x_skill = x_aura + aura_size[0] + 30 
y_skill = y_aura + aura_size[1] // 2 - skill_size[1] // 2 + 30

frame_index_aura = 0
frame_index_skill = 0
skill_active = False  

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN and not skill_active:
            skill_active = True
            frame_index_skill = 0 

    screen.fill((255, 255, 255))

    screen.blit(aura_frames[frame_index_aura % len(aura_frames)], (x_aura, y_aura))
    frame_index_aura += 1

    if skill_active:
        if frame_index_skill < len(skill_frames):
            screen.blit(skill_frames[frame_index_skill], (x_skill, y_skill))
            frame_index_skill += 1
        else:
            skill_active = False

    pg.display.flip()
    clock.tick(10)

pg.quit()
