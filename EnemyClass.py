import pygame
import BulletClass

class Enemy:
    #variables

    #constructor
    def __init__(self, model,windowWidth,windowHeight,cooldown,movement,modelSize):
        # model stuff
        self.model = pygame.image.load(model)
        self.model = pygame.transform.scale(self.model, (modelSize,modelSize))
        self.modelCenter = [(self.model.get_width()/2),(self.model.get_height()/2)]
        # movement
        self.x = (windowWidth / 2) - self.modelCenter[0]
        self.y =  ((windowHeight)/4) - self.modelCenter[1]
        self.movement = movement
        #mechanics 
        self.lastshoot = 0
        self.cooldown =  cooldown
        # hitbox
        self.hitbox = pygame.Rect(0,0,modelSize, modelSize) 
        self.hitbox = self.hitbox.move(self.x,self.y)

    #helper functions
    def getModel(self):
        return self.model
    def getPosition(self):
        return (self.x,self.y)
    def move(self, xDirection, yDirection,windowWidth,windowHeight):
        x = self.x + (xDirection * self.movement)
        y = self.y + (yDirection * self.movement)

        '''
        if self.valid(x,y,windowWidth,windowHeight):
            self.x = x
            self.y = y
            self.hitbox = self.hitbox.move(0,-self.movement)
            print("invalid")
        '''

        self.x = x
        self.y = y
        self.hitbox = self.hitbox.move(0, -self.movement)

    def valid(self,x,y,windowWidth,windowHeight):
        if x > (self.model.get_width()/4) and x < (windowWidth - (self.model.get_width())):
            if y > ((5 * windowHeight)/8) and y < ((5*windowHeight)/6):
                return True
        else:
            return False
    def getCooldown(self):
        return self.cooldown
    def setLastShoot(self, time):
        self.lastshoot = time
    def getLastShoot(self):
        return self.lastshoot
    def getHitbox(self):
        return self.hitbox
    def pew (self):
        self.setLastShoot(pygame.time.get_ticks())
        return BulletClass.Bullet('enemy', self.x,(self.y - self.model.get_height()), 'EnemyBullet.png',50,10)

    def getWorth(self):
        return 10