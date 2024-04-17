import pygame
import random
from ship import Ship
from bullet import Bullet
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, bullets, all_sprites, enemy_bullets

class Asteroid(Ship):
    def __init__(self, image_path, x, y, speed, direction=1):
        super().__init__(image_path, x, y)
        self.speed = speed
        # controls if enemy moves left or right
        self.direction = direction
        self.bounces = 0
        self.points = 1

    def update(self):
        # move horizontally
        self.rect.x -= self.speed * self.direction
        self.rect.y += self.speed * self.direction

    # asteroids cannot shoot because they have no hands to hold a gun.