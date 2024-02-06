import pygame
#Start         @ 10:13,
# pause/finish @ 

#total Time

class Player:
    def __init__(self, modelPath, modelColor, modelScale, playerName, startPosition, modelHitBox):
        self.name = playerName
        self.playerModel = setPlayerModel(modelPath, modelColor, modelScale)
        self.position = setPlayerPosition(startPosition[0], startPosition[1])
        self.hitBox = None # adjust after player movement and model works
    
    def setPlayerModel(name, colorKey = None, scale = 1):
        #load image
        model = pygame.load.image(name)

        model = setPlayerSize(scale,model)

    def setPlayerSize(scale, model):
        # adjust size
        size = model.get_size()
        size = (size[0] * scale, size[1] * scale)
        sizedModel = pygame.transform.scale(model, size)
        return sizedModel

    def setPlayerColor(model, colorKey):
        #finish later
        coloredModel = None
        return coloredModel

    def setPlayerState(code = 'Start'): 
        # we can use char or string to indicate the state
        state = code
    
    def setPlayerPosition(X,Y):
        position[0] = X
        position[1] = Y
    
    def setPlayHitbox(xLow, xHigh, yLow, yHigh):
        # coordinates that represetns raw hitbox
        hitBox[0,0] = [xLow, yLow]
        hitBox[1,0] = [xHigh, yLow]
        hitBox[0,1] = [xLow, yHigh]
        hitBox[1,1]= [xHigh, yHigh]