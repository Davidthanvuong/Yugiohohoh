import pygame as pg
import os
from pygame.event import peek as pgpeek
from pygame.font import Font
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from random import randint as rint
from random import choice
from time import time
from typing import Optional as No
from weakref import WeakMethod as weak
from weakref import ref
from typing import Callable, Generic, TypeVar
from .data import *

# Engine
from .event import Event, Mouse, Motion
from .gameobject import Component, Transform, GameObject
from .renderer import Renderer, Image, Text
from .iclickable import IClickable

from .particlesystem import ParticleSystem

# Shader
from assets.scripts.shader_burning import Shader_BurningCard, ColorBlend, Blendkey
from assets.scripts.shader_popupText import Shader_PopupText

# Code
from assets.scripts.summon import Summon
from assets.scripts.monster import Monster
from assets.scripts.monsterui import MonsterUI
from assets.scripts.card import Card, CardDeck, CardSpot

# Manager
from assets.scripts.battlecontroller import BattleController
from assets.scripts.playercontrol import UserControl, PlayerControl
from assets.scripts.opponentcontrol import OpponentControl

# Engine 2
from .sequence import Sequence, LoadingSeq, IntroSeq, MaingameSeq
from .hardcoded import Hardcoded
from .pytnk import Pytnk