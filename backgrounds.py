import pygame
from constants import all_sprites, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, SURFACE, GAME_SURFACE
from player import Player

# initialize pygame so we can use its fonts
pygame.init()
# the font used in menus
FONT = pygame.font.SysFont('Georgia', 20)
TITLE_FONT = pygame.font.SysFont('Georgia', 30)

# Menu class
class Menu(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# draw the background
def draw_background(screen):
    background = pygame.image.load('sprites/background.png')
    screen.blit(background, (0, 0))
    

def draw_main_menu(screen):
    pygame.draw.rect(SURFACE, (180, 180, 180, 5), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.blit(SURFACE, (0, 0))
    
    # play button starts the game
    play = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 325, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('PLAY', True, 'black'), (SCREEN_WIDTH / 4 + 85, 338))
    SCREEN.blit(SURFACE, (0, 0))
    
    # quit button quits out
    quit_game = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 725, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('QUIT', True, 'black'), (SCREEN_WIDTH / 4 + 90, 738))
    SCREEN.blit(SURFACE, (0, 0))
    
    # log in button logs into an existing account
    log_in = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 525, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('LOG IN', True, 'black'), (SCREEN_WIDTH / 4 + 80, 538))
    SCREEN.blit(SURFACE, (0, 0))
    
    # sign up button creates a new account
    sign_up = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 625, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('SIGN UP', True, 'black'), (SCREEN_WIDTH / 4 + 75, 638))
    SCREEN.blit(SURFACE, (0, 0))
    
    # hi score button shows the high scores
    hi_score = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 425, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('HIGH SCORES', True, 'black'), (SCREEN_WIDTH / 4 + 40, 438))
    SCREEN.blit(SURFACE, (0, 0))
    
    # title card
    pygame.draw.rect(SURFACE, (20, 20, 20), [SCREEN_WIDTH / 4 - 20, 25, 280, 200])
    SURFACE.blit(TITLE_FONT.render('SPACE SHOOTER', True, 'white'), (SCREEN_WIDTH / 4 - 20, 25))
    SURFACE.blit(TITLE_FONT.render('GAME', True, 'white'), (SCREEN_WIDTH / 4 + 65, 75))
    SURFACE.blit(FONT.render('Group 33', True, 'white'), (SCREEN_WIDTH / 4 + 65, 150))
    screen.blit(SURFACE, (0, 0))
    
    return play, quit_game, log_in, sign_up, hi_score
    

# draw the main pause menu
def draw_pause_menu(screen, upgrades, points):
    # main pause menu is gray and slightly transparent
    pygame.draw.rect(SURFACE, (128, 128, 128, 20), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.blit(SURFACE, (0, 0))
    
    # tell the user how many points they have
    screen.blit(FONT.render("POINTS: " + str(points), True, 'black'), (150, 0))
    
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
    quit_game = draw_exit_menu(screen)
    
    # same as above for the prettier sprites
    if (upgrades[5] == 0):
        sprites = draw_sprites(screen)
    else:
        sprites = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 25555, 25555, 280, 50], 0, 10)
        
    # make the back button
    back_button = pygame.draw.rect(SURFACE, 'white', [1, 1, 90, 50], 0, 10)
    SURFACE.blit(FONT.render('BACK', True, 'black'), (16, 13))
    SCREEN.blit(SURFACE, (0, 0))
    
    # return all the buttons we've made back to main
    return spread, reverse, ram, rev_spread, life, fire, sprites, quit_game, back_button
    
# draw the spread button as so:
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
    SURFACE.blit(FONT.render('NEW SPRITES: 1000p', True, 'black'), (SCREEN_WIDTH / 4, 638))
    SCREEN.blit(SURFACE, (0, 0))
    return sprites
    
# do the same for firing speed
def draw_exit_menu(screen):
    quit_game = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 725, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('QUIT', True, 'black'), (SCREEN_WIDTH / 4 + 85, 738))
    SCREEN.blit(SURFACE, (0, 0))
    return quit_game
    
