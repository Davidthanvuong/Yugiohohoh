from pytnk.engine import *
from typing import Generator

#     def trigger_support(self, slot: CardSlot):
#         print(f"[{self.go.name}] Supporting")
#         self.moving = True
#         self.targetPos = slot.transf.g_pos
#         if self.user:
#             self.user.turn_heroActionLeft -= 1

class Spell(Component):
    @staticmethod
    def create(pos: vec, data: SpellData, *a):
        spe = GameObject('Spell', pos=(pos.x, pos.y))
        spe += Image(f"card\\{data.img_path}", (150, 240), overrideHitbox=True)
        spe += Spell(data, *a)

        return spe

    def __init__(self, data: SpellData, slot: No[CardSlot] = None, isOpponent: No[bool] = None):
        self.data = data
        self.action: No[Generator] = None

        if self.data.globalUse:
            assert isOpponent is not None
            self.isOpponent = isOpponent
        else:
            assert slot is not None
            self.slot = slot

    def after_init(self):
        self.com_img = self.go.getComponent(Image)

    def update_logic(self):
        if self.action:
            try: next(self.action)
            except StopIteration:
                self.action = None
        else:
            self.action = self.on_use()

    def effect_on(self, target: 'Monster'):
        target.attack *= 2
        target.transf.scale.x *= 1.4

    def activate(self):
        if self.data.globalUse:
            for slot in CardSlot.get_occupiedSlots(self.isOpponent):
                self.effect_on(slot.occupy)
        elif self.slot.isOccupied():
            self.effect_on(self.slot.occupy)
        else:
            print("[WARNING] Do nothing")

    def anim_zoomOut(self, speed = 1.0):
        zoom = Motion.ease_out(1.0, 4.0, speed)
        spin = Motion.ease_out(-30, 30, speed)
        fade = Motion.linear(255, 0, speed)
        while not zoom.completed:
            self.transf.scale = vec(zoom.value)
            self.transf.rot = spin.value
            self.com_img.shared.native.set_alpha(fade.value)
            yield

        self.com_img.shared.native.set_alpha(255)

    def on_use(self):
        '''Zoom out xong apply effects rồi bay màu luôn'''
        yield from self.anim_zoomOut(0.5)
        self.activate()
        self.go.destroy()


class Trap(Component):
    @staticmethod
    def create(pos: vec, data: TrapData, slot: No[CardSlot] = None):
        print("[TODO] Trap card")
        trap = GameObject('Trap', pos=(pos.x, pos.y))
        trap += Image(data.get_placedPath())
        trap += Trap(data, slot)
        return trap
    
    def __init__(self, data: TrapData, slot: No[CardSlot] = None):
        self.data = data
        self.slot = slot
        self.action: No[Generator] = None


