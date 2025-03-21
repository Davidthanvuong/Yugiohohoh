import pygame as pg
from pygame.mixer import Sound
from dataclasses import dataclass

@dataclass(frozen=True)
class Volume:
    music = 0.05
    effects = 0.2

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

    @staticmethod
    def play_music():
        pg.mixer.music.load("assets/sounds/tobutobu.mp3")
        pg.mixer.music.set_volume(Volume.music)
        pg.mixer.music.play()