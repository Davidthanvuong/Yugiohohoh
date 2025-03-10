from pytnk.engine import *

class PlayerControl(Component):
    e_playerAction: Event = Event()
    # TODO: Có thể thêm dữ liệu vô event, 
    # hoặc để sang nghe thụ động, lấy dữ liệu chủ độngđộng

    def on_startTurn(self):
        pass

    def on_endTurn(self):
        pass