"""
Obstacle.py
- implements obstacles sourced from visualizer 
"""

import pygame
import math

class Obstacle(pygame.sprite.Sprite):
    @ staticmethod
    def init():
        # loads obstacle image once 
        # image taken from https://projecthvac.com/home-new/
        Obstacle.image = pygame.transform.scale(pygame.image.load(
            "images/obstacle.png").convert_alpha(), (50,50))

    def __init__(self, cx, cy, speed, angle):
        # intializes pertinent variables 
        super(Obstacle, self).__init__()
        self.cx, self.cy, self.speed, self.angle = cx, cy, speed, angle
        self.velX = self.speed * math.cos(math.radians(self.angle))
        self.velY = -self.speed * math.sin(math.radians(self.angle))
        self.updateRect()

    # code for update functions modified from: 
    # http://blog.lukasperaza.com/getting-started-with-pygame/
    def updateRect(self):
        w, h = Obstacle.image.get_size()
        self.radius = w
        self.rect = pygame.Rect(self.cx - w / 2, self.cy - h / 2, w, h)
    
    def update(self, screenWidth, screenHeight):
        super(Obstacle, self).update(screenWidth, screenHeight)
        self.cx += self.velX 
        self.cy += self.velY 
        self.updateRect()
        # removes obstacles extending beyond screen to reduce lag
        if ((self.cx + self.radius < 0) or 
            (self.cx - self.radius > screenWidth) or 
            (self.cy + self.radius < 0) or 
            (self.cy - self.radius > screenHeight)):
            self.kill()
        self.updateRect()