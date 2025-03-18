from pytnk.engine import *


class CardSlot(IClickable):
    dragging  : No['CardSlot'] = None
    selecting : No['CardSlot'] = None

    def build(self, x: int, y: int):
        forward = -1 if self.user.rightSide else 1
        slot = Image("card_back.png", (120, 80), True, True).build(parent=self.user.slotsParent,
                pos=(forward * x * 150, y * 120))
        return slot.addComponent(self)

    def __init__(self, user: 'Controller', myId: int):
        super().__init__(draggable=True)
        self.user = user
        self.myId = myId
        # self.occupy: No[ref[Monster]] = None
        self.selectMotion = Motion.linear(0, 150, 0.3, True, True)
        self._occupy: No[ref['Summon']] = None
    
    def after_init(self):
        self.com_img = self.go.getComponent(Image)

    def on_startHover(self):
        CardSlot.selecting = self
        self.selectMotion.start()

    def on_stopHover(self):
        if CardSlot.selecting is self:
            CardSlot.selecting = None
            self.com_img.overlay_alpha = 0

    def on_startDrag(self):
        if CardSlot.dragging is None:
            CardSlot.dragging = self

    def on_hovering(self):
        if CardSlot.selecting is self:
            self.com_img.overlay_alpha = self.selectMotion.value
        else: 
            self.com_img.overlay_alpha = 0

    def on_dragging(self):
        # Đè lên tính năng drag (không cho phép drag vật, chỉ drag mũi tên)
        if CardSlot.dragging is self:
            self.com_img.overlay_alpha = self.selectMotion.value

    def on_stopDrag(self):
        self.com_img.overlay_alpha = 0
        drag = CardSlot.dragging
        select = CardSlot.selecting
        if (drag is None) or (select is None):
           CardSlot.dragging = None
           return 
        if (drag is not self): return

        print(f"{drag.myId} --> {select.myId}")
        CardSlot.dragging = None
        CardSlot.selecting = None

        if (not drag.occupy) or (self.user.quickAction_left <= 0): return
        drag.occupy.interact(select)

    def update_render(self):
        if (not CardSlot.dragging) or (CardSlot.dragging is not self): return
        pos1 = CardSlot.dragging.transf.g_pos
        select = CardSlot.selecting
        pos2 = select.transf.g_pos if select else Mouse.pos
        pg.draw.line(App.screen, Color.red, pos1, pos2, 5)

    @property
    def occupy(self):
        return self._occupy() if self._occupy else None
    
    @property
    def force_occupy(self):
        o = self._occupy() # type: ignore
        assert o is not None
        return o


class Card(IClickable):
    e_placeCard: Event['Card'] = Event()

    def build(self):
        path = f"card/{self.data.img_path}" if self.user.isPlayer else "card_back.png"
        card = Image(path, (150, 240), True, True).build(parent=self.user.deck.go)
        return card + self

    def __init__(self, user: 'Controller', data: No[CardData] = None):
        super().__init__(draggable=True)
        self.data = data if data else CardData.getRandom()
        self.user = user
        self.onDeck = True
        self.selectMotion = Motion.linear(0, 150, 0.3, True, True)
        self.user.deck.updated_childs()

    def after_init(self):
        self.set_glideTarget(vec(ZERO))
        self.com_img = self.go.getComponent(Image)

    def update_logic(self):
        if self.onDeck:
            self.transf.pos = self.motion.value

        self.draggable = self.user.placeCard_left > 0

    def set_glideTarget(self, target: vec):
        self.motion = Motion.ease_out_cubic(self.transf.pos, target, 0.3)
    
    def on_startHover(self):
        self.transf.scale *= 1.1
        self.selectMotion.start()

    def on_hovering(self):
        '''Tắt chớp nháy nếu đang cầm (ngứa mắt vcl nên tắt)'''
        k = 0 if self.dragging else self.selectMotion.value
        self.com_img.overlay_alpha = k

    def on_stopHover(self):  
        self.transf.scale /= 1.1
        self.com_img.overlay_alpha = 0

    def on_startDrag(self, controlled = False):
        self.user.main.notif.startNotif(self.user.rightSide, "Thả thẻ xuống bàn để đặt")
        self.transf.rot = 0.0
        self.onDeck = False
        self.oldIndex = self.go.removeParent()
        self.user.deck.updated_childs()
        Sounds.play("picking.mp3", Volume.effects)

        # Card.sfx_picking.play()
        if not controlled:
            super().on_startDrag()

    def on_stopDrag(self):
        dist = (self.transf.g_pos.y + 100) if (self.user.rightSide) else (App.native[1] - self.transf.g_pos.y)
        if dist < 200:
            self.oldIndex = -1
        elif self.try_placeCard(CardSlot.selecting):
            self.user.placeCard_left -= 1
            self.activated = False
            self.go += Shader_BurningCard(self.com_img)
            self.go += Animation("common/spawn", playtime=1.0, looping=False)

            Sounds.play("placing.mp3", Volume.effects)
            return #self.go.destroy() # Giữ lại cho burning shader
        
        self.onDeck = True
        self.go.removeParent(reroot=False)
        self.user.deck.go.insertChildren(self.go, self.oldIndex)
        self.transf.pos -= self.user.deck.transf.g_pos
        self.user.deck.updated_childs()
        
    def try_placeCard(self, slot: No['CardSlot'] = None):
        print(f"Place card {self.data.name} to {slot.myId if slot else None}")
        if isinstance(self.data, MonsterData):
            return self.data.monster.tryPlace(self, self.data, slot)
        elif isinstance(self.data, SpellData):
            return self.data.spell.tryPlace(self, self.data, slot)
        elif isinstance(self.data, TrapData) and slot:
            return self.data.trap.tryPlace(self, self.data, slot)

        return False


class CardDeck(Component):
    '''✅ Deck lưu các cards'''
    def build(self):
        deck_y = 0 if (self.user.rightSide) else (App.native[1] - 50)
        deck = GameObject('Card Deck', self.user.go, pos=(App.center[0], deck_y), rot=(180 * self.user.rightSide))
        return deck.addComponent(self)

    def __init__(self, user: 'Controller', arc = 48, height = 1200, maxFrac = 6):
        self.user = user
        self.arc = arc
        self.height = height
        self.maxFrac = maxFrac

    def updated_childs(self):
        cards = self.go.childs
        n = len(cards)

        center = - UPWARD * self.height
        spanning = min(self.arc, self.maxFrac * n)
        for i, card in enumerate(cards):
            frac = (i - n / 2 + 0.5) / n * spanning
            card.getComponent(Card).set_glideTarget(center + (UPWARD * self.height).rotate(frac))
            card.transf.rot = -frac