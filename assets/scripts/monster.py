from pytnk.engine import *

from pytnk.engine import *

class Monster(Component):
    '''Triệu hồi từ card, hoặc extra thấm nếu spawn từ Monster khác luôn'''

    @staticmethod
    def create(pos: vec, data: MonsterData, slot: No['CardSlot'] = None):
        mon = GameObject('Monster', pos=(pos.x, pos.y), anchor=MIDBOTTOM)
        mon += Image(data.get_monsterPath(), (150, 135), overrideHitbox=True)
        user = slot.user if slot else None
        com = mon.addComponent(Monster(data, user, slot))

        MonsterUI.create(com)

        return mon

    def __init__(self, data: MonsterData, user: No['UserControl'] = None, slot: No['CardSlot'] = None):
        self.isOpponent = user.isOpponent if user else False
        self.slot = slot
        self.user = user
        if slot: 
            print(f"Yes I am totally fine ID {slot.myId}")
            slot.occupy = ref(self)

        self.defense = self.maxDefense = data.baseDEF
        self.attack = data.baseATK
        self.deathTime = 0.0
        self.deathFlash = False
        self.moving = False
        self.startMoving = False
        self.attacking = False

        # TODO: Có lẽ nên implement class Motion cho đỡ dài dòng phần di chuyển
        self.targetPos = vec(ZERO)
        self.targetSlot: 'CardSlot'
        self.oldPos = vec(ZERO)

    def after_init(self):
        self.com_img = self.go.getComponent(Image)

    def update_logic(self):
        if self.defense <= 0.0: 
            self.defense = 0.0
            self.on_death()

        if self.moving:
            if not self.startMoving:
                self.oldPos = self.transf.pos
                self.startMoving = True
                
            self.transf.pos = self.transf.pos.lerp(self.targetPos, 0.2)
            if self.transf.pos.distance_squared_to(self.targetPos) < 4:
                self.moving = False
                self.startMoving = False
                self.transf.pos = self.oldPos
                self.attacking = False
                occupy = self.targetSlot.getOccupy()
                occupy.receive_damage(self.attack)

    def trigger_attack(self, slot: 'CardSlot'):
        print(f"[{self.go.name}] Attacking")
        self.moving = True
        self.attacking = True
        self.targetSlot = slot
        self.targetPos = slot.transf.g_pos
        if self.user:
            self.user.turn_heroActionLeft -= 1

    def trigger_support(self, slot: 'CardSlot'):
        print(f"[{self.go.name}] Supporting")
        self.moving = True
        self.targetPos = slot.transf.g_pos
        if self.user:
            self.user.turn_heroActionLeft -= 1

    def receive_damage(self, dmg: float):
        self.defense -= dmg
        if self.defense <= 0.0:
            self.defense = 0.0

    def on_death(self): # TODO: Migrate sang Motion
        if self.deathTime == 0.0:
            self.deathTime = now()

        self.deathFlash = not self.deathFlash
        self.com_img.flashing = self.deathFlash
        dt = now() - self.deathTime
        if dt >= 1.0:
            if self.slot:
                self.slot.occupy = None
            self.go.destroy()

# class Monster2(Component):
#     '''Triệu hồi từ card, hoặc extra thấm nếu spawn từ Monster khác luôn'''

#     @staticmethod
#     def create(pos: vec, data: MonsterData, slot: No['CardSlot'] = None):
#         mon = GameObject('Monster', pos=(pos.x, pos.y), anchor=MIDBOTTOM)
#         mon += Image(data.get_monsterPath(), overrideHitbox=True)
#         user = slot.user if slot else None
#         com = mon.addComponent(Monster2(data, user, slot))

#         MonsterUI.create(com)

#         return mon

#     def __init__(self, data: MonsterData, user: No['UserControl'] = None, slot: No['CardSlot'] = None):
#         self.isOpponent = user.isOpponent if user else False
#         self.data = data
#         self.slot = slot
#         self.user = user
#         if slot: slot.occupy = ref(self)

#         self.monsterName = data.name
#         self.defense = self.maxDefense = data.baseDEF
#         self.attack = data.baseATK

#         self.deathTime = 0.0
#         self.deathFlash = False

#         self.targetSlot: No['CardSlot'] = None
#         self.controlledTarget: No['CardSlot'] = None    # Đè lên target gốc

#     def after_init(self):
#         self.com_img = self.go.getComponent(Image)

#     def update_logic(self):
#         pass

#     # Yield yield yield
#     def on_attack(self): pass
#     def on_defend(self): pass
#     def on_support(self): pass
#     def on_death(self): pass
#     def on_useSkill(self): pass
#     def on_chargeSkill(self): pass

#     # Hàm hỗ trợ
#     def bot_evaluate(self):
#         return 1.0
#     def receiveDamage(self, source: 'Monster', damage: float): pass
#     def previewAttack(self): pass
#     def moveToward(self, dest: vec, time: float): pass
#     def setTarget(self, slot: 'CardSlot'): pass
#     def getTarget(self) -> 'CardSlot':
#         '''Bốc target, không có thì lấy random'''
#         if self.controlledTarget:
#             return self.controlledTarget
#         if not self.targetSlot:
#             self.targetSlot = CardSlot.getAvailableSlot(self.isOpponent, not self.isOpponent, True)
#         return self.targetSlot


# '''Gà code, ghét hướng đối tượng? Đừng lo. 
# Đã có hàm thập cẩm. Cân mọi loại nhu cầu cho quái common'''
# class Dragon(Monster): pass

# def dragon_attack(self: Dragon):
#     target = self.getTarget()
#     self.moveToward(target.transf.g_pos, 0.5)

# Dragon.on_attack = dragon_attack
