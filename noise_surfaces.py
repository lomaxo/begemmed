__author__ = 'OTL'

import sys
import pygame
from pygame.constants import *
from noise import pnoise3, snoise3


class Animated_perlin_surface:
    def __init__(self):
        self.surface = []
        self.pixels = []
        self.t = 0
        self.dir = 1

    def init(self, width = 128):
        self.octaves = 5
        self.freq = 1/32.0 #16.0 * octaves
        self.period = 1/self.freq
        self.width = width
        self.scale = 1/32.0
        self.half = 0

        for i in range(width):
            self.surface.append(pygame.Surface((width, width)))
            self.pixels.append(pygame.PixelArray(self.surface[i]))
        for t in range(width):
            for y in range(width):
                for x in range(width):
                    col = int(pnoise3((x * self.scale), (y * self.scale), (t * self.scale), self.octaves, persistence=0.25)*127.0+ 128.0)
                    self.pixels[t][x, y] = (col, col, col)
                    # print(int(snoise3(x * scale - half, y * scale - half, z * scale - half, octaves=4, persistence=0.25)*127.0 + 128.0))
                    # pixels[x, y] = (0, 0, int(pnoise2(x / freq, y / freq, octaves)*127.0 + 128.0))
            self.surface[t] = pygame.transform.scale(self.surface[t], pygame.display.get_surface().get_rect().size)

        del self.pixels

    def get_surface(self):
        return self.surface[self.t]

    def update(self):
        self.t += self.dir
        if self.t >= self.width-1 or self.t<= 0:
            self.dir *= -1
            # self.t = self.t % self.width

    def draw(self, screen):
        screen.blit(self.surface[self.t], (0,0))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((700,700))
    pygame.display.set_caption("Noise")
    clock = pygame.time.Clock()

    running = True

    background = Animated_perlin_surface()
    background.init(50)

    while running:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE: running = False  # quit the game

            elif event.type == QUIT:
                running = False

        background.update()

        background.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        # print clock.get_fps()

    pygame.quit()
    sys.exit()
