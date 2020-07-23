"""
PygameGame.py
- contains base class for Game class (in Main.py)
"""

import pygame

# code modified from: http://blog.lukasperaza.com/getting-started-with-pygame/

class PygameGame(object):

    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, width=1400, height=700, fps=50, title="Flappy Beat"):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        screen = pygame.display.set_mode((self.width, self.height))
        # logo background image taken from https://projecthvac.com/home-new/
        self.logoBackground = pygame.transform.scale(
            pygame.image.load('images/obstacle.png').convert_alpha(), 
            (self.height//2, self.height//2))
        # logo designed on https://www.canva.com/
        self.logo = pygame.transform.scale(
            pygame.image.load('images/logo.png').convert_alpha(), 
            (self.height*3//10, self.height*3//10))
        # title, help, selection screens were self-made with Microsoft PPT
        self.titleScreenPic = pygame.transform.scale(
            pygame.image.load('images/titleScreen.png').convert_alpha(),
            (self.width, self.height))
        self.helpScreenPic = pygame.transform.scale(
            pygame.image.load('images/helpScreen.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenPic = pygame.transform.scale(
            pygame.image.load('images/selectionScreen.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenSolo1 = pygame.transform.scale(pygame.image.load(
            'images/selectionScreenSoloPlayer.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenSolo2 = pygame.transform.scale(pygame.image.load(
            'images/selectionScreenSoloBg.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenSolo3 = pygame.transform.scale(pygame.image.load(
            'images/selectionScreenSoloSong.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenSolo4 = pygame.transform.scale(pygame.image.load(
            'images/selectionScreenSoloPlay.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenMulti1 = pygame.transform.scale(pygame.image.load(
            'images/selectionScreenMultiPlayer.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenMulti2 = pygame.transform.scale(pygame.image.load(
            'images/selectionScreenMultiBg.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenMulti3 = pygame.transform.scale(pygame.image.load(
            'images/selectionScreenMultiSong.png').convert_alpha(),
            (self.width, self.height))
        self.selectionScreenMulti4 = pygame.transform.scale(pygame.image.load(
            'images/selectionScreenMultiPlay.png').convert_alpha(),
            (self.width, self.height))

    def run(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption(self.title)
        screen = pygame.display.set_mode((self.width, self.height))
        self._keys = dict()

        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            self.redrawAll(screen)
            pygame.display.update()

        pygame.quit()

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()