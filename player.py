import pygame
import time
from ship import Ship
from bullet import Bullet
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, bullets, all_sprites, upPressed

pygame.init()
pygame.mixer.init()

player_laser = pygame.mixer.Sound('sounds/player_fire.ogg')
player_explosion = pygame.mixer.Sound('sounds/player_explosion.ogg')
explosion = [pygame.image.load("sprites/explosion/explosion1.png"),
    pygame.image.load("sprites/explosion/explosion2.png"),
    pygame.image.load("sprites/explosion/explosion3.png"),
    pygame.image.load("sprites/explosion/explosion4.png"),
    pygame.image.load("sprites/explosion/explosion5.png"),
    pygame.image.load("sprites/explosion/explosion6.png"),
    pygame.image.load("sprites/explosion/explosion7.png"),
    pygame.image.load("sprites/explosion/explosion8.png")]

class Player(Ship):
    def __init__(self, image_path, x, y, speed):
        # initialize the player
        super(Player, self).__init__(image_path, x - 25, y)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH // 9, SCREEN_HEIGHT // 16))
        self.rect.width = SCREEN_WIDTH // 9
        self.rect.height = SCREEN_HEIGHT // 16
        self.cooldown = 0  # shooting cooldown starts at 0
        self.points = 0
        self.upgrades = [0, 0, 0, 0, 3, 0, 0] # in order: spread, reverse, reverse spread, battering ram, lives, sprite, fire rate
        self.speed = speed
        self.i_frames = 30 # give player half a second of i frames at the start
        self.original_image = self.image # keep track of original image in case user buys the new sprite option
        self.upPressed, self.downPressed, self.rightPressed, self.leftPressed, self.uprightPressed, self.upleftPressed, self.downrightPressed, self.downleftPressed, self.firePressed = False, False, False, False, False, False, False, False, False
        self.currImage = self.image

    def update(self):
        # lets the player move
        speed_x = 0
        speed_y = 0
        keys = pygame.key.get_pressed()
        # left
        if keys[pygame.K_LEFT]  or self.leftPressed or self.upleftPressed or self.downleftPressed:
            speed_x = -self.speed
        # right
        if keys[pygame.K_RIGHT]  or self.rightPressed or self.uprightPressed or self.downrightPressed:
            speed_x = self.speed
        # up
        if keys[pygame.K_UP] or self.upPressed or self.uprightPressed or self.upleftPressed:
            speed_y = -self.speed
        # down
        if keys[pygame.K_DOWN] or self.downPressed or self.downrightPressed or self.downleftPressed:
            speed_y = self.speed
        # fire a shot
        if keys[pygame.K_SPACE] or self.firePressed:
            Player.fire_bullet(self)

        # move the player
        self.move(speed_x, speed_y)
        
        # keep player stays within screen boundaries
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        
    # function that lets player shoot
    def fire_bullet(self):
        # if player is still on cooldown, dont shoot
        if self.cooldown > 0:
            return
        # if not, then...
        else:
            # set bullet to spawn at top of player head
            bullet_x = self.rect.x + 9
            bullet_y = self.rect.y - 20

            # create new bullet and add it to group
            new_bullet = Bullet("sprites/PlayerBullet.png", bullet_x, bullet_y, 5, origin=0)
            bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            
            # if player has spread, create 2 more bullets that shoot out from there
            if self.upgrades[0] == 1:
                # bullet 1
                new_bullet_A = Bullet("sprites/PlayerBullet.png", bullet_x, bullet_y, 5, origin=2)
                bullets.add(new_bullet_A)
                all_sprites.add(new_bullet_A)
                # bullet 2
                new_bullet_B = Bullet("sprites/PlayerBullet.png", bullet_x, bullet_y, 5, origin=3)
                bullets.add(new_bullet_B)
                all_sprites.add(new_bullet_B)
            
            # if player has reverse, create bullet from behind
            if self.upgrades[1] == 1:
                bullet_x = self.rect.x + 9
                bullet_y = self.rect.bottom - 5
                new_bullet_reverse = Bullet("sprites/PlayerBullet.png", bullet_x, bullet_y, 5, origin=4)
                # flip bullet backwards
                new_bullet_reverse.image = pygame.transform.rotate(new_bullet_reverse.image, 180)
                bullets.add(new_bullet_reverse)
                all_sprites.add(new_bullet_reverse)
            
            # if player has reverse spread, create 2 more
            if self.upgrades[2] == 1:
                # bullet 1
                new_bullet_reverse_A = Bullet("sprites/PlayerBullet.png", bullet_x, bullet_y, 5, origin=5)
                # flip backwards
                new_bullet_reverse_A.image = pygame.transform.rotate(new_bullet_reverse_A.image, 180)
                bullets.add(new_bullet_reverse_A)
                all_sprites.add(new_bullet_reverse_A)
                # bullet 2
                new_bullet_reverse_B = Bullet("sprites/PlayerBullet.png", bullet_x, bullet_y, 5, origin=6)
                # flip backwards
                new_bullet_reverse_B.image = pygame.transform.rotate(new_bullet_reverse_B.image, 180)
                bullets.add(new_bullet_reverse_B)
                all_sprites.add(new_bullet_reverse_B)
            
            # play its sound effect
            pygame.mixer.Sound.play(player_laser)
            
            # reset the cooldown. It lasts half a second minus 3 frames for every fire rate upgrade the player buys
            self.cooldown = 30 - 3 * self.upgrades[6]
    
    # damage the player by lower the number of lives they have. Then reset them back to the center of the screen, pause for a second, and give them a second of i frames
    def decrement_lives(self, screen):
        self.currImage = self.image
        self.i_frames = 60
        pygame.mixer.Sound.play(player_explosion)
        for i in range(8):
            self.image = explosion[i]
            self.draw_background(screen)
            all_sprites.draw(screen)
            pygame.display.flip()
            time.sleep(.1)
        self.upgrades[4] -= 1
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.image = self.currImage
        if (self.upgrades[4] > 0):
            time.sleep(.5)
        
        
    # change the player image in case user buys new sprite upgrade
    def change_sprite(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH // 9, SCREEN_HEIGHT // 16))
    
    # required to make the explosion work
    def draw_background(self, screen):
        background = pygame.image.load('sprites/background.png')
        screen.blit(background, (0, 0))

    