from .header_pygame import *

# Một đống table input
noTable = [pg.K_RETURN]

intTable = [pg.K_BACKSPACE, pg.K_RETURN, pg.K_MINUS]
intTable.extend(range(pg.K_0, pg.K_9 + 1))

floatTable = intTable.copy()
floatTable.append(pg.K_COMMA)

strTable = floatTable.copy()
strTable.extend(range(pg.K_a, pg.K_z + 1))
strTable.append(pg.K_SPACE)

tabletable: dict[str, list[int]] = { # :)))
    "int":      intTable,
    "float":  floatTable,
    "str":      strTable,
}

class DataField(IClickable):
    '''Nhập tham số vô inputfield đã kiểu dữ liệu'''

    def __init__(self, dataTask: No['DataTask'] = None, fieldType = "str", 
                 dataId=0, editable = True, halt = 500, interval = 40, **kwargs):
        super().__init__(**kwargs)
        self.editable = editable # Địa chỉ, dãy,... không được phép modify
        self.com_text = self.tf.get(Text)
        self.com_image = self.tf.get(Image)

        self.table = tabletable.get(fieldType, noTable) # Tham số từ DataTask \/
        self.active = False
        self.dataId = dataId
        self.dataTask = dataTask
        self.fieldType = fieldType

        self.interval = interval
        self.halt = halt
        self.repeat = None
        self.text_updated = False
        self.heldKey = 0
        self.cooldown = 0
        self.pressed = pg.key.get_pressed()
        self.prevKeys = self.pressed
        self.tick = pg.time.get_ticks()


    def update_click(self):
        super().update_click()
        self.text_updated = False
        if not self.editable or not self.active: return

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
            # Để tránh bị desync hoặc time sai, chạy đến khi nào ok thì thôi
            while self.tick >= self.cooldown:
                self.repeat()
                self.cooldown += self.interval
                self.text_updated = True

        if self.text_updated: # CHANGE
            if self.dataTask:
                self.dataTask.task_tryPreview(self.com_text.text, self.dataId)
            else: print("Mồ côi, bỏ qua.")
        self.prevKeys = self.pressed


    def handle_keystroke(self, k: int):
        if (not self.pressed[k]) or self.prevKeys[k]: return
        self.text_updated = True
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
            # Chỉ chuyển sang underscore khi được cho phép bởi table (abstract)
            if shift and k == pg.K_MINUS and pg.K_UNDERSCORE in self.table: 
                k = pg.K_UNDERSCORE

            self.heldKey = k
            if pg.K_a <= k <= pg.K_z: k -= shift * 32 # Trick -32 chuyển thành uppercase
            self.repeat = lambda c=chr(k): setattr(self.com_text, 'text', self.com_text.text + c)
            self.repeat()


    def on_startClick(self):
        self.com_image.changed = True # Đánh dấu đã bị chỉnh sửa
        self.active = True
        self.com_image.cache.native.fill(colormap['light'])


    def on_stopFocus(self):
        self.com_image.changed = True
        self.active = False
        self.com_image.cache.native.fill(colormap['white'])
        if self.dataTask: # CHANGED
            self.dataTask.task_tryUpdate(self.com_text.text, self.dataId)
        else:
            print("Mồ côi, bỏ qua.")



