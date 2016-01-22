import sys, pygame, math, random
from base_classes import *
from camera import Camera
import GameLoop
import EventLib
from level import Level
import itertools
#-------------------------------Convenience methods------------------------------
def sign(x):
    if x >= 0:
        return 1
    else:
        return -1

def clamp(x, low, high):
    return max(low, min(x, high))

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

def doIntervalOverlap(interval1, interval2, epsilon):
    (a, b) = interval1
    (c, d) = interval2
    return not (b < c + epsilon or d < a + epsilon)



#-----------------------------Helper classes---------------------------------

class AssetManager:
    def __init__(self):
        self.pandaRight = pygame.image.load("assets/images/panda.png").convert_alpha()
        self.pandaRight2 = pygame.image.load("assets/images/panda2.png").convert_alpha()
        self.pandaLeft = pygame.transform.flip(self.pandaRight, True, False)
        self.pandaLeft2 = pygame.transform.flip(self.pandaRight2, True, False)
        self.squashRight = pygame.image.load("assets/images/butternut_squash.png").convert_alpha()
        self.squashRight2 = pygame.image.load("assets/images/butternut_squash2.png").convert_alpha()
        self.squashLeft = pygame.transform.flip(self.squashRight, True, False)
        self.squashLeft2 = pygame.transform.flip(self.squashRight2, True, False)
        self.spikes = pygame.image.load("assets/images/spike.png").convert_alpha()
        # print(self.panda)

class TimeBomb:
    def __init__(self, time, f, bombContainer):
        self.timeSinceSetOff = 0
        self.time = time
        self.f = f
        self.bombContainer = bombContainer

    def tick(self, dt):
        self.timeSinceSetOff += dt
        if self.timeSinceSetOff > self.time:
            self.f()
            if self in self.bombContainer:
                self.bombContainer.remove(self)

class TimeLoop:
    def __init__(self, intervalTime, f):
        self.intervalTime = intervalTime
        self.counter = 0
        self.f = f
    def tick(self, dt):
        self.counter += dt
        if self.counter > self.intervalTime:
            self.f(dt)
            self.counter = self.counter % self.intervalTime
#-------------------------------Entities methods------------------------------
class Animation:
    def __init__(self, animations, intervalTimeMs):
        self.animations = animations
        self.animationIndex = 0
        self.intervalTimeMs = intervalTimeMs
        self.elapsedTime = 0

    def update(self, dt):
        self.elapsedTime += dt
        if self.elapsedTime > self.intervalTimeMs:
            self.animationIndex = (self.animationIndex + 1) % len(self.animations)
            self.elapsedTime %= self.intervalTimeMs

    def getCurrentImage(self):
        return self.animations[self.animationIndex]

