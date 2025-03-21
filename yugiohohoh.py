from pytnk.engine import *
from pytnk.pytnk import Pytnk

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
    IntroSequence().build()
    # Maingame().build(startID=0)

    while App.running:
        Pytnk.update()

    pg.quit()