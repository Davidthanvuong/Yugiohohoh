from engine import *

texte = TextEngine()
tick = 0
total = 0
fpstext = ""

while True:
    tick += 1
    total += clock.tick(30)
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

    if tick > 20:
        fpstext = f"MSPF: {'%.2f' % (20000 / total)}"
        tick = 0
        total = 0
    texte.write(fpstext, (20, 20))
    pg.display.update()