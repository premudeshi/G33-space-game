import pygame

import BulletClass
#total Time

class Player:
    #variables
    augments = ['machineGun', 'powerGun', 'sheild', 'hyperdrive']
    baseCooldown = 500
    movement = 30
    #constructor
    def __init__(self, model,windowWidth,windowHeight):
        # model stuff
        self.model = pygame.image.load(model)
        self.model = pygame.transform.scale(self.model, (100,100))
        self.modelCenter = [(self.model.get_width()/2),(self.model.get_height()/2)]
        # movement
        self.x = (windowWidth / 2) - self.modelCenter[0]
        self.y =  ((3*windowHeight)/4) - self.modelCenter[1]
        # mechanics
        self.lastshoot = 0
        self.cooldown = self.baseCooldown
        # hitbox
        self.hitbox = pygame.Rect(0,0,100, 100) 
        self.hitbox = self.hitbox.move(self.x,self.y)
        # playerInfo
        self.score = 0
        self.attackAugment = 'none'
        self.defenseAugment = 'none'
        if self.defenseAugment == 'hyperdrive':
            self.lastHyperdrive = 0

    #helper functions
    def getModel(self):
        return self.model
    def getPosition(self):
        return (self.x,self.y)
    def move(self,xDirection, yDirection,windowWidth,windowHeight):
        multiplier = 1
        if self.defenseAugment == 'hyperdrive' and self.lastHyperdrive <= 0:
         keys = pygame.key.get_pressed()
         if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
             self.lastHyperdrive = 1000
             multiplier = 4
        x = self.x + (xDirection * self.movement*multiplier)
        y = self.y + (yDirection * self.movement*multiplier)
        if self.valid(x,y,windowWidth,windowHeight):
            self.x = x
            self.y = y
            self.hitbox =  self.hitbox.move((xDirection * self.movement * multiplier), (yDirection * self.movement * multiplier))
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
            if self.attackAugment == 'machineGun' :
                self.cooldown = self.cooldown - 20
                if self.cooldown <= 50:
                    self.cooldown = 50
            elif self.attackAugment == 'powerGun':
                return BulletClass.Bullet('player', self.x,(self.y - self.model.get_height()), '128\\PlayerBullet.png', 75)
            return BulletClass.Bullet('player', self.x,(self.y - self.model.get_height()), '128\\PlayerBullet.png', 50)
    def adjustScore(self,amount):
        self.score += amount
    def getScore(self):
        return self.score
    def upgrade(self, augment, cost):
            if augment in augments:
                 if augment == 'machineGun' or augment == 'chargeShot':
                    self.attackAugment = augment
                    self.score = self.score - cost
                 else:
                    self.defenseAugment=augment
                    self.score = self.score - cost
    def getUpgrades(self):
        return [self.attackAugment, self.defenseAugment]
    def changeDefenseAugment(self, new):
        self.defenseAugment = new
    def changeAttackAugment(self, new):
        self.attackAugment = new
    def purchase(self, attackAugment, defenseAugment):
        if attackAugment != 'none':
            self.attackAugment = attackAugment
        if defenseAugment != 'none':
            self.defenseAugment = defenseAugment
    def playerUpdate(self,window):
        # this function is used for two cases
        #   1) common player functions
        #   2) upgrade functions
        # if upgrade requires an undo then we use this
        if self.cooldown < self.baseCooldown:
            self.cooldown += 5
        if self.cooldown > self.baseCooldown:
            self.cooldown = self.baseCooldown
        if self.defenseAugment == 'hyperdrive':
            self.lastHyperdrive -= 1
        window.blit(self.getModel(),self.getPosition())