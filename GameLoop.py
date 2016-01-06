import pygame

DEFAULT_WIDTH = 480
DEFAULT_HEIGHT = 320

def runGame(world, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT, caption ="NEXT 3E"):
    pygame.init()

    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(caption)

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
        screen.fill([0, 0, 0])  # need to clear screen on each Draw
        # testDraw(screen)
        world.draw(screen)
        # Display
        pygame.display.flip()
        clock.tick(60)  # 60 fps

    pygame.quit()