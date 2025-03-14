from .engine import *

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
        self.popup.playText("Starting game")

    # def after_init(self):        

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