import pygame
import time
from ship import Ship
from bullet import Bullet
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, bullets, all_sprites

class Player(Ship):
    def __init__(self, image_path, x, y, speed):
        # initialize the player
        super().__init__(image_path, x - 25, y)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH // 9, SCREEN_HEIGHT // 16))
        self.rect.width = SCREEN_WIDTH // 9
        self.rect.height = SCREEN_HEIGHT // 16
        self.cooldown = 0  # shooting cooldown starts at 0
        self.points = 500000
        self.upgrades = [0, 0, 0, 0, 3, 0, 0] # in order: spread, reverse, reverse spread, battering ram, lives, sprite, fire rate
        self.speed = speed
        self.i_frames = 30 # give player half a second of i frames at the start

    def update(self):
        # lets the player move
        speed_x = 0
        speed_y = 0
        keys = pygame.key.get_pressed()
        # left
        if keys[pygame.K_LEFT]:
            speed_x = -self.speed
        # right
        if keys[pygame.K_RIGHT]:
            speed_x = self.speed
        # up
        if keys[pygame.K_UP]:
            speed_y = -self.speed
        # down
        if keys[pygame.K_DOWN]:
            speed_y = self.speed
        # fire a shot
        if keys[pygame.K_SPACE]:
            Player.fire_bullet(self)

        # Move the player
        self.move(speed_x, speed_y)
        
        # Ensure the player stays within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        
    # function that lets the player shoot
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
            
            # reset the cooldown. It lasts half a second minus 3 frames for every fire rate upgrade the player buys
            self.cooldown = 30 - 3 * self.upgrades[6]
    
    # damage the player by lower the number of lives they have. Then reset them back to the center of the screen, pause for a second, and give them a second of i frames
    def decrement_lives(self):
        self.upgrades[4] -= 1
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.i_frames = 60
        time.sleep(0.3)
    

    