"""
User.py
- implements user class, which defines the user-controlled player 
"""

import pygame
import math
from Player import Player

class User(Player):
    @staticmethod 
    def init(name):
        # loads user image once 
        # image taken from https://picsart.com/hashtag/orb/popular-stickers
        User.userImage = pygame.transform.scale(pygame.image.load(
            "images/" + name + ".png").convert_alpha(), (50,50))
    
    def __init__(self, cx, cy):
        # intializes pertinent variables 
        super(User, self).__init__(cx, cy, User.userImage, 25)
        self.invincibleTime = 1500
        self.timeAlive = 0

    def update(self, dt, keysDown, screenWidth, screenHeight):
        # updates position in flappy-bird style based on moves
        self.timeAlive += dt
        if keysDown(pygame.K_UP):
            self.velY = self.flapY
            self.velX = 0
            self.flapped = True 

        elif keysDown(pygame.K_LEFT):
            self.velY = self.flapY
            self.velX = -self.flapX
            self.flapped = True 

        elif keysDown(pygame.K_RIGHT):
            self.velY = self.flapY
            self.velX = self.flapX
            self.flapped = True 

        else: 
            if self.velY < self.maxVelY and not self.flapped:
                self.velY += self.accY
            if self.flapped:
                self.flapped = False 

        super(User, self).update(screenWidth, screenHeight)

    # (TBD for power-ups after MVP)
    def isInvincible(self):
        return self.timeAlive < self.invincibleTime