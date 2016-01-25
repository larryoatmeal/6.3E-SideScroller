import pygame
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

#global
ASSETS = None