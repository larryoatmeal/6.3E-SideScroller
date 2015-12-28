import sys, pygame, math, random
pygame.init()

# Colors
BLACK = (0 , 0, 0 )
WHITE = (255, 255, 255)
LAVENDAR = (150, 0, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 200)
# 3:2 aspect ratio. 30x20 UNITxUNIT blocks
WIDTH = 480	
HEIGHT = 320
UNIT = 16

WORLD_WIDTH = int(WIDTH/UNIT)
WORlD_HEIGHT = int(HEIGHT/UNIT)
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("NEXT 3E")

# Main loop
keepGoing = True
clock = pygame.time.Clock()

# Fonts (font, size, bold, italics) Not working right now
# font = pygame.font.SysFont('Calibri', 25, True, False)
# Render text (text, anti-aliasing, color)
# text = font.render("6.3E", True, BLACK)

#initialize rainDrops
RAIN_DIAMETER = int(UNIT/8)
RAIN_SPEED = 2*UNIT#in units per second
NUM_RAIN_DROPS = 100
rainDrops = []
for i in range(NUM_RAIN_DROPS):
	x = random.randrange(RAIN_DIAMETER, WIDTH - RAIN_DIAMETER)
	y = random.randrange(RAIN_DIAMETER, HEIGHT - RAIN_DIAMETER)	

	rainDrops.append([x,y])



class Entity:
	def __init__(self):
		pass
	def draw(self, screen):
		pass
	def update(self, world, dt):
		pass
	#Returns true if event is 'consumed', i.e., no one downstream will receive the event
	def onEvent(self, event):
		return False

# A basic event at minimum consists of a key
# Feel free to put any other data you want into the event
class Event:
	def __init__(self, key):
		self.key = key

# For more complex events, you may even decide to subclass event, i.e.
class DamageEvent(Event):
	def inflict(self, entityWithHP):
		entityWithHP.hp -= 50

#Container of world as well as event manager
#Since World is an Entity, can have worlds within in worlds, could be messy though
class World(Entity):
	def __init__(self):
		self._entities = []
		self._listeners = []
		self._eventQueue = []
		self._players = [] #a player is an entity that responds to key commands
		#YOUR OWN WORLD PARAMS HERE

	#--STUDENTS CAN IMPLEMENT THIS---------------------#
	# Most logic should be contained in the children of the world, not the world itself
	# (The children will be automatically handled by this class itself)
	# These methods are specifically for modifying the world itself
	def world_draw(self, screen):
		#YOUR CODE HERE
		pass
	def world_update(self, dt):
		#YOUR CODE HERE
		pass
	def world_onEvent(self, event):
		#YOUR CODE HERE
		return False
	def world_keyUp(self, event):
		#YOUR CODE HERE
		pass
	def world_keyDown(self, event):
		#YOUR CODE HERE
		pass

	#--STUDENTS PROBABLY DO NOT NEED TO MODIFY THIS, BUT CAN OVERRIDE IF NECESSARY---------------------#		
	def update(self, dt):
		self.world_update(dt)	
		for entity in self._entities:
			entity.update(self, dt)
		for player in self._players:
			player.update(self, dt)
	#draw children
	def draw(self, screen):
		self.world_draw(screen)
		for entity in self._entities:
			entity.draw(screen)
		for player in self._players:
			player.draw(screen)
	def notifyListeners(self):
		for event in self._eventQueue:
			if not self.world_onEvent(event):#if not consumed by world, give to children
				for listener in self._listeners:
					consumed = listener.onEvent(event)
					if(consumed):#if consumed by child, stop trickling down
						break
	#register an Entity as part of this world
	def addEntity(self, entity):
		self._entities.append(entity)
	#remove entity from this world
	def removeEntity(self, entity):
		self._entities.remove(entity)
	#must implement onEvent(event)
	def addListener(self, listener):
		self._listeners.append(listener)
	def removeListener(self, listener):
		self._listeners.remove(listener)
	#event should be an Event class
	def publishEvent(self, event):
		self._eventQueue.append(event)
	def addPlayer(self, player):
		self._players.append(player)
	def removePlayer(self, player):
		self._players.remove(player)
	def onKeyUp(self, keyCode):
		self.world_keyUp(keyCode)
		for player in self._players:
			player.onKeyUp(keyCode)
	def onKeyDown(self, keyCode):
		self.world_keyDown(keyCode)
		for player in self._players:
			player.onKeyDown(keyCode)

