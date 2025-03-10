from pytnk.engine import *

class Monster(IClickable):
    '''Triệu hồi từ card, hoặc extra thấm nếu spawn từ Monster khác luôn'''
    e_attackPhase: Event = Event()
    e_defensePhase: Event = Event()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.defense = self.maxDefense = 100
        self.attack = 20
        self.deathTime = 0.0
        self.deathFlash = False
        self.moving = False
        self.startMoving = False

        # TODO: Có lẽ nên implement class Motion cho đỡ dài dòng phần di chuyển
        self.targetPos = vec(ZERO)
        self.oldPos = vec(ZERO)
        Monster.e_attackPhase += self.attack_phase
        Monster.e_defensePhase += self.defense_phase

    def start(self):
        self.com_render = self.go.getComponent(Image)

        # Con mej mafy di chuyển qua Hardcode đi
        ui = GameObject("UI", self.go, pos=(-50, 0))

        health = GameObject('1', ui, pos=(0, 0)) 
        health += Image("icon\\heart.png", (20, 20))
        health += Text("200", size=16)

        attack = GameObject('2', ui, pos=(20, 20))
        attack += Image("icon\\sword.png", (40, 40))
        attack += Text("800", size=16)

        ui += MonsterUI(self)
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
            if self.transf.pos.distance_squared_to(self.targetPos) < 1:
                self.moving = False
                self.startMoving = False
                self.transf.pos = self.oldPos

    def on_startHover(self):
        self.com_img.flashing = True

    def on_stopHover(self):
        self.com_img.flashing = False

    def on_startClick(self):
        self.attack_phase()

    def attack_phase(self):
        print(f"Attack phase {self.go.name}")
        self.defense -= 10.0

    def defense_phase(self):
        print(f"Defense phase {self.go.name}")

    def receive_damage(self, dmg: float):
        self.defense -= dmg
        if self.defense <= 0.0:
            self.defense = 0.0

    def on_death(self):
        if self.deathTime == 0.0:
            self.deathTime = time()

        self.deathFlash = not self.deathFlash
        self.com_img.flashing = self.deathFlash
        dt = time() - self.deathTime
        if dt >= 1.0:
            self.go.destroy()