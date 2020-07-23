"""
Player.py
- implements base Player class, which defines flappy-style motion 
"""
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, cx, cy, image, radius):
        # intializes pertinent variables 
        super(Player, self).__init__()
        self.cx, self.cy, self.image, self.radius = cx, cy, image, radius
        w, h = image.get_size()
        self.flapY = -10        # flap speed Y
        self.flapX = 5          # flap speed X
        self.velY = -10         # vertical speed (default = flap speed)
        self.velX = 0           # horizontal speed (default = none)
        self.maxVelY = 15       # max descend speed 
        self.minVelY = -14      # max ascend speed 
        self.accY = 1           # downwards acceleration
        self.flapped = False    # true when player flaps 
        self.updateRect()

    # code for update functions modified from: 
    # http://blog.lukasperaza.com/getting-started-with-pygame/
    def updateRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.cx - w / 2, self.cy - h / 2, w, h)
    
    def update(self, screenWidth, screenHeight):
        self.cx += self.velX
        self.cy += self.velY
        self.updateRect()