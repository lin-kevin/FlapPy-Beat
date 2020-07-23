"""
Main.py
- actually implements the game using entities from other files 
- reads and visualizes music 
- displays all different game screens
- contains most citations (rest are in PygameGame.py)
"""

# CITATIONS
# available song files and citations 
# all files were converted from YouTube to WAV files 
"""
AmIWrong.wav        https://www.youtube.com/watch?v=a16S-Ve8Teo
BadGuy.wav          https://www.youtube.com/watch?v=4-TbQnONe_w
Better.wav          https://www.youtube.com/watch?v=KkOF8UiB7u8
BST.wav             https://www.youtube.com/watch?v=tuEZ_8HdnwQ
ButterflyEffect.wav https://www.youtube.com/watch?v=k2pwvr8p4vM
Circles.wav         https://www.youtube.com/watch?v=4EQkYVtE-28
Eastside.wav        https://www.youtube.com/watch?v=74qn0eJSjpA
FakeLove.wav        https://www.youtube.com/watch?v=NT8ePWlgx_Y
Idol.wav            https://www.youtube.com/watch?v=9IVhjh15ofo
LucidDreams.wav     https://www.youtube.com/watch?v=hHtv2XMZlKs
OldTownRoad.wav     https://www.youtube.com/watch?v=7ysFgElQtjI
Sunflower.wav       https://www.youtube.com/watch?v=ApXoWvfEYVU
"""

# all player images taken from https://picsart.com/hashtag/orb/popular-stickers

# background image citations 
# all of them were modified on https://www.befunky.com/features/photo-effects/
"""
background1.png     https://wallpapercave.com/wp/dLXNfw8.jpg
background2.png     https://www.pexels.com/photo/scenic-view-of-forest-during-night-time-1252869/
background3.png     https://unsplash.com/photos/RGK5GDJ907U
background4.png     https://unsplash.com/photos/C8Z5DvtWQMw
background5.png     https://www.pexels.com/photo/photo-of-starry-night-1421903/
background6.png     http://www.gsfdcy.com/future-city-wallpapers.html#photo_3
"""

# importing pertinent modules 
import math 
import random 
import aubio
import pygame 
import numpy as num

# importing class entities from other .py files 
from User import User
from Opponent import Opponent 
from AIOpponent import AIOpponent 
from Obstacle import Obstacle 
from SuperObstacle import SuperObstacle 
from PygameGame import PygameGame

# color codes stored for convenience 
white = (255, 255, 255)
black = (0, 0, 0)

# reads music data 
# code for analyzing pitch and volume modified from: 
# https://gist.github.com/notalentgeek/48aeab398b6b74e3a9134a61b6b79a36 
# code for detecting beat onsets modified from:
# https://github.com/aubio/aubio/blob/master/python/demos/demo_onset.py
def read(file):
    FFTSize, sampleRate = 1024, 44100
    HOPSize = FFTSize//2

    s = aubio.source(file, sampleRate, HOPSize)
    o = aubio.onset("default", FFTSize, HOPSize, sampleRate)
    p = aubio.pitch("default", FFTSize, HOPSize, sampleRate)
    p.set_unit("Hz")
    p.set_silence(-40)

    onsets = set() # onset times in ms 
    pitchesList = []
    volumesList = []
    index = 0

    while True:
        samples, read = s()
        if o(samples):
            onsets.add(o.get_last_ms())
        pitch = p(samples)[0]
        volume = num.sum(samples**2)/len(samples)
        pitchesList += [(index, pitch)] 
        volumesList += [(index, volume)]
        index += 1
        if read < HOPSize: 
            break
    
    pitches = dict(pitchesList)
    volumes = dict(volumesList)
    return onsets, pitches, volumes

# collects data on all available songs 
onsets1, pitches1, volumes1 = read("songs/Eastside.wav")
averagePitch1 = sum(pitches1.values())/len(pitches1)
averageVolume1 = sum(volumes1.values())/len(volumes1)

onsets2, pitches2, volumes2 = read("songs/BadGuy.wav")
averagePitch2 = sum(pitches2.values())/len(pitches2)
averageVolume2 = sum(volumes2.values())/len(volumes2) 

onsets3, pitches3, volumes3 = read("songs/Better.wav")
averagePitch3 = sum(pitches3.values())/len(pitches3)
averageVolume3 = sum(volumes3.values())/len(volumes3) 

onsets4, pitches4, volumes4 = read("songs/BST.wav")
averagePitch4 = sum(pitches4.values())/len(pitches4)
averageVolume4 = sum(volumes4.values())/len(volumes4) 

onsets5, pitches5, volumes5 = read("songs/AmIWrong.wav")
averagePitch5 = sum(pitches5.values())/len(pitches5)
averageVolume5 = sum(volumes5.values())/len(volumes5) 

onsets6, pitches6, volumes6 = read("songs/Sunflower.wav")
averagePitch6 = sum(pitches6.values())/len(pitches6)
averageVolume6 = sum(volumes6.values())/len(volumes6) 

onsets7, pitches7, volumes7 = read("songs/Circles.wav")
averagePitch7 = sum(pitches7.values())/len(pitches7)
averageVolume7 = sum(volumes7.values())/len(volumes7) 

onsets8, pitches8, volumes8 = read("songs/ButterflyEffect.wav")
averagePitch8 = sum(pitches8.values())/len(pitches8)
averageVolume8 = sum(volumes8.values())/len(volumes8) 

onsets9, pitches9, volumes9 = read("songs/FakeLove.wav")
averagePitch9 = sum(pitches9.values())/len(pitches9)
averageVolume9 = sum(volumes9.values())/len(volumes9) 

onsets10, pitches10, volumes10 = read("songs/Idol.wav")
averagePitch10 = sum(pitches10.values())/len(pitches10)
averageVolume10 = sum(volumes10.values())/len(volumes10) 

onsets11, pitches11, volumes11 = read("songs/LucidDreams.wav")
averagePitch11 = sum(pitches11.values())/len(pitches11)
averageVolume11 = sum(volumes11.values())/len(volumes11) 

onsets12, pitches12, volumes12 = read("songs/OldTownRoad.wav")
averagePitch12 = sum(pitches12.values())/len(pitches12)
averageVolume12 = sum(volumes12.values())/len(volumes12) 

