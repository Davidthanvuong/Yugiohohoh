import pygame as pg
import sys

pg.init()

WHITE = (255, 255, 255)
GREEN = (0, 250, 0)

WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))

health_bar_image = pg.image.load('assets/images/hp.png')

bar_x, bar_y = 100, 100
health_bar_rect = health_bar_image.get_rect(topleft=(bar_x, bar_y))

offset_x = 267
offset_y = 200
inner_w = 106
inner_h = 11

health_rect = pg.Rect(
    health_bar_rect.x + offset_x,
    health_bar_rect.y + offset_y,
    inner_w,
    inner_h
)

dragging = False
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (health_rect.right - 10 <= mouse_x <= health_rect.right + 10 and
                health_rect.top <= mouse_y <= health_rect.bottom):
                dragging = True

        elif event.type == pg.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pg.MOUSEMOTION and dragging:
            mouse_x, _ = event.pos
            new_width = mouse_x - health_rect.left
            if new_width < 0:
                new_width = 0
            if new_width > inner_w:
                new_width = inner_w
            health_rect.width = new_width

    screen.fill(WHITE)

    screen.blit(health_bar_image, health_bar_rect)

    pg.draw.rect(screen, GREEN, health_rect)

    pg.draw.rect(screen, (255, 0, 0), health_bar_rect, 1)
    pg.draw.rect(screen, (0, 0, 255), health_rect, 1)

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()