import sys, pygame
pygame.init()

# Colors
BLACK = (0 , 0, 0 )
WHITE = (255, 255, 255)
LAVENDAR = (150, 0, 150)
# 3:2 aspect ratio. 30x20 16x16 blocks
size = (480, 320)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("NEXT 3E")

# Main loop
keepGoing = True
clock = pygame.time.Clock()

# while keepGoing:
# 	#Poll events
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			keepGoing = False

while keepGoing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			keepGoing = False;

	#Update world
	#Draw world

	screen.fill(LAVENDAR) #need to clear screen on each Draw
	pygame.display.flip() #double buffer
	clock.tick(60) #60 fps