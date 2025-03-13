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
#   Thả lên trên ô của mình bên trái mới triệu hồi được
#
#   Hiện tại chưa implement Spell card hay Trap card
#   Bot thực hiện được 2 chức năng nếu có thể:
#   - Đánh đối phương
#   - Đặt lá xuống bàn
#
#   Bug: 
#   - Game bắt đầu từ đối phương bị bug thẻ bài 
#        từ đâu xuất hiện không đúng chỗ
#   - Đổi action lúc chết dẫn đến quái bất tử
#
########################################


if __name__ == '__main__':
    Pytnk.start()
    # IntroSeq.create()
    Maingame_beginSeq.create()

    while App.running:
        Pytnk.update()

    pg.quit()

