from pytnk.engine import *

class King(Monster):
    def action_death(self):
        print("The king is dead")
        death = Motion.ease_in_cubic(255, 0, 0.5)
        Sounds.play("die.mp3", Volume.effects)
        while not death.completed:
            self.img.overlay_alpha ^= 255
            self.img.alpha = death.value
            yield

        GameObject.root.childs.clear()
        GameObject.parents_stack.clear()
        StartMenu().build()

class Dragon(Monster):
    pass

class Rias(Monster):
    def build(self, pos: vec):
        forward = -1 if self.user.rightSide else 1
        mon = Image(self.data.get_placedPath(), (200, 220), True, True)\
                    .build(pos=pos, anchor=MIDBOTTOM, scale=(forward, 1)) + self
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

        self.img.overlay_color = Color.red if self.user.rightSide else Color.blue
        self.img.overlay_alpha = 100

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
        self.user.main.shake_screen(40)
        App.blackwhiteFilter = True
        self.boomer.enabled = True
        boom = Motion.sleep(speed)
        while not boom.completed: yield

        self.boomer.enabled = False
        App.blackwhiteFilter = False

    def action_attack(self, speed = 1.0):
        # self.anim.activated = True
        # self.img.activated = False # Bị bug phần GIF, load GIF ghép 500ms trên khung hình :skull emoji:
        yield from self.moveTo_pos(App.vCenter, speed * 0.4)
        yield from self.anim_attack(0.2)
        yield from self.indian_explosion(speed)

        for slot in self.user.opponent.get_frontSlots(OCCUPIED):
            if not isinstance(slot.occupy, Monster): continue
            slot.occupy.receiveDamage(self.attack)

        yield from self.moveBack(speed * 0.4)

        # self.anim.activated = False
        # self.img.activated = True
        print("Attack completed")
        self.e_attackFinished.notify()



class NguyenDJ(Monster):
    def after_init(self):
        super().after_init()
        Sounds.play("nguyen dj.mp3", Volume.effects * 0.3)


class SungJinWoo(Monster):
    def after_init(self):
        super().after_init()
        self.anim: No[Animation] = None
        self.superMode = False
        self.isInvincible = False
        self.user.battleState.e_begin += self.endInvincible

    def receiveDamage(self, dmg: float):
        super().receiveDamage(dmg, checkDeath=False)
        percent = self.defense / self.maxDefense

        if (not self.superMode) and (percent <= 0.1):
            print("Enabled invincible")
            self.isInvincible = True
            self.superMode = True
            self.attack *= 10
            self.anim = self.go.addComponent(Animation("common/normal aura", playtime=1.0, size=(100, 150)))

        if self.isInvincible:       # Hết invis thì thôi hết cứu
            self.defense = self.maxDefense * 0.1
        else:
            return self.deathCheck()

    def endInvincible(self):
        print("Disabled invincible")
        if self.anim: self.anim.activated = False
        self.isInvincible = False