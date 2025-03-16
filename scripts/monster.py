from pytnk.engine import *

class Summon(Component):
    def __init__(self, user: 'Controller', slot: 'CardSlot'):
        self.slot = slot
        self.user = user
        self.actions: list[Generator] = []
    
    def update_logic(self):
        if len(self.actions) == 0: return
        for act in list(self.actions):
            try: next(act)
            except StopIteration:
                self.actions.remove(act)

    def interact(self, target: No['CardSlot']): pass

class Monster(Summon):
    @staticmethod
    def tryPlace(card: 'Card', data: MonsterData, slot: No['CardSlot']):
        if (slot is None) or (slot.occupy): return False # Không có khỏi cho để
        if slot.myId < 5: return False # Chỗ cho trap
        data.monster(data, card.user, slot).build(slot.transf.g_pos)
        return True

    def build(self, pos: vec):
        mon = Image(self.data.get_placedPath(), (150, 135), True, True).build(pos=pos, anchor=MIDBOTTOM) + self
        self.img = mon.getComponent(Image)

        MonsterUI(self).build()
        return self

    def __init__(self, data: MonsterData, *a):
        super().__init__(*a)
        self.data = data
        self.defense = self.maxDefense = self.data.baseDEF * 2
        self.attack = self.data.baseATK
        self.slot._occupy = ref(self)

        self.e_attackFinished: Event = Event()

        self.isDead = False
        self.targetSlot: No[CardSlot] = None
        self.user.e_end_drawPhase += self.start_attack

    def after_init(self):
        self.oldPos = self.transf.pos

     # Hàm hàm hàm hàm hàm
    def dealDamage(self):
        occupy = self.getTarget().occupy
        if (not occupy) or not isinstance(occupy, Monster): return
        occupy.receiveDamage(self.attack)

    def receiveDamage(self, dmg: float):
        self.defense -= dmg
        if (self.defense <= 0.0):
            self.defense = 0.0
            if self.isDead: return
            self.isDead = True
            self.actions.append(self.action_death())

    def setTarget(self, slot: 'CardSlot'):
        self.targetSlot = slot

    def getTarget(self):
        if self.targetSlot and self.targetSlot.occupy: 
            return self.targetSlot
        
        self.targetSlot = self.user.opponent.getAny_frontFirstSlot()
        return self.targetSlot

    def interact(self, target: No['CardSlot']):
        if (target is None) or (target.occupy is None): return
        if self.user.myId == target.myId: return # Đánh đồng đội
        self.user.quickAction_left -= 1
        self.targetSlot = target
        self.actions.append(self.action_attack())

    def start_attack(self):
        if self.user.opponent.isEmpty(): return
        self.actions.append(self.action_attack())

    # Yield yield yield
    def action_attack(self, speed = 1.0):
        '''Mặc định: đi đến target, animation đánh, đánh target, rồi về chỗ cũ'''
        yield from self.moveTo_target(self.getTarget(), speed * 0.4)
        yield from self.anim_attack(0.2)
        self.dealDamage()
        yield from self.moveBack(speed * 0.4)

        self.e_attackFinished.notify()

    def action_death(self):
        death = Motion.ease_in_cubic(255, 0, 0.5)
        Sounds.play("die.mp3", Volume.effects)
        # Monster.sfx_death.play()
        while not death.completed:
            self.img.overlay_alpha ^= 255
            self.img.alpha = death.value
            yield

        if self.slot: self.slot._occupy = None
        self.go.destroy()



    # Hàm hỗ trợ gốc
    def moveTo_pos(self, target: vec, time = 1.0):
        motion = Motion.linear(self.transf.pos, target, time)
        while not motion.completed:
            self.transf.pos = motion.value
            yield
        self.transf.pos = motion.dest

    def anim_attack(self, time = 0.5):
        '''Xoay 360 độ xong đứng đó nhìn'''
        oldRot = self.transf.rot
        rotate = Motion.ease_in(oldRot, oldRot + 360, time)
        while not rotate.completed:
            self.transf.rot = rotate.value
            yield

        self.transf.rot = rotate.dest
        afk = Motion.sleep(time * 0.5)
        while not afk.completed: yield

        self.transf.rot = oldRot



    # Hàm hỗ trợ bổ sung
    def moveBack(self, time = 1.0):
        yield from self.moveTo_pos(self.oldPos, time)

    def moveTo_target(self, target: 'CardSlot', time = 1.0):
        yield from self.moveTo_pos(target.transf.g_pos, time)



class MonsterUI(Component):
    def build(self):
        ui = GameObject("Monster UI", self.attach.go, pos=(-50, 0), enable_scale = False)

        self.health = Image("icon\\heart.png", (20, 20)).build(parent=ui)\
                        .addComponent(Text("0?", Color.white, 16))

        self.attack = Image("icon\\sword.png", (40, 40)).build(parent=ui, pos=(20, 20))\
                        .addComponent(Text("0?", Color.white, 16))

        return ui.addComponent(self)

    def __init__(self, attach: 'Monster', barWidth = 100, easeTime = 0.4):
        self.barWidth = barWidth
        self.oldRatio = 1
        self.oldDefense = attach.maxDefense
        self.ratio = 1
        self.easeTime = easeTime
        self.attach = attach
        self.ratioMotion = Motion.linear(1, attach.maxDefense / attach.defense, easeTime)

    def update_logic(self):
        self.health.text = str("%.0f" % self.attach.defense)
        self.attack.text = str(self.attach.attack)
        if self.oldDefense != self.attach.maxDefense:
            self.oldDefense = self.attach.maxDefense
            self.ratioMotion = Motion.linear(1, self.attach.maxDefense / self.attach.defense, self.easeTime)

    def update_render(self):
        pg.draw.rect(App.screen, Color.white,   (self.transf.g_pos, (self.barWidth * self.oldRatio, 10)))
        pg.draw.rect(App.screen, Color.green,   (self.transf.g_pos, (self.barWidth * self.ratio, 10)))
        pg.draw.rect(App.screen, Color.black,   (self.transf.g_pos, (self.barWidth, 10)), 2)

        self.oldRatio = self.ratioMotion.value


