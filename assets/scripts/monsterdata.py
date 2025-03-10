from pytnk.engine import *

@dataclass
class MonsterData:
    '''Thông tin và dữ liệu của mấy thằng triệu hồi'''
    name: str           # Thông tin chung
    description: str

    card_path: str      # Thông tin thẻ
    # placing_effect

    summon_path: str
    baseATK: int
    baseDEF: int
    # animTypeanimType          
    # # Rig: Simple (không có), Animation (), Human (ArmatureArmature)
    prefab: str

