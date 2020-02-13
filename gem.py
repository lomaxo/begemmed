import pygame

GEMFOLDER = 'Gems_01/'
GEMFILE = 'Gems_01_64x64_'

__author__ = 'OTL'


class Gem(pygame.sprite.Sprite):
    def __init__(self, gameState, colour):
        pygame.sprite.Sprite.__init__(self)
        self.gameState = gameState
        self.colour = colour
        self.normal_image = pygame.image.load(GEMFOLDER + GEMFILE + str(self.colour).zfill(3) + '.png').convert()
        self.clicked_image = pygame.image.load(GEMFOLDER + GEMFILE + str(self.colour + 7).zfill(3) + '.png').convert()
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.clicked_image.set_colorkey((0,0,0))
        self.selected = False
        self.pathList = []


    def update(self):
        if len(self.pathList) != 0:
            self.rect.x, self.rect.y = self.pathList.pop(0)
            # return

    def setPosition(self, x, y, xOffset=0, yOffset=0):
        self.x = x
        self.y = y
        self.rect.x = self.x * self.rect.width + xOffset
        self.rect.y = self.y * self.rect.height + yOffset
        self.gameState.grid[x][y] = self

    def select(self):
        self.image = self.clicked_image
        self.selected = True
        # print "selecting Gem at:", self.x, self.y

    def unselect(self):
        self.image = self.normal_image
        self.selected = False

    def isAdjacent(self, otherGem):
        if self.x == otherGem.x and (self.y == (otherGem.y + 1) or self.y == (otherGem.y - 1)):
            return True
        elif self.y == otherGem.y and (self.x == (otherGem.x + 1) or self.x == (otherGem.x - 1)):
            return True
        else:
            return False

    def swapWith(self, otherGem):
        x, y = otherGem.x, otherGem.y
        otherGem.move_to_grid(self.x, self.y)
        self.move_to_grid(x, y)

    def move_to_grid(self, x, y):
        self.createPathTo(self.gameState.getRectFromGrid(x, y))
        self.x, self.y = x, y
        self.gameState.grid[x][y] = self

    def createPathTo(self, toRect):
        # Create the list
        steps = 8
        fromRect = self.gameState.getRectFromGrid(self.x, self.y)
        startRect = fromRect.copy()
        # self.pathList = []
        for i in range(0, steps - 1):
            nextX = i * (toRect.x - fromRect.x) / steps + startRect.x
            nextY = i * (toRect.y - fromRect.y) / steps + startRect.y
            self.pathList.append([nextX, nextY])
        self.pathList.append([toRect.x, toRect.y])

    def isMoving(self):
        if len(self.pathList) > 0:
            return True
        else:
            return False


