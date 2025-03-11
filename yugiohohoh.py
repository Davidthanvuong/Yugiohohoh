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
#
#   Lưu ý: Tên monster có vài cái sai dẫn đến crash
#
########################################


if __name__ == '__main__':
    # TODO: Move to runtime data fetcher class?
    path = "assets\\images\\card"
    CardDeck.cardImages = [f for f in os.listdir(path) if 
                            os.path.isfile(os.path.join(path, f))]

    Pytnk.init()
    Hardcoded.create_all()    # Tạo prefab, chạy 1 lần cả đời là đủ

    print("Started game")
    Pytnk.start()
    # Pytnk.load_intro()
    Pytnk.load_maingame()

    while App.running:
        Pytnk.update()

    pg.quit()

