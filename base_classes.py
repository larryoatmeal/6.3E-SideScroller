class Entity:
	def __init__(self, world):
		self.world = world
	def draw(self, screen, cam):
		pass
	def update(self, dt):
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
#class DamageEvent(Event):
#	def inflict(self, entityWithHP):
#		entityWithHP.hp -= 50

#Container of world as well as event manager
#Since World is an Entity, can have worlds within in worlds, could be messy though





# class WorldWithCollision(World):
# 	def __init__(self):
# 		super().__init__()
# 		self._collidesWithPlayer = []

# 	def update(self):
# 		super().update()

# 	def checkCollisionWithPlayer(self):
# 		for player in self._players:
# 			for sprite in self._collidesWithPlayer:
# 				if player.getRect().collideRect(sprite.getRect()):




class World(Entity):
	def __init__(self):
		self._entities = set()
		self._listeners = set()
		self._eventQueue = []
		self._players = []#a player is an entity that responds to key commands
		#YOUR OWN WORLD PARAMS HERE

		#commonly accessed parameters here
		self.player_position = None
		self.camera = None
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
		print("EVENT:" + event.key)

		return False
	def world_keyUp(self, event):
		#YOUR CODE HERE
		pass
	def world_keyDown(self, event):
		#YOUR CODE HERE
		pass

	#--STUDENTS PROBABLY DO NOT NEED TO MODIFY THIS, BUT CAN OVERRIDE IF NECESSARY---------------------#		

	def cameraFollowPlayer(self):
		#can make this more complicated
		# self.camera.pos = self.player_position
		pass

	def update(self, dt):
		self.notifyListeners()
		self.world_update(dt)	
		for entity in self._entities:
			entity.update(dt)
		for player in self._players:
			player.update(dt)
			self.player_position = (player.x, player.y)
			if self.camera:#can add flag to change this
				self.cameraFollowPlayer()
	#draw children
	def draw(self, screen):
		self.world_draw(screen)
		for entity in self._entities:
			entity.draw(screen, self.camera)
		for player in self._players:
			player.draw(screen, self.camera)
	def notifyListeners(self):
		for event in self._eventQueue:
			if not self.world_onEvent(event):#if not consumed by world, give to children
				for listener in self._listeners:
					consumed = listener.onEvent(event)
					if(consumed):#if consumed by child, stop trickling down
						break
		self._eventQueue = []
	#register an Entity as part of this world
	def addEntity(self, entity):
		self._entities.add(entity)
	#remove entity from this world
	def removeEntity(self, entity):
		if entity in self._entities:
			self._entities.remove(entity)
	#must implement onEvent(event)
	def addListener(self, listener):

		self._listeners.add(listener)
	def removeListener(self, listener):
		if listener in self._listeners:
			self._listeners.remove(listener)

	def removeFromAll(self, obj):
		self.removeEntity(obj)
		self.removeListener(obj)

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
	def setCamera(self, cam):
		self.camera = cam