class Spell(Summon):
    @staticmethod
    def tryPlace(card: 'Card', data: SpellData, slot: No['CardSlot']):
        if data.globalUse: # Đặt đâu chả được
            data.spell(data, card.user, slot).build(card.transf.g_pos)
            return True
        if (slot is None) or (not slot.occupy): return False
        data.spell(data, card.user, slot).build(slot.transf.g_pos)
        return True

    def build(self, pos: vec):
        mon = Image(self.data.get_placedPath(), (150, 135), True, True).build(pos=pos) + self
        self.img = mon.getComponent(Image)
        return self

    def __init__(self, data: SpellData, *a):
        super().__init__(*a)
        self.data = data
        self.actions.append(self.on_use())

    def effect_on(self, target: 'Summon'):
        if isinstance(target, Monster):
            target.attack *= 2
            target.transf.scale.x *= 1.4

    def activate(self):
        if self.data.globalUse:
            for slot in self.user.get_occupiedSlots():
                self.effect_on(slot.force_occupy)
        elif self.slot.occupy:
            self.effect_on(self.slot.occupy)

    def anim_zoomOut(self, speed = 1.0):
        zoom = Motion.ease_out(1.0, 4.0, speed)
        spin = Motion.ease_out(-30, 30, speed)
        fade = Motion.linear(255, 0, speed)
        while not zoom.completed:
            self.transf.scale = vec(zoom.value)
            self.transf.rot = spin.value
            self.img.alpha = fade.value
            yield

    def on_use(self):
        '''Zoom out xong apply effects rồi bay màu luôn'''
        yield from self.anim_zoomOut(0.5)
        self.activate()
        self.go.destroy()

class Trap(Summon):
    @staticmethod
    def tryPlace(card: 'Card', data: TrapData, slot: 'CardSlot'):
        if (slot is None) or (slot.occupy): return False # Không có khỏi cho để
        if slot.myId >= 5: return False # Chỗ cho trap
        data.trap(data, card.user, slot).build(slot.transf.g_pos)
        return True

    def build(self, pos: vec):
        mon = Image(self.data.get_placedPath(), (150, 135), True, True).build(pos=pos, anchor=MIDBOTTOM) + self
        self.img = mon.getComponent(Image)

        return self

    def __init__(self, data: TrapData, *a):
        super().__init__(*a)
        self.data = data

class King(Monster):

    def after_init(self):
        super().after_init()
        self.maxDefense = self.defense = self.data.baseDEF * 10

    def action_death(self):
        self.user.e_king_die.notify()
        yield from super().action_death()


class Dragon(Monster):
    pass

class Rias(Monster):
    def build(self, pos: vec):
        side = -1 if self.user.rightSide else 1
        mon = Image(self.data.get_placedPath(), (200, 220), True, True)\
                    .build(pos=pos, anchor=MIDBOTTOM, scale=(side, 1)) + self
        self.img = mon.getComponent(Image)
        # self.anim = mon.addComponent(Animation("akeno/akeno aura", (400, 300), looping=True, playtime=1.0))
        # self.anim.activated = False # Chỉ bật khi combat

        beam = Animation("rias/rias_skill", (640, 480), True, override_hitbox=True).build(parent=self.go, anchor=MIDLEFT)
        self.uibeam = beam.getComponent(Animation)
        self.uibeam.activated = False

        self.boomer = GameObject("Boomer", self.go, startEnabled=False)
        for y in range(5):
            for x in range(5):
                boompos = (x * 150, (y - 1) * 150)
                Animation("common/fire boom", playtime=1.0).build(parent=self.boomer, pos=boompos, anchor=MIDBOTTOM)
        MonsterUI(self).build()
        return self
    
    def anim_attack(self, time=1.0):
        self.uibeam.activated = True
        # self.uibeam.playtime = time
        beambeam = Motion.sleep(time)
        while not beambeam.completed: yield

        self.uibeam.activated = False

    def indian_explosion(self, speed = 1.0):
        print("Indian explosion")
        self.boomer.enabled = True
        boom = Motion.sleep(speed)
        while not boom.completed: yield

        self.boomer.enabled = False

    def action_attack(self, speed = 1.0):
        # self.anim.activated = True
        # self.img.activated = False # Bị bug phần GIF, load GIF ghép 500ms trên khung hình :skull emoji:
        yield from self.moveTo_pos(App.vCenter, speed * 0.4)
        yield from self.anim_attack(0.2)
        yield from self.indian_explosion(speed)

        for slot in self.user.opponent.get_occupiedSlots():
            if not isinstance(slot.occupy, Monster): continue
            slot.occupy.receiveDamage(self.attack)

        yield from self.moveBack(speed * 0.4)

        # self.anim.activated = False
        # self.img.activated = True
        self.e_attackFinished.notify()



class NguyenDJ(Monster):
    def after_init(self):
        super().after_init()
        Sounds.play("nguyen dj.mp3", Volume.effects * 0.3)