__author__ = 'OTL'

import os, sys
import pygame

DATA_FOLDER = "data"
MUSIC_FOLDER = "music"
SOUND_FOLDER = "sounds"
FONT_FOLDER = "fonts"
DEFAULT_FONT = "PressStart2P"

sounds = {}
fonts = {}

# TODO Make this resistant to missing files with try statements...

def get_music_file(song_name, extension="ogg"):
    path = os.path.join(DATA_FOLDER, MUSIC_FOLDER)
    file_name = os.path.join(path, song_name + "." + extension)
    return file_name

def play_music(song_name, extension="ogg"):
    try:
        pygame.mixer.music.load(get_music_file(song_name, extension))
        pygame.mixer.music.play(0)
    except pygame.error, message:
            print('Cannot load music:', song_name)
            raise SystemExit, message

def play_sound(sound_name, extension="wav"):
    if not sounds.has_key(sound_name):
        path = os.path.join(DATA_FOLDER, SOUND_FOLDER)
        file_name = os.path.join(path, sound_name + "." + extension)
        # TODO: Work out why this isn't raising exceptions
        try:
            sounds[sound_name] = pygame.mixer.Sound(file_name)
            print(sounds[sound_name])
        except pygame.error, message:
            print 'Cannot load sound:', file_name
            raise SystemExit, message
        except:
            print("Unexpected error", sys.exc_info()[0])
            raise


    print(sounds[sound_name].play())

def get_font(size, font_name = DEFAULT_FONT, extension="ttf"):
    if not fonts.has_key((font_name, size)):
        path = os.path.join(DATA_FOLDER, FONT_FOLDER)
        file_name = os.path.join(path, font_name + "." + extension)
        try:
            fonts[(font_name, size)] = pygame.font.Font(file_name, size)
        except: # pygame.error, message:
            # print("Unexpected error", sys.exc_info()[0])
            # raise
            print('Cannot load font: ' + file_name)
            raise SystemExit
    return fonts[(font_name, size)]