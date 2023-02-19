import pygame
import constants as const

class Timer():
    def __init__(self):
        """
        Konstruktor timera
        """
        self.count = 0
        self.rate = 60
        self.total_sec = 0
        self.minutes = 0
        self.seconds = 0
     
    def update(self, screen, font, x, y):
        """
        Wypisywanie aktualnego czasu gry
        """
        self.total_sec = self.count // 60
        self.minutes = self.total_sec //60
        self.seconds = self.total_sec % 60
        output = "{0:02}:{1:02}".format(self.minutes,self.seconds)
        screen.blit(font.render(output, True, const.JASNYBEZOWY), [x, y])
        self.count += 1
        

        