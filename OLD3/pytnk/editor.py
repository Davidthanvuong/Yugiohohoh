from .header_pygame import *

class Editor(Component):
    inst: 'Editor'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Editor.inst = self