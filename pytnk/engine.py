import pygame as pg
import os
from pygame.event import peek as pgpeek
from pygame.font import Font
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from random import randint as rint
from random import uniform
from random import choice
from time import time as now
from typing import Optional as No
from weakref import WeakMethod as weak
from weakref import ref
from typing import Callable, Generic, TypeVar
from .data import *

# Engine
from .event import Event, Mouse
from .motion import Motion
from .gameobject import Component, Transform, GameObject
from .renderer import Renderer, Image, Text
from .iclickable import IClickable

from .particlesystem import ParticleSystem

# Shader
from assets.scripts.shader_burning import Shader_BurningCard, ColorBlend, Blendkey
from assets.scripts.shader_popupText import Shader_PopupText

# Code
from assets.scripts.monsterui import MonsterUI
from assets.scripts.monster import Monster
from assets.scripts.card import Card, CardDeck, CardSlot

# Manager
# from assets.scripts.battlemanager import BattleManager
from assets.scripts.playercontrol import UserControl, PlayerControl
from assets.scripts.opponentcontrol import OpponentControl

# Engine 2
from .maingame import Maingame
from .sequence import IntroSeq, StartMenu, LoadingSeq, Maingame_beginSeq
# from .hardcoded import Hardcoded
from .pytnk import Pytnk