import sys, pygame, math, random
from base_classes import *
from camera import Camera
import EventLib

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LAVENDAR = (150, 0, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 200)

# 3:2 aspect ratio. 30x20 UNITxUNIT blocks
WIDTH = 480
HEIGHT = 320
UNIT = 16
WORLD_WIDTH = int(WIDTH / UNIT) #width of screen in world units
WORlD_HEIGHT = int(HEIGHT / UNIT)
MAP_WIDTH = 2 * WORLD_WIDTH #width of entire map in world units
MAP_HEIGHT = 2 * WORlD_HEIGHT

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("NEXT 3E")


# # Fonts (font, size, bold, italics) Not working right now
# font = pygame.font.SysFont('Courier New', 25, True, False)
# # Render text (text, anti-aliasing, color)
# text = font.render("6.3E", True, BLACK)


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


def testDraw(screen):
    # Draw rectangle
    pygame.draw.rect(screen, RED, [UNIT * 3, UNIT * 3, UNIT * 5, UNIT * 5])
    # Draw line
    pygame.draw.line(screen, RED, [0, 0], [UNIT * 29, UNIT * 19], 5)
    # Draw sinusoid
    for i in range(2 * UNIT, 25 * UNIT):
        x = i
        y = int(3 * UNIT * math.cos(x / (4 * UNIT))) + 10 * UNIT
        pygame.draw.line(screen, RED, [x, y], [x + 1, y])

#-----------------------------Helper classes---------------------------------

class AssetManager:
    def __init__(self):
        self.panda = pygame.image.load("assets/images/panda.png").convert_alpha()
        self.squash = pygame.image.load("assets/images/delicata_squash.png").convert_alpha()
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

class RainDrops(Entity):
    RAIN_DIAMETER = 1.0 / 8
    RAIN_SPEED = 2  # in units per second
    NUM_RAIN_DROPS = 100

    def __init__(self, world):
        super().__init__(world)
        self.rainDrops = []
        for i in range(RainDrops.NUM_RAIN_DROPS):
            x = random.uniform(0, WORLD_WIDTH)
            y = random.uniform(0, WORlD_HEIGHT)
            v_x = 0
            self.color = list(BLUE)
            self.rainDrops.append([x, y, v_x])

    def update(self, dt):
        for coord in self.rainDrops:
            coord[1] += RainDrops.RAIN_SPEED * dt / 1000.0
            coord[0] += coord[2] * dt / 1000.0
            coord[2] *= 0.9
            if coord[1] > WORlD_HEIGHT:
                coord[1] = -RainDrops.RAIN_DIAMETER
                coord[0] = random.uniform(0, WORLD_WIDTH)

    def draw(self, screen, camera):
        for coord in self.rainDrops:
            #note this class does not obey camera
            pygame.draw.circle(screen, self.color, (int(coord[0] * UNIT), int(coord[1] * UNIT)), 1)

    def onEvent(self, event):
        if (event.key == EventLib.WALL_COLLISION):
            # push raindrops
            for coord in self.rainDrops:
                if (random.randrange(0, 2) == 1):
                    coord[2] = -10
                else:
                    coord[2] = 10
            randIndex = random.randrange(0, 3)
            self.color[randIndex] = random.randrange(20, 255)

class SquarePlayer(Player):
    FRICTION = 2 / 1000.0
    FORCE = 0.1 / 1000.0
    COLOR_A = (255, 0, 100)
    COLOR_B = (0, 255, 170)
    TRANSITION_PERIOD = 10000  # 10000 ms = 10s
    BOOST_DISABLE_TIME = 5

    def __init__(self, world, pos, dim):
        super().__init__(world, pos, dim)
        self.v_x = 0
        self.v_y = 0
        self.a_x = 0
        self.a_y = 0
        self.ext_a_x = 0
        self.ext_a_y = 0

        self.time = 0
        self.gradient_scale = 0
        self.color = list(SquarePlayer.COLOR_A)
        self.timeBombs = set()
        self.flinched = False
    
    def onKeyDown(self, keyPressed):
        print("SquarePlayer received key down", keyPressed)
        if keyPressed == pygame.K_d:
            self.a_x = SquarePlayer.FORCE
        elif keyPressed == pygame.K_w:
            self.a_y = -SquarePlayer.FORCE
        elif keyPressed == pygame.K_a:
            self.a_x = -SquarePlayer.FORCE
        elif keyPressed  == pygame.K_s:
            self.a_y = SquarePlayer.FORCE

    def onKeyUp(self, keyPressed):
        if keyPressed == pygame.K_d or keyPressed == pygame.K_a:
            self.a_x = 0
        elif keyPressed == pygame.K_w or keyPressed == pygame.K_s:
            self.a_y = 0

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color, camera.transform(self.getRect()))

    def checkCollision(self, world):

        worldBoundaries = [self.w, self.h, MAP_WIDTH - self.w, MAP_HEIGHT - self.h]
        SquarePlayerBoundaries = [self.x, self.y, self.w, self.h]
        if not doRectsOverlap(worldBoundaries, SquarePlayerBoundaries):
            world.publishEvent(Event(EventLib.WALL_COLLISION))
            # if(self.x < 0 or self.x > WORLD_WIDTH-self.w):#left/right wall collision
            REBOUND = 1.2
            self.v_y = -REBOUND * self.v_y

            # if(self.y < 0 or self.y > WORlD_HEIGHT-self.h):#up/down wall collision
            self.v_x = -REBOUND * self.v_x

    def update(self, dt):

        boostX = self.a_x
        boostY = self.a_y
        if self.flinched:#if flinched, don't apply accel
            boostX = 0
            boostY = 0

        self.v_x += (boostX - self.v_x * SquarePlayer.FRICTION) * dt
        self.v_y += (boostY - self.v_y * SquarePlayer.FRICTION) * dt

        self.x += self.v_x * dt
        self.y += self.v_y * dt
        self.checkCollision(self.world)

        self.time = (self.time + dt) % SquarePlayer.TRANSITION_PERIOD
        self.gradient_scale = (math.cos(self.time * 2 * math.pi / SquarePlayer.TRANSITION_PERIOD) + 1) / 2

        for i in range(0, 3):
            mix = self.gradient_scale * SquarePlayer.COLOR_A[i] + (1 - self.gradient_scale) * SquarePlayer.COLOR_B[i]
            self.color[i] = clamp(mix, 0, 255)

        for bomb in self.timeBombs.copy():
            bomb.tick(dt)
    def unflinch(self):
        print("unflinched")
        self.flinched = False

    def onEvent(self, event):
        if event.key == EventLib.PLAYER_COLLIDED_APPLY_PHYSICS:
            self.v_x = -random.uniform(0.5, 0.9)*(self.v_x + sign(self.v_x)*0.01)
            self.v_y = -random.uniform(0.5, 0.9)*(self.v_y + sign(self.v_y)*0.01)
            self.x += self.v_x
            self.y += self.v_y

            if not self.flinched:
                self.flinched = True
                self.timeBombs.add(TimeBomb(100, self.unflinch, self.timeBombs))

    def onCollide(self, entity):
        entity.onEvent(EventLib.SetColorEvent(self.color))

