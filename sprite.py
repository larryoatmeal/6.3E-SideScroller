from base_classes import *
import pygame
from pygame import Rect
class Sprite(Entity):
	#world: world container sprite belongs to
	#cam: camera to convert world positions to pixels
	#pos: (x,y)
	#dim: (w,h)
	def __init__(self, world, pos, dim):
		self.x, self.y = pos
		self.w, self.h = dim
		self.world = world
		self.image = None
	def getRect(self):#lol
		return Rect(self.x, self.y, self.w, self.h)
	def getPixelRect(self, cam):
		return cam.transform(self.getRect())
	def draw(self, screen, cam):
		rect = self.getPixelRect(cam)
		if(self.image):
			screen.blit(self.image, rect)
		else:
			pygame.draw.rect(screen, (125, 125, 125), rect)
	def update(self, dt):
		pass
		#can change self.image to change what image is being displayed