from .carddata import MonsterData, SpellData, TrapData
from .monster import Monster, Spell, Trap
import scripts.custom_monster as mons

uno = SpellData(
    name = 'Uno',
    description = 'Một lá bài',
    drop_rate = 0.6,
    img_path = 'reverse card.jpg',
    globalUse = True,
    _class = Spell
)

troll = SpellData(
    name = 'Troll',
    description = 'Lá bài troll',
    drop_rate = 0.6,
    img_path = 'troll.jpg',
    globalUse = False,
    _class = Spell
)

king = MonsterData(
    name = 'King',
    description = 'King of the game',
    drop_rate = 0,
    img_path = 'king.jpg',
    baseATK = 100,
    baseDEF = 10000,
    _class = mons.King
)


# ✅
sung_jin_woo = MonsterData(
    name = 'Sung Jin Woo',
    description = 'Last Stand: When this card\'s HP drops below 10%, its power surges, increasing its DMG by 10x for 1 turn before resetting its evolution stacks.',
    drop_rate = 0.6, #!!!!
    img_path = 'sung jin woo.jpg',
    baseATK = 1000,
    baseDEF = 1000,
    _class = mons.SungJinWoo
)


# 🚧
Akeno = MonsterData(
    name = 'Akeno',
    description = 'Effect: Boosts team DMG by 15%. Charms enemies, slowing by 45% and stunning for 3 seconds.',
    drop_rate = 0.002,
    img_path = 'akeno.jpg',
    baseATK = 5555,
    baseDEF = 2222,
    _class = Monster
)


# ✅
Black_man_crying = MonsterData(
    name = 'Black man crying',
    description = 'Bro is onto smth (he\'s cooked)\nEffect: Nothin (bro just praying)',
    drop_rate = 0.6,
    img_path = 'praying.jpg',
    baseATK = 2000,
    baseDEF = 1250,
    _class = Monster
)


# 🚧
dragon = MonsterData(
    name = 'Dragon-drag',
    description = 'Stun + instantly deal dmg to all enemies.',
    drop_rate = 0.005,
    img_path = 'dragon.jpg',
    baseATK = 6000,
    baseDEF = 8000,
    _class = mons.Dragon
)


# 🚧
Brainrot = MonsterData(
    name = 'Brainrot',
    description = 'Makes the whole opponent’s team braindead.',
    drop_rate = 0.4,
    img_path = 'brainrot.jpg',
    baseATK = 1250,
    baseDEF = 1000,
    _class = Monster
)


# Ahedog = MonsterData(
#     name = 'Ahedog',
#     description = 'Lingang guliguli guli watak lingkangu linkanguh',
#     drop_rate = 0.6,
#     img_path = 'ahedog.jpg',
#     baseATK = 1000,
#     baseDEF = 1500,
#     _class = Monster
# )


# ✅
Amir = MonsterData(
    name = 'Amir',
    description = '"I\'m built different, sir"',
    drop_rate = 0.4,
    img_path = 'amir.jpg',
    baseATK = 500,
    baseDEF = 2500,
    _class = Monster
)



# 🚧
AngryKaren = MonsterData(
    name = 'Angry Karen',
    description = 'Boost x2 HP for teammates (only "gay" or "les")',
    drop_rate = 0.4,
    img_path = 'karen.jpg',
    baseATK = 1250,
    baseDEF = 1500,
    _class = Monster
)


# 🚧 Lồng tiếng bị ăn khi chết :))
# Tấn công tiếng ba da bing gì đóđó
ChickenNugget = MonsterData(
    name = 'Chicken Nugget',
    description = 'Bro is weak asf (actually yummy)',
    drop_rate = 0.5,
    img_path = 'chicken nugget.jpg',
    baseATK = 1000,
    baseDEF = 1,
    _class = Monster
)



