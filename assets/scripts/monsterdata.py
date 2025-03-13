from pytnk.engine import *

database: dict[str, 'MonsterData'] = {}
listed: list['MonsterData'] = []
weights: list[float] = []

@dataclass
class MonsterData:
    '''Thông tin và dữ liệu của mấy thằng triệu hồi'''
    name: str
    description: str
    drop_rate: float
    card_path: str
    # placing_effect
    baseATK: int
    baseDEF: int
    _monsterClass: No[type['Monster']] = None

    def __post_init__(self):
        database[self.name] = self
        listed.append(self)
        weights.append(self.drop_rate)

    def get_monsterPath(self):
        return os.path.join("monster", os.path.splitext(
            os.path.basename(self.card_path))[0] + ".png")

    @property
    def monster(self):
        assert self._monsterClass is not None
        return self._monsterClass

    @staticmethod
    def getRandom():
        return choices(listed, weights, k=1)[0]