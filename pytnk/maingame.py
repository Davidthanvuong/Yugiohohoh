from .header_pygame import *

class Maingame(Component):
    inst: 'Maingame'

    def __init__(self, **kwargs):
        Maingame.inst = self        
        tf = Transform('Maingame', ZERO, ZERO, Window.native, Game.inst.tf)
        tf.root = Transform.roots['Maingame'] = (tf, pg.Surface(Window.native, pg.SRCALPHA))
        Image(bind=tf, path="woodfloor.jpg", fit=True, standalone=True)
        Game.maingameTf = tf

        super().__init__(bind=tf, **kwargs)