# 🚧
DavidGoggins = MonsterData(
    name = 'David Goggins',
    description = '"Mental toughness is a lifestyle."\nBuff 15% DMG + 15% HP for all male cards, debuff 20% DMG all enemies. (effect overwhelming fear)',
    drop_rate = 0.04, #!!!!
    img_path = 'goggins.jpg',
    baseATK = 4500,
    baseDEF = 5500,
    _class = Monster
)


Diddy = MonsterData(
    name = 'Diddy',
    description = 'Bros bout to cook the whole generation, If this card faces "gay" or "les", x10 times dmg.',
    drop_rate = 0.02,
    img_path = 'diddy.jpg',
    baseATK = 6969,
    baseDEF = 4200,
    _class = Monster
)


DuongCaby = MonsterData(
    name = 'Duong Cabybara',
    description = '"Hi! (we\'re not talking about the freaky white thingy on his mouth)"',
    drop_rate = 0.2,
    img_path = 'Duong caby.jpg',
    baseATK = 2222,
    baseDEF = 2222,
    _class = Monster
)


BadassEminemSlug = MonsterData(
    name = 'Badass Eminem Slug',
    description = '"this is sooo badass"',
    drop_rate = 0.3,
    img_path = 'eminem.jpg',
    baseATK = 1750,
    baseDEF = 1000,
    _class = Monster
)


FreakySonic = MonsterData(
    name = 'Freaky Sonic',
    description = '"Quy nguyen flashback."',
    drop_rate = 0.07,
    img_path = 'freaky sonic.jpg',
    baseATK = 2000,
    baseDEF = 3000,
    _class = Monster
)


Glonk = MonsterData(
    name = 'Glonk',
    description = '"Does absolutely nothing and dies. (my ranked teammates)"',
    drop_rate = 0.5,
    img_path = 'glonk.jpg',
    baseATK = 1,
    baseDEF = 1,
    _class = Monster
)


HoangMinhThien = MonsterData(
    name = 'Hoang Minh Thien',
    description = '"Transforms all allied cards, switching their gender for 2 rounds."',
    drop_rate = 0.4,
    img_path = 'hmt.jpg',
    baseATK = 1000,
    baseDEF = 1250,
    _class = Monster
)


ishowsmurf = MonsterData(
    name = 'Ishowsmurf',
    description = 'Bros too small fr',
    drop_rate = 0.5,
    img_path = 'ishowsmurf.jpg',
    baseATK = 500,
    baseDEF = 500,
    _class = Monster
)


khoa_trich = MonsterData(
    name = 'Khoa Trinh',
    description = 'Tich thu may tinh doi phuong - debuff 10% hp (chi ap dung voi thanh vien 10 tin lm)',
    drop_rate = 0.5,
    img_path = 'khoa trich.jpg',
    baseATK = 900,
    baseDEF = 600,
    _class = Monster
)


longma = MonsterData(
    name = 'Little Longma',
    description = 'Longma boss, the one who drops Tushita?',
    drop_rate = 0.5,
    img_path = 'longma.jpg',
    baseATK = 2000,
    baseDEF = 500,
    _class = Monster
)


nguyen_dj = MonsterData(
    name = 'Nguyen DJ',
    description = 'DJ sigma, effect: +5% all attacks',
    drop_rate = 0.2, #!!!!
    img_path = 'nguyendj.jpg',
    baseATK = 2500,
    baseDEF = 1000,
    _class = mons.NguyenDJ
)


nguyen_nguyen_gay = MonsterData(
    name = 'Nguyen Nguyen (gay ver)',
    description = 'Gay ahh card will curse the opponent\'s cards, effect -5% to all attacks. Last 2 rounds only.',
    drop_rate = 0.5,
    img_path = 'nguyen gay ver.jpg',
    baseATK = 500,
    baseDEF = 250,
    _class = Monster
)


nhat = MonsterData(
    name = 'Nhat (zesty ver)',
    description = 'Bro is not Itoshi Rin :skull:',
    drop_rate = 0.3,
    img_path = 'nhat.jpg',
    baseATK = 1500,
    baseDEF = 750,
    _class = Monster
)