class Panda(Player):
    def __init__(self, world, pos, dim, assets):
        super().__init__(world, pos, dim)
        self.assets = assets

        #per second
        self.v_x = 0
        self.v_y = 0
        self.a_x = 0
        self.a_y = 0

        self.max_v_x = 20
        self.max_v_y = 20

        self.WALKING_RIGHT = "WALKING_RIGHT"
        self.WALKING_LEFT = "WALKING_LEFT"
        self.STANDING = "STANDING"
        self.MID_AIR = "MID_AIR"
        self.isFacingLeft = False
        self.state = self.STANDING
        self.justHitTile = False
        self.hp = 100
        self.currentlyPressedKeys = set()#can be useful to store

        self.jumpSemaphore = 1


        self.consumeOnce = []
        self.onPlatForm = False

        rightAnimationTextures = [assets.pandaRight, assets.pandaRight2]
        leftAnimationTextures = [assets.pandaLeft, assets.pandaLeft2]

        self.rightAnimation = Animation(rightAnimationTextures, 100)
        self.leftAnimation = Animation(leftAnimationTextures, 100)

    def jump(self, dt):

        if self.jumpSemaphore > 0:
            self.v_y += -12
            self.jumpSemaphore -= 1

    def flinch(self, dt):
        self.v_x += -5
        self.v_y += -10


    def onKeyDown(self, keyPressed):
        self.currentlyPressedKeys.add(keyPressed)
        if keyPressed == pygame.K_w:
            print("W pressed")
            self.state = self.MID_AIR
            self.consumeOnce.append(self.jump)
        if keyPressed == pygame.K_a:
            self.isFacingLeft = True
        if keyPressed == pygame.K_d:
            self.isFacingLeft = False

    def onKeyUp(self, keyPressed):
        self.currentlyPressedKeys.remove(keyPressed)

    def mapKeysToState(self):
        if pygame.K_a in self.currentlyPressedKeys:
            self.state = self.WALKING_LEFT
        elif pygame.K_d in self.currentlyPressedKeys:
            self.state = self.WALKING_RIGHT
        else:
            self.state = self.STANDING

    def draw(self, screen, camera):
        if self.isFacingLeft:
            screen.blit(self.leftAnimation.getCurrentImage(), camera.transform(self.getRect()))
        else:
            screen.blit(self.rightAnimation.getCurrentImage(), camera.transform(self.getRect()))

    def onEvent(self, event):
        # print(event)
        # print(event["key"])
        # if event["key"] == "damage":
        #     print("Damage taken", event.damage)
        # else:
        #     print("Blah")
        # print(event
        if(event.key == EventLib.DamageEvent.key):
            print("DAMAGE RECEIVED")
            self.hp -= event.damage
            print(self.hp)
        elif(event.key == EventLib.FlinchEvent.key):
            print("FLINCHED")
            self.consumeOnce.append(self.flinch)
            # self.v_y = -10

    def update(self, dt):
        # print(self.state)
        self.mapKeysToState()

        #update animations
        self.rightAnimation.update(dt)
        self.leftAnimation.update(dt)


        # print(self.state)
        # print(self.x, self.y)
        # print(self.v_x, self.v_y)

        walkingForce = 0
        if self.state == self.WALKING_LEFT:
            walkingForce = -50
        elif self.state == self.WALKING_RIGHT:
            walkingForce = 50
        elif self.state == self.STANDING:
            #hard stop
            walkingForce = 0
            self.v_x = 0

        self.a_x = walkingForce

        for f in self.consumeOnce:
            f(dt)
        self.consumeOnce.clear()

        self.platforming(dt)

    #cap
        self.v_x = clamp(self.v_x, -self.max_v_x, self.max_v_x)
        self.v_y = clamp(self.v_y, -self.max_v_y, self.max_v_y)

    def platforming(self, dt):
        if self.onPlatForm:
            self.a_y = 0
        else:
            self.a_y = 40
        deltaSeconds = dt / 1000.0
        proposedX = self.x + self.v_x * deltaSeconds
        proposedY = self.y + self.v_y * deltaSeconds
        proposedV_X = self.v_x + self.a_x * deltaSeconds
        proposedV_y = self.v_y + self.a_y * deltaSeconds
        proposedRect = (proposedX, proposedY, self.w, self.h)

        tiles = list(self.world.getIntersectingPlatforms(proposedRect))

        #modify proposed values if necessary

        # self.onPlatForm = False
        detectedOnPlatform = False
        for tile in self.world.getIntersectingPlatforms(proposedRect):
            xOverlap = doIntervalOverlap([tile.x, tile.x + tile.w],[proposedX, proposedX + self.w], 0.01)
            if self.v_y >= 0 and proposedY + self.h > tile.y and self.y + self.h <= tile.y and xOverlap: #falling down
                proposedY = tile.y - self.h
                detectedOnPlatform = True
                if not self.onPlatForm: #only fire onland if not already landed
                    self.onland(dt)
            # noOverlapY = proposedY > tile.y + tile.h - 0.1 or tile.y > proposedY + self.h - 0.1
            # overlapY = not noOverlapY
            # print(tile.getRect())
            # print(overlapY)

            yOverlap = doIntervalOverlap([tile.y, tile.y + tile.h],[proposedY, proposedY + self.h], 0.01)
            if self.v_x > 0 and yOverlap:
                proposedX = tile.x - self.w
                proposedV_X = 0
            if self.v_x < 0 and yOverlap:
                proposedX = tile.x + tile.w
                proposedV_X = 0

        self.onPlatForm = detectedOnPlatform

        if self.onPlatForm:
            proposedV_y = 0
        self.x = proposedX
        self.y = proposedY
        self.v_x = proposedV_X
        self.v_y = proposedV_y

    def onland(self, dt):
        # print("Onland")
        if self.jumpSemaphore < 2:
            self.jumpSemaphore += 1


class SquashBulletSeed(Player):
    def __init__(self, world, pos, dim):
        super().__init__(world, pos, dim)
        self.cleanWhenOutOfView = True

    def draw(self, screen, cam):
        pygame.draw.circle(screen, [125,125,0],cam.transformPoint((self.x, self.y + 0.5)), cam.scale(0.3))
    def update(self, dt):
        self.x -= dt/1000.0*5
        if self.world.getIntersectingPlatforms(self.getCollideRect()): #collision
            self.kill()
    def onCollide(self, entity):
        print("COLLISION")
        entity.onEvent(EventLib.DamageEvent(10))
        entity.onEvent(EventLib.FlinchEvent())
        self.kill()
    def getCollideRect(self):
        # return super().getCollideRect()
        xScale = 0.5
        xInset = xScale * self.w
        yScale = 0.5
        yInset = xScale * self.h

        x = self.x + xInset
        y = self.y + yInset
        w = self.w - 2 * xInset
        h = self.h - 2 * yInset

        return (x, y, 0, 0)





