import sys, pygame, math, random
from base_classes import *
from camera import Camera
import GameLoop
import EventLib
from level import Level

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
    return doRectsOverlap(sprite1.getRect(), sprite2.getRect())

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
        self.isFacingLeft = False
        self.state = self.STANDING
        self.justHitTile = False

        self.currentlyPressedKeys = set()#can be useful to store

        self.consumeOnce = []
        self.onPlatForm = False

        rightAnimationTextures = [assets.pandaRight, assets.pandaRight2]
        leftAnimationTextures = [assets.pandaLeft, assets.pandaLeft2]

        self.rightAnimation = Animation(rightAnimationTextures, 100)
        self.leftAnimation = Animation(leftAnimationTextures, 100)


    def jump(self, dt):
        self.v_y = -10

    def onKeyDown(self, keyPressed):
        self.currentlyPressedKeys.add(keyPressed)
        if keyPressed == pygame.K_w:
            print("W pressed")
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

    def update(self, dt):
        self.mapKeysToState()

        #update animations
        self.rightAnimation.update(dt)
        self.leftAnimation.update(dt)


        # print(self.state)
        # print(self.x, self.y)
        # print(self.v_x, self.v_y)
        if self.state == self.WALKING_LEFT:
            self.a_x = -50
        elif self.state == self.WALKING_RIGHT:
            self.a_x = 50
        elif self.state == self.STANDING:
            #hard stop
            self.a_x = 0
            self.v_x = 0

        for f in self.consumeOnce:
            f(dt)
        self.consumeOnce.clear()

        deltaSeconds = dt / 1000.0

        if self.onPlatForm:
            self.a_y = 0
        else:
            self.a_y = 20


             #gravity
        # for tileRect in self.adjacentTiles:
        #     (t_x, t_y, t_w, t_h) = tileRect
        #     if self.y + self.h >= t_y:
        #         if self.v_y > 0:
        #             self.v_y = 0
        #             self.a_y = 0
        #             self.y = t_y - self.h
        #     # if self.x + self.w >= t_x:
        #     #     if self.v_x > 0:
        #     #         self.v_x = 0
        #     #         self.a_x = 0
        #     #         self.x = t_x - self.x

        proposedX = self.x + self.v_x * deltaSeconds
        proposedY = self.y + self.v_y * deltaSeconds
        proposedV_X = self.v_x + self.a_x * deltaSeconds
        proposedV_y = self.v_y + self.a_y * deltaSeconds    
        proposedRect = (proposedX, proposedY, self.w, self.h)

        tiles = list(self.world.getIntersectingTiles(proposedRect))

        #modify proposed values if necessary
        self.onPlatForm = False
        for tile in self.world.getIntersectingTiles(proposedRect):
            xOverlap = doIntervalOverlap([tile.x, tile.x + tile.w],[proposedX, proposedX + self.w], 0.01)
            if self.v_y >= 0 and proposedY + self.h > tile.y and self.y + self.h <= tile.y and xOverlap: #falling down
                proposedY = tile.y - self.h
                self.onPlatForm = True
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

        if self.onPlatForm:
            proposedV_y = 0
   
            
        self.x = proposedX
        self.y = proposedY
        self.v_x = proposedV_X
        self.v_y = proposedV_y

        #cap
        self.v_x = clamp(self.v_x, -self.max_v_x, self.max_v_x)
        self.v_y = clamp(self.v_y, -self.max_v_y, self.max_v_y)

        # for tileRect in self.adjacentTiles:
        #     (t_x, t_y, t_w, t_h) = tileRect
        #     if self.y + self.h > t_y and self.y < t_y:
        #         self.y = t_y - self.h
        #     if self.y < t_y + t_h and self.y + self.h > t_y:
        #         #push down
        #         # self.y = t_y + t_h
        #         self.v_y = 1
        #     # #ontop if self.y + self.h > t_y - MARGIN
        #     # MARGIN = 0.1
        #     if self.y + self.h > t_y - MARGIN and self.y < t_y:
        #         #consider as on top, ignore left and right
        #         pass
        #     else:
        #         if self.x + self.w > t_x:
        #             self.x = t_x - self.w

class Squash(Player):
    def __init__(self, world, pos, dim, assets):
        super().__init__(world, pos, dim)
        self.rightAnimationTextures = [assets.squashRight, assets.squashRight2]
        self.leftAnimationTextures = [assets.squashLeft, assets.squashLeft2]

        self.leftAnimation = Animation(self.leftAnimationTextures, 100)
        self.rightAnimation = Animation(self.rightAnimationTextures, 100)

    def update(self, dt):
        self.leftAnimation.update(dt)
        self.rightAnimation.update(dt)

    def draw(self, screen, cam):
        # super().draw(screen, cam) don't call super unless you want demo
        screen.blit(self.rightAnimation.getCurrentImage(), cam.transform(self.getRect()))

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
        self.initLevel()

    def initLevel(self):
        self.level.load(self)

    def addCollidesWithPlayer(self, sprite):
        self._collidesWithPlayer.add(sprite)

    def removeFromAll(self, obj):
        super().removeFromAll(obj)
        self._collidesWithPlayer.remove(obj)

    def cameraFollowPlayer(self):
        self.camera.pos[0] = clamp(self.player_position[0] - self.camera.worldW/2, 0, self.MAP_WIDTH - self.camera.worldW)
        self.camera.pos[1] = clamp(self.player_position[1] - self.camera.worldH/2, 0, self.MAP_HEIGHT - self.camera.worldH)

    def world_update(self, dt):
        super().world_update(dt)
        #handle collisions here
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

    def getIntersectingTiles(self, rect):
        return filter(lambda platform: doRectsOverlap(platform.getRect(), rect), self._platforms)

    def kill(self, entity):
        super().kill(entity)
        self._collidesWithPlayer.pop(entity, None)
        self._platforms.pop(entity, None)
        self._projectiles.pop(entity, None)

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
    world._platforms.add(grass)
def enemy_func(world, pos):
    print("Adding enemy", pos)
    enemy = Squash(world, pos, (1,1), assets)
    world.addEntity(enemy)
    pass

def spike_func(world, pos):
    print("Adding spike", pos)
    spike = Spike(world, pos, (1, 1), assets)
    world.addEntity(spike)
    pass

def empty_func(world, pos):
    pass

def player_func(world, pos):
    panda = Panda(world, pos, (1,1), assets)
    world.addPlayer(panda)
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