import pygame
from ship import Ship
from constants import SCREEN_HEIGHT

class Bullet(Ship):
    def __init__(self, image_path, x, y, speed, origin):
        super().__init__(image_path, x, y)
        self.speed = speed
        # origin defines what type of bullet it is (player normal, player spread, enemy, etc)
        self.origin = origin  

    def update(self):
        # move bullet 
        if (self.origin == 0): 
            # normal player bullet, moves up
            self.rect.y -= self.speed * 2
        elif (self.origin == 1): 
            # enemy bullet, moves down
            self.rect.y += self.speed * 2
        elif (self.origin == 2): 
            # player spread bullet A, moves diagonally
            self.rect.y -= self.speed * 2
            self.rect.x += self.speed - 3
        elif (self.origin == 3): 
            # player spread bullet B, moves diagonally 
            self.rect.y -= self.speed * 2
            self.rect.x -= self.speed - 3
        elif (self.origin == 4): 
            # reverse shot
            self.rect.y += self.speed * 2
        elif (self.origin == 5): 
            # player reverse spread bullet A, moves diagonally
            self.rect.y += self.speed * 2
            self.rect.x += self.speed - 3
        elif (self.origin == 6): 
            # player reverse spread bullet B, moves diagonally
            self.rect.y += self.speed * 2
            self.rect.x -= self.speed - 3

        # if bullet is out of bounds, kill it
        if self.rect.bottom < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.kill()