from typing import Optional as No
from typing import Callable, Generic, TypeVar, Generator, cast
import random, os, math
from dataclasses import dataclass
from random import randint as rint
from random import uniform as rfloat
from weakref import WeakMethod as weak
from weakref import ref
from time import time as now
from pygame.event import peek as pgpeek

# Standalone
from .data import *
from .event import Event, Mouse
from .motion import Motion
from .sound import Sounds, Volume
from .fsm import Phase, LinearStateMachine, FiniteState
# from .sound import Sound

# Component System
from .gameobject import Component, Transform, GameObject
from .iclickable import IClickable


# Renderer
from .renderer import LazySurface, LoadedImage, Image, Text, Blendkey, ColorBlend
from .anim import Animation
from scripts.shader_burning import Shader_BurningCard
from scripts.damageindicator import DamagePooling

# Data
from scripts.carddata import card_database, CardData, MonsterData, SpellData, TrapData

# Final
from scripts.sequence import IntroSeq, StartMenu

from scripts.monster import Summon, Monster, MonsterUI, Spell, Trap
from scripts.card import Card, CardDeck, CardSlot
from scripts.controller import Controller
from scripts.playercontroller import PlayerController, My_EndPhaseButton
from scripts.botcontroller import BotController
from scripts.maingame import Maingame

from scripts.carddata_implement import *