"""
SuperObstacle.py
- implements super obstacles sourced from visualizer 
"""

import pygame
import math
from Obstacle import Obstacle

class SuperObstacle(Obstacle):
    @ staticmethod
    def init():
        # loads super obstacle image once
        # image taken from https://projecthvac.com/home-new/ 
        SuperObstacle.image = pygame.transform.scale(pygame.image.load(
            "images/obstacle.png").convert_alpha(), (100, 100))
    
    def __init__(self, cx, cy, speed, angle):
        # intializes pertinent variables 
        super(SuperObstacle, self).__init__(cx, cy, speed, angle)
        self.cx, self.cy, self.speed, self.angle = cx, cy, speed, angle
        self.velX = self.speed * math.cos(math.radians(self.angle))
        self.velY = -self.speed * math.sin(math.radians(self.angle))
        self.updateRect()

    # code for update functions modified from: 
    # http://blog.lukasperaza.com/getting-started-with-pygame/
    def updateRect(self):
        w, h = SuperObstacle.image.get_size()
        self.radius = w
        self.rect = pygame.Rect(self.cx - w / 2, self.cy - h / 2, w, h)
    def update(self, screenWidth, screenHeight):
        super(SuperObstacle, self).update(screenWidth, screenHeight)
        self.cx += self.velX 
        self.cy += self.velY 
        self.updateRect()
        # removes super obstacles extending beyond screen to reduce lag
        if ((self.cx + self.radius < 0) or 
            (self.cx - self.radius > screenWidth) or 
            (self.cy + self.radius < 0) or 
            (self.cy - self.radius > screenHeight)):
            self.kill()
        self.updateRect()