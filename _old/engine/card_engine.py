from .settings import *

# class Card:
#     pass

# class CardDeck:
#     def __init__(self, pos: tuple[float, float], length: float = 1000, ty: bool = False):
#         self.pos = pos
#         self.length = length
#         self.ty = ty

#     def render(self):



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


def render_member(pos: tuple[float, float], ty: bool = False, isPlayer: bool = False):
    _player = player if ty else pg.transform.flip(player, True, False)
    _guard = guard if not ty else pg.transform.flip(guard, True, False)
    _select = my_select if not ty else ty_select

    if isPlayer:
        _summon_rect = _player.get_rect(midbottom = pos)
        screen.blit(_player, _summon_rect)
    else:
        _summon_rect = _guard.get_rect(midbottom = pos)
        screen.blit(_guard, _summon_rect)
 
    _select = pg.transform.rotate(_select, pg.time.get_ticks() / 15)
    _select_dim = (_select.get_width(), _select.get_height() * 0.4)
    _select = pg.transform.scale(_select, _select_dim)
    _select_rect = _select.get_rect(center = _summon_rect.midbottom)

    screen.blit(_select, _select_rect)