# draw the hi scores
def draw_hi_scores(screen, nameArr, scoreArr):
    # background rect
    pygame.draw.rect(SURFACE, (0, 0, 0), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])
    screen.blit(SURFACE, (0, 0))
    # "HI SCORE" text on top
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 25, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('HIGH SCORES', True, 'black'), (SCREEN_WIDTH / 4 + 40, 38))
    # score 1
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 125, 280, 50], 0, 10)
    SURFACE.blit(FONT.render(nameArr[0] + '   ' +str(scoreArr[0]), True, 'black'), (SCREEN_WIDTH / 4 + 40, 138))
    # score 2
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 225, 280, 50], 0, 10)
    SURFACE.blit(FONT.render(nameArr[1] + '   ' +str(scoreArr[1]), True, 'black'), (SCREEN_WIDTH / 4 + 40, 238))
    # score 3
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 325, 280, 50], 0, 10)
    SURFACE.blit(FONT.render(nameArr[2] + '   ' +str(scoreArr[2]), True, 'black'), (SCREEN_WIDTH / 4 + 40, 338))
    # score 4
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 425, 280, 50], 0, 10)
    SURFACE.blit(FONT.render(nameArr[3] + '   ' + str(scoreArr[3]), True, 'black'), (SCREEN_WIDTH / 4 + 40, 438))
    # score 5
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 525, 280, 50], 0, 10)
    SURFACE.blit(FONT.render(nameArr[4] + '   ' + str(scoreArr[4]), True, 'black'), (SCREEN_WIDTH / 4 + 40, 538))
    # quit button
    quit_hi_scores = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 725, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('BACK', True, 'black'), (SCREEN_WIDTH / 4 + 85, 738))
    SCREEN.blit(SURFACE, (0, 0))
    # return the quit button so it can be used in main
    return quit_hi_scores

# log in screen
def draw_log_in(screen):
    # black background
    pygame.draw.rect(SURFACE, (0, 0, 0), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])
    
    # 'LOG IN' text on top
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 25, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('LOG IN', True, 'black'), (SCREEN_WIDTH / 4 + 80, 38))
    # username box
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 125, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('USERNAME:', True, 'black'), (SCREEN_WIDTH / 4 + 50, 138))
    # box for the user to type the username into
    username = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 225, 280, 50], 2)
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 325, 280, 50], 0, 10)
    # password box
    SURFACE.blit(FONT.render('PASSWORD:', True, 'black'), (SCREEN_WIDTH / 4 + 55, 338))
    # box for the user to type the password into
    password = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 425, 280, 50], 2)
    # enter button
    enter_log_in = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 625, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('ENTER', True, 'black'), (SCREEN_WIDTH / 4 + 80, 638))
    SCREEN.blit(SURFACE, (0, 0))
    # back button
    quit_log_in = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 725, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('BACK', True, 'black'), (SCREEN_WIDTH / 4 + 85, 738))
    SCREEN.blit(SURFACE, (0, 0))
    # update screen
    screen.blit(SURFACE, (0, 0))
    # return the buttons and text boxes
    return username, password, enter_log_in, quit_log_in
    
# sign up screen. similar to log in
def draw_sign_up(screen):
    # black background
    pygame.draw.rect(SURFACE, (0, 0, 0), [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT])
    # 'SIGN UP' on top
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 25, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('SIGN UP', True, 'black'), (SCREEN_WIDTH / 4 + 70, 38))
    # USERNAME text
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 125, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('USERNAME:', True, 'black'), (SCREEN_WIDTH / 4 + 50, 138))
    # username text box
    username = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 225, 280, 50], 2)
    # PASSWORD text
    pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 325, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('PASSWORD:', True, 'black'), (SCREEN_WIDTH / 4 + 55, 338))
    # password text box
    password = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 425, 280, 50], 2)
    # confirmation text box
    matchPassword = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 525, 280, 50], 2)
    # enter button
    enter_sign_up = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 625, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('ENTER', True, 'black'), (SCREEN_WIDTH / 4 + 80, 638))
    SCREEN.blit(SURFACE, (0, 0))
    # back button
    quit_sign_up = pygame.draw.rect(SURFACE, 'white', [SCREEN_WIDTH / 4 - 20, 725, 280, 50], 0, 10)
    SURFACE.blit(FONT.render('BACK', True, 'black'), (SCREEN_WIDTH / 4 + 85, 738))
    SCREEN.blit(SURFACE, (0, 0))
    # update the screen
    screen.blit(SURFACE, (0, 0))
    # return the buttons and boxes
    return username, password, matchPassword, enter_sign_up, quit_sign_up
    
def draw_game_buttons(screen):
    left = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (30, 650), 25)
    
    right = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (200, 650), 25)
    
    up = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (115, 580), 25)
    
    down = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (115, 720), 25)
    
    upright = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (157, 615), 25)
    
    downright = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (157, 685), 25)
    
    upleft = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (72, 615), 25)
    
    downleft = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (72, 685), 25)
    
    fire = pygame.draw.circle(GAME_SURFACE, (255, 255, 255, 20), (400, 650), 35)
    
    menu_button = pygame.draw.rect(GAME_SURFACE, (255, 255, 255, 100), [350, 0, 90, 50], 0, 10)
    
    GAME_SURFACE.blit(FONT.render('MENU', True, 'black'), (360, 10))
    
    screen.blit(GAME_SURFACE, (0, 0))
    pygame.display.flip()
    
    return up, left, right, down, upright, upleft, downright, downleft, fire, menu_button