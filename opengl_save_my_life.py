# import pygame
# #from pygame.locals import *
# from OpenGL.GL import * # type: ignore
# # from OpenGL.GLUT import *
# import time
# import math

# pygame.init()
# width, height = 1600, 800
# screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

# glEnable(GL_TEXTURE_2D)
# glOrtho(0, width, height, 0, -1, 1)

# def create_glTexture(path: str):
#     texture = glGenTextures(1)
#     img = pygame.image.load(f"image\\{path}").convert_alpha()
#     img_data = pygame.image.tobytes(img, "RGBA", True)
#     glBindTexture(GL_TEXTURE_2D, texture)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.get_width(), img.get_height(), 0, 
#                  GL_RGBA, GL_UNSIGNED_BYTE, img_data)
#     return texture

# texture1 = create_glTexture("card_empty.png")
# texture2 = create_glTexture("card_back.png")

# def draw_quad(x, y, angle):
#     glPushMatrix()
#     glTranslatef(x, y, 0)
#     glRotatef(angle, 0, 0, 1)
#     glBindTexture(GL_TEXTURE_2D, texture2)
#     glBegin(GL_QUADS)
#     sx, sy = 1600, 100
#     px, py = 0.5, 0.5
#     ox, oy = sx * -px, sy * -py
#     glTexCoord2f(0, 0); glVertex2f(0  + ox, sy + oy)
#     glTexCoord2f(1, 0); glVertex2f(sx + ox, sy + oy)
#     glTexCoord2f(1, 1); glVertex2f(sx + ox, 0  + oy)
#     glTexCoord2f(0, 1); glVertex2f(0  + ox, 0  + oy)
#     glEnd()
#     glPopMatrix()

# clock = pygame.time.Clock()
# angle = 0
# last_fps_time = time.time()
# frame = 0

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#             running = False
    
#     glClear(GL_COLOR_BUFFER_BIT)
#     angle += 60 * (clock.get_time() / 1000.0)
#     cnt = 0
#     for y in range(10, height - 10, 100):
#         for x in range(10, width - 10, 100):
#             draw_quad(x, y, angle)
#             cnt += 1
    
#     pygame.display.flip()
#     clock.tick()
#     frame += 1
#     if time.time() - last_fps_time >= 0.5:
#         fps = frame / (time.time() - last_fps_time)
#         print(f"Draw per frame ({cnt}): Pixel: {cnt * 200 * 300 * fps / 1e9:.3f}B, FPS: {fps:.2f}")
#         last_fps_time = time.time()
#         frame = 0
    
# pygame.quit()