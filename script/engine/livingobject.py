from .gameobject import *

class LivingObject(GameObject):
    def __init__(self, maxhealth: float = 15, **kwargs):
        super().__init__(**kwargs)
        self.maxhealth = maxhealth
        self.health = maxhealth * 0.8

    # @abstractmethod
    # def update(self): pass
    
    # @abstractmethod
    # def onHover(self): pass

    # @abstractmethod
    # def onClick(self): pass

    @abstractmethod
    def onDeath(self): pass

    @abstractmethod
    def onDebug(self): pass