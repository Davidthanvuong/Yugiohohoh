from importer.gobj import *

class Card(Imager, IClickable):
	paths = {
		'back': "card_back.png",
		'empty': "card_empty.png",
	}

	def __init__(self, pos: vec = vec(CENTER), back: bool = False, **kwargs):
		self.role = 'back' if back else 'empty'
		super().__init__(
			Card.paths[self.role], 
			size=vec(200, 300), 
			pos=pos, spin=-5,
			host=self, **kwargs)
		

	def update(self):
		self.iclickable_update()
		render(self)