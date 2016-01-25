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


def doRectsOverlap(rect1, rect2):
    topLeft1 = (rect1[0], rect1[1])
    topLeft2 = (rect2[0], rect2[1])
    bottomRight1 = (topLeft1[0] + rect1[2], topLeft1[1] + rect1[3])
    bottomRight2 = (topLeft2[0] + rect2[2], topLeft2[1] + rect2[3])

    # print(topLeft1, bottomRight1, topLeft2, bottomRight2)
    if (topLeft1[0] > bottomRight2[0] or topLeft2[0] > bottomRight1[0]):
        # print("HERE")
        return False
    if (topLeft1[1] > bottomRight2[1] or topLeft2[1] > bottomRight1[1]):
        # print("HERE2")
        return False
    return True

def doSpritesOverlap(sprite1, sprite2):
    return doRectsOverlap(sprite1.getCollideRect(), sprite2.getCollideRect())

def clamp(x, low, high):
    return max(low, min(x, high))

class WorldPlus(World):
    def __init__(self, level):
        super().__init__()
        self._collidesWithPlayer = set()
        self._platforms = set()
        self._projectiles = set()
        self.MAP_WIDTH = 60
        self.MAP_HEIGHT = 60
        self.level = level
        self.MAP_WIDTH = level.width
        self.MAP_HEIGHT = level.height
        self.levelHolder = {}

        self.playerProjectiles = set()
        self.enemies = set()

        self.loadedCoordinates = {} #level sprites that are currently visible/active
        self.loadedCoordinatesCount = {} #number of times sprite has been respawned
        self.persistedCoordinates = {} #level sprites that are currently invisible
        self.spriteToLevelCoord = {}

        self.deaths = {}
        self._platformGrid = {}
        self.initLevel()#this needs to be last

    def addPlatform(self, platform, pos):
        self._platformGrid[pos] = platform

    def canRespawn(self, i, j):
        if (i,j) in self.loadedCoordinatesCount:
            (spawnNum, maxSpawn) = self.loadedCoordinatesCount[(i,j)]
            if maxSpawn > 0 and spawnNum > maxSpawn: #if maxSpawn negative, infinite respawn
                return False
        return True

    def loadLevelVisible(self, rect):
        (x, y, w, h) = rect
        x = max(int(x), 0) #floor
        y = max(int(y), 0) #floor
        lastX = int(x + w)
        lastY = int(y + h)
        for i in range(x, min(lastX + 1, self.level.width)):
            for j in range(y, min(lastY + 1, self.level.height)):

                if (i,j) not in self.loadedCoordinates and (i,j) not in self.deaths:

                    # if (i, j) in self.persistedCoordinates:
                    #     self.loadedCoordinates[(i,j)] = self.persistedCoordinates[(i,j)]
                    # #as long as self.loadedCoordinates[(i,j)] is not < threshold
                    if self.canRespawn(i, j):
                        sprite = self.level.loadPos(self, i, j)
                        self.spriteToLevelCoord[sprite] = (i, j)

                        if sprite:
                            self.loadedCoordinates[(i,j)] = sprite
                            if (i,j) in self.loadedCoordinatesCount:
                                self.loadedCoordinatesCount[(i, j)][0] += 1
                            else:
                                self.loadedCoordinatesCount[(i, j)] = [1, sprite.MAX_SPAWN]
                #     if(i,j) in self.loadedCoordinatesCount:
                #         if self.loadedCoordinates[(i,j)] < 2:
                #             self.loadedCoordinatesCount[(i,j)] += 1
                #             sprite = self.level.loadPos(self, i, j)
                #             if sprite:
                #                     self.loadedCoordinates[(i,j)] = sprite
                #
                #     else:
                #         self.loadedCoordinatesCount[(i,j)] = 1
                #         sprite = self.level.loadPos(self, i, j)
                #
                #         if sprite:
                #             self.loadedCoordinates[(i,j)] = sprite
                #
                #
                # if sprite:
                #         if (i,j) in self.loadedCoordinatesCount:
                #             # if self.loadedCoordinatesCount[(i,j)] < 2:#only load once
                #             #     self.loadedCoordinatesCount[(i,j)] += 1
                #             # self.loadedCoordinates[(i,j)] = sprite
                #
                #             self.loadedCoordinates[(i, j)] = sprite
                #             pass
                #         else:
                #             self.loadedCoordinatesCount[(i,j)] = 1
                #             self.loadedCoordinates[(i,j)] = sprite

    def unloadLevelVisible(self, rect):
        # print(self.loadedCoordinates)
        coordsToUnload = set()
        for (coord, sprite) in self.loadedCoordinates.items():
            # print(coord, sprite)
            if not doRectsOverlap(sprite.getRect(), rect):
                print("Unloading", coord)
                if not isinstance(sprite, Player):
                    coordsToUnload.add(coord)

        for coord in coordsToUnload:
            sprite = self.loadedCoordinates[coord]
            if sprite:
                sprite.kill()
            self.persistedCoordinates[coord] = sprite
            self.loadedCoordinates.pop(coord)

        for sprite in self._entities:
            if sprite.cleanWhenOutOfView:
                if not doRectsOverlap(sprite.getRect(), rect):
                    sprite.kill()
        # sprite.kill()

