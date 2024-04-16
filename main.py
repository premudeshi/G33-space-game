import pygame
import sys
import random
from player import Player
from enemy import Enemy
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, bullets, all_sprites, enemies, enemy_bullets, LEVEL
from backgrounds import draw_pause_menu, Menu, draw_spread, draw_main_menu, draw_background
from accounts import login, signUp
from alien import Alien
from asteroid import Asteroid

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


    def main_menu(self):
        while True:
            start, quit_game = draw_main_menu(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start.collidepoint(event.pos):
                        self.run()
                    elif quit_game.collidepoint(event.pos):
                        pygame.quit()
                        return
                        
            pygame.display.flip()

    def run(self):
        # game loop
        running = True
        # game starts not paused
        paused = False
        # timer that controls when the first enemies spawn
        spawnTimer = random.randint(60, 120)
        # runs until player games over. Will be edited to when player quits out of the main menu when implemented
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
                    # TODO: ADD NEW SPRITES
            
            # when game is running
            if not paused:
                # quit out if player game overs. Will be updated to send to the main menu when implemented.
                if self.player.upgrades[4] == 0:
                    quit()
                
                
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
                            self.player.points += (15 * LEVEL)

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
                            self.player.points += (15 * LEVEL * enemy.points)


                # update the screen
                draw_background(self.screen)
                all_sprites.draw(self.screen)
                self.screen.blit(FONT.render("LIVES: " + str(self.player.upgrades[4]), True, 'white'), (25, 0))
                self.screen.blit(FONT.render("POINTS: " + str(self.player.points), True, 'white'), (150, 0))
                self.screen.blit(FONT.render("LEVEL: " + str(LEVEL), True, 'white'), (25, 25))
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
                    spawnTimer = random.randint(180, 300)
                    
                # otherwise, decrease their timer
                else:
                    spawnTimer -= 1
                    
                ##if self.player.points > 1500 * LEVEL:
                  ##  self.player.points += 500 * LEVEL
                   ## LEVEL += 1
            
            # if game is paused, call the pause screen options in backgrounds.py
            else:
                spread, reverse, ram, rev_spread, life, fire, sprites = draw_pause_menu(self.screen, self.player.upgrades)
                pygame.display.flip()
        
        # quit, will be replaced to send back to main menu when implemented
        pygame.quit()
        sys.exit()

# run the game
if __name__ == "__main__":
    game = main()
    game.main_menu()