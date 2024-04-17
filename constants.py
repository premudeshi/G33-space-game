import pygame

# screen dimensions
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 800
# create the screen and a surface for other menus
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SURFACE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) #SRCALPHA allows us to make the screen transparent
# several sprite groups to keep things organized
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()