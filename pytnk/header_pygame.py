from pygame import Vector2 as vec
from pygame.event import peek as pgpeek
from dataclasses import dataclass
from typing import Optional as No
from abc import abstractmethod
from enum import Enum
from .config import *

tff = tuple[float, float]

ALLOW_DEVELOPER = True
TOPLEFT = ZERO = (0, 0)
CENTER = (0.5, 0.5)
ONE = (1, 1)

from .transform import Transform, Component
from .game import MouseInfo, mouse, Game
from .iclickable import IClickable
from .flexarray import FlexArray
from .image import Image, Text
from .inputfield import InputField
from .maingame import Maingame
from .editor import InspectorMenu, HierarchyMenu, AssetsMenu, load_editors

from assets.scripts.card import Card, CardDeck

#from .maingame import Maingame
# from .abstract_renderer import render
# from .transform import Transform, Component
# from .image import Image, Text
# from .ui import IClickable, FlexibleMenu
# from .editor_inspector import DataField, DataTask, ToggleHeader, Inspector
# from .editor import Editor