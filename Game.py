import pygame
import GameLoop
import Scene1
from camera import Camera
class Game:
	def __init__(self):
		self.currentScene = None
		self.currentWorld = None
		# self.screen = pygame.display.set_mode(size)
		WIDTH = 480
		HEIGHT = 320

		WORLD_WIDTH = 30 #width of screen in world units
		size = (WIDTH, HEIGHT)
		self.screen = pygame.display.set_mode(size)
		self.cam = Camera(WIDTH, HEIGHT, WORLD_WIDTH)
		# GameLoop.runWorld(self.currentScene)	
		#load first scene
		#self.loadScene(self, scene)
	def loadScene(self, scene):
		self.currentScene = scene
		self.currentWorld = scene.getWorld()
		self.currentScene.game = self
		self.currentWorld.setCamera(self.cam)

	def run(self):
		GameLoop.runWorld(self.currentWorld, self.screen)

def startGame(firstScene):
	pygame.init()
	pygame.display.set_caption("NEXT 3E")
	game = Game()
	firstScene.game = game
	game.loadScene(firstScene)
	game.run()
if __name__ == "__main__":
	startGame(Scene1.Scene1())