those_who_knows = MonsterData(
    name = 'Those Who Knows',
    description = 'Effect: This card\'s presence cringes opponents, reducing their HP by 15% and Speed by 20%.',
    drop_rate = 0.2,
    img_path = 'pico.jpg',
    baseATK = 2000,
    baseDEF = 1000,
    _class = Monster
)


bui_dinh_quy = MonsterData(
    name = 'Bui Dinh Quy',
    description = '+1 sadboy lanh lung, effect -5% hp doi thu, +5% all attacks (last for 1 round only)',
    drop_rate = 0.3,
    img_path = 'quy.jpg',
    baseATK = 1000,
    baseDEF = 500,
    _class = Monster
)


rias_gremory = MonsterData(
    name = 'Rias Gremory',
    description = 'Distribute your power evenly and increase all allies’ lifesteal and defense by 5%.',
    drop_rate = 0.05, #!!!!
    img_path = 'rias.jpg',
    baseATK = 10000,
    baseDEF = 7000,
    _class = mons.Rias
)


rizz_monk = MonsterData(
    name = 'Rizz Monk',
    description = 'Rizz the opponent, effect slowing 15% + stunning for 2 sec.',
    drop_rate = 0.3,
    img_path = 'rizz monkey.jpg',
    baseATK = 1500,
    baseDEF = 1500,
    _class = Monster
)


sans = MonsterData(
    name = 'Sans',
    description = 'Unique: When defeated, it revives itself with 50% HP and 125% DMG. (this effect can only activate once)',
    drop_rate = 0.002,
    img_path = 'sans.jpg',
    baseATK = 5000,
    baseDEF = 3000,
    _class = Monster
)


shrekk = MonsterData(
    name = 'Shrekk',
    description = 'Fat ass shrekk',
    drop_rate = 0.5,  
    img_path = 'shrekk.jpg',
    baseATK = 1,
    baseDEF = 5000,
    _class = Monster
)


toc_che_mat_sama = MonsterData(
    name = 'Toc Che Mat - Sama',
    description = 'Mukbang all enemies’ cards under 150 cm high',
    drop_rate = 0.01, 
    img_path = 'toc che mat.jpg',
    baseATK = 0,
    baseDEF = 2000,
    _class = Monster
)


donal_trump = MonsterData(
    name = 'Donal Trump',
    description = 'x2 dmg if the opponent is gay.',
    drop_rate = 0.08,  
    img_path = 'trump.jpg',
    baseATK = 2000,
    baseDEF = 1500,
    _class = Monster
)


#####################################

zhong_xina = MonsterData(
    name = 'Zhong Xina',
    description = 'My bro is sending nukes lol',
    drop_rate = 0.1,  
    img_path = 'zhong xina.jpg',
    baseATK = 3500,
    baseDEF = 1500,
    _class = Monster
)

egg_man = MonsterData(
    name = 'Egg Man',
    description = '”Xue Hua Piao Piao”',
    drop_rate = 0.4,  
    img_path = 'egg man.jpg',
    baseATK = 999,
    baseDEF = 500,
    _class = Monster
)

lee_ching_chong = MonsterData(
    name = 'Lee ching chong',
    description = '”Ching chong ding dong”',
    drop_rate = 0.4,  
    img_path = 'lee ching chong.jpg',
    baseATK = 2200,
    baseDEF = 800,
    _class = Monster
)

christiano_mcdonal = MonsterData(
    name = 'Christiano McDonal',
    description = 'Too fat ngl',
    drop_rate = 0.4,  
    img_path = 'christiano mcdonal.jpg',
    baseATK = 1000,
    baseDEF = 800,
    _class = Monster
)

messi = MonsterData(
    name = 'Messi',
    description = 'Bro retired.',
    drop_rate = 0.4,  
    img_path = 'messi.jpg',
    baseATK = 800,
    baseDEF = 1000,
    _class = Monster
)