import pygame
from constants import all_sprites, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, SURFACE
from player import Player

# initialize pygame so we can use its fonts
pygame.init()
# the font used in menus
FONT = pygame.font.SysFont('Georgia', 20)

# Menu class
class Menu(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# draw the main pause menu
def draw_pause_menu(screen, upgrades):
    # main pause menu is gray and slightly transparent
    pygame.draw.rect(SURFACE, (128, 128, 128, 20), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.blit(SURFACE, (0, 0))
    
    # if sprea hasn't been bought, draw its button. If it has, we hide a button wayyyy outside the game's boundaries so python doesn't yell at us for it being null
    if (upgrades[0] == 0):
        spread = draw_spread(screen)
    else:
        spread = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 25555, 25555, 280, 50], 0, 10)
    # same for reverse
    if (upgrades[1] == 0):
        reverse = draw_reverse(screen)
    else:
        reverse = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 25555, 25555, 280, 50], 0, 10)
    # same for battering ram
    if (upgrades[3] == 0):
        ram = draw_ram(screen)
    else:
        ram = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 25555, 25555, 280, 50], 0, 10)
    # same for reverse spread, but it only appears if both regular spread and reverse shot have been purchased
    if (upgrades[2] == 0 and upgrades[0] == 1 and upgrades[1] == 1):
        rev_spread = draw_rev_spread(screen)
    else:
        rev_spread = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 25555, 25555, 280, 50], 0, 10)
    # always let the player but more lives and a faster firing speed
    life = draw_life(screen)
    fire = draw_fire(screen)
    
    # same as above for the prettier sprites
    if (upgrades[5] == 0):
        sprites = draw_sprites(screen)
    else:
        sprites = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 25555, 25555, 280, 50], 0, 10)
        
    # return all the buttons we've made back to main
    return spread, reverse, ram, rev_spread, life, fire, sprites
    
# draw the psread button as so:
def draw_spread(screen):
    # first, create the button itself. It will be white and have rounded edges (what the 0, 10 at the end means)
    spread = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 25, 280, 50], 0, 10)
    # now add its text. It will use our above font in black
    SURFACE.blit(FONT.render('SPREAD SHOT: 1000p', True, 'black'), (SCREEN_WIDTH / 4 + 5, 38))
    # draw it to the screen and return it
    SCREEN.blit(SURFACE, (0, 0))
    return spread
    
# do the same for reverse
def draw_reverse(screen):
    reverse = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 125, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('REVERSE: 500p', True, 'black'), (SCREEN_WIDTH / 4 + 35, 138))
    SCREEN.blit(SURFACE, (0, 0))
    return reverse

# do the same for battering ram
def draw_ram(screen):
    ram = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 225, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('BATTERING RAM: 2500p', True, 'black'), (SCREEN_WIDTH / 4 - 7, 238))
    SCREEN.blit(SURFACE, (0, 0))
    return ram
    
# do the same for reverse spread
def draw_rev_spread(screen):
    rev_spread = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 325, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('REVERSE SPREAD: 1500p', True, 'black'), (SCREEN_WIDTH / 4 - 15, 338))
    SCREEN.blit(SURFACE, (0, 0))
    return rev_spread
    
# do the same for bonus lives
def draw_life(screen):
    life = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 425, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('LIFE UP: 5000p', True, 'black'), (SCREEN_WIDTH / 4 + 38, 438))
    SCREEN.blit(SURFACE, (0, 0))
    return life
    
# do the same for firing speed
def draw_fire(screen):
    fire = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 525, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('FIRE UP: 1000p', True, 'black'), (SCREEN_WIDTH / 4 + 38, 538))
    SCREEN.blit(SURFACE, (0, 0))
    return fire
    
# do the same for prettier sprites
def draw_sprites(screen):
    sprites = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 625, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('NEW SPRITES: 10000p', True, 'black'), (SCREEN_WIDTH / 4, 638))
    SCREEN.blit(SURFACE, (0, 0))
    return sprites