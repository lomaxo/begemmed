from random import randint
#import pygame, os
from pygame.constants import *
from pygame.rect import Rect
import resources

from gem import *
# This is just some stuff.
__author__ = 'OTL'

CLOCK_TICK = pygame.USEREVENT + 2
# FONT_PATH = "tiki_tropic"

class MainGame():
    def __init__(self, screen, size, colours, xOffset=0, yOffset=0):
        self.size = size
        self.selectedGems = []
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.colours = colours
        self.score = 10
        self.screen = screen
        self.next_state = "this"
        self.gameOver = False
        # TODO move font loading to resources module
        # self.font = pygame.font.Font(os.path.join(FONT_PATH, "Tiki Tropic.ttf"), 40)

        self.background = pygame.image.load('background.png').convert()
        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))

        pygame.time.set_timer(CLOCK_TICK, 1000)

        # Create the grid of Gems
        self.gems = []
        self.grid = []
        self.tripletsToRemove = []
        for x in range(0, size):
            newList = []
            for y in range(0, size):
                newList.append(0)
            self.grid.append(newList)

        for x in range(0, size):
            # self.grid.append([])
            newList = []
            for y in range(0, size):
                newgem = Gem(self, randint(1, colours))
                newgem.setPosition(x, y, xOffset, yOffset)
                self.gems.append(newgem)
                # newList.append(newgem)
                # self.grid[x].append(newList)

        self.sprites = pygame.sprite.RenderPlain(self.gems)

    def update(self):
        self.updateGrid()
        # Fall
        for gem in self.gems:
            if (gem.y < self.size - 1) and (self.grid[gem.x][gem.y + 1] == 0):
                gem.move_to_grid(gem.x, gem.y + 1)
                # print "Falling", self.x, self.y

        self.updateGrid()
        # Create new gems
        for x in range(0, self.size):
            if self.grid[x][0] == 0:
                # if (self.grid[x][1] != 0 and self.grid[x][1].isMoving() == False)
                test_sprite = pygame.sprite.Sprite()
                test_sprite.rect = self.getRectFromGrid(x, -1)
                if pygame.sprite.spritecollide(test_sprite, self.sprites, False):
                    continue
                newGem = Gem(self, randint(1, self.colours))
                newGem.setPosition(x, -1, self.xOffset, self.yOffset)
                self.gems.append(newGem)
                self.grid[x][0] = newGem
                newGem.add(self.sprites)

        self.updateGrid()
        if self.isGridComplete() and not self.isAnyMoving():
            if self.check_moves_available() == False:
                print("THE END!!!")
                self.next_state = "gameover"
                # self.gameOver = True
            self.checkTriplets()
            self.removeFoundTriplets()

        if self.score <= 0:
            self.next_state = "gameover"
        # Update all the sprites
        self.sprites.update()


    def draw(self):
        # Draw the screen
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0,0))
        self.sprites.draw(self.screen)

        # Put the score on the screen below the grid
        text = resources.get_font(40).render("Score: " + str(self.score), True, (128, 128, 128))
        textpos = text.get_rect()
        textpos.left = self.xOffset
        textpos.top = self.yOffset * 2 + self.size * 64
        self.screen.blit(text, textpos)

    def do_event(self, event):
        if event.type == MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            self.detectClick(click_pos)
        if event.type == MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()
            self.detectClick(click_pos)
        if event.type == KEYUP:
            if event.key == K_q:
             self.next_state = "gameover"
        if event.type == CLOCK_TICK:
            print("Tick!")
            self.score -= 1

    def getRectFromGrid(self, x, y):
        return Rect(x * self.gems[0].rect.width + self.xOffset, y * self.gems[0].rect.height + self.yOffset,
                    self.gems[0].rect.width, self.gems[0].rect.height)

    def gem_exists(self, x, y):
        if x < 0 or y < 0: return 0
        elif x >= self.size or y >= self.size: return 0
        elif self.grid[x][y] == 0: return 0
        else: return self.grid[x][y].colour


    def detectClick(self, pos):
        if self.isAnyMoving(): return
        clicked_sprite = [s for s in self.sprites if s.rect.collidepoint(pos)]
        # Add the clicked gem to the list of selected gems and tell it that it is selected.
        self.selectedGems += clicked_sprite
        for s in clicked_sprite:
            s.select()

        # If there are now two selected, check if a valid swap, then swap their positions
        if len(self.selectedGems) >= 2:
            if self.selectedGems[0].isAdjacent(self.selectedGems[1]):
                self.selectedGems[0].swapWith(self.selectedGems[1])
                i = len(self.tripletsToRemove)
                self.checkTriplets()
                # print len(self.tripletsToRemove) - i, "new triplets found"
                if (len(self.tripletsToRemove) - i) < 1:
                    self.selectedGems[1].swapWith(self.selectedGems[0])
                    # self.wrong.play()
                    resources.play_sound("Powerup25")

            self.unselectAll()

    def unselectAll(self):
        for s in self.selectedGems:
            s.unselect()
            self.selectedGems = []

    def check_moves_available(self):

        # Return True if the board is in a state where a matching
        # move can be made on it. Otherwise return False.

        # The patterns in oneOffPatterns represent gems that are configured
        # in a way where it only takes one move to make a triplet.
        oneOffPatterns = (((0,1), (1,0), (2,0)),
                          ((0,1), (1,1), (2,0)),
                          ((0,0), (1,1), (2,0)),
                          ((0,1), (1,0), (2,1)),
                          ((0,0), (1,0), (2,1)),
                          ((0,0), (1,1), (2,1)),
                          ((0,0), (0,2), (0,3)),
                          ((0,0), (0,1), (0,3)))

        # The x and y variables iterate over each space on the board.
        # If we use + to represent the currently iterated space on the
        # board, then this pattern: ((0,1), (1,0), (2,0))refers to identical
        # gems being set up like this:
        #
        #     +A
        #     B
        #     C
        #
        # That is, gem A is offset from the + by (0,1), gem B is offset
        # by (1,0), and gem C is offset by (2,0). In this case, gem A can
        # be swapped to the left to form a vertical three-in-a-row triplet.
        #
        # There are eight possible ways for the gems to be one move
        # away from forming a triple, hence oneOffPattern has 8 patterns.

        for x in range(self.size):
            for y in range(self.size):
                for pat in oneOffPatterns:
                    # check each possible pattern of "match in next move" to
                    # see if a possible move can be made.
                    if (self.gem_exists(x+pat[0][0], y+pat[0][1]) == self.gem_exists(x+pat[1][0], y+pat[1][1]) == self.gem_exists(x+pat[2][0], y+pat[2][1]) != 0) or (self.gem_exists(x+pat[0][1], y+pat[0][0]) == self.gem_exists(x+pat[1][1], y+pat[1][0]) == self.gem_exists(x+pat[2][1], y+pat[2][0]) != 0):
                        return True # return True the first time you find a pattern
        return False



    def checkTriplets(self):
        # if self.isAnyMoving(): return
        # For every Gem, check if there are two or more identical gems to the right and below
        self.updateGrid()
        triplet = []
        # Check horizontally
        for y in range(0, self.size):
            lastColour = 0
            triplet = []
            for x in range(0, self.size):
                # print "Colour", self.grid[x][y].colour
                if self.grid[x][y] == 0: continue
                if self.grid[x][y].colour == lastColour or len(triplet) == 0:
                    triplet.append(self.grid[x][y])
                    lastColour = self.grid[x][y].colour
                else:
                    if len(triplet) >= 3:
                        if triplet not in self.tripletsToRemove:
                            self.tripletsToRemove.append(triplet)
                        # print "Triplet found!", triplet[0].colour, len(triplet)

                    triplet = [self.grid[x][y]]
                    lastColour = self.grid[x][y].colour
            if len(triplet) >= 3:
                self.tripletsToRemove.append(triplet)

        # Check vertically
        for x in range(0, self.size):
            lastColour = 0
            triplet = []
            for y in range(0, self.size):
                # print "Colour", self.grid[x][y].colour
                if self.grid[x][y] == 0: continue
                if self.grid[x][y].colour == lastColour or len(triplet) == 0:
                    triplet.append(self.grid[x][y])
                    lastColour = self.grid[x][y].colour
                else:
                    if len(triplet) >= 3:
                        if triplet not in self.tripletsToRemove:
                            self.tripletsToRemove.append(triplet)
                        # print "Triplet found!", triplet[0].colour, len(triplet)

                    triplet = [self.grid[x][y]]
                    lastColour = self.grid[x][y].colour


            # # also check the last group
            if len(triplet) >= 3:
                self.tripletsToRemove.append(triplet)

    def updateGrid(self):
        # Empty the grid
        for y in range(0, self.size):
            for x in range(0, self.size):
                self.grid[x][y] = 0

        # Then refill it
        for gem in self.gems:
            self.grid[gem.x][gem.y] = gem

    def isAnyMoving(self):
        for gem in self.gems:
            if gem.isMoving(): return True

        return False


    def removeFoundTriplets(self):
        # Remove the list of triplets already found
        # if not self.isAnyMoving():
        if len(self.tripletsToRemove) > 0:
            # print "Number of triplets found:", len(self.tripletsToRemove)
            # self.ping.play()
            resources.play_sound("Powerup6")
        while len(self.tripletsToRemove) > 0:
            t = self.tripletsToRemove.pop()
            self.score += len(t) * len(t)
            # print "Set of", len(t), "increasing score by", len(t)*len(t), "to", self.score
            for gem in t:
                self.removeGem(gem)

    def removeGem(self, gem):
        if gem in self.gems:
            self.gems.remove(gem)
        gem.remove(self.sprites)
        self.grid[gem.x][gem.y] = 0
        del gem

    def highlightGemsToRemove(self):
        while len(self.tripletsToRemove) > 0:
            t = self.tripletsToRemove.pop()
            for gem in t:
                gem.select()

    def isGridComplete(self):
        self.updateGrid()
        for column in self.grid:
            for gem in column:
                if gem == 0: return False
        return True


