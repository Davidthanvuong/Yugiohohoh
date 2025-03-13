from pytnk.engine import *
from typing import Generator

#     def trigger_support(self, slot: CardSlot):
#         print(f"[{self.go.name}] Supporting")
#         self.moving = True
#         self.targetPos = slot.transf.g_pos
#         if self.user:
#             self.user.turn_heroActionLeft -= 1


class Monster(Component):
    '''Triệu hồi từ card, hoặc extra thấm nếu spawn từ Monster khác luôn'''

    @staticmethod
    def create(pos: vec, data: MonsterData, slot: No[CardSlot] = None):
        mon = GameObject('Monster', pos=(pos.x, pos.y), anchor=MIDBOTTOM)
        mon += Image(data.get_monsterPath(), (150, 135), overrideHitbox=True)
        user = slot.user if slot else None
        com = mon.addComponent(Monster(data, user, slot))

        MonsterUI.create(com)
        return mon

    def __init__(self, data: MonsterData, user: No['UserControl'] = None, slot: No[CardSlot] = None):
        self.isOpponent = user.isOpponent if user else False
        self.data = data
        self.mySlot = slot
        self.user = user
        if slot: slot.occupy = self

        self.monsterName = data.name
        self.defense = self.maxDefense = data.baseDEF
        self.attack = data.baseATK

        self.isAttacking = False
        self.isDead = False

        from .playercontrol import UserControl

        self.targetSlot: No[CardSlot] = None
        self.controlledTarget: No[CardSlot] = None    # Đè lên target gốc
        self.action: No[Generator] = None
        UserControl.e_endPhase += self.on_endPhase

    def after_init(self):
        self.com_img = self.go.getComponent(Image)
        self.oldPos = self.transf.pos

    def update_logic(self):
        if self.action:
            try: next(self.action)
            except StopIteration:
                self.action = None

    def update_render(self):
        if not pgpeek(pg.KEYDOWN): return
        if not pg.key.get_pressed()[pg.K_SPACE]: return
        # Đè space để hiện relation line

        target = self.tryGetTarget()
        if not target: return
        color = Color.forward if self.isOpponent else Color.freedom

        pg.draw.line(App.screen, color, self.transf.g_pos + UPWARD * 3 * self.isOpponent, target.transf.g_pos, 2)


    def on_endPhase(self, user: 'UserControl'):
        '''Đánh lần lượt khi hết phase'''
        if user.isOpponent != self.isOpponent: return
        if CardSlot.getState(allEmpty=True, search=not self.isOpponent): return
        self.action = self.action_attack()

    # Hàm hàm hàm hàm hàm
    def dealDamage(self):
        self.getTarget().occupy.receiveDamage(self.attack)

    def receiveDamage(self, dmg: float):
        self.defense -= dmg
        if (not self.isDead) and (self.defense <= 0.0):
            self.defense = 0.0
            self.isDead = True
            self.action = self.action_death()

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

        if CardSlot.getState(allEmpty=True, search=not self.isOpponent):
            return None
        
        self.targetSlot = CardSlot.getAvailableSlot(self.isOpponent, not self.isOpponent, True)
        return self.targetSlot

    # Yield yield yield
    def action_attack(self):
        '''Mặc định: đi đến target, animation đánh, đánh target, rồi về chỗ cũ'''
        self.isAttacking = True

        yield from self.moveTo_target(self.getTarget(), 0.4)
        yield from self.anim_attack(0.2)
        self.dealDamage()
        yield from self.moveBack(0.4)

        self.isAttacking = False
        if self.user: self.user.turn_heroActionLeft -= 1


    def action_death(self):
        death = Motion.linear(0, 1, 1.0)
        while not death.completed:
            self.com_img.flashing ^= True
            yield

        if self.mySlot: self.mySlot.occupy = None
        self.go.destroy()



    # Hàm hỗ trợ gốc
    def moveTo_pos(self, target: vec, time = 1.0):
        motion = Motion.linear(self.transf.pos, target, time)
        while not motion.completed:
            self.transf.pos = motion.value
            yield

    def anim_attack(self, time = 0.5):
        '''Xoay 360 độ xong đứng đó nhìn'''
        oldRot = self.transf.rot
        rotate = Motion.ease_in(oldRot, oldRot + 360, time)
        while not rotate.completed:
            self.transf.rot = rotate.value
            yield

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
    


# '''Gà code, ghét hướng đối tượng? Đừng lo. 
# Đã có hàm thập cẩm. Cân mọi loại nhu cầu cho quái common'''
# class Dragon(Monster): pass

# def dragon_attack(self: Dragon):
#     target = self.getTarget()
#     self.moveToward(target.transf.g_pos, 0.5)

# Dragon.on_attack = dragon_attack
