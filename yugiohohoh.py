from time import time
from pytnk.header_pygame import *

#   _   _        _  _                                  _      _  _ 
#  | | | |      | || |                                | |    | || |
#  | |_| |  ___ | || |  ___     __      __ ___   _ __ | |  __| || |
#  |  _  | / _ \| || | / _ \    \ \ /\ / // _ \ | '__|| | / _` || |
#  | | | ||  __/| || || (_) |_   \ V  V /| (_) || |   | || (_| ||_|
#  \_| |_/ \___||_||_| \___/( )   \_/\_/  \___/ |_|   |_| \__,_|(_)
#                           |/                                     

 
if __name__ == '__main__':
    world = Window()("Hello")  

    SceneLoader.create_maingameScene()
    if ALLOW_DEVELOPER:
        SceneLoader.create_editorScenes()
    
    while Window.running:
        world.inputHandle()
        world.mainLoop()
        world.outputHandle()

    pg.quit()