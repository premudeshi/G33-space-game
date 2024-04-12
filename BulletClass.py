import pygame

class Bullet: 
    movement = 5
    def __init__(self, origin, x, y, model, size, worth):
        self.origin = origin
        self.worth = worth
        self.model = pygame.image.load(model)
        self.model = pygame.transform.scale(self.model, (size,size))
        self.modelCenter = [(self.model.get_width()/2),(self.model.get_height()/2)]

        self.x = x + int(self.modelCenter[0])
        self.y = y + int(self.modelCenter[1])

        self.hitbox = pygame.Rect(0,0, size, size) 
        self.hitbox = self.hitbox.move(self.x,self.y)
    def __str__(self):
        return f"bullet was shot by {self.origin} and its current poition is ({x},{y})"
    def move(self):
        if self.origin == 'player':
            self.y -= self.movement
            self.hitbox = self.hitbox.move(0,-self.movement)
        else:
            self.y += self.movement
            self.hitbox = self.hitbox.move(0,self.movement)
    def getModel(self):
        return self.model
    def getPosition(self): 
        return (self.x,self.y)
    def offScreen(self, screenX, screenY):
        if self.x > screenX or self.x < 0:
            return True
        elif self.y > screenY or self.y < 0:
            return True
        else:
            return False
    def getHitbox(self):
        return self.hitbox
    def getOrigin(self):
        return self.origin