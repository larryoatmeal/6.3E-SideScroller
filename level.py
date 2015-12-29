from base_classes import *
from pygame import Rect
from sprite import *
class Level:
	def __init__(self, world):

	def pixelToEntity(self, color, pos):
		#Grass
		world = self.world
		cam = self.cam

		if color == Color(17, 200, 17):
			return Grass(world, pos, (1,1))



