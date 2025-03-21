from pytnk.engine import *

#   _   _        _  _                                  _      _  _ 
#  | | | |      | || |                                | |    | || |
#  | |_| |  ___ | || |  ___     __      __ ___   _ __ | |  __| || |
#  |  _  | / _ \| || | / _ \    \ \ /\ / // _ \ | '__|| | / _` || |
#  | | | ||  __/| || || (_) |_   \ V  V /| (_) || |   | || (_| ||_|
#  \_| |_/ \___||_||_| \___/( )   \_/\_/  \___/ |_|   |_| \__,_|(_)
#                           |/                                     
#


if __name__ == '__main__':
    Pytnk.start()
    # IntroSeq.create()
    Maingame_beginSequence.create()

    while App.running:
        Pytnk.update()

    pg.quit()

