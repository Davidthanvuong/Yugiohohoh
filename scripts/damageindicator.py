from pytnk.engine import *

class DamagePooling:
    '''Test thử DoD - Lập trình hướng dữ liệu cho một đống số damage'''
    lifetimes: list[float] = []
    numbers: list[int] = []
    positions: list[vec] = []
    velocities: list[vec] = []
    landed: list[bool] = []
    enabled: list[bool] = []

    gravity: float = 500
    start_lifetime: float = 1.0
    deviate_x: int = 20
    deviate_y: int = 30

    i_free: int = 0
    i_range: int = 0        # Thay vì xử lí từ 0 -> n, thì chỉ một đoạn từ i_range -> i_free
    allocated: int = 2001
    max_number: int = 20

    lazy_max: pg.Surface
    numberFont: pg.font.Font

    @classmethod
    def init(cls):
        cls.lifetimes = [0] * cls.allocated
        cls.numbers = [0] * cls.allocated
        cls.positions = [vec(0, 0)] * cls.allocated
        cls.velocities = [vec(0, 0)] * cls.allocated
        cls.landed = [False] * cls.allocated
        cls.enabled = [False] * cls.allocated

        cls.numberFont = pg.font.Font(None, 40)
        cls.lazy_max = cls.numberFont.render(str(-cls.max_number), True, Color.white)

    @classmethod
    def spawn_number(cls, number: int, pos: vec):
        while number > 0:
            sign = rint(0, 1) * 2 - 1
            deviated_pos = pos + vec(
                rint(-cls.deviate_x, cls.deviate_x),
                rint(-cls.deviate_y, cls.deviate_y)
            )
            cls.lifetimes[cls.i_free] = cls.start_lifetime
            cls.numbers[cls.i_free] = min(number, cls.max_number)
            cls.positions[cls.i_free] = deviated_pos
            cls.velocities[cls.i_free] = vec(sign * rint(20, 200), rint(-450, 100))
            cls.landed[cls.i_free] = False
            cls.enabled[cls.i_free] = True
            cls.i_free = (cls.i_free + 1) % cls.allocated
            number -= cls.max_number

    @classmethod
    def update_pool(cls):
        dt = Motion.dt
        blits: list[tuple[pg.Surface, vec]] = []
        i = cls.i_range
        while i != cls.i_free:
            if cls.lifetimes[i] < 0: # Đang không hoạt động
                cls.enabled[cls.i_range] = False
                i = (i + 1) % cls.allocated
                cls.i_range = i
                continue

            if cls.velocities[i].y > 200: # Dừng tại dy = 10 (như có mặt phẳng tàng hình)
                cls.landed[i] = True

            if not cls.landed[i]:
                cls.velocities[i].y += cls.gravity * dt
                cls.positions[i] += cls.velocities[i] * dt

            cls.lifetimes[i] -= dt

            if cls.numbers[i] == cls.max_number:
                blits.append((cls.lazy_max, cls.positions[i]))
            else:
                number_sf = cls.numberFont.render(str(-cls.numbers[i]), True, Color.white)
                blits.append((number_sf, cls.positions[i]))

            i = (i + 1) % cls.allocated

        App.screen.blits(blits)