# def unloadNotVisible(self, rect):
    #     for ((x,y) in

    def initLevel(self):
        #load entire level in beginning. Will unload later
        self.loadLevelVisible(self.level.getRect())

    def addCollidesWithPlayer(self, sprite):
        self._collidesWithPlayer.add(sprite)
    # def addProjectile(self, sprite):
    #     self._projectiles.add(sprite)

    def addEnemy(self, enemy):
        self.enemies.add(enemy)

    def addPlayerProjectile(self, projectile):
        self.playerProjectiles.add(projectile)

    def removeFromAll(self, obj):
        super().removeFromAll(obj)
        self._collidesWithPlayer.remove(obj)

    def cameraFollowPlayer(self):
        self.camera.pos[0] = clamp(self.player_position[0] - self.camera.worldW/2, 0, self.MAP_WIDTH - self.camera.worldW)
        self.camera.pos[1] = clamp(self.player_position[1] - self.camera.worldH/2, 0, self.MAP_HEIGHT - self.camera.worldH)

    def getVisible(self, entities):
        return filter(lambda entity: doRectsOverlap(entity.getRect(), self.camera.getRect()), entities)

    def world_update(self, dt):
        super().world_update(dt)
        #handle collisions here

        self.loadLevelVisible(self.camera.getRect())
        self.unloadLevelVisible(self.camera.getRect())
        self.camera.getRect()

        # print("Loaded", len(self.loadedCoordinates))
        # print("Entities", len(self._entities))

        for player in self._players:
            # print(player.getRect())
            for sprite in self._collidesWithPlayer:
                # print(sprite.getRect())
                if doSpritesOverlap(player, sprite):
                    # print("Collision between ", player, sprite)
                    try:
                        player.onCollide(sprite)
                    except AttributeError:
                        pass
                    try:
                        sprite.onCollide(player)
                    except AttributeError:
                        pass

        for enemy in self.enemies:
            for projectile in self.playerProjectiles:
                if doSpritesOverlap(enemy, projectile):
                    enemy.onCollideProjectile(projectile)
                    projectile.onCollideEnemy(enemy)
        # for projectile in self._projectiles:
        #     for entity in itertools.chain(self._players, self._collidesWithPlayer):
        #     # for entity in itertools.chain(self._platforms, self._players, self._collidesWithPlayer):
        #         if doSpritesOverlap(projectile, entity):
        #             projectile.onCollide(entity)
        #             entity.onCollide(projectile)
        #     # for tile in self._platforms:
        #     #     if doSpritesOverlap(projectile, tile):
        #     #         projectile.onCollide(tile)
        #     #         tile.onCollide(projectile)
        #     # for player in self._players:
    #O(n) of area of rect
    def getIntersectingPlatforms(self, rect):
        (x, y, w, h) = rect
        startX = int(x)
        startY = int(y)
        endX = int(x + w)
        endY = int(y + h)
        platforms = list()

        for i in range(startX, endX + 1):
            for j in range(startY, endY + 1):
                if (i,j) in self._platformGrid:
                    platforms.append(self._platformGrid[(i,j)])
        return platforms

    def removeReferences(self, entity):
        super().removeReferences(entity)
        if entity in self._collidesWithPlayer:
            self._collidesWithPlayer.remove(entity)
        if entity in self._platforms:
            self._platforms.remove(entity)
        if entity in self._projectiles:
            self._projectiles.remove(entity)
        if entity in self.spriteToLevelCoord:
            coord = self.spriteToLevelCoord[entity]
            self.loadedCoordinates.pop(coord, None)
            self.persistedCoordinates.pop(coord, None)
        if entity in self.playerProjectiles:
            self.playerProjectiles.remove(entity)
        if entity in self.enemies:
            self.enemies.remove(entity)

    def draw(self, screen):
        super().draw(screen)
        self.drawUI(screen)

    def drawUI(self, screen):
        maxLength = 150
        maxHp = 100
        length = max(maxLength * self._players[0].hp / maxHp, 0)
        pygame.draw.rect(screen, [0, 255, 0], [30, 10, length, 5])

    def doDeath(self, entity):
        self.deaths[self.spriteToLevelCoord[entity]] = 1
        entity.kill()