class Panda(Sprite):
    def __init__(self, world, pos, dim, assets):
        super().__init__(world, pos, dim)
        self.assets = assets

    def draw(self, screen, camera):
        screen.blit(assets.panda, camera.transform(self.getRect()))

    def update(self, dt):
        # print(world.player_position)
        if self.world.player_position:
            self.x += 0.1 * (world.player_position[0] - self.x)
            self.y += 0.1 * (world.player_position[1] - self.y)

class MusicPlayer:
    def __init__(self):
        pass

    def onEvent(self, event):
        pass

    def playNote(self, note):
        pass

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
        # message player directly
        # player.onEvent(Event(EventLib.PLAYER_COLLIDED_APPLY_PHYSICS))
        # tell world
        pass
        # self.world.publishEvent(EventLib.NoteEvent(60))

class MyWorld(World):
    def __init__(self):
        super().__init__()
        self._collidesWithPlayer = set()

    def addCollidesWithPlayer(self, sprite):
        self._collidesWithPlayer.add(sprite)

    def removeFromAll(self, obj):
        super().removeFromAll(obj)
        self._collidesWithPlayer.remove(obj)

    def cameraFollowPlayer(self):
        # super().cameraFollowPlayer()

        # xOffset = self.player_position[0] - self.camera.pos[0]
        #
        # if xOffset > self.camera.worldW:
        #     self.camera.pos[0] += self.camera.worldW
        # if xOffset < 0:
        #     self.camera.pos[0] -= self.camera.worldW
        #
        # yOffset = self.player_position[1] - self.camera.pos[1]
        #
        # if yOffset > self.camera.worldH:
        #     self.camera.pos[1] += self.camera.worldH
        # if yOffset < 1:
        #     self.camera.pos[1] -= self.camera.worldH

        self.camera.pos[0] = clamp(self.player_position[0] - WORLD_WIDTH/2, 0, MAP_WIDTH - WORLD_WIDTH)
        self.camera.pos[1] = clamp(self.player_position[1] - WORlD_HEIGHT/2, 0, MAP_HEIGHT- WORlD_HEIGHT)

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
                        print("Player does not have onCollide method")
                        pass
                    try:
                        sprite.onCollide(player)
                    except AttributeError:
                        pass
                        # print("Sprite does not have onCollide method")

#------------------------Wire up world------------------------------#
assets = AssetManager()
world = MyWorld()
player = SquarePlayer(world, (5, 5), (1, 1))
rainDrops = RainDrops(world)
panda = Panda(world, (0,0), (1,1), assets)
world.addPlayer(player)
world.addEntity(rainDrops)
world.addEntity(panda)

world.addListener(rainDrops)
cam = Camera(WIDTH, HEIGHT, WORLD_WIDTH)


for x in range(10, 50, 5):
    for y in range(10, 30, 5):
        squash = SquareTile(world, (x, y), (1, 1))
        # squash.image = assets.squash
        world.addEntity(squash)
        world.addCollidesWithPlayer(squash)
world.setCamera(cam)

# Main loop
keepGoing = True
clock = pygame.time.Clock()
while keepGoing:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False
        elif event.type == pygame.KEYDOWN:
            # handle keydown
            world.onKeyDown(event.key)
            if event.key == pygame.K_q:  # q
                keepGoing = False
        elif event.type == pygame.KEYUP:
            # handle keyup
            world.onKeyUp(event.key)
    # Update world
    deltaTime = clock.get_time()
    world.update(deltaTime)
    # Draw world
    screen.fill(LAVENDAR)  # need to clear screen on each Draw
    # testDraw(screen)
    world.draw(screen)
    # Display
    pygame.display.flip()
    clock.tick(60)  # 60 fps

pygame.quit()
