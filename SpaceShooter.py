import pygame
import pandas as pd

import BulletClass as pew
import PlayerClass
import EnemyClass
""" Usefull Functions"""

"""start of the game"""
#variables 
windowHeight = 0
windowWidth = 0
gameStatus = True
FPS = 60
modelPath = 'PlayerModel1.png' # put the remainder of your directory here with loaded png
enemyCount = 0 # used to set limit on enemies in game may use point system for type of enemy later
spawnTimer = 0
spawnInterval = 5000
bullets = []
enemies = [] 
menuQuite = False

#game init
(passes, fails) = pygame.init()
pygame.key.set_repeat(50,50)
clock = pygame.time.Clock()

windowHeight = pygame.display.Info().current_h
windowWidth = pygame.display.Info().current_w

color = (0,0,0)
window = pygame.display.set_mode((windowWidth,windowHeight))
window.fill(color)
#player init
player = PlayerClass.Player(modelPath,windowWidth,windowHeight)
window.blit(player.getModel(),player.getPosition())
#running game
#screen init
while gameStatus:
    window.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameStatus = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1,0,windowWidth,windowHeight)
        if keys[pygame.K_RIGHT]:
            player.move(1,0,windowWidth,windowHeight)
        if keys[pygame.K_UP]:
            player.move(0,-1,windowWidth,windowHeight)
        if keys[pygame.K_DOWN]:
            player.move(0,1,windowWidth,windowHeight)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and (pygame.time.get_ticks() - player.getLastShoot()) >= player.getCooldown():
            bullets.append(player.pew())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            gameStatus = False
        if spawnTimer >= spawnInterval and enemyCount < 3:
            spawnTimer = 0
            enemy = EnemyClass.Enemy("EnemyModel1.png",windowWidth,windowHeight,350,45,60,)
            enemies.append(enemy)
            window.blit(enemy.getModel(), enemy.getPosition())

    player.playerUpdate(window)

    pygame.draw.rect(window, (0, 255, 0), player.getHitbox(), 1)
    for bullet in  bullets: 
        bullet.move()
        window.blit(bullet.getModel(), bullet.getPosition())
        pygame.draw.rect(window, (255, 0, 0), bullet.getHitbox(), 1)  # Draw bullet hitbox
        if bullet.getHitbox().colliderect(player.getHitbox()) and (bullet.getOrigin() == 'enemy'):
            # Remove the bullet and player when they collide
            bullets.remove(bullet)
            if player.getUpgrades()[1] == 'shield':
                    player.changeDefenseAugment('none')
            else:
                gameStatus = False  # change later to bring back to main menu

        for enemy in enemies:
            if bullet.getHitbox().colliderect(enemy.getHitbox()) and (bullet.getOrigin() == 'player'):
                # Remove the bullet and enemy when they collide
                bullets.remove(bullet)
                enemies.remove(enemy)
                player.adjustScore(enemy.getWorth()) # 10 points for enemy ship consider changing later for diff enemy types
           
        
    bullets = [bullet for bullet in bullets if bullet.getPosition()[1] < windowHeight and bullet.getPosition()[1] > 0]

    for enemy in enemies:
        enemy.move(0,-1,windowWidth,windowHeight)
        window.blit(enemy.getModel(), enemy.getPosition())
        pygame.draw.rect(window, (255, 0, 0), enemy.getHitbox(), 1)
        if (pygame.time.get_ticks() - enemy.getLastShoot()) >= enemy.getCooldown():
            bullets.append(enemy.pew())  # Draw enemy hitbox

    pygame.display.flip()
    spawnTimer += clock.tick(FPS)