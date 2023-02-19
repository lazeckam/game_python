import pygame
import random

import constants as const
from platform import Platform, SurprisePlatform
from player import Enemy, Coin, Key, FlyingEnemy, Sign
 

class Level():
    """ 
    Super klasa reprezentująca poziomy.
    """
 
    def __init__(self, player):
        """ Konstruktor. Tworzenie odpowiednich Group. """
        self.platform_list = pygame.sprite.Group()
        self.surprisefast_list = pygame.sprite.Group()
        self.surpriseslow_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.deadenemy_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.key_list = pygame.sprite.Group()
        self.player = player
 
        # szybkość przesuwania się świata
        self.world_shift = -300
        
    def update(self):
        """ Aktualizuje wszystko na poziomie."""
        self.platform_list.update()
        self.enemy_list.update()
        self.deadenemy_list.update()
        self.coin_list.update()
        self.key_list.update()
        self.surprisefast_list.update()
        self.surpriseslow_list.update()
 
    def draw(self, screen):
        """ Rysuje wszystko na poziomie. """
 
        # tło
        screen.fill(const.WHITE)
        screen.blit(self.background,(self.world_shift // 3,0))
 
        # wszystkie grupy Spritów
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.deadenemy_list.draw(screen)
        self.coin_list.draw(screen)
        self.key_list.draw(screen)
        self.surprisefast_list.draw(screen)
        self.surpriseslow_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ Przesuwanie osi współrzędnych zgodnie z przesuwaniem się świata."""
 
        # Keep track of the shift amount
        self.world_shift+= shift_x
 
        # Aktualizujemy współrzędne x wszystkich Spritów na poziomie
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            
        for deadenemy in self.deadenemy_list:
            deadenemy.rect.x += shift_x
            
        for coin in self.coin_list:
            coin.rect.x += shift_x
            
        for key in self.key_list:
            key.rect.x += shift_x
            
        for surprise in self.surprisefast_list:
            surprise.rect.x += shift_x
        
        for surprise in self.surpriseslow_list:
            surprise.rect.x += shift_x
 
 
# Tworzymy konkretne poziomy
class Level_01(Level):
    """ Tworzy poziom 1. """
 
    def __init__(self, player):
        """ Konstruktor poziomu 1. """
        Level.__init__(self, player)
 
        self.level_limit = -2350
 
        # wszystkie platformy z poziomu
        level = [[580, 500, 3], [1000, 500, 3],
                 [800, 350, 6], [870, 350, 7], [940, 350, 8],
                 [1250, 300, 3],
                 [300, const.SCREEN_HEIGHT - 70, 0],
                 [1200, 500, 3], [1500, 500, 3],
                 [1700, 300, 6], [1770, 300, 7], [1840, 300, 7], [1910, 300, 8],
                 [2000, 500, 3], [2200, 350, 6], [2270, 350, 7], [2340, 350, 8],
                 [2600, 500, 3]
                 ]
        for i in range(50):
            level.append([370 + 70 * i, const.SCREEN_HEIGHT - 70, 1])
        for platform in level:
            block = Platform(platform[2])
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            block.player = self.player
            self.platform_list.add(block)
        
        # wszystkie platformy z niespodziankami z poziomu
        block = SurprisePlatform()
        block.rect.x = 1400
        block.rect.y = 300
        block.player = self.player
        self.platform_list.add(block)
        
        # wszyscy wrogowie z poziomu
        x_enemy = [700, 1300, 2300]
        for i in x_enemy:
            enemy = Enemy(random.randint(0,2))
            enemy.rect.x = i
            enemy.rect.bottom = const.SCREEN_HEIGHT - 70
            enemy.player = self.player   
            self.enemy_list.add(enemy)
                                
        enemy0 = FlyingEnemy(2100, 100, 3)
        enemy0.rect.bottom = 200
        enemy0.player = self.player   
        self.enemy_list.add(enemy0)
        
        enemy0 = FlyingEnemy(500, 250, 4)
        enemy0.rect.bottom = 350
        enemy0.player = self.player   
        self.enemy_list.add(enemy0)
        
        # wszystkie monety z poziomu
        odl = (1010 - 800 - 20) / 4
        for i in range(4):
            coin = Coin(800 + odl * i + 10, 280)
            coin.player = self.player   
            self.coin_list.add(coin)
        coin = Coin(1250 + 35 - 30, 230)
        coin.player = self.player   
        self.coin_list.add(coin)
        odl = (70 * 4 - 20) / 6
        for i in range(6):
            coin = Coin(1700 + odl * i + 10, 240)
            coin.player = self.player   
            self.coin_list.add(coin)
        odl = (70 * 3 - 20) / 4
        for i in range(4):
            coin = Coin(2200 + odl * i + 10, 240)
            coin.player = self.player   
            self.coin_list.add(coin)
          
        # wszystkie klucze z poziomu
        key = Key(1070 + 60 - 30, 450)
        key.player = self.player   
        self.key_list.add(key)
        
        key = Key(2000 + 35 - 30, 400)
        key.player = self.player   
        self.key_list.add(key)
        
        # strzałka
        sign = Sign(2880, 600 - 140)
        sign.player = self.player   
        self.deadenemy_list.add(sign)
        
        #tło
        self.background = pygame.image.load("background.png").convert()
        self.background.set_colorkey(const.WHITE)
        
class Level_02(Level):
    """ Tworzy poziom 2. """
 
    def __init__(self, player):
        """ Konstruktor poziomu 2. """
        Level.__init__(self, player)
        self.player.rect.x = 320
        self.player.rect.y = 300
 
        self.level_limit = -2480
 
        # wszystkie platformy z poziomu
        level = [[300, const.SCREEN_HEIGHT - 70, 0], [440, const.SCREEN_HEIGHT - 70, 2],
                 
                 [510, const.SCREEN_HEIGHT - 135, 0], [580, const.SCREEN_HEIGHT - 135, 2], 
                 [510, const.SCREEN_HEIGHT - 70, 9], [580, const.SCREEN_HEIGHT - 70, 9],
                 
                 [790, const.SCREEN_HEIGHT - 70, 0],[860, const.SCREEN_HEIGHT - 70, 1], [930, const.SCREEN_HEIGHT - 70, 2],
                 [790, 320, 6], [930, 320, 8],
                 
                 [1070, const.SCREEN_HEIGHT - 130, 0], [1140, const.SCREEN_HEIGHT - 130, 2],
                 [1070, const.SCREEN_HEIGHT - 70, 9], [1140, const.SCREEN_HEIGHT - 70, 9],
                 [1210, 280, 6], [1280, 280, 8],
                 
                 [1350, const.SCREEN_HEIGHT - 130, 0], [1420, const.SCREEN_HEIGHT - 130, 2],
                 [1350, const.SCREEN_HEIGHT - 70, 9], [1420, const.SCREEN_HEIGHT - 70, 9],
                 [1490, 250, 6], [1560, 250, 8],
                 
                 [1630, const.SCREEN_HEIGHT - 190, 0], [1700, const.SCREEN_HEIGHT - 190, 2],
                 [1630, const.SCREEN_HEIGHT - 130, 9], [1700, const.SCREEN_HEIGHT - 130, 9],
                 [1630, const.SCREEN_HEIGHT - 70, 9], [1700, const.SCREEN_HEIGHT - 70, 9],
                 
                 [1910, const.SCREEN_HEIGHT - 250, 0], [1980, const.SCREEN_HEIGHT - 250, 2],
                 [1910, const.SCREEN_HEIGHT - 190, 9], [1980, const.SCREEN_HEIGHT - 190, 9],
                 [1910, const.SCREEN_HEIGHT - 130, 9], [1980, const.SCREEN_HEIGHT - 130, 9],
                 [1910, const.SCREEN_HEIGHT - 70, 9], [1980, const.SCREEN_HEIGHT - 70, 9],
                 
                 [2260, const.SCREEN_HEIGHT - 70, 0],
                 
                 [2330, 500, 3], [2800, 500, 3],
                 [2400, 350, 3], [2730, 350, 3]
                 ]
        for i in range(2):
            level.append([370 + 70 * i, const.SCREEN_HEIGHT - 70, 1])
        for i in range(20):
            level.append([2260 + 70 + 70 * i, const.SCREEN_HEIGHT - 70, 1])   
            
        for platform in level:
            block = Platform(platform[2])
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            block.player = self.player
            self.platform_list.add(block)
        
        # wszystkie platformy z niespodziankami z poziomu
        block = SurprisePlatform()
        block.rect.x = 860
        block.rect.y = 305
        block.player = self.player
        self.platform_list.add(block)
        
        block = SurprisePlatform()
        block.rect.x = 2400 + (2800 - (2330 + 70))/2 - 35
        block.rect.y = 310
        block.player = self.player
        self.platform_list.add(block)

        
        # wszyscy wrogowie z poziomu  
        x_enemy = [2500]
        for i in x_enemy:
            enemy = Enemy(random.randint(0,2))
            enemy.rect.x = i
            enemy.rect.bottom = const.SCREEN_HEIGHT - 70
            enemy.player = self.player   
            self.enemy_list.add(enemy)
        
        enemy0 = FlyingEnemy(1000, 300, 3)
        enemy0.rect.bottom = 200
        enemy0.player = self.player   
        self.enemy_list.add(enemy0)
        
        enemy0 = FlyingEnemy(500, 300, 4)
        enemy0.rect.bottom = 350
        enemy0.player = self.player   
        self.enemy_list.add(enemy0)
        
        enemy0 = FlyingEnemy(2495, 220, 3)
        enemy0.rect.bottom = 250
        enemy0.player = self.player   
        self.enemy_list.add(enemy0)
        
        # wszystkie monety z poziomu
        odl = [795, 935, 1215, 1285, 1075, 1145, 1355, 1425, 1635, 1705, 1495, 1565, 1915, 1985]
        poz = [230, 230,  210,  210,  410,  410,  410,  410,  350,  350,  190,  190,  290,  290]
        for i in range(len(odl)):
            coin = Coin(odl[i], poz[i])
            coin.player = self.player   
            self.coin_list.add(coin)
        odl = list(range(2050, 2289, 30))
        for i in odl:
            coin = Coin(i, 0.015 * (i - 2132) * (i - 2132) + 150)
            coin.player = self.player   
            self.coin_list.add(coin)
          
        # wszystkie klucze z poziomu
        key = Key(2335, 450)
        key.player = self.player   
        self.key_list.add(key)
        
        # strzałka
        sign = Sign(3000, 600 - 140)
        sign.player = self.player   
        self.deadenemy_list.add(sign)
        
        # tło
        self.background = pygame.image.load("background.png").convert()
        self.background.set_colorkey(const.WHITE)
        
class Level_03(Level):
    """ Tworzy poziom 3. """
 
    def __init__(self, player):
        """ Konstruktor poziomu 3. """
        Level.__init__(self, player)
        self.player.rect.x = 320
        self.player.rect.y = 300
 
        self.level_limit = -2500
 
        # wszystkie platformy z poziomu
        level = [[300, const.SCREEN_HEIGHT - 70, 0], [370, const.SCREEN_HEIGHT - 70, 1], [440, const.SCREEN_HEIGHT - 70, 1], [510, const.SCREEN_HEIGHT - 70, 1], [580, const.SCREEN_HEIGHT - 70, 1], [650, const.SCREEN_HEIGHT - 70, 2],
                 [350, 270, 3],[475, 400, 6], [545, 400, 8], [790, 400, 3],
                 
                 [930, const.SCREEN_HEIGHT - 70, 0], [1000, const.SCREEN_HEIGHT - 70, 2], [1140, 400, 3],
                 [1280, const.SCREEN_HEIGHT - 70, 0], [1350, const.SCREEN_HEIGHT - 70, 2],
                 
                 [1700, const.SCREEN_HEIGHT - 70, 0],
                 [1770, 500, 3], [2050, 500, 3], [2330, 500, 3], [2610, 500, 3],
                 
                 #[1910, 290, 3], [2190, 290, 3],
                 [1910, 320, 6], [1980, 320, 7], [2050, 320, 7], [2120, 320, 7], [2190, 320, 7], [2260, 320, 8],
                 [2470, 400, 3]
                 ]
        for i in range(30):
            level.append([1700 + 70 + 70 * i, const.SCREEN_HEIGHT - 70, 1])
            
        for platform in level:
            block = Platform(platform[2])
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            block.player = self.player
            self.platform_list.add(block)
        
        # wszystkie platformy z niespodziankami z poziomu
        block = SurprisePlatform()
        block.rect.x = 510
        block.rect.y = 200
        block.player = self.player
        self.platform_list.add(block)

        
        # wszyscy wrogowie z poziomu     
        x_enemy = [1880, 2200, 2500]
        j = 0
        for i in x_enemy:
            enemy = Enemy(j)
            enemy.rect.x = i
            enemy.rect.bottom = const.SCREEN_HEIGHT - 70
            enemy.player = self.player   
            self.enemy_list.add(enemy)
            j += 1
            
        enemy0 = FlyingEnemy(2020, 230, 4)
        enemy0.rect.bottom = 300
        enemy0.player = self.player   
        self.enemy_list.add(enemy0)
        
        enemy0 = FlyingEnemy(750, 290, 4)
        enemy0.rect.bottom = 360
        enemy0.player = self.player   
        self.enemy_list.add(enemy0)
        
        enemy0 = FlyingEnemy(1090, 290, 3)
        enemy0.rect.bottom = 360
        enemy0.player = self.player   
        self.enemy_list.add(enemy0)
        
        # wszystkie monety z poziomu
        odl = list(range(685, 965, 40))
        for i in odl:
            coin = Coin(i, 0.015 * (i - 825 + 30) * (i - 825 + 30) + 150)
            coin.player = self.player   
            self.coin_list.add(coin)
        odl = list(range(1035, 1245, 40))
        for i in odl:
            coin = Coin(i, 0.015 * (i - 1035 - 105 + 30) * (i - 1035 - 105 + 30) + 150)
            coin.player = self.player   
            self.coin_list.add(coin)
        odl = list(range(1775, 2616, 84))
        for i in odl:
            coin = Coin(i, 450)
            coin.player = self.player   
            self.coin_list.add(coin)
        odl = list(range(1915, 2195, 70))
        for i in odl:
            coin = Coin(i, 240)
            coin.player = self.player   
            self.coin_list.add(coin)
          
        # wszystkie klucze z poziomu
        key = Key(515, 350)
        key.player = self.player   
        self.key_list.add(key)
        
        # strzałka
        sign = Sign(2800, 600 - 140)
        sign.player = self.player   
        self.deadenemy_list.add(sign)
        
        # tło
        self.background = pygame.image.load("background.png").convert()
        self.background.set_colorkey(const.WHITE)