import pygame as pg
import sys

pg.init()

WHITE = (255, 255, 255)
GREEN = (0, 250, 0)

WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))

# Setup health
health_bar_image = pg.image.load('assets/images/hp.png')
bar_x, bar_y = 100, 100
health_bar_rect = health_bar_image.get_rect(topleft=(bar_x, bar_y))

#Setup green rect
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

# Setup nv
offset_x1 = 268
offset_y1 = 215

character_image = pg.image.load('assets/images/notsafecard/Akeno.jpg')

scale_factor = 0.25  # optimise scale
original_size = character_image.get_size()
new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))  
character_image = pg.transform.scale(character_image, new_size)  

character_rect = character_image.get_rect(topleft=(health_bar_rect.x + offset_x1, health_bar_rect.y + offset_y1))

font = pg.font.Font(None, 36)

dragging = False
is_dying = False
dying_progress = 0
show_died_message = False
running = True
clock = pg.time.Clock()

def onDie():
    global is_dying, dying_progress
    is_dying = True
    dying_progress = 0
    print("Die") 

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

    if health_rect.width <= 0 and not is_dying and not show_died_message:
        onDie()

    if is_dying:
        character_rect.y += 10  
        angle = dying_progress * 6  
        rotated_image = pg.transform.rotate(character_image, angle)
        rotated_rect = rotated_image.get_rect(center=character_rect.center)
        dying_progress += 1
        if dying_progress >= 60:  
            is_dying = False
            show_died_message = True

    screen.fill(WHITE)
    screen.blit(health_bar_image, health_bar_rect)
    pg.draw.rect(screen, GREEN, health_rect)

    if show_died_message:
        died_text = font.render("DIED EZ NOOB NIGGA", True, (255, 0, 0))
        screen.blit(died_text, (WIDTH // 2 - died_text.get_width() // 2,
                                HEIGHT // 2 - died_text.get_height() // 2))
    else:
        if is_dying:
            screen.blit(rotated_image, rotated_rect)  
        else:
            screen.blit(character_image, character_rect) 
    #DEBUG
    pg.draw.rect(screen, (255, 0, 0), health_bar_rect, 1)
    pg.draw.rect(screen, (0, 0, 255), health_rect, 1)

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()