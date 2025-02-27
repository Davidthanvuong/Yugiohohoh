from typing import Tuple

NATIVE = (800, 500)
CENTER = (400, 250)
ZERO = (0, 0)
HALF = (0.5, 0.5)
ONE = (1, 1)

TARGET_FPS = 60
RUNNING = True
USE_OPENGL = False

DEVELOPER_MODE = True
FONT_SIZE = 20

colormap: dict[str, Tuple[int, int, int]] = {
    'gray': (100, 100, 100),
    'light': (180, 180, 180),
    'white': (255, 255, 255),
    'forward': (255, 50, 50),
    'upward': (50, 50, 255),
    'freedom': (50, 255, 50),
    'relation': (50, 150, 150),
    'pivot': (0, 255, 0),
}