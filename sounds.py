__author__ = 'OTL'
import pygame, random, os
import resources

SONG_END = pygame.USEREVENT + 1

# TODO Move all this to the resources module
# TODO: Add volume control and mute?

class Music():
    def __init__(self):
        pygame.mixer.music.set_endevent(SONG_END)
        self._songs = [
            'Visager_-_01_-_Title_Theme',
            'Visager_-_02_-_Castle_Theme',
            'Visager_-_03_-_Shrine',
            'Visager_-_04_-_The_Great_Forest',
            'Visager_-_05_-_Windy_Bluffs',
            'Visager_-_06_-_Pyramid_Level',
            'Visager_-_07_-_Ice_Cave',
            'Visager_-_08_-_Airship',
            'Visager_-_09_-_Dark_Sanctum_Boss_Fight',
            'Visager_-_10_-_Village_Dreaming',
            'Visager_-_11_-_The_Final_Road',
        ]

        self._currently_playing_song = self._songs[10]

        resources.play_music(self._currently_playing_song)


    def on_event(self, event):
        if event.type == SONG_END:
            print("Song ended!")
            self.play_next_random()

    def play(self,  song_number):
        resources.play_music(self._songs[song_number])
        self._currently_playing_song = self._songs[song_number]


    def play_next_random(self):
        next_song = random.choice(self._songs)
        while next_song == self._currently_playing_song:
            next_song = random.choice(self._songs)
        self._currently_playing_song = next_song
        resources.play_music(next_song)

