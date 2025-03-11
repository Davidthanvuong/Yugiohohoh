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
#   - Bug: Drag thẻ bài đối phương sẽ báo lỗi (đang sửa cho skill đó)
#   - Bug: Click CardSlot lâu lâu bị giữ lại và không nhả ra được
# 
#   - Vẫn chưa sinh thêm thẻ hay cho opponent tấn công
#
########################################


if __name__ == '__main__':
    # TODO: Move to runtime data fetcher class?
    path = "assets\\images\\card"
    CardDeck.cardImages = [f for f in os.listdir(path) if 
                            os.path.isfile(os.path.join(path, f))]

    Pytnk.start()
    IntroSeq.create_default()
    # Maingame_beginSeq.create_default()

    while App.running:
        Pytnk.update()

    pg.quit()

