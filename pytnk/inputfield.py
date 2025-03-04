from .header_pygame import *

noTable = [pg.K_RETURN]

intTable = [pg.K_BACKSPACE, pg.K_RETURN, pg.K_MINUS]
intTable.extend(range(pg.K_0, pg.K_9 + 1))

floatTable = intTable.copy()
floatTable.append(pg.K_COMMA)

strTable = floatTable.copy()
strTable.extend(range(pg.K_a, pg.K_z + 1))
strTable.append(pg.K_SPACE)

tabletable: dict[type, list[int]] = { # :)))
    int:      intTable,
    float:  floatTable,
    str:      strTable,
    Component: strTable
}

class InputField(IClickable):
    '''Khung nhập được có khả năng kiểm kiểu dữ liệu'''
    def __init__(self, halt = 500, interval = 40, value = None, task: No['DataTask'] = None, fieldId: int = -1, **kwargs):
        super().__init__(**kwargs)
        self.type_halt = halt
        self.type_interval = interval
        self.repeatLambda = None
        self.heldKey = 0
        self.cooldown = 0
        self.pressed = pg.key.get_pressed()
        self.prevKeys = self.pressed
        self.tick = pg.time.get_ticks()
        self.text_updated = False
        self.valid = True

        #self.caret = self.tf.childrens[0]
        self.com_text = self.tf.getComponent(Text)
        self.com_image = self.tf.getComponent(Image)
        self.task = task
        self.valueType = type(value)
        self.oldValue = value
        self.keymap = tabletable.get(self.valueType, noTable)
        self.editable = self.keymap is not noTable
        self.fieldId = fieldId
        print(self.editable, value, self.valueType, self.keymap)


    def update_click(self):
        super().update_click()
        self.textChanged = False
        if not self.editable or not self.wasFocus: return
        
        self.tick = pg.time.get_ticks()
        self.pressed = pg.key.get_pressed()
        for k in self.keymap:
            # Không nhận nút không nhấn hoặc nhận thêm nút đã nhấn 
            # (nhưng được lặp lại sau self.halt ms: thằng bên dưới dòng for)
            self.handle_keystroke(k)

        if not self.pressed[self.heldKey]:
            self.repeat = None
            self.heldKey = 0
        elif self.repeat:
            # Để tránh bị desync hoặc time sai, chạy đến khi nào ok thì thôi
            while self.tick >= self.cooldown:
                self.repeat()
                self.cooldown += self.type_interval
                self.text_updated = True

        if self.text_updated:
            self.try_updateValue()
        self.prevKeys = self.pressed


    def handle_keystroke(self, k: int):
        if (not self.pressed[k]) or self.prevKeys[k]: return
        self.text_updated = True
        self.cooldown = self.tick + self.type_halt # Dừng một khoảng trước khi gõ lặp lại
        self.heldKey = k

        if k == pg.K_RETURN:
            mouse.lastFocus = None # Enter xác nhận
        elif k == pg.K_BACKSPACE:
            if self.pressed[pg.K_LCTRL]:
                self.com_text.text = ""
            else:
                self.heldKey = k
                self.repeat = lambda: setattr(self.com_text, 'text', self.com_text.text[:-1])
                self.repeat()
        else:
            shift = self.pressed[pg.K_LSHIFT]
            # Chỉ chuyển sang underscore khi được cho phép bởi table
            if shift and k == pg.K_MINUS and pg.K_UNDERSCORE in self.keymap: 
                k = pg.K_UNDERSCORE

            self.heldKey = k
            if pg.K_a <= k <= pg.K_z: k -= shift * 32 # Trick -32 chuyển thành uppercase
            self.repeat = lambda c=chr(k): setattr(self.com_text, 'text', self.com_text.text + c)
            self.repeat()


    def typecheck_number(self):
        '''Hỗ trợ số nguyên, thập phân...'''
        try:
            type(self.valueType)(self.com_text.text) # type: ignore
            return True
        except ValueError:
            return False

    def typecheck_ref(self):
        '''Hỗ trợ gán reference'''
        return False

    
    def try_updateValue(self):
        match self.valueType:
            case 'int' | 'float': 
                self.valid = self.typecheck_number()
            case 'Component':
                print("component")
                self.valid = self.typecheck_ref()
            case _:
                print("str") # String luôn đúng
                self.valid = True

        if self.task:
            self.task.set_variable(self.valid, 
                type(self.valueType)(self.com_text.text), self.fieldId) # type: ignore


    def on_startHover(self):
        self.com_image.changed = True
        self.com_image.cache.texture.fill(colormap['light'])


    def on_stopHover(self):
        self.com_image.changed = True
        self.com_image.cache.texture.fill(colormap['white'])


    def on_startClick(self):
        pass # todo: Hiển thị caret


    def on_stopFocus(self):
        if self.valid: return
        print("Invalid. Not try except nah")
        self.com_text.text = str(self.oldValue)


class DataTask(IClickable):
    def set_variable(self, value, id):
        pass
        # try:
        #     if self.multiField:
        #         self.value[id] = type(self.value[id])(value)
        #     else: self.value = type(self.value)(value)
        #     setattr(self.target, self.name, self.value)
        #     self.invalid = False
        # except ValueError:
        #     print("Bad")
        #     self.invalid = True