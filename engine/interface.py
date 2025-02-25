from importer.pygame import *
from .transform import Transform

from .abstract_renderer import render

class IClickable():
    '''Interface cho tính năng lướt, click, kéo, thả chuột'''
    def __init__(self, host: Transform, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.clickable = False
        self.draggable = False # Cho phép kéo thả
        self.init = False
        
    def after_init(self):
        self.white = Transform(
            imgpath="white.png", 
            imgsize=self.host.size, 
            pivot=self.host.pivot)

    def iclickable_update(self):
        '''Cập nhật của interface sẽ kiểm xem chuột\n
        hiện đang làm gì hitbox vật hiện theo dõi (host)'''
        if not self.init:
            self.after_init()
            self.init = True
        render(self.white)
        #TASK: QuanDNA
            

    @abstractmethod
    def on_startHover(): pass
    
    @abstractmethod
    def on_startClick(): pass
    
    @abstractmethod
    def on_stopHover(): pass
    
    @abstractmethod
    def on_stoClick(): pass
    
    @abstractmethod
    def on_hovering(): pass
    
    @abstractmethod
    def on_clicking(): pass