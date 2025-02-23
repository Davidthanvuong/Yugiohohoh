from ..engine.gameobject import *

class Card(GameObject):
	paths = {
		'back': "card_back.png",
		'empty': "card_empty.png",
	}

	def __init__(self, pos: vec = vec(CENTER), back: bool = False):
		super().__init__()
		self.pos = pos
		self.role = 'back' if back else 'empty'
		self.image = Imager(
			Card.paths[self.role], 
			size=vec(200, 300), 
			rotation=-5,
			pivot=vec(0, 0)
		)

	def update(self):
		render(self.image, self.pos)