from pytnk.engine import *

card_database: dict[str, 'CardData'] = {}
listed: list['CardData'] = []
weights: list[float] = []

@dataclass
class CardData:
    name: str
    description: str
    img_path: str
    drop_rate: float

    def __post_init__(self):
        card_database[self.name] = self
        listed.append(self)
        weights.append(self.drop_rate)

    def get_placedPath(self):
        new_path = os.path.join("monster", os.path.splitext(
            os.path.basename(self.img_path))[0] + ".png")

        full = f"assets\\images\\{new_path}"
        if not os.path.exists(full):
            print(f"[Error] Không tìm thấy ảnh tại {full}")
            return f"card\\{self.img_path}"

        return new_path


    @staticmethod
    def getRandom():
        return random.choices(listed, weights, k=1)[0]


@dataclass
class MonsterData(CardData):
    '''Thông tin và dữ liệu của mấy thằng triệu hồi'''
    baseATK: int
    baseDEF: int
    _class: type['Monster']

    @property
    def monster(self):
        assert self._class is not None
        return self._class
    

@dataclass
class SpellData(CardData):
    globalUse: bool
    _class: type['Spell']
    
    @property
    def spell(self):
        print(f"Spell {self._class}")
        assert self._class is not None
        return self._class
    

@dataclass
class TrapData(CardData):
    _class: type['Trap']

    @property
    def trap(self):
        assert self._class is not None
        return self._class