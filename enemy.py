import pygame
import random
from ship import Ship
from bullet import Bullet
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, bullets, all_sprites, enemy_bullets

enemy_laser = pygame.mixer.Sound('sounds/enemy_fire.mp3')

class Enemy(Ship):
    def __init__(self, image_path, x, y, speed, direction=1):
        super().__init__(image_path, x, y)
        self.speed = speed
        # controls if enemy moves left or right
        self.direction = direction
        # bullet cooldown between 1 and 2 seconds
        self.cooldown = random.randint(60, 120)
        self.points = 3

    def update(self):
        # move horizontally
        self.rect.x += self.speed * self.direction


        # check if enemy has reached edges
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            # change direction if so
            self.direction *= -1

        # move downwards
        self.rect.y += self.speed 
        
        # if cant fire yet, decrease cooldown
        if (self.cooldown > 0):
            self.cooldown -= 1
            
        # otherwise, shoot
        self.fire_bullet()
    
    # enemy firing much simpler than player
    def fire_bullet(self):
        # if on cooldown, do nothing
        if self.cooldown > 0:
            return
        # otherwise, we fire
        else:
            # bullet comes at bottom center
            bullet_x = self.rect.x + 7
            bullet_y = self.rect.bottom

            # create new bullet and add it to group. Origin 1 is for enemies
            new_bullet = Bullet("sprites/EnemyBullet.png", bullet_x, bullet_y, 5, origin=1)
            enemy_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            self.cooldown = random.randint(60, 180)
            # play its sound effect
            pygame.mixer.Sound.play(enemy_laser)