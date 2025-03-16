import random
import os

path = "assets\\images\\summoncard"
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

custom_probabilities = {
    #secret
    'rias.jpg': 0.0001,
    'Akeno.jpg': 0.0002,
    'dragon.jpg': 0.009,
    #normal
    'Amir.jpg': 0.3,
    'angry karen.jpg': 0.4,
    'brainrot.jpg': 0.90,
    'chicken nugget.jpg': 0.94,
    'David goggins.jpg': 0.007,
    'diddy.jpg': 0.008,
    'Duong caby.jpg': 0.12,
    'eminem.jpg': 0.89,
    'glonk.jpg': 0.22,
    'hmt.jpg': 0.82,
    'ishowsmurf.jpg': 0.92,
    'khoa trich.jpg': 0.35,
    'man praying.jpg': 0.9,
    'nguyen dj.jpg': 0.45,
    'nhat.jpg': 0.8,
    'pico.jpg': 0.65,
    'quy.jpg': 0.75,
    'red card.jpg': 0.5,
    'reverse card.jpg': 0.5,
    'sans.jpg': 0.02,
    'shrekk.jpg': 0.85,
    'sigma hitler.jpg': 0.05,
    'sung jin woo.jpg': 0.80,
    'swap.jpg': 0.45,
    'toc che mat.jpg': 0.29,
    'troll.jpg': 0.20,
    'trump.jpg': 0.50
}

probabilities = [custom_probabilities.get(f, 0) for f in files]

total = sum(probabilities)
if total != 1:
    probabilities = [p / total for p in probabilities]

def choose_card(files, probabilities):
    return random.choices(files, weights = probabilities, k = 1)[0]

# # Danh sách người chơi
# players = ['Player1', 'Player2', 'Player3']

# # Chia 5 lá cho mỗi thg
# for player in players:
#     print(f"Chia bài cho {player}:")
#     for _ in range(5):
#         chosen_card = choose_card(files, probabilities)
#         print(f" - {chosen_card}")