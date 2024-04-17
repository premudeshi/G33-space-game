import pygame
import sys
import random
import time
from player import Player
from enemy import Enemy
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, bullets, all_sprites, enemies, enemy_bullets, upPressed
from backgrounds import draw_pause_menu, Menu, draw_spread, draw_main_menu, draw_background, draw_hi_scores, draw_log_in, draw_sign_up, draw_game_buttons
from accounts import login, signUp, storeScores, writeScores
from alien import Alien
from asteroid import Asteroid

pygame.init()
pygame.mixer.init()

FONT = pygame.font.SysFont('Georgia', 20)

class main:
    def __init__(self):
        # initialize pygame
        pygame.init()

        # set up screen
        self.WIDTH, self.HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = SCREEN
        pygame.display.set_caption("Space Shooter")

        # create player object
        self.player = Player("sprites/fancyPlayer.png", self.WIDTH // 2, self.HEIGHT // 2, speed = 5)

        # create sprite group for player  
        all_sprites.add(self.player)



    # the main menu as seen when starting the game or after dying
    def main_menu(self, logged_in, username):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/menu_theme.mp3')
        pygame.mixer.music.play(-1)
        # read the current high scores
        nameArr, scoreArr = storeScores()
        # loop until player quits or starts game
        while True:
            draw_background(self.screen)
            # main menu function 
            start, quit_game, log_in, sign_up, hi_score = draw_main_menu(self.screen)
            # handle button presses
            for event in pygame.event.get():
                # quit on quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # button is pushed, figure out which
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # game should start if player is logged in. If they arent, tell them to log in
                    if start.collidepoint(event.pos):
                        if (logged_in):
                            self.run(username)
                        else:
                            self.screen.fill((128, 128, 128))
                            pygame.draw.rect(self.screen, 'black', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], 20)
                            self.screen.blit(FONT.render('PLEASE LOG IN', True, 'white'), (140, 375))
                            pygame.display.flip()
                            time.sleep(2)
                    # let player quit if they click quit
                    elif quit_game.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    # let player log in by calling log_in_screen
                    elif log_in.collidepoint(event.pos):
                        logged_in, username = self.log_in_screen()
                        # if successfully logged in, inform the player
                        if logged_in:
                            self.screen.fill((128, 128, 128))
                            pygame.draw.rect(self.screen, 'black', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], 20)
                            self.screen.blit(FONT.render('SUCCESSFULLY LOGGED IN', True, 'white'), (75, 375))
                            pygame.display.flip()
                            time.sleep(2)
                        # if not, also inform the player
                        else:
                            self.screen.fill((128, 128, 128))
                            pygame.draw.rect(self.screen, 'black', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], 20)
                            self.screen.blit(FONT.render('INCORRECT USERNAME', True, 'white'), (100, 350))
                            self.screen.blit(FONT.render('OR PASSWORD', True, 'white'), (150, 400))
                            pygame.display.flip()
                            time.sleep(2)
                    # let player sign up by calling sign_up_screen. Pretty much the same as log in
                    elif sign_up.collidepoint(event.pos):
                        # if account successfully created, tell the player
                        if self.sign_up_screen():
                            self.screen.fill((128, 128, 128))
                            pygame.draw.rect(self.screen, 'black', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], 20)
                            self.screen.blit(FONT.render('ACCOUNT CREATED', True, 'white'), (115, 375))
                            pygame.display.flip()
                            time.sleep(2)
                        # if not, also tell the player
                        else:
                            self.screen.fill((128, 128, 128))
                            pygame.draw.rect(self.screen, 'black', [0, 0, SCREEN_WIDTH, SCREEN_HEIGHT], 20)
                            self.screen.blit(FONT.render('COULD NOT', True, 'white'), (155, 350))
                            self.screen.blit(FONT.render('CREATE ACCOUNT', True, 'white'), (120, 400))
                            pygame.display.flip()
                            time.sleep(2)
                    # if player wants to view high scores, call display_hi_scores
                    elif hi_score.collidepoint(event.pos):
                        self.display_hi_scores(nameArr, scoreArr)
            # update the screen
            pygame.display.flip()
            
    # display the high scores
    def display_hi_scores(self, nameArr, scoreArr):
        # repeat until player quits out
        while True:
            # call draw_hi_scores to show the high scores and create a back button
            back = draw_hi_scores(self.screen, nameArr, scoreArr)
            for event in pygame.event.get():
                # if player quits, let them
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if player hits back, return to the main menu
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back.collidepoint(event.pos):
                        return
                        
            pygame.display.flip()
            
    # log in screen allows the player to log into an existing account
    def log_in_screen(self):
        # create variables to hold the enterred username and password
        username = "" 
        password = ""
        # these control which textbox, if any, is open
        userActive = False 
        passActive = False
        
        while True:
            # call draw_log_in to create the display and text boxes
            usernameBox, passwordBox, enter, back = draw_log_in(self.screen)
            # create a surface for each text box
            username_surface = FONT.render(username, True, (255, 255, 255))
            password_surface = FONT.render(password, True, (255, 255, 255))
            # update the screen
            self.screen.blit(username_surface, (usernameBox.x + 5, usernameBox.y + 12))
            self.screen.blit(password_surface, (passwordBox.x + 5, passwordBox.y + 12))
            for event in pygame.event.get():
                # let player quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if player touches a button, figure out which
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if it's on the username, set it to be active
                    if usernameBox.collidepoint(event.pos):
                        userActive = True
                        passActive = False
                    # same for password
                    elif passwordBox.collidepoint(event.pos):
                        userActive = False
                        passActive = True
                    # if user hits enter, call login() to see if they successfully logged in or not and return in agreement
                    elif enter.collidepoint(event.pos):
                        return (login(username, password), username)
                    # if the user goes back, return false
                    elif back.collidepoint(event.pos):
                        return False, username
                    # otherwise, the user clicked nothing. Set both text boxes to false
                    else:
                        userActive = False
                        passActive = False
                # if the user is typing...
                if (userActive or passActive):
                    pygame.key.start_text_input()
                    if event.type == pygame.KEYDOWN:
                        # if the username is open
                        if userActive == True:
                            # if the user clicks backspace, go back 1 character
                            if event.key == pygame.K_BACKSPACE:
                                username = username[:-1]
                            # otherwise, add the character to the username string
                            else:
                                username += event.unicode
                        # do the same for the password if the password box is open
                        elif passActive == True:
                            if event.key == pygame.K_BACKSPACE:
                                password = password[:-1]
                            else:
                                password += event.unicode
                # update the display
                pygame.display.flip()
            
    # sign up is almost the exact same as log in, but with a "confirm your password" entry
    def sign_up_screen(self):
        # 3 strings and active variables
        username = "" 
        password = ""
        matchPassword = ""
        userActive = False 
        passActive = False
        matchActive = False
        while True:
            # let draw_sign_up draw everything to the screen
            usernameBox, passwordBox, matchBox, enter, back = draw_sign_up(self.screen)
            # render the surfaces and draw them to the screen
            username_surface = FONT.render(username, True, (255, 255, 255))
            password_surface = FONT.render(password, True, (255, 255, 255))
            match_surface = FONT.render(matchPassword, True, (255, 255, 255))
            self.screen.blit(username_surface, (usernameBox.x + 5, usernameBox.y + 12))
            self.screen.blit(password_surface, (passwordBox.x + 5, passwordBox.y + 12))
            self.screen.blit(match_surface, (matchBox.x + 5, matchBox.y + 12))
            for event in pygame.event.get():
                # let player quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if player clicks determine where
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if they click on the username box, set it active
                    if usernameBox.collidepoint(event.pos):
                        userActive = True
                        passActive = False
                        matchActive = False
                    # same for password
                    elif passwordBox.collidepoint(event.pos):
                        userActive = False
                        passActive = True
                        matchActive = False
                    # same for the second password
                    elif matchBox.collidepoint(event.pos):
                        userActive = False
                        passActive = False
                        matchActive = True
                    # if they hit enter, return in agreement with signUp
                    elif enter.collidepoint(event.pos):
                        return (signUp(username, password, matchPassword))
                    # if they hit back, return false
                    elif back.collidepoint(event.pos):
                        return False
                    # otherwise, they clicked out of all text boxes
                    else:
                        userActive = False
                        passActive = False
                        matchActive = False
                if event.type == pygame.KEYDOWN:
                    # once again, type in box that's currently active. -1 char if player backspaces
                    if userActive == True:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += event.unicode
                    elif passActive == True:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        else:
                            password += event.unicode
                    elif matchActive == True:
                        if event.key == pygame.K_BACKSPACE:
                            matchPassword = matchPassword[:-1]
                        else:
                            matchPassword += event.unicode
            # update display
            pygame.display.flip()

    def run(self, username):
        # game loop
        running = True
        # game starts not paused
        paused = False
        # timer that controls when the first enemies spawn
        spawnTimer = random.randint(60, 120)
        # keep track of high scores in case we beat one
        nameArr, scoreArr = storeScores()
        # define the level the player starts on
        LEVEL = 1
        # reset points to 0 at start of new game and remove all upgrades
        self.player.points = 0
        self.player.upgrades = self.upgrades = [0, 0, 0, 0, 3, 0, 0] # in order: spread, reverse, reverse spread, battering ram, lives, sprite, fire rate
        # reset the player's model
        self.player.change_sprite("sprites/FancyPlayer.png")
        # kill any enemies that exist from the last time the game was played
        for enemy in enemies:
            all_sprites.remove(enemy)
            enemies.remove(enemy)
            self.player.points += (15 * LEVEL * enemy.points)
        # play the game music
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/game_theme.mp3')
        pygame.mixer.music.play(-1)
        # runs until player quits
        while running:
            # events are quitting, pausing/unpausing, and buying in the shop
            for event in pygame.event.get():
                # quit when player wants to quit
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # using p to pause for right now. Will be changed to touchscreen button when switched to mobile
                    if event.key == pygame.K_p:
                        if paused == False:
                            paused = True
                        else:
                            paused = False
                # shop items already touchscreen compatible
                if event.type == pygame.MOUSEBUTTONDOWN and paused:
                    # spread shot button
                    if spread.collidepoint(event.pos):
                        if (self.player.points >= 1000):
                            self.player.points -= 1000
                            self.player.upgrades[0] = 1
                    # reverse shot button
                    elif reverse.collidepoint(event.pos):
                        if (self.player.points >= 500):
                            self.player.points -= 500
                            self.player.upgrades[1] = 1
                    # reverse spread shot button
                    elif rev_spread.collidepoint(event.pos):
                        if (self.player.points >= 1500):
                            self.player.points -= 1500
                            self.player.upgrades[2] = 1
                    # battering ram button
                    elif ram.collidepoint(event.pos):
                        if (self.player.points >= 2500):
                            self.player.points -= 2500
                            self.player.upgrades[3] = 1
                    # life up button
                    elif life.collidepoint(event.pos):
                        if (self.player.points >= 5000):
                            self.player.points -= 5000
                            self.player.upgrades[4] += 1
                    # firing speed up button
                    elif fire.collidepoint(event.pos):
                        if (self.player.points >= 1000):
                            self.player.points -= 1000
                            self.player.upgrades[6] += 1
                    # secondary sprite option for the player
                    elif sprites.collidepoint(event.pos):
                        if (self.player.points >= 1000):
                            self.player.change_sprite("sprites/PlayerModel1.png")
                            self.player.upgrades[5] = 1
                            self.player.points -= 1000
                    # quit game by killing player
                    elif quit_game.collidepoint(event.pos):
                        self.player.upgrades[4] = 0
                        paused = False
                    # unpause if player hits back
                    elif back_button.collidepoint(event.pos):
                        paused = False
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if up.collidepoint(event.pos):
                        self.player.upPressed = True
                    elif down.collidepoint(event.pos):
                        self.player.downPressed = True
                    elif left.collidepoint(event.pos):
                        self.player.leftPressed = True
                    elif right.collidepoint(event.pos):
                        self.player.rightPressed = True
                    elif upright.collidepoint(event.pos):
                        self.player.uprightPressed = True
                    elif upleft.collidepoint(event.pos):
                        self.player.upleftPressed = True
                    elif downright.collidepoint(event.pos):
                        self.player.downrightPressed = True
                    elif downleft.collidepoint(event.pos):
                        self.player.downleftPressed = True
                    elif fire_button.collidepoint(event.pos):
                        self.player.firePressed = True
                    elif menu_button.collidepoint(event.pos):
                        paused = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.player.upPressed = False
                    self.player.downPressed = False
                    self.player.rightPressed = False
                    self.player.leftPressed = False
                    self.player.uprightPressed = False
                    self.player.upleftPressed = False
                    self.player.downrightPressed = False
                    self.player.downleftPressed = False
                    self.player.firePressed = False
            
            # when game is running
            if not paused:
                # update all sprites
                all_sprites.update()
            
                # If player touches enemy bullet, kill them
                enemy_bullet_collisions = pygame.sprite.spritecollide(self.player, enemy_bullets, True)
                for bullet in enemy_bullet_collisions:
                    if (self.player.i_frames <= 0):
                        self.player.decrement_lives()
                        for enemy in enemies:
                            all_sprites.remove(enemy)
                            enemies.remove(enemy)

                # if player shoots an enemy, kill the enemy. Will add explosion later
                for enemy in enemies:
                    player_bullet_collisions = pygame.sprite.spritecollide(enemy, bullets, True)
                    for bullet in player_bullet_collisions:
                        if bullet.origin != 1 and bullet.origin != 7:  # check if bullet origin is not from enemy (must be from player)
                            # kill the enemy 
                            all_sprites.remove(enemy)
                            enemies.remove(enemy)
                            self.player.points += (15 * enemy.points)

                # if enemy touches player, kill player unless they have battering ram upgrade, in which case kill enemy
                for enemy in enemies:
                    # while already looping through enemies, we add their random ability to track the player
                    if (random.randint(1, 50) == 1 and enemy.points == 3):
                        # every frame that the enemy is moving away from the player, they have a 2% chance to correct themselves
                        if (((self.player.rect.x - enemy.rect.x > 0) and (enemy.direction == -1))) or ((self.player.rect.x - enemy.rect.x < 0) and (enemy.direction == 1)):
                            enemy.direction = enemy.direction * -1
                    if pygame.sprite.collide_rect(self.player, enemy):
                        # determine if player has battering ram or if they ran into an asteroid, which still kills them
                        if self.player.upgrades[3] == 0 or enemy.points == 1:
                            # if not, kill player
                            self.player.decrement_lives()
                            for enemy in enemies:
                                all_sprites.remove(enemy)
                                enemies.remove(enemy)
                        else:
                            # if so, kill the enemy 
                            all_sprites.remove(enemy)
                            enemies.remove(enemy)
                            self.player.points += (15 * enemy.points)


                # update the screen
                draw_background(self.screen)
                all_sprites.draw(self.screen)
                self.screen.blit(FONT.render("LIVES: " + str(self.player.upgrades[4]), True, 'white'), (25, 0))
                self.screen.blit(FONT.render("POINTS: " + str(self.player.points), True, 'white'), (150, 0))
                self.screen.blit(FONT.render("LEVEL: " + str(LEVEL), True, 'white'), (25, 25))
                up, left, right, down, upright, upleft, downright, downleft, fire_button, menu_button = draw_game_buttons(self.screen)
                pygame.display.flip()

                # ensure game runs at 60fps
                pygame.time.Clock().tick(60)
                self.player.cooldown -= 1
                
                # if player has active i frames from dying, decrease them
                if self.player.i_frames > 0:
                    self.player.i_frames -= 1
                
                # if an enemy is due to spawn, spawn them as so:
                if spawnTimer <= 0:
                    # pick a random number of enemies based on the level
                    for i in range(LEVEL * random.randint(1, 2) - 2 * random.randint(0, LEVEL) + 1):
                        # summon the enemy at a random position offscreen
                        enemy = Enemy("sprites/EnemyModel1.png", random.randint(0, 400), random.randint(1, 5) * -50, speed = 2 * (pow(1.05, LEVEL)))
                        # create the enemy
                        enemy.image = pygame.transform.scale(enemy.image, (SCREEN_WIDTH // 9, SCREEN_HEIGHT // 16))
                        enemy.rect.width = SCREEN_WIDTH // 9
                        enemy.rect.height = SCREEN_HEIGHT // 16
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                    if (random.randint(1, 10) < LEVEL): # ALIEN
                        alien = Alien("sprites/UFO.png", 600, self.player.rect.y + 200, speed = 2)
                        # create the alien
                        alien.image = pygame.transform.scale(alien.image, (SCREEN_WIDTH // 9, SCREEN_HEIGHT // 16))
                        alien.rect.width = SCREEN_WIDTH // 9
                        alien.rect.height = SCREEN_HEIGHT // 16
                        all_sprites.add(alien)
                        enemies.add(alien)
                    if (random.randint(0, 5) < LEVEL): # METEOR
                        asteroid = Asteroid("sprites/asteroid.png", 600, self.player.rect.y - 600, speed = 7)
                        # create the asteroid
                        asteroid.image = pygame.transform.scale(asteroid.image, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 8))
                        asteroid.rect.width = SCREEN_WIDTH // 6
                        asteroid.rect.height = SCREEN_HEIGHT // 8
                        all_sprites.add(asteroid)
                        enemies.add(asteroid)
                    # reset the timer
                    spawnTimer = random.randint(180, 240)
                    
                # otherwise, decrease their timer
                else:
                    spawnTimer -= 1
                    
                # level the player up every 350 points they get and award them 50 points
                if (self.player.points >= 350 * LEVEL):
                    LEVEL += 1
                    self.player.points += 50
                    
                # send the player back to the main menu when they game over
                if self.player.upgrades[4] == 0:
                    writeScores(nameArr, scoreArr, username, self.player.points)
                    self.main_menu(True, username)
                    
                    
                
                
                
                
            
            # if game is paused, call the pause screen options in backgrounds.py
            else:
                spread, reverse, ram, rev_spread, life, fire, sprites, quit_game, back_button = draw_pause_menu(self.screen, self.player.upgrades, self.player.points)
                pygame.display.flip()
        
        # quit, will be replaced to send back to main menu when implemented
        pygame.quit()
        sys.exit()

# run the game
if __name__ == "__main__":
    game = main()
    game.main_menu(False, '')
