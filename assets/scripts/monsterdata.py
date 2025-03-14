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
sung_jin_woo = MonsterData(
name = 'Sung Jin Woo',
description = 'Last Stand: When this card’s HP drops below 10%, its power surges, increasing its DMG by 10× for 1 turn before resetting its evolution stacks.',
drop_rate = 0.6,
card_path = 'sung jin woo.jpg',
baseATK = 1000,
baseDEF = 1000
)

Akeno = MonsterData(
name = 'Akeno',
description = 'Effect: Boosts team DMG by 15%. Charms enemies, slowing by 45% and stunning for 3 seconds.',
drop_rate = 0.002,
card_path = 'Akeno.jpg',
baseATK = 5555,
baseDEF = 2222
)

Black_man_crying = MonsterData(
name = 'Black man crying',
description = 'Bro is onto smth (he\'s cooked)\nEffect: Nothin (bro just praying)',
drop_rate = 0.6,
card_path = 'man praying.jpg',
baseATK = 2000,
baseDEF = 1250
)

Dragon = MonsterData(
name = 'Dragon-drag',
description = 'Stun + instantly deal dmg to all enemies.',
drop_rate = 0.005,
card_path = 'dragon.jpg',
baseATK = 6000,
baseDEF = 8000
)

Brainrot = MonsterData(
name = 'Brainrot',
description = 'Makes the whole opponent’s team braindead.',
drop_rate = 0.4,
card_path = 'brainrot.jpg',
baseATK = 1250,
baseDEF = 1000
)

Ahedog = MonsterData(
name = 'Ahedog',
description = 'Lingang guliguli guli watak lingkangu linkanguh',
drop_rate = 0.6,
card_path = 'Ahedog.jpg',
baseATK = 1000,
baseDEF = 1500
)

Amir = MonsterData(
name = 'Amir',
description = '"I\'m built different, sir"',
drop_rate = 0.4,
card_path = 'Amir.jpg',
baseATK = 500,
baseDEF = 2500
)

AngryKaren = MonsterData(
name = 'Angry Karen',
description = 'Boost x2 HP for teammates (only "gay" or "les")',
drop_rate = 0.4,
card_path = 'angry karen.jpg',
baseATK = 1250,
baseDEF = 1500
)

ChickenNugget = MonsterData(
name = 'Chicken Nugget',
description = 'Bro is weak asf (actually yummy)',
drop_rate = 0.5,
card_path = 'chicken nugget.jpg',
baseATK = 1000,
baseDEF = 1
)

DavidGoggins = MonsterData(
name = 'David Goggins',
description = '"Mental toughness is a lifestyle."\nBuff 15% DMG + 15% HP for all male cards, debuff 20% DMG all enemies. (effect overwhelming fear)',
drop_rate = 0.04,
card_path = 'David goggins.jpg',
baseATK = 4500,
baseDEF = 5500
)

Diddy = MonsterData(
name = 'Diddy',
description = 'Bros bout to cook the whole generation, If this card faces "gay" or "les", x10 times dmg.',
drop_rate = 0.02,
card_path = 'diddy.jpg',
baseATK = 6969,
baseDEF = 4200
)

DuongCaby = MonsterData(
name = 'Duong Cabybara',
description = '"Hi! (we\'re not talking about the freaky white thingy on his mouth)"',
drop_rate = 0.2,
card_path = 'Duong caby.jpg',
baseATK = 2222,
baseDEF = 2222
)

BadassEminemSlug = MonsterData(
name = 'Badass Eminem Slug',
description = '"this is sooo badass"',
drop_rate = 0.3,
card_path = 'eminem.jpg',
baseATK = 1750,
baseDEF = 1000
)

FreakySonic = MonsterData(
name = 'Freaky Sonic',
description = '"Quy nguyen flashback."',
drop_rate = 0.07,
card_path = 'freaky sonic.jpg',
baseATK = 2000,
baseDEF = 3000
)

Glonk = MonsterData(
name = 'Glonk',
description = '"Does absolutely nothing and dies. (my ranked teammates)"',
drop_rate = 0.5,
card_path = 'glonk.jpg',
baseATK = 0,
baseDEF = 0
)

