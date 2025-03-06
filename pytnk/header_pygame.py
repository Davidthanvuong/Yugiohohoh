# Standalone
from pygame.event import peek as pgpeek
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from random import randint as rint
from random import choice
from .data import *

# Engine
from .event import Event
from .window import Scene, Window, Scope
from .gameobject import Component, GameObject#, Transform
from .image import Image, Text, FontPreset, SharedImage
from .menu import Menu
from .iclickable import IClickable
from .flexarray import FlexArray
from .editors.menus import MaingameMenu, InspectorMenu, HierarchyMenu, AssetsMenu

# Assets
from assets.scripts import *

# Afterload
from .sceneloader import SceneLoader


#from .inputfield import InputField
#from .editor import InspectorMenu, HierarchyMenu, AssetsMenu, load_editors

#from assets.scripts.card import Card, CardDeck

#from .maingame import Maingame
# from .abstract_renderer import render
# from .transform import Transform, Component
# from .image import Image, Text
# from .ui import IClickable, FlexibleMenu
# from .editor_inspector import DataField, DataTask, ToggleHeader, Inspector
# from .editor import Editor