class Monster(Component):
    '''Triệu hồi từ card, hoặc extra thấm nếu spawn từ Monster khác luôn'''
    sfx_death: pg.mixer.Sound

    @staticmethod
    def create(pos: vec, data: MonsterData, slot: No[CardSlot] = None):
        mon = GameObject('Monster', pos=(pos.x, pos.y), anchor=MIDBOTTOM)
        mon += Image(data.get_placedPath(), (150, 135), support_overlay=True, overrideHitbox=True)
        user = slot.user if slot else None
        com = mon.addComponent(data.monster(data, user, slot))

        MonsterUI.create(com)
        return mon

    @staticmethod
    def load_sound():
        Monster.sfx_death = get_sound("die")

    def __init__(self, data: MonsterData, user: No['UserControl'] = None, slot: No[CardSlot] = None):
        self.side = user.side if user else False
        self.data = data
        self.mySlot = slot
        self.user = user
        if slot: slot.occupy = self

        self.monsterName = data.name
        self.defense = self.maxDefense = data.baseDEF * 2
        self.attack = data.baseATK

        self.isAttacking = False
        self.isDead = False

        self.targetSlot: No[CardSlot] = None
        self.controlledTarget: No[CardSlot] = None    # Đè lên target gốc
        self.actions: list[Generator] = []

        from .playercontrol import UserControl
        UserControl.e_endPhase += self.on_endPhase

    def after_init(self):
        self.com_img = self.go.getComponent(Image)
        self.oldPos = self.transf.pos

    def update_logic(self):
        if len(self.actions) == 0: return
        for act in list(self.actions):
            try: next(act)
            except StopIteration:
                self.actions.remove(act)

    def update_render(self):
        if not pgpeek(pg.KEYDOWN): return
        if not pg.key.get_pressed()[pg.K_SPACE]: return
        # Đè space để hiện relation line

        target = self.tryGetTarget()
        if not target: return
        color = Color.forward if self.side else Color.freedom

        pg.draw.line(App.screen, color, self.transf.g_pos + UPWARD * 3 * self.side, target.transf.g_pos, 2)

    def on_endPhase(self, user: 'UserControl'):
        '''Đánh lần lượt khi hết phase của người chơi'''
        if user.side != self.side: return
        if CardSlot.isAnySideEmpty(): return
        self.actions.append(self.action_attack(uniform(0.5, 2.0)))

    # Hàm hàm hàm hàm hàm
    def dealDamage(self):
        self.getTarget().occupy.receiveDamage(self.attack)

    def receiveDamage(self, dmg: float):
        self.defense -= dmg
        if (not self.isDead) and (self.defense <= 0.0):
            self.defense = 0.0
            self.isDead = True
            self.actions.append(self.action_death())

    def setTarget(self, slot: CardSlot):
        self.targetSlot = slot

    def getTarget(self) -> CardSlot:
        target = self.tryGetTarget()
        if not target: raise ValueError("No target found")
        return target

    def tryGetTarget(self) -> CardSlot | None:
        if self.controlledTarget and self.controlledTarget.isOccupied():
            return self.controlledTarget
        self.controlledTarget = None

        if self.targetSlot and self.targetSlot.isOccupied():
            return self.targetSlot

        if CardSlot.isEmpty(not self.side):
            return None
        
        self.targetSlot = CardSlot.getAny_occupiedFrontSlot(not self.side)
        return self.targetSlot

    # Yield yield yield
    def action_attack(self, speed = 1.0):
        '''Mặc định: đi đến target, animation đánh, đánh target, rồi về chỗ cũ'''
        self.isAttacking = True

        yield from self.moveTo_target(self.getTarget(), speed * 0.4)
        yield from self.anim_attack(0.2)
        self.dealDamage()
        yield from self.moveBack(speed * 0.4)

        self.isAttacking = False
        if self.user: self.user.turn_heroActionLeft -= 1


    def action_death(self):
        death = Motion.linear(0, 1, 1.0)
        Monster.sfx_death.play()
        while not death.completed:
            self.com_img.overlay_opacity ^= 255
            yield

        if self.mySlot: self.mySlot.occupy = None
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

    def moveTo_target(self, target: CardSlot, time = 1.0):
        yield from self.moveTo_pos(target.transf.g_pos, time)

    # def on_attack(self): pass
    # def on_defend(self): pass
    # def on_support(self): pass
    # def on_death(self): pass
    # def on_useSkill(self): pass
    # def on_chargeSkill(self): pass

    # def bot_evaluate(self): return 1.0

    # def receiveDamage(self, source: 'Monster', damage: float): pass
    # def previewAttack(self): pass
    # def moveToward(self, dest: vec, time: float): pass
    


'''Gà code, ghét hướng đối tượng? Đừng lo. 
Đã có hàm thập cẩm. Cân mọi loại nhu cầu cho quái common'''
class Dragon(Monster): pass

def dragon_attack(self: Dragon, speed = 1.0):
    self.isAttacking = True # TODO: Refactor lại OpponentControl để loại luôn biến này

    yield from self.moveTo_target(self.getTarget(), 0.4)
    yield from self.anim_attack(1)
    self.dealDamage()
    yield from self.moveBack(0.4)

    self.isAttacking = False
    if self.user: self.user.turn_heroActionLeft -= 1

Dragon.action_attack = dragon_attack