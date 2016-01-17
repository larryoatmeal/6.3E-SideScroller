import pygame
import math

pygame.init()
size = (300, 200)
screen = pygame.display.set_mode(size)
# def hexToArray(str):

PURPLE = [125, 0, 125]
ORANGE = [255, 128, 0]
BLUE = [10, 10, 255]
GREEN = [5, 100, 150]
WHITE = [255, 220, 255]
clock = pygame.time.Clock()

def rekt(screen):
    pygame.draw.rect(screen, BLUE, (0,12, 24, 16))

def drawCosine(screen):
    startX = 50
    endX = 250
    dx = 1

    period = 10
    amp = 31

    # print(range(startX, endX, dx))

    for x in range(startX, endX, dx):
        y = 31 * math.cos(math.pi/period * x) + 100
        # print(y)
        #Amplitude * cos(2pi/PERIOD * x)
        pygame.draw.rect(screen, GREEN, (x, y, dx, 5))

hectorX = 50
hectorY = 50
keepGoing = True

squashSprite = pygame.image.load("assets/images/butternut_squash.png").convert()
squashSprite = pygame.transform.scale(squashSprite, (32, 32))


class Squash:

    def __init__(self, image, width, height):
        self.x = 0
        self.y = 0
        self.v_x = 0
        self.v_y = 0
        self.a_x = 0
        self.a_y = 0
        self.image = image
        self.width = width
        self.height = height

    def draw(self, screen):
        # print("Draw called in squash")
        screen.blit(self.image, [self.x, self.y])
        pass

    def onKey(self, keyCode):
        if(keyCode == pygame.K_a):
            print("A was pressed")
            self.a_x = -200
        elif(keyCode == pygame.K_d):
            self.a_x = 200
        elif(keyCode == pygame.K_w):
            self.a_y = -200 
        elif(keyCode == pygame.K_s):
            self.a_y = 200 
        pass

    def onKeyUp(self, keyCode):
        if(keyCode == pygame.K_d):
            print("D was released")
            self.a_x = 0
        elif(keyCode == pygame.K_a):
            self.a_x = 0
        elif(keyCode == pygame.K_w):
            self.a_y = 0
        elif(keyCode == pygame.K_s):
            self.a_y = 0
        pass

    def update(self, dt):
        # print("Update called in squash")
        # self.x += 1
        dtInSeconds = dt/1000.0

        self.x += self.v_x * dtInSeconds 
        self.y += self.v_y * dtInSeconds
        self.v_x += (self.a_x - self.v_x * 0.8) * dtInSeconds
        self.v_y += (self.a_y - self.v_y * 0.8) * dtInSeconds

        #Top and bottom walls
        if self.y < 0 or self.y > 200 - self.height: #hacky
            self.v_y *= -1
        if self.x < 0 or self.x > 300 - self.width:
            self.v_x *= -1

        pass

squash = Squash(squashSprite, 32, 32)

while keepGoing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False
        elif event.type == pygame.KEYDOWN:
            squash.onKey(event.key)

            if event.key == pygame.K_w:
                print("W pressed")
                hectorY -= 5
            elif event.key == pygame.K_s:
                hectorY += 5
        elif event.type == pygame.KEYUP:
            squash.onKeyUp(event.key)
    
        # elif event.type == pygame.KEYDOWN:
        #     # handle keydown
        #     # world.onKeyDown(event.key)
        #     if event.key == pygame.K_w:#q
        #         hectorY +=
        # # elif event.type == pygame.KEYUP:
        # #     # handle keyup
        # #     world.onKeyUp(event.key)

    #DRAW------------------------------------------

    #clear screen
    screen.fill(ORANGE) #need to clear screen on each Draw
    
    pygame.draw.circle(screen, PURPLE, (150, 100), 50)
    rekt(screen)
    drawCosine(screen)
    pygame.draw.rect(screen, WHITE, (hectorX, hectorY, 50, 50))
    squash.draw(screen)



    pygame.display.flip()

    #UPDATE-----------------------------------------
    if(hectorX > size[0]):
        hectorX = 0
    #velocity = distance/time
    #distance = velocity * time
    #10 pixels/second 

    deltaTime = clock.get_time()

    velocity = 10
    distance = velocity * deltaTime / 1000.0
    hectorX += distance
    squash.update(deltaTime)
    # print(deltaTime)
    clock.tick(60)
# size = (WIDTH, HEIGHT)
# screen = pygame.display.set_mode(size)
# pygame.display.set_caption("NEXT 3E")