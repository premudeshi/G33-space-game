import pygame
import random
from ship import Ship
from bullet import Bullet
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, bullets, all_sprites, enemy_bullets

pygame.init()
pygame.mixer.init()

alien_laser = pygame.mixer.Sound('sounds/alien_fire.mp3')


class Alien(Ship):
    def __init__(self, image_path, x, y, speed, direction=1):
        super().__init__(image_path, x, y)
        self.speed = speed
        # controls if enemy moves left or right
        self.direction = direction
        # bullet cooldown between .5 and 1 second
        self.cooldown = random.randint(30, 60)
        self.bounces = 0
        self.points = 5

    def update(self):
        # move horizontally
        self.rect.x -= self.speed * self.direction
   
        # if cant fire yet, decrease cooldown
        if (self.cooldown > 0):
            self.cooldown -= 1
            
        # check if enemy has reached edges
        if (self.rect.right >= SCREEN_WIDTH and self.direction == -1 ) or (self.rect.left <= 0 and self.direction == 1):
            if (self.bounces < 2):
                # change direction if so. Should only happen twice before the enemy leaves if it still hasnt been killed
                self.direction *= -1
                self.bounces += 1
            
        # otherwise, shoot
        self.fire_bullet()
    
    # enemy firing much simpler than player
    def fire_bullet(self):
        # if on cooldown, do nothing
        if self.cooldown > 0:
            return
        # otherwise, we fire
        else:
            # bullet comes at top center
            bullet_x = self.rect.x + 7
            bullet_y = self.rect.top

            # create new bullet and add it to group. Origin 7 is for enemies that shoot upwards
            new_bullet = Bullet("sprites/EnemyBullet.png", bullet_x, bullet_y, 5, origin=7)
            new_bullet.image = pygame.transform.rotate(new_bullet.image, 180)
            enemy_bullets.add(new_bullet)
            all_sprites.add(new_bullet)
            self.cooldown = random.randint(60, 180)
            # play its sound effect
            pygame.mixer.Sound.play(alien_laser)