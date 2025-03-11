from pytnk.engine import *

class Monster(Component):
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