from base_classes import *
from pygame import Rect
from sprite import *

# Eventually this class will read a "pixmap", an image where the pixels 
# correspond to certain entities at locations in the world for easy level creation

# Level will manage initializing entities when they become visible, as well as 
# cleaning up entities that are no longer visibile
class Level:
	def __init__(self, world):
		pass

	def pixelToEntity(self, color, pos):
		#Grass
		world = self.world
		cam = self.cam

		if color == Color(17, 200, 17):
			return Grass(world, pos, (1,1))



