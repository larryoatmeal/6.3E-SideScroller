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
size = (WIDTH, HEIGHT)
UNIT = 16
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
RAIN_SPEED = int(UNIT/16)
NUM_RAIN_DROPS = 100
rainDrops = []
for i in range(NUM_RAIN_DROPS):
	x = random.randrange(RAIN_DIAMETER, WIDTH - RAIN_DIAMETER)
	y = random.randrange(RAIN_DIAMETER, HEIGHT - RAIN_DIAMETER)	

	rainDrops.append([x,y])
while keepGoing:
	# Poll for events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			keepGoing = False
		elif event.type == pygame.KEYDOWN:
			# handle keydown
			print("KEYDOWN", event.key)
			if event.key == 113:#q
				keepGoing = False

		elif event.type == pygame.KEYUP:
			# handle keyup
			print("KEYUP")
	# Update world
	for coord in rainDrops:
		coord[1] += RAIN_SPEED
		if coord[1] > HEIGHT:
			coord[1] = -RAIN_DIAMETER

	# Draw world
	screen.fill(LAVENDAR) #need to clear screen on each Draw

	#Draw rain
	for coord in rainDrops:
		pygame.draw.circle(screen, BLUE, coord, RAIN_DIAMETER)
	

	pygame.draw.rect(screen, RED, [UNIT*3, UNIT*3, UNIT*5, UNIT*5])
	pygame.draw.line(screen, RED, [0, 0], [UNIT*29, UNIT*19], 5)
	#Draw sinusoid
	for i in range(2 * UNIT, 25 * UNIT):
		x = i
		y = int(3*UNIT*math.cos(x/(4*UNIT))) + 10*UNIT
		pygame.draw.line(screen, RED, [x, y], [x + 1, y])
	
	# Draw text
	# screen.blit(text, [0, 0])

	# Display
	pygame.display.flip() 
	clock.tick(60) #60 fps
pygame.quit()