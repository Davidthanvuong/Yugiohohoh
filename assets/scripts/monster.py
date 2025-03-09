from pytnk.engine import *

class Monster(IClickable):
    e_attackPhase: Event = Event()
    e_defensePhase: Event = Event()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.defense = self.maxDefense = 100
        self.attack = 20
        self.deathTime = 0.0
        self.deathFlash = False
        Monster.e_attackPhase += self.attack_phase
        Monster.e_defensePhase += self.defense_phase

    def start(self):
        self.com_render = self.go.getComponent(Image)

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