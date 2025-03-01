from typing import Tuple

ALLOW_DEVELOPER = True
NATIVE = (1900, 1040)

TARGET_FPS = 60
FONT_SIZE = 16
USE_OPENGL = False

colormap: dict[str, Tuple[int, int, int]] = {
    'dark': (60, 60, 60),
    'gray': (100, 100, 100),
    'light': (180, 180, 180),
    'white': (255, 255, 255),
    'forward': (255, 50, 50),
    'upward': (50, 50, 255),
    'freedom': (50, 255, 50),
    'relation': (50, 150, 150),
    'pivot': (0, 255, 0),
}