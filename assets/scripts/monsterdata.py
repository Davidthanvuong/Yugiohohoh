from pytnk.engine import *

database: dict[str, 'MonsterData'] = {}
listed: list['MonsterData'] = []
weights: list[float] = []

@dataclass
class MonsterData:
    '''Thông tin và dữ liệu của mấy thằng triệu hồi'''
    name: str           # Thông tin chung
    description: str
    drop_rate: float
    card_path: str      # Thông tin thẻ
    # placing_effect
    baseATK: int
    baseDEF: int

    def __post_init__(self):
        database[self.name] = self
        listed.append(self)
        weights.append(self.drop_rate)

    def get_monsterPath(self):
        return os.path.join("monster", os.path.splitext(
            os.path.basename(self.card_path))[0] + ".png")

    @staticmethod
    def getRandom():
        return choices(listed, weights, k=1)[0]



Rias = MonsterData(
    name = 'Rias',
    description = 'Một con quỷ đẹp',
    drop_rate = 0.0001,
    card_path = 'rias.jpg',
    baseATK = 20000,
    baseDEF = 7000
)

Akeno = MonsterData(
    name = 'Akeno',
    description = 'Một con quỷ xinh',
    drop_rate = 0.0002,
    card_path = 'akeno.jpg',
    baseATK = 15000,
    baseDEF = 8000
)

Dragon = MonsterData(
    name = 'Dragon',
    description = 'Con rồng',
    drop_rate = 0.009,
    card_path = 'dragon.jpg',
    baseATK = 10000,
    baseDEF = 10000
)

