import pygame as pg
from enum import Enum

class Path(Enum):
    default = ""
    summon = "summon\\"

def load(name: str, path: Path = Path.default) -> pg.Surface:
    return pg.image.load(f"image\\{path.value}{name}").convert_alpha()

def scale(sf: pg.Surface, size: tuple[float, float]) -> pg.Surface:
    return pg.transform.scale(sf, size)

def rotate(sf: pg.Surface, deg: float) -> pg.Surface:
    return pg.transform.rotate(sf, deg)

def recolor(sf: pg.Surface, a: tuple[int, int, int], b: tuple[int, int, int]) -> pg.Surface:
    for x in range(sf.get_width()):
        for y in range(sf.get_height()):
            if sf.get_at((x, y)) == a:
                sf.set_at((x, y), b)
    return sf