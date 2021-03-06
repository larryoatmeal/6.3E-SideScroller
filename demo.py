import sys, pygame, math, random, EventLib
from base_classes import *
pygame.init()

#demo2.py is probably more useful to look at

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

# # Fonts (font, size, bold, italics) Not working right now
# font = pygame.font.SysFont('Courier New', 25, True, False)
# # Render text (text, anti-aliasing, color)
# text = font.render("6.3E", True, BLACK)

class RainDrops(Entity):
    RAIN_DIAMETER = 1.0/8
    RAIN_SPEED = 2#in units per second
    NUM_RAIN_DROPS = 100
    def __init__(self, world):
        self.world = world
        self.rainDrops = []
        for i in range(RainDrops.NUM_RAIN_DROPS):
            x = random.uniform(0, WORLD_WIDTH)
            y = random.uniform(0, WORlD_HEIGHT)
            v_x = 0
            self.color = list(BLUE)
            self.rainDrops.append([x,y,v_x])
    def update(self, dt):
        for coord in self.rainDrops:
            coord[1] += RainDrops.RAIN_SPEED*dt/1000.0
            coord[0] += coord[2] * dt/1000.0
            coord[2] *= 0.9
            if coord[1] > WORlD_HEIGHT:
                coord[1] = -RainDrops.RAIN_DIAMETER
                coord[0] = random.uniform(0, WORLD_WIDTH)
    def draw(self, screen, camera):
        for coord in self.rainDrops:
            pygame.draw.circle(screen, self.color, toPix(coord[:2]), 1)
    def onEvent(self, event):
        if event.key == EventLib.WALL_COLLISION:
            #push raindrops
            for coord in self.rainDrops:
                if random.randrange(0, 2) == 1:
                    coord[2] = -10
                else:
                    coord[2] = 10
            randIndex = random.randrange(0, 2)#only deal with R and G
            self.color[randIndex] = random.randrange(150, 255)


class Player(Entity):
    FRICTION = 10/1000.0
    FORCE = 0.05/1000.0
    COLOR_A = (255, 0, 100)
    COLOR_B = (0, 255, 170)
    TRANSITION_PERIOD = 10000 #10000 ms = 10s

    def __init__(self, world):
        self.world = world
        self.x = 5 #world units
        self.y = 5

        self.w = 1 #world units
        self.h = 1

        self.v_x = 0
        self.v_y = 0

        self.a_x = 0
        self.a_y = 0

        self.time = 0
        self.gradient_scale = 0
        self.color = list(Player.COLOR_A)
    # def getBoundingRectangle(self):
    #   return [self.x, self.y, self.x + self.width, self.y + self.height]
    def onKeyDown(self, keyPressed):
        print("Player received key down", keyPressed)
        if keyPressed == pygame.K_d:
            self.a_x = Player.FORCE
        elif keyPressed == pygame.K_w:
            self.a_y = -Player.FORCE
        elif keyPressed == pygame.K_a:
            self.a_x = -Player.FORCE
        elif keyPressed == pygame.K_s:
            self.a_y = Player.FORCE
    def onKeyUp(self, keyPressed):
        if keyPressed == pygame.K_d or keyPressed == pygame.K_a:
            self.a_x = 0
        elif keyPressed == pygame.K_w or keyPressed == pygame.K_s:
            self.a_y = 0
    # def centerPix(self):
    #   return [int((self.x + self.width)*UNIT/2.0), int((self.y + self.height)*UNIT/2.0)]
    def draw(self, screen, camera):
        rect = toPix([self.x, self.y, self.w, self.h])
        pygame.draw.rect(screen, self.color, rect)


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

    def checkCollision(self, world):
        worldBoundaries = [self.w, self.h, WORLD_WIDTH-self.w, WORlD_HEIGHT-self.h]
        playerBoundaries = [self.x, self.y, self.w, self.h]
        if not self.doRectsOverlap(worldBoundaries, playerBoundaries):
            world.publishEvent(Event(EventLib.WALL_COLLISION))
            # if(self.x < 0 or self.x > WORLD_WIDTH-self.w):#left/right wall collision
            self.v_y = -1.2*self.v_y

            # if(self.y < 0 or self.y > WORlD_HEIGHT-self.h):#up/down wall collision
            self.v_x = -1.2*self.v_x

    def update(self, dt):
        self.v_x += (self.a_x - self.v_x * Player.FRICTION) * dt
        self.v_y += (self.a_y - self.v_y * Player.FRICTION) * dt
        self.x += self.v_x * dt
        self.y += self.v_y * dt
        self.checkCollision(self.world)

        self.time = (self.time + dt) % Player.TRANSITION_PERIOD
        self.gradient_scale = (math.cos(self.time*2*math.pi/Player.TRANSITION_PERIOD) + 1)/2


        for i in range(0, 3):
            mix = self.gradient_scale*Player.COLOR_A[i] + (1-self.gradient_scale)*Player.COLOR_B[i]
            self.color[i] = clamp(mix, 0, 255)

def clamp(x, low, high):
    return max(low, min(x, high))

def toPix(coord):
    pixCoords = []
    for i in coord:
        pixCoords.append(int(UNIT * i))
    return pixCoords
def testDraw(screen):
    #Draw rectangle
    pygame.draw.rect(screen, RED, [UNIT*3, UNIT*3, UNIT*5, UNIT*5])
    #Draw line
    pygame.draw.line(screen, RED, [0, 0], [UNIT*29, UNIT*19], 5)
    # Draw sinusoid
    for i in range(2 * UNIT, 25 * UNIT):
        x = i
        y = int(3*UNIT*math.cos(x/(4*UNIT))) + 10*UNIT
        pygame.draw.line(screen, RED, [x, y], [x + 1, y])

class Panda(Entity):
    def __init__(self, world, assets):
        self.world = world
        self.assets = assets
        self.x = 0
        self.y = 0
    def draw(self, screen, camera):
        screen.blit(assets.panda, toPix([self.x, self.y]))
    def update(self, dt):
        # print(world.player_position)
        if(self.world.player_position):
            self.x += 0.1 * (world.player_position[0] - self.x)
            self.y += 0.1 * (world.player_position[1] - self.y)

class AssetManager:
    def __init__(self):
        self.panda = pygame.image.load("assets/images/panda.png").convert_alpha()
        # print(self.panda)
assets = AssetManager()


world = World()
player = Player(world)
rainDrops = RainDrops(world)
panda = Panda(world, assets)
world.addPlayer(player)
world.addEntity(rainDrops)
world.addEntity(panda)
world.addListener(rainDrops)

#Main loop
while keepGoing:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False
        elif event.type == pygame.KEYDOWN:
            # handle keydown
            world.onKeyDown(event.key)
            if event.key == pygame.K_q:#q
                keepGoing = False
        elif event.type == pygame.KEYUP:
            # handle keyup
            world.onKeyUp(event.key)
    #Update world
    deltaTime = clock.get_time()
    world.update(deltaTime)
    # Draw world
    screen.fill(LAVENDAR) #need to clear screen on each Draw
    # testDraw(screen)
    world.draw(screen)
    # Display
    pygame.display.flip()
    clock.tick(60) #60 fps

pygame.quit()
