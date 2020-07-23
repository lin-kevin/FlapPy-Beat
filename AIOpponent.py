"""
AIOpponent.py
- implements AI opponent class, which defines the AI-controlled opponent 
"""

import pygame
from Player import Player

class AIOpponent(Player):
    @staticmethod 
    def init():
        # loads opponent image once 
        # image taken from: https://picsart.com/i/sticker-orb-circle-magic-
        # sphere-bubble-red-blue-colorful-241757945032212
        AIOpponent.oppImage = pygame.transform.scale(pygame.image.load(
            "images/opp3.png").convert_alpha(), (50,50))

    def __init__(self, cx, cy):
        # intializes pertinent variables 
        super(AIOpponent, self).__init__(cx, cy, AIOpponent.oppImage, 25)
    
    def update(self, dt, screenWidth, screenHeight, move):
        # updates position in flappy-bird style based on moves
        if move == "up":
            self.velY = self.flapY
            self.velX = 0
            self.flapped = True 

        if move == "left":
            self.velY = self.flapY
            self.velX = -self.flapX
            self.flapped = True 

        if move == "right":
            self.velY = self.flapY
            self.velX = self.flapX
            self.flapped = True 

        if move == "down":
            if self.velY < self.maxVelY:
                self.velY += self.accY
            if self.flapped:
                self.flapped = False 
        super(AIOpponent, self).update(screenWidth, screenHeight)