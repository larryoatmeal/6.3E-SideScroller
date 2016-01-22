import pygame

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
        self.MAX_SPAWN = -1 #default infinite spawn
        self.cleanWhenOutOfView = False
    def getCollideRect(self):
        return [self.x, self.y, self.w, self.h]
    def getRect(self):#lol
        return [self.x, self.y, self.w, self.h]
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




    def kill(self):#removes self from world
        self.world.kill(self)
    #can change self.image to change what image is being displayed

class Player(Sprite):
    def __init__(self, world, pos, dim):
        super().__init__(world, pos, dim)
        self.cleanWhenOutOfView = False

    # def getBoundingRectangle(self):
    #   return [self.x, self.y, self.x + self.width, self.y + self.height]




    def onKeyDown(self, keyPressed):
        pass
    def onKeyUp(self, keyPressed):
        pass

# A basic event at minimum consists of a key
# Feel free to put any other data you want into the event
class Event:
    def __init__(self, key):
        self.key = key

# class WorldWithCollision(World):
#   def __init__(self):
#       super().__init__()
#       self._collidesWithPlayer = []

#   def update(self):
#       super().update()

#   def checkCollisionWithPlayer(self):
#       for player in self._players:
#           for sprite in self._collidesWithPlayer:
#               if player.getRect().collideRect(sprite.getRect()):


#Container of world as well as event manager
#Since World is an Entity, can have worlds within in worlds, could be messy though

class World(Entity):
    def __init__(self):
        self.DEBUG = True
        self._entities = {}
        self._listeners = set()
        self._eventQueue = []
        self._players = [] #probably only need to deal with one, but just in case
        #YOUR OWN WORLD PARAMS HERE
        #commonly accessed parameters here
        self.player_position = None #assuming here that there is just one player
        self.camera = None
        self.killList = list()
        self.addlist = list() #list of functions
    #--STUDENTS CAN OVERRIDE THIS---------------------#
    # Most logic should be contained in the children of the world, not the world itself
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
    def cameraFollowPlayer(self):
        #can make this more complicated
        # self.camera.pos = self.player_position
        pass

    #--STUDENTS PROBABLY DO NOT NEED TO OVERRIDE THIS, BUT CAN IF NECESSARY---------------------#
    def update(self, dt):
        self.notifyListeners()
        self.world_update(dt)

        keys = self._entities.keys()

        for entity in list(self._entities):#the entity is the key
            entity.update(dt)
        for player in list(self._players):
            player.update(dt)
            self.player_position = (player.x, player.y)
            if self.camera:#can add flag to change this
                self.cameraFollowPlayer()

    #draw children
    def draw(self, screen):
        self.world_draw(screen)
        #Draw by z value
        z0 = set()
        z1 = set()
        z2 = set()

        for entity, z in self._entities.items():
            if z == 0:
                z0.add(entity)
            if z == 1:
                z1.add(entity)
            if z == 2:
                z2.add(entity)
            else:#default add to back
                z0.add(entity)

        for player in self._players:
            z1.add(player) #add player to layer 1 default
        layers = [z0, z1, z2]

        for layer in layers:
            for entity in layer:
                entity.draw(screen, self.camera)

    def notifyListeners(self):
        for event in self._eventQueue:
            if not self.world_onEvent(event):#if not consumed by world, give to children
                for listener in self._listeners:
                    consumed = listener.onEvent(event)
                    if(consumed):#if consumed by child, stop trickling down
                        break
        self._eventQueue = []
    #register an Entity as part of this world
    def addEntity(self, entity, z = 1): #0 back, 1 middle, 2 back
        self._entities[entity] = z #doesn't really matter what the value is

    #remove entity from this world
    def removeEntity(self, entity):
        if entity in self._entities:
            # self._entities.remove(entity)
            self._entities.pop(entity, None)

    #listener must implement onEvent(event)
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

    def removeReferences(self, entity):
        # print(entity)
        # print(len(self._entities))
        if entity in self._listeners:
            self._listeners.remove(entity)
        self._entities.pop(entity, None)
        # print(len(self._entities))

    def kill(self, entity):
        self.killList.append(entity)

    def cleanup(self):
        # print(self.killList)
        for entity in self.killList:
            self.removeReferences(entity)
        self.killList.clear()