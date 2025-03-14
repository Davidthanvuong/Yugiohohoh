import pygame as pg
from PIL import Image, ImageSequence
from time import time

def load_gif(path, size):
    #load gif và chuyển frame để scale size
    gif = Image.open(path)
    frames = []
    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        img = pg.image.fromstring(frame.convert("RGBA").tobytes(), frame.size, "RGBA") 
        frames.append(img)
        print(f"Frame {i} completed")
    frames = [pg.transform.scale(frame, size) for frame in frames]
    return frames

def run_animation():

    aura_path = "assets/Animations/rias/rias_aura.gif"
    skill_path = "assets/Animations/rias/rias_skill.gif"
    aura_size = (300, 300)
    skill_size = (350, 100)

    start = time()
    n = 1
    stress_test = [(load_gif(aura_path, aura_size), load_gif(skill_path, skill_size)) for _ in range(n)]

    dt = time() - start
    print(f"Thời gian load {n} Rias GIF + skills: {dt:.2f}s")
    print(f"{n} Rias tượng trưng cho {n} con khác nhau (Ultra rare) sẽ load lúc chạy game")

    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    aura_frames = stress_test[0][0]
    skill_frames = stress_test[0][1]

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

        # aura
        screen.blit(aura_frames[frame_index_aura % len(aura_frames)], (x_aura, y_aura))
        frame_index_aura += 1

        if skill_active:
            if frame_index_skill < len(skill_frames):
                screen.blit(skill_frames[frame_index_skill], (x_skill, y_skill))
                frame_index_skill += 1
            else:
                skill_active = False

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    run_animation()
