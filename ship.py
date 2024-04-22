import pygame

# basic ship class to be extended
class Ship(pygame.sprite.Sprite):

    # ships have an image and position
    def __init__(self, image_path, x, y):
        super(Ship, self).__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    # ships are able to move
    def move(self, speed_x, speed_y):
        self.rect.x += speed_x
        self.rect.y += speed_y