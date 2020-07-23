"""
Opponent.py
- implements opponent class, which defines another player in multiplayer mode
"""

import pygame
from Player import Player

class Opponent(Player):
    @staticmethod 
    def init(name):
        # loads opponent image once 
        # image taken from: https://picsart.com/i/sticker-orb-circle-magic-
        # sphere-bubble-red-blue-colorful-241757945032212
        Opponent.oppImage = pygame.transform.scale(pygame.image.load(
            "images/" + name + ".png").convert_alpha(), (50,50))

    def __init__(self, cx, cy):
        # intializes pertinent variables 
        super(Opponent, self).__init__(cx, cy, Opponent.oppImage, 25)

    def update(self, dt, keysDown, screenWidth, screenHeight):
        # updates position in flappy-bird style based on moves
        if keysDown(pygame.K_w):
            self.velY = self.flapY
            self.velX = 0
            self.flapped = True 

        elif keysDown(pygame.K_a):
            self.velY = self.flapY
            self.velX = -self.flapX
            self.flapped = True 

        elif keysDown(pygame.K_d):
            self.velY = self.flapY
            self.velX = self.flapX
            self.flapped = True 

        else: 
            if self.velY < self.maxVelY and not self.flapped:
                self.velY += self.accY
            if self.flapped:
                self.flapped = False 
    
        super(Opponent, self).update(screenWidth, screenHeight)