import pygame
import random
from spritesheet_functions import SpriteSheet
from player import Surprise, Coin

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 

class Platform(pygame.sprite.Sprite):
    """ Zwykła platforma. """
    
    platform_type = []
        
    def __init__(self, type_of_graphics):
        """ Konstruktor zwykłej platformy """
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)
        

        sprite_sheet = SpriteSheet("tiles_spritesheet.png")

        image = sprite_sheet.get_image(72*7, 72*9, 70, 70)  #dolna platforma - zakończenie z lewej
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*7, 72*8, 70, 70)  #dolna platforma - środkowa bez zakończeń
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*7, 72*7, 70, 70)  #dolna platforma - zakończenie z prawej
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*8, 72*6, 70, 40)  #wisząca platforma - zakończenie z obydwu stron
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*6, 72*4, 70, 70)  #żółta dziurka na klucze
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*6, 72*5, 70, 70)  #czerwona dziurka od klucza
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*8, 72*5, 70, 40)  #wisząca platforma - zakończenie z lewej
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*8, 72*4, 70, 40)  #wisząca platforma - środkowa
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*8, 72*3, 70, 40)  #wisząca platforma - zakończenie z prawej
        self.platform_type.append(image)
        image = sprite_sheet.get_image(72*8, 72*12, 70, 70)  #ziemista platforma - poniżej innej platformy
        self.platform_type.append(image)
        
        self.image = self.platform_type[type_of_graphics]
        self.rect = self.image.get_rect()

        
class SurprisePlatform(Platform):
    """ 
    Na tę platformę można wskakiwać, a dodatkowo jak się posiada kluczyk i się puknie tę platformę od dołu, 
    to wyskakuje niespodzianka.
    """
    open_surprise = False           # czy już niespodzianka wyskoczyła
    
    def __init__(self):
        Platform.__init__(self, 4)  # SurprisePlatform dziedziczy po zwykłej platformie
    
    def update(self):
        if self.open_surprise == False:
            if self.rect.y + self.rect.height >= self.player.rect.y and ((self.rect.x < self.player.rect.x + self.player.rect.width) and (self.rect.x + self.rect.width > self.player.rect.x)) and self.rect.y < self.player.rect.y:
                if self.player.collected_keys > 0:
                    self.image = self.platform_type[5]    
                    self.player.collected_keys -= 1
                    self.open_surprise = True
                    open_sound = pygame.mixer.Sound("lock_open.wav")
                    open_sound.play()

                    wynik_losowania = random.randint(0,2)
                    if wynik_losowania == 0:
                        surprise = Surprise(self.rect.x, self.rect.y - 70, 0)
                        surprise.player = self.player
                        self.player.level.surprisefast_list.add(surprise)
                    elif wynik_losowania == 1:
                        coin = Coin(self.rect.x + 5, self.rect.y - 60)
                        coin.player = self.player
                        self.player.level.coin_list.add(coin)
                    else:
                        surprise = Surprise(self.rect.x, self.rect.y - 70, 1)
                        surprise.player = self.player
                        self.player.level.surpriseslow_list.add(surprise)
