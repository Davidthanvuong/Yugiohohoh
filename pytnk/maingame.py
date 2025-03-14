from .engine import *
from typing import Generator, cast

class Maingame(Component):
    @staticmethod
    def create(oppoStartFirst = False):
        game = GameObject('Maingame Scene')

        player = PlayerControl.create(game)
        oppon = OpponentControl.create(game)

        popup = Shader_PopupText.create()

        if oppoStartFirst:
            oppon.getComponent(OpponentControl).startPhase()
        else: player.getComponent(PlayerControl).startPhase()

        game += Maingame(player, oppon, popup)
        return game
    
    def __init__(self, player: GameObject, oppo: GameObject, popup: GameObject):
        self.user1_played = False
        self.user2_played = False

        self.user1 = player.getComponent(PlayerControl)
        self.user2 = oppo.getComponent(OpponentControl)
        self.popup = popup.getComponent(Shader_PopupText)
        UserControl.e_endPhase += self.listen_endPhase
        King.e_onDeath += self.listen_defeat
        self.popup.playText("Starting game")

        self.action: No[Generator] = None
        self.loser: No[King] = None
        self.spawned = False
        self.spawnTime = Motion.linear(0, 1, 1.0)

    def update_logic(self):
        if not self.spawned and self.spawnTime.completed:
            self.spawned = True

            from assets.scripts.carddata import database
            player = CardSlot.sides[PLAYER][2]
            oppo = CardSlot.sides[OPPONENT][10]
            print(player.transf.g_pos, oppo.transf.g_pos)
            Monster.create(player.transf.g_pos, cast('MonsterData', database['King']), player)
            Monster.create(oppo.transf.g_pos, cast('MonsterData', database['King']), oppo)

        if self.action:
            try: next(self.action)
            except StopIteration:
                self.action = None

    def listen_endPhase(self, user: UserControl):
        print(f"[Maingame] {user.go.name} đã kết thúc lượt")
        if user.side == OPPONENT:
            self.user2_played = True
            self.popup.playText("Your's turn")
        else: 
            self.user1_played = True
            self.popup.playText("Opponent's turn")

        if self.user1_played and self.user2_played:
            self.user1_played = False
            self.user2_played = False
            print("[Maingame] Cả 2 thằng đều đã chơi")
            print("[Maingame] Hô hô, bốc thêm lá nào")
            
            self.user1.drawPhase()
            self.user2.drawPhase()

    def listen_defeat(self, king: King):
        if self.loser: return

        print(f"[Maingame] {king.go.name} đã bị tiêu diệt")
        self.loser = king
        self.action = self.endGame()

        es = self.endScreen = GameObject('End Screen', anchor=CENTER, pos=App.center)
        path = "victory.jpg" if king.side == OPPONENT else "defeat.jpg"
        self.endImg = cast(Image, es.addComponent(Image(path, App.native, support_overlay=True)))

        re = Restart.create(self)

    def endGame(self):
        fadein = Motion.linear(0, 200, 1.0)
        while not fadein.completed:
            self.endImg.overlay_opacity = fadein.value
            yield

        self.endImg.overlay_opacity = 200



class Restart(IClickable):
    @staticmethod
    def create(mg: Maingame):
        restart = GameObject('Restart', anchor=CENTER, pos=App.center)
        restart += Image("icon/white.png", (300, 100), support_overlay=True, overrideHitbox=True)
        restart += Text("Click to restart")
        restart += Restart(mg)
        return restart
    
    def __init__(self, mg: Maingame):
        super().__init__()
        self.mg = mg

    def on_startClick(self):
        GameObject.root.childs = []

        from pytnk.sequence import LoadingSeq
        LoadingSeq.create()
        CardSlot.sides = ([], [])
        self.go.enabled = False