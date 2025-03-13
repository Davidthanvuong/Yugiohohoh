from .monsterdata import MonsterData
from .monster import Monster, Dragon

MonsterData._monsterClass = Monster

rias = MonsterData(
    name = 'Rias',
    description = 'Một con quỷ đẹp',
    drop_rate = 0.0001,
    card_path = 'rias.jpg',
    baseATK = 20000,
    baseDEF = 7000
)

akeno = MonsterData(
    name = 'Akeno',
    description = 'Một con quỷ xinh',
    drop_rate = 0.0002,
    card_path = 'akeno.jpg',
    baseATK = 15000,
    baseDEF = 8000
)

dragon = MonsterData(
    name = 'Dragon',
    description = 'Con rồng',
    drop_rate = 0.009,
    card_path = 'dragon.jpg',
    baseATK = 10000,
    baseDEF = 10000,
    _monsterClass=Dragon
)