class Player(Entity):
	FRICTION = 2/1000.0
	FORCE = 0.05/1000.0

	def __init__(self):
		self.x = 5 #world units
		self.y = 5

		self.w = 1 #world units
		self.h = 1

		self.v_x = 0
		self.v_y = 0

		self.a_x = 0
		self.a_y = 0
	# def getBoundingRectangle(self):
	# 	return [self.x, self.y, self.x + self.width, self.y + self.height]
	def onKeyDown(self, keyPressed):
		print("Player received key down", keyPressed)
		if(keyPressed == pygame.K_d):
			self.a_x = Player.FORCE
		elif(keyPressed == pygame.K_w):
			self.a_y = -Player.FORCE
		elif(keyPressed == pygame.K_a):
			self.a_x = -Player.FORCE
		elif(keyPressed == pygame.K_s):
			self.a_y = Player.FORCE
	def onKeyUp(self, keyPressed):
		if(keyPressed == pygame.K_d or keyPressed == pygame.K_a):
			self.a_x = 0
		elif(keyPressed == pygame.K_w or keyPressed == pygame.K_s):
			self.a_y = 0
	# def centerPix(self):
	# 	return [int((self.x + self.width)*UNIT/2.0), int((self.y + self.height)*UNIT/2.0)]
	def draw(self, screen):
		rect = toPix([self.x, self.y, self.w, self.h])
		pygame.draw.rect(screen, WHITE, rect)


	def doRectsOverlap(self, rect1, rect2):
		topLeft1 = (rect1[0], rect1[1])
		topLeft2 = (rect2[0], rect2[1])
		bottomRight1 = (topLeft1[0] + rect1[2], topLeft1[1] + rect1[3])
		bottomRight2 = (topLeft2[0] + rect2[2], topLeft2[1] + rect2[3])

		# print(topLeft1, bottomRight1, topLeft2, bottomRight2)


		if(topLeft1[0] > bottomRight2[0] or topLeft2[0] > bottomRight1[0]):
			# print("HERE")
			return False
		if(topLeft1[1] > bottomRight2[1] or topLeft2[1] > bottomRight1[1]):
			# print("HERE2")
			return False

		return True

	def checkCollision(self):
		worldBoundaries = [self.w, self.h, WORLD_WIDTH-self.w, WORlD_HEIGHT-self.h]
		playerBoundaries = [self.x, self.y, self.w, self.h]
		if not self.doRectsOverlap(worldBoundaries, playerBoundaries):
			print("Collision with wall")
			# if(self.x < 0 or self.x > WORLD_WIDTH-self.w):#left/right wall collision
			self.v_y = -1.2*self.v_y

			# if(self.y < 0 or self.y > WORlD_HEIGHT-self.h):#up/down wall collision
			self.v_x = -1.2*self.v_x



	def update(self, world, dt):
		self.v_x += (self.a_x - self.v_x * Player.FRICTION) * dt
		self.v_y += (self.a_y - self.v_y * Player.FRICTION) * dt
		self.x += self.v_x * dt
		self.y += self.v_y * dt
		self.checkCollision()

def updateRainDrops(dt):
	# Update world
	for coord in rainDrops:
		coord[1] += RAIN_SPEED*dt/1000.0
		if coord[1] > HEIGHT:
			coord[1] = -RAIN_DIAMETER
def integerize(coord):
	return list(map(lambda x: int(x), coord))
def toPix(coord):
	pixCoords = []
	for i in coord:
		pixCoords.append(int(UNIT * i))
	return pixCoords
def drawBackground(screen):
	# Draw rain
	for coord in rainDrops:
		pygame.draw.circle(screen, BLUE, integerize(coord), RAIN_DIAMETER)
	#Draw rectangle
	pygame.draw.rect(screen, RED, [UNIT*3, UNIT*3, UNIT*5, UNIT*5])
	#Draw line
	pygame.draw.line(screen, RED, [0, 0], [UNIT*29, UNIT*19], 5)
	# Draw sinusoid
	for i in range(2 * UNIT, 25 * UNIT):
		x = i
		y = int(3*UNIT*math.cos(x/(4*UNIT))) + 10*UNIT
		pygame.draw.line(screen, RED, [x, y], [x + 1, y])

world = World()
player = Player()
world.addPlayer(player)


#Main loop
while keepGoing:
	# Poll for events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			keepGoing = False
		elif event.type == pygame.KEYDOWN:
			# handle keydown
			world.onKeyDown(event.key)
			print("KEYDOWN", event.key)
			if event.key == 113:#q
				keepGoing = False

		elif event.type == pygame.KEYUP:
			# handle keyup
			world.onKeyUp(event.key)

			print("KEYUP")
	#Update world

	deltaTime = clock.get_time()

	updateRainDrops(deltaTime)
	world.update(deltaTime)
	# Draw world
	screen.fill(LAVENDAR) #need to clear screen on each Draw
	drawBackground(screen)
	world.draw(screen)

	# Draw text
	# screen.blit(text, [0, 0])

	# Display
	pygame.display.flip() 
	clock.tick(60) #60 fps


pygame.quit()