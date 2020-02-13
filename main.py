#!/usr/bin/env python

import sys, os
from game import *
from menus import *
import sounds

# TODO Move Print statements to a debug function
# TODO make Python3 compatible

GEMWIDTH = 64
GRIDSIZE = 8

pygame.init()
screen = pygame.display.set_mode((GEMWIDTH * (GRIDSIZE+2), 768))
pygame.display.set_caption("Begemmed!")
clock = pygame.time.Clock()

musicPlayer = sounds.Music()

# Create the game state variable

gameState = MainMenu(screen)
mainGame = MainGame(screen, GRIDSIZE, 7, GEMWIDTH, GEMWIDTH)
# Main Game Loop

running = True
i = 0
timer = 0
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == K_ESCAPE: running = False  # quit the game

        elif event.type == QUIT:
            running = False

        # Send all other events to the current game state
        musicPlayer.on_event(event)
        gameState.do_event(event)


    # Update
    gameState.update()
    gameState.draw()
    pygame.display.flip()

    # Change game state if requested
    if gameState.next_state == "main":
        gameState = MainGame(screen, GRIDSIZE, 7, GEMWIDTH, GEMWIDTH)
    elif gameState.next_state == "menu":
        gameState = MainMenu(screen)
    elif gameState.next_state == "gameover":
        gameState = GameOver(screen)
    elif gameState.next_state == "quit":
        running = False

    clock.tick(30)
    # print clock.get_fps()

pygame.quit()
sys.exit()
