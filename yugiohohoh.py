from pytnk.engine import *


#   _   _        _  _                                  _      _  _ 
#  | | | |      | || |                                | |    | || |
#  | |_| |  ___ | || |  ___     __      __ ___   _ __ | |  __| || |
#  |  _  | / _ \| || | / _ \    \ \ /\ / // _ \ | '__|| | / _` || |
#  | | | ||  __/| || || (_) |_   \ V  V /| (_) || |   | || (_| ||_|
#  \_| |_/ \___||_||_| \___/( )   \_/\_/  \___/ |_|   |_| \__,_|(_)
#                           |/                                     
#
########## Dành cho developer ##########
#
#   Thả card xuống phía dưới để undo việc triệu hồi
#   Hiện tại chưa có cách đặt đúng quái / bảng triệu hồi của đối phương
#   Intro vẫn chưa được thống nhất, có ý tưởng nhớ nói (Pytnk.load_intro())
#
#   Bug thành chức năng đi: Lá spell cho phép bóc lá của đối phương (nhưng không được nhìn)
#
########################################


if __name__ == '__main__':
    Pytnk.init()
    # Hardcoded.create_all()    # Tạo prefab, chạy 1 lần cả đời là đủ

    Pytnk.start()
    Pytnk.load_intro()
    # Pytnk.load_maingame()

    while App.running:
        Pytnk.update()

    pg.quit()

