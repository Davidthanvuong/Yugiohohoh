from .engine import *

class Maingame(Component):
    @staticmethod
    def create(oppoStartFirst = False):
        game = GameObject('Maingame Scene')

        player = PlayerControl.create(game)
        oppon = OpponentControl.create(game)

        if oppoStartFirst:
            oppon.getComponent(OpponentControl).startPhase()
        else: player.getComponent(PlayerControl).startPhase()

        game += Maingame(player, oppon)
        return game
    
    def __init__(self, player: GameObject, oppo: GameObject):
        self.user1_played = False
        self.user2_played = False

        self.user1 = player.getComponent(PlayerControl)
        self.user2 = oppo.getComponent(OpponentControl)
        UserControl.e_endPhase += self.listen_endPhase

    # def after_init(self):        

    def listen_endPhase(self, user: UserControl):
        print(f"[Maingame] {user.go.name} đã kết thúc lượt")
        if user.isOpponent:
            self.user2_played = True
        else: self.user1_played = True

        if self.user1_played and self.user2_played:
            self.user1_played = False
            self.user2_played = False
            print("[Maingame] Cả 2 thằng đều đã chơi")
            print("[Maingame] Hô hô, bốc thêm lá nào")
            
            self.user1.drawPhase()
            self.user2.drawPhase()