HoangMinhThien = MonsterData(
name = 'Hoang Minh Thien',
description = '"Transforms all allied cards, switching their gender for 2 rounds."',
drop_rate = 0.4,
card_path = 'hmt.jpg',
baseATK = 1000,
baseDEF = 1250
)

ishowsmurf = MonsterData(
name = 'Ishowsmurf',
description = 'Bros too small fr',
drop_rate = 0.5,
card_path = 'ishowsmurf.jpg',
baseATK = 500,
baseDEF = 500
)

khoa_trich = MonsterData(
name = 'Khoa Trinh',
description = 'Tich thu may tinh doi phuong - debuff 10% hp (chi ap dung voi thanh vien 10 tin lm)',
drop_rate = 0.5,
card_path = 'khoa trich.jpg',
baseATK = 900,
baseDEF = 600
)

longma = MonsterData(
name = 'Little Longma',
description = 'Longma boss, the one who drops Tushita?',
drop_rate = 0.5,
card_path = 'longma.jpg',
baseATK = 2000,
baseDEF = 500
)

nguyen_dj = MonsterData(
name = 'Nguyen DJ',
description = 'DJ sigma, effect: +5% all attacks',
drop_rate = 0.2,
card_path = 'nguyen dj.jpg',
baseATK = 2500,
baseDEF = 1000
)

nguyen_nguyen_gay = MonsterData(
name = 'Nguyen Nguyen (gay ver)',
description = 'Gay ahh card will curse the opponent\'s cards, effect -5% to all attacks. Last 2 rounds only.',
drop_rate = 0.5,
card_path = 'nguyen gay ver.jpg',
baseATK = 500,
baseDEF = 250
)

nhat = MonsterData(
name = 'Nhat (zesty ver)',
description = 'Bro is not Itoshi Rin :skull:',
drop_rate = 0.3,
card_path = 'nhat.jpg',
baseATK = 1500,
baseDEF = 750
)

those_who_knows = MonsterData(
name = 'Those Who Knows',
description = 'Effect: This card\'s presence cringes opponents, reducing their HP by 15% and Speed by 20%.',
drop_rate = 0.2,
card_path = 'pico.jpg',
baseATK = 2000,
baseDEF = 1000
)

bui_dinh_quy = MonsterData(
name = 'Bui Dinh Quy',
description = '+1 sadboy lanh lung, effect -5% hp doi thu, +5% all attacks (last for 1 round only)',
drop_rate = 0.3,
card_path = 'quy.jpg',
baseATK = 1000,
baseDEF = 500
)

rias_gremory = MonsterData(
name = 'Rias Gremory',
description = 'Distribute your power evenly and increase all allies’ lifesteal and defense by 5%.',
drop_rate = 0.0003,
card_path = 'rias.jpg',
baseATK = 20000,
baseDEF = 7000
)

rizz_monk = MonsterData(
name = 'Rizz Monk',
description = 'Rizz the opponent, effect slowing 15% + stunning for 2 sec.',
drop_rate = 0.3,
card_path = 'rizz monk.jpg',
baseATK = 1500,
baseDEF = 1500
)

sans = MonsterData(
name = 'Sans',
description = 'Unique: When defeated, it revives itself with 50% HP and 125% DMG. (this effect can only activate once)',
drop_rate = 0.002,
card_path = 'sans.jpg',
baseATK = 5000,
baseDEF = 3000
)

shrekk = MonsterData(
name = 'Shrekk',
description = 'Fat ass shrekk',
drop_rate = 0.5,  
card_path = 'shrekk.jpg',
baseATK = 1,
baseDEF = 5000
)

toc_che_mat_sama = MonsterData(
name = 'Toc Che Mat - Sama',
description = 'Mukbang all enemies cards under 150 cm high',
drop_rate = 0.01, 
card_path = 'toc che mat.jpg',
baseATK = 0,
baseDEF = 2000
)

donal_trump = MonsterData(
name = 'Donal Trump',
description = 'x2 dmg if the opponent is gay.',
drop_rate = 0.08,  
card_path = 'trump.jpg',
baseATK = 2000,
baseDEF = 1500
)
