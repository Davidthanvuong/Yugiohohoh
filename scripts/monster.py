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
        if slot.user.myId != card.user.myId: return False # Đặt nhầm phe kìa?
        if slot.myId < 5: return False # Chỗ cho trap
        data.monster(data, card.user, slot).build(slot.transf.g_pos)
        return True

    def build(self, pos: vec):
        forward = -1 if self.user.rightSide else 1
        mon = Image(self.data.get_placedPath(), (150, 135), True, True).build(pos=pos, anchor=MIDBOTTOM, scale=(forward, 1)) + self
        self.img = mon.getComponent(Image)
        self.img.overlay_color = Color.red if self.user.rightSide else Color.blue
        self.img.overlay_alpha = 100

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
        self.user.battleState.e_begin += self.start_attack

    def after_init(self):
        self.oldPos = self.transf.pos

     # Hàm hàm hàm hàm hàm
    def dealDamage(self):
        occupy = self.getTarget().occupy
        if (not occupy) or not isinstance(occupy, Monster): return
        occupy.receiveDamage(self.attack)

    def deathCheck(self):
        if (self.defense > 0.0): return
        self.defense = 0.0
        if self.isDead: return
        self.isDead = True
        self.e_attackFinished.notify()
        self.actions.append(self.action_death())

    def receiveDamage(self, dmg: float, checkDeath = True):
        oldDef = self.defense
        self.defense -= dmg
        if checkDeath: self.deathCheck()
        DamagePooling.spawn_number(int(oldDef - self.defense), self.transf.g_pos)

    def setTarget(self, slot: 'CardSlot'):
        self.targetSlot = slot

    def getTarget(self):
        if self.targetSlot and self.targetSlot.occupy: 
            return self.targetSlot
        
        self.targetSlot = self.user.opponent.choose_frontSlot(OCCUPIED)
        return self.targetSlot

    def interact(self, target: No['CardSlot']):
        if (target is None) or (target.occupy is None): return
        if self.user.myId == target.myId: return # Đánh đồng đội
        self.user.quickAction_left -= 1
        self.targetSlot = target
        self.actions.append(self.action_attack())

    def start_attack(self):
        print(f"{self.data.name}: {self.user.myId} bắt đầu tấn công")
        if self.user.opponent.isEmpty(FRONT): return
        self.actions.append(self.action_attack())

    # Yield yield yield
    def action_attack(self, time = 1.0):
        '''Mặc định: đi đến target, animation đánh, đánh target, rồi về chỗ cũ'''
        yield from self.moveTo_target(self.getTarget(), time * 0.4)
        yield from self.anim_attack(time)
        self.dealDamage()
        yield from self.moveBack(time * 0.4)

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

    def anim_attack(self, time = 1.0):
        '''Xoay 360 độ xong đứng đó nhìn'''
        rotate1 = Motion.ease_in(0, 30, time * 0.25)
        while not rotate1.completed:
            self.transf.rot = rotate1.value
            yield

        rotate2 = Motion.ease_out(30, -60, time * 0.25)
        while not rotate2.completed:
            self.transf.rot = rotate2.value
            yield

        rotate3 = Motion.ease_in(-60, 0, time * 0.15)
        while not rotate3.completed:
            self.transf.rot = rotate3.value
            yield

        afk = Motion.sleep(time * 0.35)
        while not afk.completed: yield

        self.transf.rot = 0.0


    # Hàm hỗ trợ bổ sung
    def moveBack(self, time = 1.0):
        yield from self.moveTo_pos(self.oldPos, time)

    def moveTo_target(self, target: 'CardSlot', time = 1.0):
        yield from self.moveTo_pos(target.transf.g_pos, time)



class MonsterUI(Component):
    def build(self):
        ui = GameObject("Monster UI", self.attach.go, pos=(0, 0), enable_scale = False)

        self.health = Image("icon\\heart.png", (20, 20)).build(parent=ui, pos=(-50, 0))\
                        .addComponent(Text("0?", Color.white, 16))

        self.attack = Image("icon\\sword.png", (40, 40)).build(parent=ui, pos=(-30, 20))\
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
        if self.oldDefense != self.attach.defense:
            self.oldDefense = self.attach.defense
            self.ratio = self.attach.defense / self.attach.maxDefense
            self.ratioMotion = Motion.linear(self.oldRatio, self.ratio, self.easeTime)

    def update_render(self):
        pos = self.transf.g_pos - FORWARD * 50
        pg.draw.rect(App.screen, Color.white,   (pos, (self.barWidth * self.oldRatio, 10)))
        pg.draw.rect(App.screen, Color.green,   (pos, (self.barWidth * self.ratio, 10)))
        pg.draw.rect(App.screen, Color.black,   (pos, (self.barWidth, 10)), 2)

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
            for slot in self.user.get_frontSlots(OCCUPIED):
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