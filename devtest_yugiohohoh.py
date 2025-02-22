import pygame as pg
from pygame import gfxdraw

RES = (1600, 1000)

def load_image(name: str) -> pg.Surface:
    return pg.image.load(name).convert_alpha()

def scale(sf: pg.Surface, size: tuple[float, float]) -> pg.Surface:
    return pg.transform.scale(sf, size)

pg.init()
pg.display.set_caption('Yugiohohoh: Pivot demo @ 22/02/2025')
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()

background = scale(load_image("images\\fs_woodfloor_seemless.jpg"), RES)
background.set_alpha(200)

card = {
    'front': scale(load_image("images\\card_front_empty.png"), (200, 300)),
    'back': scale(load_image("images\\card_back.png"), (200, 300))
}
player = scale(load_image("images\\eldenring.png"), (200, 350))
guard = scale(load_image("images\\stickman.png"), (100, 200))
vignette = scale(load_image("images\\vignette.png"), (RES[0] * 2.5, RES[1]))

select = load_image("images\\select_circle_dot.png")
opponent_select = load_image("images\\select_circle_dot.png")

for x in range(select.get_width()):
    for y in range(select.get_height()):
        if select.get_at((x, y)) == (0, 0, 0):  # Check for black with full alpha
            select.set_at((x, y), (255, 255, 255))  # Change to white

for x in range(opponent_select.get_width()):
    for y in range(opponent_select.get_height()):
        if opponent_select.get_at((x, y)) == (0, 0, 0):  # Check for black with full alpha
            opponent_select.set_at((x, y), (255, 0, 0))  # Change to white

def render_card():
    my_pivot = (150, RES[1] - 150)
    for i in range(10):
        card_rotated = pg.transform.rotate(card['front'], 3)
        card_rect = card_rotated.get_rect(topleft = my_pivot + pg.Vector2(i * 80, 0))
        screen.blit(card_rotated, card_rect)
    
    their_pivot = (RES[0] - 150, 150)
    for i in range(10):
        card_rotated = pg.transform.rotate(card['back'], 3)
        card_rect = card_rotated.get_rect(bottomright = their_pivot + pg.Vector2(i * -80, 0))
        screen.blit(card_rotated, card_rect)


def render_member(pos: tuple[float, float], opponent: bool = False, isPlayer: bool = False):
    _player = player if opponent else pg.transform.flip(player, True, False)
    _guard = guard if not opponent else pg.transform.flip(guard, True, False)
    _select = select if not opponent else opponent_select

    if isPlayer:
        member_rect = _player.get_rect(midbottom = pos)
        screen.blit(_player, member_rect)
    else:
        member_rect = _guard.get_rect(midbottom = pos)
        screen.blit(_guard, member_rect)
 
    _select = pg.transform.rotate(_select, pg.time.get_ticks() / 15)
    select_dim = (_select.get_width(), _select.get_height() * 0.4)
    _select = pg.transform.scale(_select, select_dim)
    select_rect = _select.get_rect(center = member_rect.midbottom)

    screen.blit(_select, select_rect)


class TextEngine:
    def __init__(self):
        self.game_font = pg.font.Font('Comic.ttf', 20)

    def write(self, txt: str, pos):
        img = self.game_font.render(txt, True, (255, 255, 255))
        rect = img.get_rect(topleft = pos)
        screen.blit(img, rect)

defFont = TextEngine()


while True:
    mspf = clock.tick(30)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0)) # Background

    render_member((150, RES[1] // 2 - 100))
    render_member((150, RES[1] // 2))
    render_member((250, RES[1] // 2 + 100), False, True)
    render_member((150, RES[1] // 2 + 200))
    render_member((150, RES[1] // 2 + 300))

    render_member((RES[0] - 150, RES[1] // 2 - 100), True)
    render_member((RES[0] - 150, RES[1] // 2), True)
    render_member((RES[0] - 250, RES[1] // 2 + 100), True, True)
    render_member((RES[0] - 150, RES[1] // 2 + 200), True)
    render_member((RES[0] - 150, RES[1] // 2 + 300), True)

    render_card()
    vignette_rect = vignette.get_rect(center = (RES[0] // 2, RES[1] // 2))
    screen.blit(vignette, vignette_rect)

    defFont.write(f"MSPF: {mspf}", (20, 20))
    pg.display.update()

# import pygame as pg

# RESOLUTION = (800, 800)

# def scale(sf: pg.Surface, size: tuple[float, float]) -> pg.Surface:
#     if size[0] > 31: # Must be using pixel mode
#         return pg.transform.scale(sf, size)

#     _dim = (int(sf.get_width() * size[0]), int(sf.get_height() * size[1]))
#     return pg.transform.scale(sf, _dim)

# def rotate(sf: pg.Surface, deg: float) -> pg.Surface:
#     return pg.transform.rotate(sf, deg)

# def load_image(name: str) -> pg.Surface:
#     return pg.image.load(name).convert_alpha()

# pg.init()
# screen = pg.display.set_mode(RESOLUTION)
# clock = pg.time.Clock()

# card = {
#     'empty': scale(load_image("cards\\card_front_empty.png"), (300, 450)), 
#     'back':  scale(load_image("cards\\card_back.png"), (300, 450))
# }
# show_card = False

# def event_handler():
#     global show_card
#     for e in pg.event.get():
#         if e.type == pg.QUIT:
#             pg.quit()
#             quit()
#         if e.type == pg.KEYDOWN:
#             if e.key == pg.K_SPACE:
#                 show_card = not show_card

# def update():
#     event_handler()
#     screen.fill((255, 255, 255))

#     card_surface = card['empty' if show_card else 'back']
#     card_rect = card_surface.get_rect(center=(RESOLUTION[0] // 2, RESOLUTION[1] // 2))
#     screen.blit(card_surface, card_rect)


# if __name__ == "__main__":
#     while True:
#         update()
#         pg.display.update()
#         clock.tick(60)