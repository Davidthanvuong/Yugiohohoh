from importer.pygame import *
from .transform import Transform

from .abstract_renderer import render

class IClickable():
    '''Interface cho tính năng lướt, click, kéo, thả chuột'''
    def __init__(self, host: Transform, clickable = True, draggable = False, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.clickable = clickable
        self.draggable = draggable # Cho phép kéo thả
        self.white = Transform(
            imgpath="white.png", 
            imgsize=self.host.imgsize,
            parent=self.host, 
            pivot=self.host.pivot)

    def iclick_update(self):
        '''Cập nhật của interface sẽ kiểm xem chuột\n
        hiện đang làm gì hitbox vật hiện theo dõi (host)'''
        render(self.white)
        
        #TASK: QuanDNA
        #Check bằng pt của chatgpt
        #chạy đống hàm ở dưới.
        #on_start: vừa mới chạm
        #on_-ing: đang
        #on_stop: vừa mới ngưng
            
    @abstractmethod
    def on_startHover(self): pass
    
    @abstractmethod
    def on_startClick(self): pass
    
    @abstractmethod
    def on_stopHover(self): pass
    
    @abstractmethod
    def on_stoClick(self): pass
    
    @abstractmethod
    def on_hovering(self): pass
    
    @abstractmethod
    def on_clicking(self): pass