from .header_pygame import *

numericTable = [pg.K_BACKSPACE, pg.K_RETURN]
numericTable.extend(range(pg.K_0, pg.K_9 + 1))

literalTable = numericTable
literalTable.extend(range(pg.K_a, pg.K_z + 1))
literalTable.append(pg.K_SPACE)
literalTable.append(pg.K_MINUS)


class DataField(IClickable):
    def __init__(self, numericOnly = True, editable = True, halt = 500, interval = 40, **kwargs):
        super().__init__(**kwargs)
        self.editable = editable # Địa chỉ, dãy,... không được phép modify
        self.com_text = self.tf.get(Text)
        self.com_rect = self.tf.get(Image)
        self.numericMode = numericOnly
        self.table = numericTable if numericOnly else literalTable
        self.active = False

        self.halt = halt
        self.interval = interval
        self.repeat = None
        self.heldKey = 0
        self.cooldown = 0
        self.pressed = pg.key.get_pressed()
        self.prevKeys = self.pressed
        self.tick = pg.time.get_ticks()

    def logic_update(self):
        if not self.active: return

        self.tick = pg.time.get_ticks()
        self.pressed = pg.key.get_pressed()
        for k in self.table:
            # Không nhận nút không nhấn hoặc nhận thêm nút đã nhấn 
            # (nhưng được lặp lại sau self.halt ms: thằng bên dưới dòng for)
            self.handle_keystroke(k)

        if not self.pressed[self.heldKey]:
            self.repeat = None
            self.heldKey = 0
        elif self.repeat:
            # Tránh không đồng bộ, chạy đến khi nào ok thì thôi
            while self.tick >= self.cooldown:
                self.repeat()
                self.cooldown += self.interval

        self.prevKeys = self.pressed

    def handle_keystroke(self, k: int):
        if (not self.pressed[k]) or self.prevKeys[k]: return
        self.cooldown = self.tick + self.halt
        self.heldKey = k

        if k == pg.K_RETURN:
            MOUSE.lastFocus = None
        elif k == pg.K_BACKSPACE:
            if self.pressed[pg.K_LCTRL]:
                self.com_text.text = ""
            else:
                self.heldKey = k
                self.repeat = lambda: setattr(self.com_text, 'text', self.com_text.text[:-1])
                self.repeat()
        else:
            shift = self.pressed[pg.K_LSHIFT]
            if k == pg.K_MINUS:
                if shift: k = pg.K_UNDERSCORE
                else: return

            self.heldKey = k
            if pg.K_a <= k <= pg.K_z: k -= shift * 32  # Uppercase if shift is pressed
            self.repeat = lambda c=chr(k): setattr(self.com_text, 'text', self.com_text.text + c)
            self.repeat()

    def on_startClick(self):
        print("START CLICK")
        self.com_rect.changed = True
        self.active = True
        self.com_rect.cache.texture.fill(colormap['light'])

    def on_stopFocus(self):
        print("STOP FOCUS")
        self.com_rect.changed = True
        self.active = False
        self.com_rect.cache.texture.fill(colormap['white'])

