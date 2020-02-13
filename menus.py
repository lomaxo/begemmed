__author__ = 'OTL'

import pygame
from pygame.locals import *
import resources
import noise_surfaces


# TODO add buttons

class MenuItem():
    def __init__(self, caption, new_state):
        self.caption = caption
        self.text_normal = resources.get_font(40).render(caption, True, (128,255,128))
        self.text_highlight = resources.get_font(50).render(caption, True, (255,255,255))
        self.text_surface = self.text_normal

        self.new_state = new_state

        self.rect = self.text_surface.get_rect()
        # self.rect.left = x
        # self.rect.top = y

class Menu():
    def __init__(self, state, top=100):
        self.state = state
        self.menu_selected = None
        self.menu_items = []
        self.top = top

    def draw(self, screen):
        # Draw the menu items
        for item in self.menu_items:
            screen.blit(item.text_surface, item.rect)

    def do_event(self, event):
        if event.type == MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.menu_selected = None
            for item in self.menu_items:
                if item.rect.collidepoint(mouse_pos):
                    item.text_surface = item.text_highlight
                    self.menu_selected = item
                else:
                    item.text_surface = item.text_normal
        if event.type == MOUSEBUTTONUP:
            if self.menu_selected is not None:
                print(self.menu_selected.caption)
                self.state.next_state = self.menu_selected.new_state

    def add_item(self, menu_item):
        menu_item.rect.center = self.state.screen.get_rect().center
        if len(self.menu_items) > 0:
            menu_item.rect.top = self.menu_items[-1].rect.top + (self.menu_items[-1].rect.height * 1.5)
        else:
            menu_item.rect.top = self.top
        self.menu_items.append(menu_item)



class MainMenu():
    def __init__(self,screen):
        self.screen = screen
        self.next_state = "this"

        # Create the menu
        self.menu = Menu(self, 300)
        self.menu.add_item(MenuItem("Play", "main"))
        self.menu.add_item(MenuItem("Quit", "quit"))
        self.background = noise_surfaces.Animated_perlin_surface()
        self.background.init(50)


    def update(self):
        self.background.update()
        pass

    def draw(self):
        # self.screen.fill((0,0,0))
        self.background.draw(self.screen)
        text = resources.get_font(60).render("Begemmed!", True, (128, 255, 128))
        textpos = text.get_rect(center = self.screen.get_rect().center)
        textpos.y = 100
        self.screen.blit(text, textpos)
        text = resources.get_font(35).render("by Oliver Lomax", True, (128, 255, 128))
        # textpos = text.get_rect(center = self.screen.get_rect().center)
        textpos.y += 100
        self.screen.blit(text, textpos)
        text = resources.get_font(25).render("Music by Visager", True, (128, 255, 128))
        textpos = text.get_rect(center = self.screen.get_rect().center)
        textpos.y += 300
        self.screen.blit(text, textpos)

        # Draw the menu items
        self.menu.draw(self.screen)


    def do_event(self, event):
        if event.type == KEYUP:
            if event.key == K_SPACE:
                self.next_state = "main"
        #  Send events to the menu
        self.menu.do_event(event)

class GameOver():
    def __init__(self,screen):
        self.screen = screen
        self.next_state = "this"
        resources.play_sound("die")


    def update(self):
        pass

    def draw(self):
        # Create the fading background effect
        screen_rect = self.screen.get_rect()
        filler = pygame.Surface((screen_rect.width, screen_rect.height), pygame.SRCALPHA, 32)
        filler.fill((100,100,100,10))
        self.screen.blit(filler, (0,0))

        text = resources.get_font(50).render("Game Over!", True, (0, 200, 0))
        textpos = text.get_rect(center = self.screen.get_rect().center)
        self.screen.blit(text, textpos)

        text = resources.get_font(20).render("Press any key to continue", True, (0, 200, 0))
        textpos = text.get_rect(center = self.screen.get_rect().center)
        textpos.y += 300
        self.screen.blit(text, textpos)

    def do_event(self, event):
        if event.type == KEYUP:
            # if event.key == K_SPACE:
            self.next_state = "menu"
