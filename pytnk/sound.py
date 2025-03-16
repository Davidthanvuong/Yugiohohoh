import pygame as pg
from pygame.mixer import Sound
from dataclasses import dataclass

@dataclass(frozen=True)
class Volume:
    music = 0.5
    effects = 0.5

class Sounds:
    database: dict[str, Sound] = {}

    @staticmethod
    def play(name: str, strength: float = 1.0):
        sound = Sounds.database.get(name)
        if sound is None:
            sound = pg.mixer.Sound(f"assets/sounds/{name}")
            sound.set_volume(strength)
            Sounds.database[name] = sound
        sound.play()