class Squash(Sprite):

    def shootBullet(self, dt):
        bullet = SquashBulletSeed(self.world, (self.x, self.y), (1,1))
        self.world.addEntity(bullet)
        self.world.addCollidesWithPlayer(bullet)
        # self.world.addProjectile(bullet)

    def __init__(self, world, pos, dim, assets):
        super().__init__(world, pos, dim)
        self.rightAnimationTextures = [assets.squashRight, assets.squashRight2]
        self.leftAnimationTextures = [assets.squashLeft, assets.squashLeft2]

        self.leftAnimation = Animation(self.leftAnimationTextures, 100)
        self.rightAnimation = Animation(self.rightAnimationTextures, 100)
        self.bulletLoop = TimeLoop(1000, self.shootBullet)

    def update(self, dt):
        self.leftAnimation.update(dt)
        self.rightAnimation.update(dt)
        self.bulletLoop.tick(dt)

    def draw(self, screen, cam):
        # super().draw(screen, cam) don't call super unless you want demo
        screen.blit(self.rightAnimation.getCurrentImage(), cam.transform(self.getRect()))

    def onCollide(self, player):
        self.kill()



class SquareTile(Sprite):
    def __init__(self, world, pos, dim):
        super().__init__(world, pos, dim)
        self.color = [255, 30, 50]

    def draw(self, screen, cam):
        pygame.draw.rect(screen, self.color, cam.transform(self.getRect()))
    def onEvent(self, event):
        if event.key == EventLib.SET_COLOR:
            self.color = event.color.copy()
    def onCollide(self, player):
        #direct message player
        player.onEvent(EventLib.PlayerOnTileEvent(self.getRect()))

class Spike(Sprite):
    def __init__(self, world, pos, dim, assets):
        super().__init__(world, pos, dim)
        self.image = assets.spikes
        self.RESET_TIME = 500
        self.time = self.RESET_TIME

    def update(self, dt):
        super().update(dt)
        self.time = min(self.time + dt, self.RESET_TIME)

    def onCollide(self, player):
        # print(self.time)
        if self.time >= self.RESET_TIME:
            self.time = 0
            player.onEvent(EventLib.DamageEvent(10))
            player.onEvent(EventLib.FlinchEvent())
            # player.onEvent({
            #         "key": "damage",
            #         "damage": 10
            #     })

class MyWorld(World):
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



        self.loadedCoordinates = {} #level sprites that are currently visible/active
        self.loadedCoordinatesCount = {} #number of times sprite has been respawned
        self.persistedCoordinates = {} #level sprites that are currently invisible
        self.spriteToLevelCoord = {}

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

                if (i,j) not in self.loadedCoordinates:

                    if (i, j) in self.persistedCoordinates:
                        self.loadedCoordinates[(i,j)] = self.persistedCoordinates[(i,j)]
                    #as long as self.loadedCoordinates[(i,j)] is not < threshold
                    elif self.canRespawn(i, j):
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
            # if sprite:
            #     sprite.kill()

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
    def addProjectile(self, sprite):
        self._projectiles.add(sprite)

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

    def draw(self, screen):
        super().draw(screen)
        self.drawUI(screen)

    def drawUI(self, screen):
        maxLength = 150
        maxHp = 100
        length = max(maxLength * self._players[0].hp / maxHp, 0)
        pygame.draw.rect(screen, [0, 255, 0], [30, 10, length, 5])


#------------------------Wire up world------------------------------#
# 3:2 aspect ratio. 30x20 UNITxUNIT blocks
WIDTH = 480
HEIGHT = 320

WORLD_WIDTH = 30 #width of screen in world units

pygame.init()

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("NEXT 3E")

assets = AssetManager()

def grass_func(world, pos):
    # player = Player(world, pos, (50, 75))
    # world.addPlayer(player)
    print("Adding grass", pos)
    grass = SquareTile(world, pos, (1,1))
    world.addEntity(grass)
    # world._platforms.add(grass)
    world.addPlatform(grass, pos)
    return grass
def enemy_func(world, pos):
    print("Adding enemy", pos)
    enemy = Squash(world, pos, (1,1), assets)
    world.addEntity(enemy)
    world.addCollidesWithPlayer(enemy)
    return enemy

def spike_func(world, pos):
    print("Adding spike", pos)
    spike = Spike(world, pos, (1, 1), assets)
    world.addEntity(spike)
    world.addCollidesWithPlayer(spike)
    return spike

def empty_func(world, pos):
    pass
    return None

def player_func(world, pos):
    panda = Panda(world, pos, (1,1), assets)
    world.addPlayer(panda)
    return panda
level_mapping = {
    (0, 255, 0): grass_func,
    (0, 0, 255): enemy_func,
    (255, 0, 0): spike_func,
    (0, 0, 0): empty_func,
    (255, 255, 255): player_func
}

level = Level("assets/levels/demo_level.png", level_mapping)
world = MyWorld(level)

cam = Camera(WIDTH, HEIGHT, WORLD_WIDTH)
world.setCamera(cam)

GameLoop.runGame(world, WIDTH, HEIGHT)