class Game(PygameGame):
    def init(self):
        # initializes variables and pygame functionality 
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.DOUBLEBUF)
        self.timeSoFar = 0
        self.userScore = self.oppScore = self.AIOppScore = 100 
        self.font = pygame.font.SysFont('tektonproboldcondotf', 20)
        self.bigFont = pygame.font.SysFont('tektonproboldcondotf', 60)
        self.titleScreen = True
        self.selectionScreen, self.helpScreen = False, False 
        self.gameScreen, self.endScreen, self.userLoss = False, False, False
        self.selectionScreenStage = None 
        self.modeSelection = ""
        self.oppSelection = None 
        self.userSelection = None 
        self.backgroundSelection = None 
        self.songSelection = None 
        self.playAgain = False 
        
        # initilizes entities featured in game 
        User.init("user1")
        self.user = User(self.width*3//4, self.height//2)
        self.userGroup = pygame.sprite.GroupSingle(self.user)
        Opponent.init("opp1")
        self.opp = Opponent(self.width//4, self.height//2)
        self.oppGroup = pygame.sprite.GroupSingle(self.opp)
        AIOpponent.init()
        self.AIOpp = AIOpponent(self.width//4, self.height//2)
        self.AIOppGroup = pygame.sprite.GroupSingle(self.AIOpp)
        Obstacle.init()
        self.obstacle = pygame.sprite.Group()
        self.obstacleTracker = set()
        SuperObstacle.init()
        self.superObstacle = pygame.sprite.Group()
        self.superObstacleTracker = set()

    def getAIMove(self):
        # returns AI move based on location of obstacles (orbs) and itself 
        bufferRoom = 150
        nearCollision = 200
        if self.AIOpp.cy > self.height - bufferRoom:
            return "up"
        for self.superOrb in self.superObstacleTracker:
            if self.AIOpp.cy < bufferRoom:
                return "down"
            elif self.AIOpp.cy > self.height - bufferRoom:
                return "up"
            elif self.AIOpp.cx < bufferRoom:
                return "right"
            elif self.AIOpp.cx > self.width//2 - bufferRoom:
                return "left"
            elif (abs(self.superOrb.cx - self.AIOpp.cx) < nearCollision and
                abs(self.superOrb.cy - self.AIOpp.cy) < nearCollision and 
                self.superOrb.cy > self.AIOpp.cy):
                if self.superOrb.cx > self.AIOpp.cx:
                    return "left"
                if self.superOrb.cx < self.AIOpp.cx:
                    return "right"
        for self.orb in self.obstacleTracker:
            if self.AIOpp.cy < bufferRoom:
                return "down"
            elif self.AIOpp.cy > self.height - bufferRoom:
                return "up"
            elif self.AIOpp.cx < bufferRoom:
                return "right"
            elif self.AIOpp.cx > self.width//2 - bufferRoom:
                return "left"
            elif (abs(self.orb.cx - self.AIOpp.cx) < nearCollision//2 and
                abs(self.orb.cy - self.AIOpp.cy) < nearCollision//2 and 
                self.orb.cy > self.AIOpp.cy):
                if self.orb.cx > self.AIOpp.cx:
                    return "left"
                if self.orb.cx < self.AIOpp.cx:
                    return "right"
        return "down"

    def visualizeMusic(self, dt):
        # visualizes music by generating obstacles based on beat onsets 
        for onset in self.onsets:
            if ((self.timeSoFar < max(self.onsets)//1) and (not self.endScreen) 
                and (self.timeSoFar - dt//4 < onset < self.timeSoFar + dt//4)):
                currentIndex = (onset/(max(self.onsets))*len(self.pitches)-1)//1 
                # determines angle based on pitch measurements 
                if self.pitches[currentIndex] > self.averagePitch: 
                    angle = random.randint(120, 180)
                else: angle = random.randint(180, 240)
                # generates obstacles to be added depending on ... 
                speed = 18
                self.obstacle1 = Obstacle(
                    self.width//2, self.height//2, speed, angle)
                self.obstacle2 = Obstacle(
                    self.width//2, self.height//2, speed, 360 - angle)
                self.obstacle3 = Obstacle(
                    self.width//2, self.height//2, -speed, -angle)
                self.obstacle4 = Obstacle(
                    self.width//2, self.height//2, -speed, 360 + angle)
                self.superObstacle1 = SuperObstacle(
                    self.width//2, self.height//2, speed//2, angle)
                self.superObstacle2 = SuperObstacle(
                    self.width//2, self.height//2, -speed//2, -angle)
                # ... volume measurements 
                if self.volumes[currentIndex] > self.averageVolume * 2:
                    self.superObstacle.add(self.superObstacle1)
                    self.superObstacle.add(self.superObstacle2)
                    self.superObstacleTracker.add(self.superObstacle1)
                    self.superObstacleTracker.add(self.superObstacle2)
                elif self.volumes[currentIndex] > self.averageVolume * 1.5:
                    self.obstacle.add(self.obstacle1, self.obstacle2)
                    self.obstacle.add(self.obstacle3, self.obstacle4)
                    self.obstacleTracker.add(self.obstacle1)
                    self.obstacleTracker.add(self.obstacle2)
                    self.obstacleTracker.add(self.obstacle3)
                    self.obstacleTracker.add(self.obstacle4)
                else:
                    self.obstacle.add(self.obstacle1, self.obstacle3)
                    self.obstacleTracker.add(self.obstacle1)
                    self.obstacleTracker.add(self.obstacle3)
            # ends visualization if battle ends 
            if ("Battle" in self.modeSelection 
            and self.timeSoFar >= max(self.onsets)//1):
                self.endScreen = True 
            # continues song in endless mode 
            elif ("Endless" in self.modeSelection
            and self.timeSoFar >= max(self.onsets)//1):
                self.playAgain = True 
                self.playMusic()

    def checkCollisions(self):
        # checks for collisions with obstacles and adjusts scores
        if pygame.sprite.groupcollide(
            self.userGroup, self.obstacle, False, True,
            pygame.sprite.collide_circle_ratio(0.5)):
            self.userScore -= 1
        if pygame.sprite.groupcollide(
            self.userGroup, self.superObstacle, False, True,
            pygame.sprite.collide_circle_ratio(0.4)):
            self.userScore -= 5
                
        if "solo" in self.modeSelection:
            if pygame.sprite.groupcollide(
                self.AIOppGroup, self.obstacle, False, True,
                pygame.sprite.collide_circle_ratio(0.5)):
                self.AIOppScore -= 1
            if pygame.sprite.groupcollide(
                self.AIOppGroup, self.superObstacle, False, True,
                pygame.sprite.collide_circle_ratio(0.4)):
                self.AIOppScore -= 5

        if "multi" in self.modeSelection:
            if pygame.sprite.groupcollide(
                self.oppGroup, self.obstacle, False, True,
                pygame.sprite.collide_circle_ratio(0.5)):
                self.oppScore -= 1
            if pygame.sprite.groupcollide(
                self.oppGroup, self.superObstacle, False, True,
                pygame.sprite.collide_circle_ratio(0.4)):
                self.oppScore -= 5

    def checkEnd(self):
        # checks for end of game if player 
        # 1) scores 0 points or 
        if ((pygame.sprite.groupcollide(
            self.userGroup, self.obstacle, True, True,
            pygame.sprite.collide_circle_ratio(0.5)) 
            and self.userScore <= 1) 
            or (pygame.sprite.groupcollide(
            self.userGroup, self.superObstacle, True, True,
            pygame.sprite.collide_circle_ratio(0.4)) 
            and self.userScore <= 5)):
                self.endScreen = True 
                self.userLoss = True 
        if ((pygame.sprite.groupcollide(
            self.oppGroup, self.obstacle, True, True,
            pygame.sprite.collide_circle_ratio(0.5)) 
            and self.oppScore <= 1) 
            or (pygame.sprite.groupcollide(
            self.oppGroup, self.superObstacle, True, True,
            pygame.sprite.collide_circle_ratio(0.4)) 
            and self.oppScore <= 5)):
                self.endScreen = True 
                self.userLoss = False  
        if ((pygame.sprite.groupcollide(
            self.AIOppGroup, self.obstacle, True, True,
            pygame.sprite.collide_circle_ratio(0.5)) 
            and self.AIOppScore <= 1) 
            or (pygame.sprite.groupcollide(
            self.AIOppGroup, self.superObstacle, True, True,
            pygame.sprite.collide_circle_ratio(0.4)) 
            and self.AIOppScore <= 5)):
                self.endScreen = True 
                self.userLoss = False  

        # 2) falls out of given boundaries 
        userRadius = 25
        if ((self.user.cx + userRadius < self.width//2) or 
            (self.user.cx - userRadius > self.width) or 
            (self.user.cy + userRadius < 0) or 
            (self.user.cy - userRadius > self.height)):
                self.endScreen = True 
                self.userLoss = True 
        if "multi" in self.modeSelection: 
            if ((self.opp.cx - userRadius > self.width//2) or 
                (self.opp.cx + userRadius < 0) or 
                (self.opp.cy + userRadius < 0) or 
                (self.opp.cy - userRadius > self.height)):
                    self.endScreen = True 
                    self.userLoss = False 
        # note: AI programmed to never fall out of given boundaries

    def timerFired(self, dt):
        if self.gameScreen == True:
            # updates time and all entities movements 
            self.timeSoFar += dt
            self.userGroup.update(dt, self.isKeyPressed, self.width, self.height)
            self.oppGroup.update(dt, self.isKeyPressed, self.width, self.height)
            self.obstacle.update(self.width, self.height)
            self.superObstacle.update(self.width, self.height)
            AImove = self.getAIMove()
            self.AIOppGroup.update(dt, self.width, self.height, AImove)

            # calls function to visualize music 
            self.visualizeMusic(dt)

            # checks for collisions and end of game if game is still going
            if not self.endScreen:
                self.checkCollisions()
                self.checkEnd()

            # removes data on obstacles off screen to reduce lag 
            superOrbR = 50
            orbR = 25
            superObstacleTrackerUpdate = set()
            obstacleTrackerUpdate = set()
            for self.superOrb in self.superObstacleTracker:
                if ((self.superOrb.cx + superOrbR > 0) or 
                    (self.superOrb.cx - superOrbR < self.width) or 
                    (self.superOrb.cy + superOrbR > 0) or 
                    (self.superOrb.cy - superOrbR < self.height)):
                    superObstacleTrackerUpdate.add(self.superOrb)
            for self.orb in self.obstacleTracker:
                if ((self.orb.cx + orbR > 0) or 
                    (self.orb.cx - orbR < self.width) or 
                    (self.orb.cy + orbR > 0) or 
                    (self.orb.cy - orbR < self.height)):
                    obstacleTrackerUpdate.add(self.orb)
            self.superObstacleTracker = superObstacleTrackerUpdate
            self.obstacleTracker = obstacleTrackerUpdate

            # reduces lag in case game becomes extremely busy 
            if len(self.superObstacleTracker) > 100:
                self.superObstacleTracker = set()
            if len(self.obstacleTracker) > 100:
                self.obstacleTracker = set()
    
    def drawTitleScreen(self, screen):
        # draws title screen
        if self.titleScreen == True:
            self.screen.blit(self.titleScreenPic, [0,0])
    
    def drawSelectionScreen(self, screen): 
        # draws different stages of selection screen
        if self.selectionScreen == True:
            self.screen.blit(self.selectionScreenPic, [0,0])
            if self.selectionScreenStage == "S1":
                self.screen.blit(self.selectionScreenSolo1, [0,0])
            elif self.selectionScreenStage == "M1":
                self.screen.blit(self.selectionScreenMulti1, [0,0])
            elif self.selectionScreenStage == "S2":
                self.screen.blit(self.selectionScreenSolo2, [0,0])
            elif self.selectionScreenStage == "M2":
                self.screen.blit(self.selectionScreenMulti2, [0,0])
            elif self.selectionScreenStage == "S3":
                self.screen.blit(self.selectionScreenSolo3, [0,0])
            elif self.selectionScreenStage == "M3":
                self.screen.blit(self.selectionScreenMulti3, [0,0])
            elif self.selectionScreenStage == "S4":
                self.screen.blit(self.selectionScreenSolo4, [0,0])
            elif self.selectionScreenStage == "M4":
                self.screen.blit(self.selectionScreenMulti4, [0,0])
            
            # draws shaded rectangle over game mode selection
            modeTopMargin = 45 
            modeButtonMargin = 20
            modeButtonHeight = 40
            modeButtonWidth = 305 
            modeButtonGap = 53
            modeBlit = pygame.Surface((modeButtonWidth, modeButtonHeight))
            modeBlit.set_alpha(200)
            pygame.draw.rect(modeBlit, black, modeBlit.get_rect(), 10)
            
            if self.modeSelection == "soloBattle":
                screen.blit(modeBlit, (modeButtonMargin, modeTopMargin))
            elif self.modeSelection == "soloEndless":
                screen.blit(modeBlit, 
                (modeButtonMargin + modeButtonWidth + modeButtonGap, modeTopMargin))
            elif self.modeSelection == "multiBattle":
                screen.blit(modeBlit, (modeButtonMargin, 
                modeTopMargin + modeButtonHeight + modeButtonMargin))
            elif self.modeSelection == "multiEndless":
                screen.blit(modeBlit, 
                (modeButtonMargin + modeButtonWidth + modeButtonGap,
                modeTopMargin + modeButtonHeight + modeButtonMargin))

            # draws shaded rectangle over player selection(s)
            playerTopMargin = 205
            playerLeftMargin = 15
            playerMargin = 37 
            playerSide = 140
            playerBlit = pygame.Surface((playerSide, playerSide))
            playerBlit.set_alpha(200)
            pygame.draw.rect(playerBlit, black, playerBlit.get_rect(), 10)

            if "solo" in self.modeSelection:
                if self.userSelection == "opp1":
                    screen.blit(playerBlit, (playerLeftMargin, playerTopMargin))
                elif self.userSelection == "opp2":
                    screen.blit(playerBlit, 
                    (playerLeftMargin + playerSide + playerMargin, playerTopMargin))
                elif self.userSelection == "user1":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*2 + playerMargin*2, 
                    playerTopMargin))
                elif self.userSelection == "user2":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*3 + playerMargin*3, 
                    playerTopMargin))
                elif self.userSelection == "opp3":
                    screen.blit(playerBlit, (playerLeftMargin, 
                    playerTopMargin + playerSide + playerMargin))
                elif self.userSelection == "opp4":
                    screen.blit(playerBlit, 
                    (playerLeftMargin + playerSide + playerMargin, 
                    playerTopMargin + playerSide + playerMargin))
                elif self.userSelection == "user3":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*2 + playerMargin*2, 
                    playerTopMargin + playerSide + playerMargin))
                elif self.userSelection == "user4":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*3 + playerMargin*3, 
                    playerTopMargin + playerSide + playerMargin))
                elif self.userSelection == "opp5":
                    screen.blit(playerBlit, (playerLeftMargin, 
                    playerTopMargin + playerSide*2 + playerMargin*2))
                elif self.userSelection == "opp6":
                    screen.blit(playerBlit, 
                    (playerLeftMargin + playerSide + playerMargin, 
                    playerTopMargin + playerSide*2 + playerMargin*2))
                elif self.userSelection == "user5":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*2 + playerMargin*2, 
                    playerTopMargin + playerSide*2 + playerMargin*2))
                elif self.userSelection == "user6":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*3 + playerMargin*3, 
                    playerTopMargin + playerSide*2 + playerMargin*2))
        
            elif "multi" in self.modeSelection:
                if self.oppSelection == "opp1":
                    screen.blit(playerBlit, (playerLeftMargin, playerTopMargin))
                if self.oppSelection == "opp2":
                    screen.blit(playerBlit, 
                    (playerLeftMargin + playerSide + playerMargin, playerTopMargin))
                if self.userSelection == "user1":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*2 + playerMargin*2, 
                    playerTopMargin))
                if self.userSelection == "user2":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*3 + playerMargin*3, 
                    playerTopMargin))
                if self.oppSelection == "opp3":
                    screen.blit(playerBlit, (playerLeftMargin, 
                    playerTopMargin + playerSide + playerMargin))
                if self.oppSelection == "opp4":
                    screen.blit(playerBlit, 
                    (playerLeftMargin + playerSide + playerMargin, 
                    playerTopMargin + playerSide + playerMargin))
                if self.userSelection == "user3":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*2 + playerMargin*2, 
                    playerTopMargin + playerSide + playerMargin))
                if self.userSelection == "user4":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*3 + playerMargin*3, 
                    playerTopMargin + playerSide + playerMargin))
                if self.oppSelection == "opp5":
                    screen.blit(playerBlit, (playerLeftMargin, 
                    playerTopMargin + playerSide*2 + playerMargin*2))
                if self.oppSelection == "opp6":
                    screen.blit(playerBlit, 
                    (playerLeftMargin + playerSide + playerMargin, 
                    playerTopMargin + playerSide*2 + playerMargin*2))
                if self.userSelection == "user5":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*2 + playerMargin*2, 
                    playerTopMargin + playerSide*2 + playerMargin*2))
                if self.userSelection == "user6":
                    screen.blit(playerBlit,
                    (playerLeftMargin + playerSide*3 + playerMargin*3, 
                    playerTopMargin + playerSide*2 + playerMargin*2))
            
            # draws shaded rectangle over background selection
            bgTopMargin = 45
            bgButtonMargin = 15
            bgButtonWidth = 213
            bgButtonHeight = 106  
            bgBlit = pygame.Surface((bgButtonWidth, bgButtonHeight))
            bgBlit.set_alpha(200)
            pygame.draw.rect(bgBlit, black, bgBlit.get_rect(), 10)

            if self.backgroundSelection == "background1":
                screen.blit(bgBlit, (self.width//2 + bgButtonMargin, bgTopMargin))
            if self.backgroundSelection == "background2": 
                screen.blit(bgBlit, 
                (self.width//2 + bgButtonMargin*2 + bgButtonWidth, bgTopMargin))
            if self.backgroundSelection == "background3":
                screen.blit(bgBlit, 
                (self.width//2 + bgButtonMargin*3 + bgButtonWidth*2, bgTopMargin))
            if self.backgroundSelection == "background4":
                screen.blit(bgBlit, (self.width//2 + bgButtonMargin, 
                bgTopMargin + bgButtonHeight + bgButtonMargin))
            if self.backgroundSelection == "background5": 
                screen.blit(bgBlit, 
                (self.width//2 + bgButtonMargin*2 + bgButtonWidth, 
                bgTopMargin + bgButtonHeight + bgButtonMargin))
            if self.backgroundSelection == "background6":
                screen.blit(bgBlit, 
                (self.width//2 + bgButtonMargin*3 + bgButtonWidth*2, 
                bgTopMargin + bgButtonHeight + bgButtonMargin))
            
            # draws shaded rectangle over song selection
            songTopMargin = 340 
            songButtonMargin = 12
            songButtonWidth = 334 
            songButtonHeight = 30 
            songButtonGap = 40
            songBlit = pygame.Surface((songButtonWidth, songButtonHeight))
            songBlit.set_alpha(200)
            pygame.draw.rect(songBlit, black, songBlit.get_rect(), 10)

            if self.songSelection == "Eastside":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin, songTopMargin))
            if self.songSelection == "BadGuy":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin*2 + songButtonWidth, 
                songTopMargin))
            if self.songSelection == "Better":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin,
                songTopMargin + songButtonHeight + songButtonMargin)) 
            if self.songSelection == "BST":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin*2 + songButtonWidth,
                songTopMargin + songButtonHeight + songButtonMargin)) 
            if self.songSelection == "AmIWrong":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin,
                songTopMargin + songButtonHeight*2 + songButtonMargin*2)) 
            if self.songSelection == "Sunflower":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin*2 + songButtonWidth,
                songTopMargin + songButtonHeight*2 + songButtonMargin*2)) 
            if self.songSelection == "Circles":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin,
                songTopMargin + songButtonHeight*3 + songButtonMargin*3)) 
            if self.songSelection == "ButterflyEffect":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin*2 + songButtonWidth,
                songTopMargin + songButtonHeight*3 + songButtonMargin*3)) 
            if self.songSelection == "FakeLove":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin,
                songTopMargin + songButtonHeight*4 + 
                songButtonMargin*3 + songButtonGap))
            if self.songSelection == "Idol":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin,
                songTopMargin + songButtonHeight*5 + 
                songButtonMargin*4 + songButtonGap))
            if self.songSelection == "LucidDreams":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin,
                songTopMargin + songButtonHeight*6 + 
                songButtonMargin*5 + songButtonGap))
            if self.songSelection == "OldTownRoad":
                screen.blit(songBlit, 
                (self.width//2 + songButtonMargin,
                songTopMargin + songButtonHeight*7 + 
                songButtonMargin*6 + songButtonGap))

    def drawHelpScreen(self, screen):
        # draws help screen 
        if self.helpScreen == True:
            self.screen.blit(self.helpScreenPic, [0,0])
        
    def drawEndScreen(self, screen):
        # draws end of game screen
        if self.endScreen == True:
            blackImage = pygame.Surface((self.width,self.height))
            blackImage.set_alpha(200)
            pygame.draw.rect(blackImage, black, blackImage.get_rect(), 10)
            screen.blit(blackImage, (0, 0))

            self.winner = self.bigFont.render("WINNER!", False, white)
            self.draw = self.bigFont.render("IT'S A DRAW!", False, white)
            w, h = self.winner.get_size()
            if (not self.userLoss or (self.userScore > self.oppScore) or 
            (self.userScore > self.AIOppScore)):
                self.screen.blit(self.winner, 
                [self.width*3//4 - w//2, self.height//4])
            elif (self.userLoss or (self.userScore < self.oppScore) or 
            (self.userScore < self.AIOppScore)):
                self.screen.blit(self.winner, 
                [self.width//4 - w//2, self.height//4])
            elif not self.userLoss: 
                self.screen.blit(self.winner, 
                [self.width*3//4 - w//2, self.height//4])
            else:
                w, h = self.draw.get_size()
                self.screen.blit(self.draw, 
                [self.width//2 - w//2, self.height//4])

            self.endTextTop = self.font.render("GAME OVER", False, white)
            margin = 100
            self.screen.blit(self.endTextTop, 
                [self.width//2 - margin//2, self.height//margin])
            
            if "solo" in self.modeSelection:
                self.endScoreLeft = self.bigFont.render(
                    f"SCORE: {self.AIOppScore}", False, white)
            if "multi" in self.modeSelection:
                self.endScoreLeft = self.bigFont.render(
                    f"SCORE: {self.oppScore}", False, white)
            w, h = self.endScoreLeft.get_size()
            self.screen.blit(self.endScoreLeft, 
                [self.width//4 - w//2, self.height//2 - h//2])

            self.endScoreRight = self.bigFont.render(
                f"SCORE: {self.userScore}", False, white)
            w, h = self.endScoreRight.get_size()
            self.screen.blit(self.endScoreRight, 
                [self.width*3//4 - w//2, self.height//2 - h//2])

            self.endTextBottom = self.font.render(
                "PRESS SPACE TO RESTART", False, white)
            w, h = self.endTextBottom.get_size()
            self.screen.blit(self.endTextBottom, 
                [self.width//2 - w//2, self.height - h])

    def redrawAll(self, screen):
        # draws all entities and surfaces in game
        if self.backgroundSelection != None:
            self.screen.blit(self.background, [0, 0])

        self.userGroup.draw(screen)
        if "solo" in self.modeSelection: self.AIOppGroup.draw(screen)
        if "multi" in self.modeSelection: self.oppGroup.draw(screen)
        self.obstacle.draw(screen)
        self.superObstacle.draw(screen)

        self.screen.blit(self.logoBackground, 
            [self.width//2 - self.height//4, self.height//2 - self.height//4])
        w, h = self.logo.get_size()
        self.screen.blit(self.logo, 
            [self.width//2 - w//2, self.height//2 - h//2])

        textMargin = 50
        self.userTextSurface = self.font.render(
            f'SCORE: {self.userScore}', False, white)
        self.screen.blit(self.userTextSurface, 
            [self.width*3//4 - textMargin, self.height//textMargin])
        if "solo" in self.modeSelection:
            self.AIOppTextSurface = self.font.render(
                f'SCORE: {self.AIOppScore}', False, white)
            self.screen.blit(self.AIOppTextSurface, 
                [self.width//4 - textMargin, self.height//textMargin])
        if "multi" in self.modeSelection:
            self.oppTextSurface = self.font.render(
                f'SCORE: {self.oppScore}', False, white)
            self.screen.blit(self.oppTextSurface, 
                [self.width//4, self.height//50])

        self.drawEndScreen(screen)
        self.drawTitleScreen(screen)
        self.drawSelectionScreen(screen)
        self.drawHelpScreen(screen)
        self.screen.set_alpha(None)
    
    def keyPressed(self, keyCode, modifier):
        # restarts game upon pressing space 
        if self.endScreen == True:
            if keyCode == pygame.K_SPACE:
                pygame.mixer.music.stop()
                Game.init(self)
                
    def mousePressed(self, x, y):
        if self.titleScreen == True:
            titleButtonH = 55
            titleButtonVertMargin = 80
            titleButtonHorMargin = 612
            # if user presses play "button" 
            if ((x > titleButtonHorMargin) 
            and (x < self.width - titleButtonHorMargin)
            and (y > titleButtonVertMargin)
            and (y < titleButtonVertMargin + titleButtonH)):
                self.selectionScreen = True
                self.titleScreen = False 
            # if user presses help "button" 
            if ((x > titleButtonHorMargin) 
            and (x < self.width - titleButtonHorMargin)
            and (y > self.height - titleButtonVertMargin - titleButtonH)
            and (y < self.height - titleButtonVertMargin)):
                self.helpScreen = True 
                self.titleScreen = False 

        elif self.helpScreen == True:
            # if user presses back "button"
            backButtonSide = 49
            backButtonMargin = 20
            if ((x > backButtonMargin)
            and (x < backButtonMargin + backButtonSide)
            and (y > self.height - backButtonMargin - backButtonSide)
            and (y < self.height - backButtonMargin)):
                self.titleScreen = True 
                self.helpScreen = False 

        elif self.selectionScreen == True:
            # user selects song
            modeTopMargin = 45 
            modeButtonMargin = 20
            modeButtonHeight = 40
            modeButtonWidth = 305 
            modeButtonGap = 53

            if ((x > modeButtonMargin)
            and (x < modeButtonMargin + modeButtonWidth)
            and (y > modeTopMargin)
            and (y < modeTopMargin + modeButtonHeight)): 
                self.modeSelection = "soloBattle"
                self.selectionScreenStage = "S1"

            if ((x > modeButtonMargin + modeButtonWidth + modeButtonGap)
            and (x < modeButtonMargin + modeButtonWidth*2 + modeButtonGap)
            and (y > modeTopMargin)
            and (y < modeTopMargin + modeButtonHeight)): 
                self.modeSelection = "soloEndless"
                self.selectionScreenStage = "S1"
            
            if ((x > modeButtonMargin)
            and (x < modeButtonMargin + modeButtonWidth)
            and (y > modeTopMargin + modeButtonHeight + modeButtonMargin)
            and (y < modeTopMargin + modeButtonHeight*2 + modeButtonMargin)):
                self.modeSelection = "multiBattle"
                self.selectionScreenStage = "M1"

            if ((x > modeButtonMargin + modeButtonWidth + modeButtonGap)
            and (x < modeButtonMargin + modeButtonWidth*2 + modeButtonGap)
            and (y > modeTopMargin + modeButtonHeight + modeButtonMargin)
            and (y < modeTopMargin + modeButtonHeight*2 + modeButtonMargin)):
                self.modeSelection = "multiEndless"
                self.selectionScreenStage = "M1"

            # user selects player(s)
            playerTopMargin = 205
            playerLeftMargin = 15
            playerMargin = 37 
            playerSide = 140

            if ((x > playerLeftMargin) and (x < playerLeftMargin + playerSide)
            and (y > playerTopMargin) and (y < playerTopMargin + playerSide)):
                if "solo" in self.modeSelection: self.userSelection = "opp1"
                else: self.oppSelection = "opp1"
            
            if ((x > playerLeftMargin + playerSide + playerMargin) 
            and (x < playerLeftMargin + playerSide*2 + playerMargin) 
            and (y > playerTopMargin) and (y < playerTopMargin + playerSide)):
                if "solo" in self.modeSelection: self.userSelection = "opp2"
                else: self.oppSelection = "opp2"
            
            if ((x > playerLeftMargin + playerSide*2 + playerMargin*2) 
            and (x < playerLeftMargin + playerSide*3 + playerMargin*2) 
            and (y > playerTopMargin) and (y < playerTopMargin + playerSide)):
                self.userSelection = "user1"
            
            if ((x > playerLeftMargin + playerSide*3 + playerMargin*3) 
            and (x < playerLeftMargin + playerSide*4 + playerMargin*3) 
            and (y > playerTopMargin) and (y < playerTopMargin + playerSide)):
                self.userSelection = "user2"
            
            if ((x > playerLeftMargin) and (x < playerLeftMargin + playerSide)
            and (y > playerTopMargin + playerSide + playerMargin) 
            and (y < playerTopMargin + playerSide*2 + playerMargin)):
                if "solo" in self.modeSelection: self.userSelection = "opp3"
                else: self.oppSelection = "opp3"
            
            if ((x > playerLeftMargin + playerSide + playerMargin) 
            and (x < playerLeftMargin + playerSide*2 + playerMargin) 
            and (y > playerTopMargin + playerSide + playerMargin) 
            and (y < playerTopMargin + playerSide*2 + playerMargin)):
                if "solo" in self.modeSelection: self.userSelection = "opp4"
                else: self.oppSelection = "opp4"
            
            if ((x > playerLeftMargin + playerSide*2 + playerMargin*2) 
            and (x < playerLeftMargin + playerSide*3 + playerMargin*2) 
            and (y > playerTopMargin + playerSide + playerMargin) 
            and (y < playerTopMargin + playerSide*2 + playerMargin)):
                self.userSelection = "user3"
            
            if ((x > playerLeftMargin + playerSide*3 + playerMargin*3) 
            and (x < playerLeftMargin + playerSide*4 + playerMargin*3) 
            and (y > playerTopMargin + playerSide + playerMargin) 
            and (y < playerTopMargin + playerSide*2 + playerMargin)):
                self.userSelection = "user4"

            if ((x > playerLeftMargin) and (x < playerLeftMargin + playerSide)
            and (y > playerTopMargin + playerSide*2 + playerMargin*2) 
            and (y < playerTopMargin + playerSide*3 + playerMargin*2)):
                if "solo" in self.modeSelection: self.userSelection = "opp5"
                else: self.oppSelection = "opp5"
            
            if ((x > playerLeftMargin + playerSide + playerMargin) 
            and (x < playerLeftMargin + playerSide*2 + playerMargin) 
            and (y > playerTopMargin + playerSide*2 + playerMargin*2) 
            and (y < playerTopMargin + playerSide*3 + playerMargin*2)):
                if "solo" in self.modeSelection: self.userSelection = "opp6"
                else: self.oppSelection = "opp6"
            
            if ((x > playerLeftMargin + playerSide*2 + playerMargin*2) 
            and (x < playerLeftMargin + playerSide*3 + playerMargin*2) 
            and (y > playerTopMargin + playerSide*2 + playerMargin*2) 
            and (y < playerTopMargin + playerSide*3 + playerMargin*2)):
                self.userSelection = "user5"
            
            if ((x > playerLeftMargin + playerSide*3 + playerMargin*3) 
            and (x < playerLeftMargin + playerSide*4 + playerMargin*3) 
            and (y > playerTopMargin + playerSide*2 + playerMargin*2) 
            and (y < playerTopMargin + playerSide*3 + playerMargin*2)):
                self.userSelection = "user6"
            
            if "solo" in self.modeSelection and self.userSelection != None:
                self.selectionScreenStage = "S2"
            if ("multi" in self.modeSelection  
            and (self.userSelection != None) and (self.oppSelection != None)):
                self.selectionScreenStage = "M2"

            if self.userSelection != None:
                User.init(self.userSelection)
                self.user = User(self.width*3//4, self.height//2)
                self.userGroup = pygame.sprite.GroupSingle(self.user)
            if self.oppSelection != None:
                Opponent.init(self.oppSelection)
                self.opp = Opponent(self.width//4, self.height//2)
                self.oppGroup = pygame.sprite.GroupSingle(self.opp)

            # user selects background
            bgTopMargin = 45
            bgButtonMargin = 15
            bgButtonWidth = 213
            bgButtonHeight = 106  

            if ((x > self.width//2 + bgButtonMargin)
            and (x < self.width//2 + bgButtonMargin + bgButtonWidth)
            and (y > bgTopMargin) and (y < bgTopMargin + bgButtonHeight)): 
                self.backgroundSelection = "background1"
            
            if ((x > self.width//2 + bgButtonMargin*2 + bgButtonWidth)
            and (x < self.width//2 + bgButtonMargin*2 + bgButtonWidth*2)
            and (y > bgTopMargin) and (y < bgTopMargin + bgButtonHeight)):
                self.backgroundSelection = "background2"
            
            if ((x > self.width//2 + bgButtonMargin*3 + bgButtonWidth*2)
            and (x < self.width//2 + bgButtonMargin*3 + bgButtonWidth*3)
            and (y > bgTopMargin) and (y < bgTopMargin + bgButtonHeight)):
                self.backgroundSelection = "background3"

            if ((x > self.width//2 + bgButtonMargin)
            and (x < self.width//2 + bgButtonMargin + bgButtonWidth)
            and (y > bgTopMargin + bgButtonHeight + bgButtonMargin) 
            and (y < bgTopMargin + bgButtonHeight*2 + bgButtonMargin)): 
                self.backgroundSelection = "background4"
            
            if ((x > self.width//2 + bgButtonMargin*2 + bgButtonWidth)
            and (x < self.width//2 + bgButtonMargin*2 + bgButtonWidth*2)
            and (y > bgTopMargin + bgButtonHeight + bgButtonMargin) 
            and (y < bgTopMargin + bgButtonHeight*2 + bgButtonMargin)): 
                self.backgroundSelection = "background5"
            
            if ((x > self.width//2 + bgButtonMargin*3 + bgButtonWidth*2)
            and (x < self.width//2 + bgButtonMargin*3 + bgButtonWidth*3)
            and (y > bgTopMargin + bgButtonHeight + bgButtonMargin) 
            and (y < bgTopMargin + bgButtonHeight*2 + bgButtonMargin)): 
                self.backgroundSelection = "background6"
            
            if ("solo" in self.modeSelection 
            and self.backgroundSelection != None): 
                self.selectionScreenStage = "S3"
            if ("multi" in self.modeSelection  
            and self.backgroundSelection != None):
                self.selectionScreenStage = "M3"
            
            if self.backgroundSelection != None:
                self.background = pygame.transform.scale(
                pygame.image.load("images/" + 
                self.backgroundSelection + ".png").convert_alpha(), 
                (self.width, self.height)) 

            # user selects song
            # corresponding song data transferred to usable form for visualizer
            songTopMargin = 340 
            songButtonMargin = 12
            songButtonWidth = 334 
            songButtonHeight = 30 
            songButtonGap = 40

            if ((x > self.width//2 + songButtonMargin)
            and (x < self.width//2 + songButtonMargin + songButtonWidth)
            and (y > songTopMargin) and (y < songTopMargin + songButtonHeight)):
                self.songSelection = "Eastside"
                self.onsets = onsets1 
                self.pitches = pitches1 
                self.volumes = volumes1
                self.averagePitch = averagePitch1
                self.averageVolume = averageVolume1
                pygame.mixer.music.load("songs/Eastside.wav")
            
            if ((x > self.width//2 + songButtonMargin*2 + songButtonWidth)
            and (x < self.width//2 + songButtonMargin*2 + songButtonWidth*2)
            and (y > songTopMargin) and (y < songTopMargin + songButtonHeight)):
                self.songSelection = "BadGuy"
                self.onsets = onsets2 
                self.pitches = pitches2 
                self.volumes = volumes2
                self.averagePitch = averagePitch2
                self.averageVolume = averageVolume2
                pygame.mixer.music.load("songs/BadGuy.wav")

            if ((x > self.width//2 + songButtonMargin)
            and (x < self.width//2 + songButtonMargin + songButtonWidth)
            and (y > songTopMargin + songButtonHeight + songButtonMargin) 
            and (y < songTopMargin + songButtonHeight*2 + songButtonMargin)):
                self.songSelection = "Better"
                self.onsets = onsets3 
                self.pitches = pitches3 
                self.volumes = volumes3
                self.averagePitch = averagePitch3
                self.averageVolume = averageVolume3
                pygame.mixer.music.load("songs/Better.wav")
            
            if ((x > self.width//2 + songButtonMargin*2 + songButtonWidth)
            and (x < self.width//2 + songButtonMargin*2 + songButtonWidth*2)
            and (y > songTopMargin + songButtonHeight + songButtonMargin) 
            and (y < songTopMargin + songButtonHeight*2 + songButtonMargin)):
                self.songSelection = "BST" 
                self.onsets = onsets4 
                self.pitches = pitches4 
                self.volumes = volumes4
                self.averagePitch = averagePitch4
                self.averageVolume = averageVolume4
                pygame.mixer.music.load("songs/BST.wav")

            if ((x > self.width//2 + songButtonMargin)
            and (x < self.width//2 + songButtonMargin + songButtonWidth)
            and (y > songTopMargin + songButtonHeight*2 + songButtonMargin*2) 
            and (y < songTopMargin + songButtonHeight*3 + songButtonMargin*2)):
                self.songSelection = "AmIWrong"
                self.onsets = onsets5 
                self.pitches = pitches5
                self.volumes = volumes5
                self.averagePitch = averagePitch5
                self.averageVolume = averageVolume5
                pygame.mixer.music.load("songs/AmIWrong.wav")
            
            if ((x > self.width//2 + songButtonMargin*2 + songButtonWidth)
            and (x < self.width//2 + songButtonMargin*2 + songButtonWidth*2)
            and (y > songTopMargin + songButtonHeight*2 + songButtonMargin*2) 
            and (y < songTopMargin + songButtonHeight*3 + songButtonMargin*2)):
                self.songSelection = "Sunflower"
                self.onsets = onsets6 
                self.pitches = pitches6 
                self.volumes = volumes6
                self.averagePitch = averagePitch6
                self.averageVolume = averageVolume6
                pygame.mixer.music.load("songs/Sunflower.wav")

            if ((x > self.width//2 + songButtonMargin)
            and (x < self.width//2 + songButtonMargin + songButtonWidth)
            and (y > songTopMargin + songButtonHeight*3 + songButtonMargin*3) 
            and (y < songTopMargin + songButtonHeight*4 + songButtonMargin*3)):
                self.songSelection = "Circles"
                self.onsets = onsets7 
                self.pitches = pitches7 
                self.volumes = volumes7
                self.averagePitch = averagePitch7
                self.averageVolume = averageVolume7
                pygame.mixer.music.load("songs/Circles.wav")
            
            if ((x > self.width//2 + songButtonMargin*2 + songButtonWidth)
            and (x < self.width//2 + songButtonMargin*2 + songButtonWidth*2)
            and (y > songTopMargin + songButtonHeight*3 + songButtonMargin*3) 
            and (y < songTopMargin + songButtonHeight*4 + songButtonMargin*3)):
                self.songSelection = "ButterflyEffect"
                self.onsets = onsets8 
                self.pitches = pitches8 
                self.volumes = volumes8
                self.averagePitch = averagePitch8
                self.averageVolume = averageVolume8
                pygame.mixer.music.load("songs/ButterflyEffect.wav")
            
            if ((x > self.width//2 + songButtonMargin)
            and (x < self.width//2 + songButtonMargin + songButtonWidth)
            and (y > songTopMargin + songButtonHeight*4 + 
                songButtonMargin*3 + songButtonGap) 
            and (y < songTopMargin + songButtonHeight*5 + 
                songButtonMargin*3 + songButtonGap)):
                self.songSelection = "FakeLove"
                self.onsets = onsets9 
                self.pitches = pitches9 
                self.volumes = volumes9
                self.averagePitch = averagePitch9
                self.averageVolume = averageVolume9
                pygame.mixer.music.load("songs/FakeLove.wav")
            
            if ((x > self.width//2 + songButtonMargin)
            and (x < self.width//2 + songButtonMargin + songButtonWidth)
            and (y > songTopMargin + songButtonHeight*5 + 
                songButtonMargin*4 + songButtonGap) 
            and (y < songTopMargin + songButtonHeight*6 + 
                songButtonMargin*4 + songButtonGap)):
                self.songSelection = "Idol"
                self.onsets = onsets10 
                self.pitches = pitches10 
                self.volumes = volumes10
                self.averagePitch = averagePitch10
                self.averageVolume = averageVolume10
                pygame.mixer.music.load("songs/Idol.wav")
    
            if ((x > self.width//2 + songButtonMargin)
            and (x < self.width//2 + songButtonMargin + songButtonWidth)
            and (y > songTopMargin + songButtonHeight*6 + 
                songButtonMargin*5 + songButtonGap) 
            and (y < songTopMargin + songButtonHeight*7 + 
                songButtonMargin*5 + songButtonGap)):
                self.songSelection = "LucidDreams"
                self.onsets = onsets11
                self.pitches = pitches11
                self.volumes = volumes11
                self.averagePitch = averagePitch11
                self.averageVolume = averageVolume11
                pygame.mixer.music.load("songs/LucidDreams.wav")

            if ((x > self.width//2 + songButtonMargin)
            and (x < self.width//2 + songButtonMargin + songButtonWidth)
            and (y > songTopMargin + songButtonHeight*7 + 
                songButtonMargin*6 + songButtonGap) 
            and (y < songTopMargin + songButtonHeight*8 + 
                songButtonMargin*6 + songButtonGap)):
                self.songSelection = "OldTownRoad"
                self.onsets = onsets12 
                self.pitches = pitches12 
                self.volumes = volumes12
                self.averagePitch = averagePitch12
                self.averageVolume = averageVolume12
                pygame.mixer.music.load("songs/OldTownRoad.wav")

            if ("solo" in self.modeSelection
            and self.userSelection != None
            and self.backgroundSelection != None
            and self.songSelection != None): 
                self.selectionScreenStage = "S4"
            
            if ("multi" in self.modeSelection
            and self.oppSelection != None 
            and self.userSelection != None
            and self.backgroundSelection != None
            and self.songSelection != None): 
                self.selectionScreenStage = "M4"

            # user clicks play (note only when all required selections made^)
            playButtonMargin = 83
            playButtonWidth = 181
            playButtonHeight = 50

            if ((x > self.width - playButtonMargin - playButtonWidth)
            and (x < self.width - playButtonMargin)
            and (y > self.height - playButtonMargin - playButtonHeight)
            and (y < self.height - playButtonMargin)): 
                self.gameScreen = True
                self.selectionScreen = False
                self.playMusic()
    
    def playMusic(self):
        # plays music 
        if "Battle" in self.modeSelection and self.gameScreen == True:
            pygame.mixer.music.play(0)
        # implements endless mode 
        # by playing song again and re-setting visualization parameters
        elif "Endless" in self.modeSelection or self.playAgain == True: 
            pygame.mixer.music.play(0)
            self.timeSoFar = 0
            self.playAgain = False 

# runs game 
Game(1400, 700).run()