class DataTask(IClickable):
    '''Một dãy hoặc chỉ một DataField dùng để thay đổi dữ liệu vật'''

    def __init__(self, target: Component, name: str, **kwargs):
        super().__init__(hoverable=False, clickable=False, **kwargs)
        self.target = target
        self.com_text = self.tf.get(Text)
        self.value = getattr(target, name)
        self.defaultValue = self.value
        self.varname = name
        self.multiField = False

        self.fields_tf: list[Transform] = []
        self.editable = True
        self.getFields()


    def getFields(self): # Trình bày như cưc
        self.fields_tf.clear()
        f1 = Transform.prefab("DataField", self.tf)
        self.fields_tf.append(f1)
        size = self.tf.hitbox
        if isinstance(self.value, vec): # fields kép
            f2 = Transform.prefab("DataField", self.tf)
            fieldsize = vec((size.x - 100) // 2 - 3 - 2, size.y - 4)
            
            f1.pos = vec(100, size.y // 2)
            f2.pos = vec(100 + fieldsize.x + 5, size.y // 2)

            f1.get(Image).size = f1.hitbox = f2.get(Image).size = f2.hitbox = fieldsize
            self.fields_tf.append(f2)
            self.multiField = True
            f1.get(DataField).com_text.text = str(self.value[0])
            f2.get(DataField).com_text.text = str(self.value[1])
        else:
            f1.pos = vec(100, size.y // 2) # Canh giữa trái chiếm gần hết nguyên box
            f1.get(Image).size = f1.hitbox = vec(size.x - 100 - 3, size.y - 4)
            f1.get(DataField).com_text.text = str(self.value)
            self.multiField = False
        
        for i, tf in enumerate(self.fields_tf):
            f = tf.get(DataField)
            f.dataId = i
            f.dataTask = self
            #f.com_text.text = self.defaultValue
            if self.multiField:
                f.fieldType = type(self.value[i]).__name__ # type: ignore
            else:
                f.fieldType = type(self.value).__name__
            self.com_text.text = self.varname

            print(type(self.value))
            if isinstance(self.value, None | Component): # todo: class RefField(DataField)
                f.editable = False
                f.com_text.text = "*****"
                print("Undefined behavior")
            elif not isinstance(self.value, int | float | str):
                f.editable = False


    def task_tryPreview(self, value, id):
        try:
            if self.multiField:
                new_value = type(self.value[id])(value)
                setattr(self.target, self.varname[id], new_value)
                self.value[id] = new_value
                setattr(self.target, self.varname, self.value)
            else: 
                new_value = type(self.value)(value)
                setattr(self.target, self.varname, new_value)
        except ValueError:
            print("Bad")
            pass # Sự phẫn nộ của người lửa

    def task_tryUpdate(self, value, id):
        try:
            if self.multiField:
                new_value = type(self.value[id])(value)
                setattr(self.target, self.varname[id], new_value)
            else: 
                new_value = type(self.value)(value)
                setattr(self.target, self.varname, new_value)
        except Exception as e:
            print(f"Giá trị không hợp lệ {value}. Lỗi {e}")
            if self.multiField:
                self.fields_tf[id].get(DataField).com_text.text = str(self.value[id]) # Undo
            else:
                self.fields_tf[id].get(DataField).com_text.text = str(self.value) # Undo
            setattr(self.target, self.varname, self.defaultValue)

    def on_startHover(self): pass
    def on_stopHover(self): pass


class ToggleHeader(IClickable):
    '''Một dãy các DataTask cho từng Component để thay đổi dữ liệu của nó'''

    def __init__(self, target_com: Component, **kwargs):
        super().__init__(hoverable=False, clickable=False, **kwargs)
        #self.com_text = self.tf.get(Text)
        self.target_com = target_com

        self.fields: list[DataField] = []
        self.folded = False
        self.getTasks()

    def getTasks(self, clear=False):
        if clear: self.fields.clear()
        for name, value in self.target_com.__dict__.items():
            task_tf = Transform.prefab("DataTask", self.tf)
            task = task_tf.get(DataTask)
            task.target = self.target_com
            task.value = getattr(self.target_com, name)
            task.defaultValue = value
            task.varname = name
            task.com_text.text = name
            task_tf.hitbox.x = self.tf.hitbox[0] - 10
            task.getFields()

    def on_startHover(self): pass
    def on_stopHover(self): pass
    def on_startClick(self): pass


class Inspector(Component):
    '''Inspector có khả năng hiển thị hết dữ liệu và có thể thay đổi chúng theo ý muốn
    Bao nhiêu tầng lớp đây? Inspector -> ToggleHeader -> DataTask -> DataField'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def inspectTransform(self, tf: Transform):
        # todo: Custom inspect cho Transform
        # Có thể là monster sẽ hiển thị dữ liệu đặc biệt trên đó?
        for com in tf.coms.values():
            header_tf = Transform.prefab("ToggleHeader", self.tf)
            header = header_tf.get(ToggleHeader)
            header.target_com = com
            header_tf.hitbox.x = self.tf.hitbox[0] - 10