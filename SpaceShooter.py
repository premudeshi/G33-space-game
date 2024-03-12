import pygame
"""start of the game"""
#variables 
windowHeight = 1030
windowWidth = 800
gameStatus = True
modelPath = 'C:\\Users\\' # put the remainder of your directory here with loaded png
playerX = 0
playerY = 0
movement = 30

#game init
(passes, fails) = pygame.init()
pygame.key.set_repeat(50,50)
#screen init
color = (0,0,0)
window = pygame.display.set_mode((windowWidth,windowHeight))
window.fill(color)

#player init
playerModel = pygame.image.load(modelPath)
playerModel = pygame.transform.scale(playerModel, (100,100))
playerX = (windowWidth / 2) - (playerModel.get_width()/2)
playerY =  ((3*windowHeight)/4) + (playerModel.get_height()*0)
#running game
while gameStatus:
    window.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameStatus = FALSE
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and playerX > (playerModel.get_width()/4):
            playerX -= movement
        if keys[pygame.K_RIGHT] and playerX < (windowWidth - (playerModel.get_width())):
            playerX += movement
        if keys[pygame.K_UP] and playerY > ((5 * windowHeight)/8):
            playerY -= movement
        if keys[pygame.K_DOWN] and playerY < ((5*windowHeight)/6):
            playerY += movement
    pygame.display.flip()
