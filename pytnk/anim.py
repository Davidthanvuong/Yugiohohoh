from pytnk.engine import *
from PIL import Image as PILImage
from typing import cast

class SharedGIF:
    database: dict[str, 'SharedGIF'] = {}
    frameskip: float = 1.0

    def __init__(self, path: str):
        self.pil = PILImage.open(f"assets/animations/{path}.gif")
        self.frameCount = int(self.pil.n_frames * SharedGIF.frameskip) # type: ignore
        self.frames: list[No[LazySurface]] = [None] * self.frameCount
        self.surfaces: list[pg.Surface] = [None] * self.frameCount # type: ignore

    @classmethod
    def load(cls, path: str):
        gif = cls.database.get(path)
        if not gif: gif = cls.database[path] = cls(path)
        return gif



class Animation(Component):
    def __init__(self, path: str = "", size: No[tff | int] = None, looping: bool = True,
                 playtime = 1.0, enable_overlay = False, override_hitbox = False):
        self.path = path
        self.gif = SharedGIF.load(path)
        self.size = vec(size if size else self.gif.pil.size)
        self.looping = looping
        self.playtime = playtime
        self.enable_overlay = enable_overlay
        self.override_hitbox = override_hitbox
        self.overlay_alpha = 0
        self.alpha = 255
        self.playback = Motion.linear(0, self.gif.frameCount - 1, self.playtime, True)

    def update_render(self):
        i_frame = int(self.playback.value)
        lazyFrame = self.gif.frames[i_frame]
        if lazyFrame is None: 
            # POV: 4 format khác nhau
            # GIF -> PIL Image -> Binary -> Pygame Image
            lazyFrame = LazySurface(self.transf, self.enable_overlay)
            self.gif.pil.seek(i_frame)
            pil_img = self.gif.pil.copy()
            bin_img = pil_img.convert("RGBA").tobytes()
            pygame_img = pg.image.frombuffer(bin_img, pil_img.size, "RGBA")

            self.gif.frames[i_frame] = lazyFrame
            self.gif.surfaces[i_frame] = pygame_img
        
        if not lazyFrame.unchanged:
            lazyFrame.recreate(self.gif.surfaces[i_frame], self.size)
            if self.override_hitbox: self.transf.hitbox = self.size

        lazyFrame.render(self.alpha, int(self.overlay_alpha), newPos=self.transf.g_pos)