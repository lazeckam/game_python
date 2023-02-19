import math
import pygame
import os
import constants as const
from spritesheet_functions import SpriteSheet, Enemy_type
 

class Player(pygame.sprite.Sprite):
    """
    Klasa reprezentująca gracza.
    """
    walking_frames_l = []    # lista lewych profili gracza
    walking_frames_r = []    # lista prawych profili gracza
    standing_frame = []
    life = 3                 # liczba żyć - domyślnie gracz ma 3 życia
    dead_enemies = 0         # liczba wrógów, których gracz zdeptał
    fast = 1                 # 
    collected_coins = 0      # liczba monet, które zebrał
    collected_keys = 0       # liczba kluczy, które zebrał
    direction = "R"          # w którą stronę idzie (od tego zależy który profil będzie wyświetlany)
    
    def __init__(self):
        """ Konstruktor gracza. """
        super().__init__()
        
        sprite_sheet = SpriteSheet("p1_walk.png")
        
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        
        # startowy ludek
        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
 
        self.change_x = 0  # początkowe prędkości równe 0
        self.change_y = 0
 
        self.level = None
 
    def update(self):
        """ Ruchy gracza i interakcja z innymi obiektami. """
        # Spadanie 
        self.calc_grav()
 
        # Ruchy w poziomie
        self.rect.x += self.change_x
        
        # Ruszanie się ciała przy chodzeniu
        if self.direction == "R":
            frame = (self.rect.x + self.level.world_shift // 15) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        elif self.direction == "L":
            frame = (self.rect.x + self.level.world_shift // 15) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
       
        # Zderzenia z platformami w poziomie
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)        
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        
        # Ruchy w pionie
        self.rect.y += self.change_y
        
        # Zderzenia z platfomami w pionie
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:                 # obicie się głową o platformę
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:               # wskoczenie na platformę
                self.rect.top = block.rect.bottom
            self.change_y = 0                     # potem koniec ruchu w pionie, możliwe jedynie opadanie zgodnie z grawitacją
        
        # Zbieranie monet
        blocks_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, True)
        for block in blocks_hit_list:
            self.collected_coins += 1
            coins_sound = pygame.mixer.Sound("coin.wav")
            coins_sound.play()
        
        # Zbieranie kluczy
        blocks_hit_list = pygame.sprite.spritecollide(self, self.level.key_list, True)
        for block in blocks_hit_list:
            self.collected_keys += 1
            
        # Zbieranie niespodzianek
        blocks_hit_list = pygame.sprite.spritecollide(self, self.level.surprisefast_list, True)
        for block in blocks_hit_list:
            if self.fast == 1:
                self.fast += 1
        blocks_hit_list = pygame.sprite.spritecollide(self, self.level.surpriseslow_list, True)
        for block in blocks_hit_list:
            if self.fast > 1:
                self.fast = 1
        
        # Zderzenia z wrogami (można poprawić, np. żeby odbijało i w inną stronę niż robak idzie, jak gracz stoi)
        blocks_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for block in blocks_hit_list:
            #if self.rect.y + self.rect.height < block.rect.y: --- głupie, bo nie działa - powinno zawsze być True
            self.life -= 1  
            hit_sound = pygame.mixer.Sound("hit.wav")
            hit_sound.play()
            self.rect.x = self.rect.x - self.change_x * 10   # jak wpadniesz, to niech cię odbije w przeciwną stronę
            if self.change_x == 0:                           # a jak stoisz, to niech cię odbije w lewo o 40
                self.rect.x = self.rect.x - 40
            
    def calc_grav(self):
        """ Liczy, o ile gracz opada pod wpływem grawitacji. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35 * self.fast
 
        if self.rect.y >= const.SCREEN_HEIGHT + 100 and self.change_y >= 0:  # jak nie ma platformy, spada w dziurę
            self.change_y = 0
            self.rect.y = const.SCREEN_HEIGHT
 
    def jump(self):
        """ Liczy ruch w górę gracza, gdy wciśnięta zostanie strzałka w górę. """
        
        self.rect.y += 2   # sprawdzamy, czy możemy skoczyć (czy nie ma jakiejś przeszkody nad nami)
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        if len(platform_hit_list) > 0 or self.rect.bottom >= const.SCREEN_HEIGHT + 50: # jeśli możemy skoczyć, to skoczmy
            self.change_y = -10 * self.fast
 
    def go_left(self):
        """ Liczy ruch w lewo gracza, gdy wciśnięta zostanie strzałka w lewo. """
        self.change_x = -6 * self.fast
        self.direction = "L"

    def go_right(self):
        """ Liczy ruch w prawo gracza, gdy wciśnięta zostanie strzałka w prawo. """
        self.change_x = 6 * self.fast
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        
class Enemy(pygame.sprite.Sprite):
    """
    Klasa reprezentująca wrogów gracza.
    """
    walking_frames_l = []
    walking_frames_r = []
    direction = "L"
    no_frame = 0 
    frame = 0
    dead = False
    def __init__(self,type_of):
        """ Konstruktor wroga."""
        super().__init__()
        
        self.walking_frames_r, self.walking_frames_l = Enemy_type(type_of)
        
        self.image = self.walking_frames_r[0]   # najpierw idzie w lewo, r tu oznacza lewo
        self.rect = self.image.get_rect()
        
        self.change_x = 1                       #prędkość robaczka
       
    
    def update(self):
        """ Aktualizacja wroga."""
        if self.dead == False:                   # jak martwy, to ma być w tle i nic poza tym
            self.rect.x += self.change_x         # rusza się o change_x, jak zderza się z platformą, to zawraca
            if len(pygame.sprite.spritecollide(self, self.player.level.platform_list, False)) > 0:
                self.change_x *= -1
                if self.direction == "R":        # zawraca, czyli zmienia kierunek, w którym idzie
                    self.direction = "L"
                else:
                    self.direction = "R"
                    
            if self.direction == "R":            # ma się wić i to wić w odpowiednim kierunku z okiem w głowie, a nie w ogonie
                if self.no_frame == 15:
                    self.frame = 1 - self.frame
                    self.image = self.walking_frames_r[self.frame]
                    self.no_frame = 0
                else:
                    self.no_frame += 1
            else:
                if self.no_frame == 15:
                    self.frame = 1 - self.frame
                    self.image = self.walking_frames_l[self.frame]
                    self.no_frame = 0
                else:
                    self.no_frame += 1
                
            #a tutaj sprawdzam, czy player zdeptał zwierzątko
            if self.rect.y <= self.player.rect.y + self.player.rect.height + self.player.change_y + 2:
                if self.rect.x + 1 < self.player.rect.x + self.player.rect.width and self.rect.x + self.rect.width - 1 > self.player.rect.x:
                    if self.direction == "R":                   # zwierzątko umiera w odpowiednim kierunku
                        self.image = self.walking_frames_r[2]
                    else:
                        self.image = self.walking_frames_l[2]
                    self.change_x = 0                           # i już się więcej nie rusza
                    self.player.level.enemy_list.remove(self)   # i już playerowi nie zagraża
                    self.player.level.deadenemy_list.add(self)  # ale trup ma być widoczny na planszy
                    self.dead = True
                    kill_sound = pygame.mixer.Sound("kill.wav")
                    kill_sound.play()
        else:
            if self.rect.y < const.SCREEN_HEIGHT + 200:
                self.rect.y += 5
                self.change_y = 0

class FlyingEnemy(pygame.sprite.Sprite):
    """
    Klasa reprezentująca latających wrogów gracza.
    """
    walking_frames_l = []
    walking_frames_r = []
    direction = "L"
    no_frame = 0 
    frame = 0
    dead = False
    where = [0, 0]
    x_start = 0
    y_start = 0
    sign = 1
    def __init__(self, x, y, type_of):
        """ Konstruktor latającaego wroga"""
        super().__init__()
        
        self.walking_frames_r, self.walking_frames_l = Enemy_type(type_of)
        
        self.image = self.walking_frames_r[0]   # najpierw idzie w lewo, r tu oznacza lewo
        self.rect = self.image.get_rect()

        self.rect.x = x                         #początkowe położenie
        self.rect.y = y
        
        self.change_x = 1                       #prędkość robaczka
        self.change_y = 0
        self.where = [x - 200, x + 200]
        self.x_start = x
        self.y_start = y
    
    def update(self):
        """ Aktualizacja latającego wroga."""
        self.where[0] = self.player.level.world_shift + 300 + self.x_start - 200
        self.where[1] = self.player.level.world_shift + 300 + self.x_start + 200
        if self.dead == False:                   # jak martwy, to ma być w tle i nic poza tym
            self.rect.x += self.change_x         # rusza się o change_x, jak zderza się z platformą, to zawraca
            if len(pygame.sprite.spritecollide(self, self.player.level.platform_list, False)) > 0:
                self.change_x *= -1
                self.rect.x += self.change_x 
                if self.direction == "R":        # zawraca, czyli zmienia kierunek, w którym idzie
                    self.direction = "L"
                else:
                    self.direction = "R"
            if self.rect.x < self.where[0] or self.rect.x > self.where[1]:  # żeby robaczek nie fruwał poza wyznaczonym obszarem
                self.change_x *= -1
                self.rect.x += self.change_x 
                if self.direction == "R":
                    self.direction = "L"
                else:
                    self.direction = "R"
            self.rect.y = 20*math.sin((self.rect.x - self.player.level.world_shift)/10) + self.y_start  # robaczek ma fruwać po sinusoidzie
             
            if len(pygame.sprite.spritecollide(self, self.player.level.platform_list, False)) > 0: # jak walnie coś górą lub dołem
                self.change_x *= -1
                self.rect.x += self.change_x 
                if self.direction == "R":
                    self.direction = "L"
                else:
                    self.direction = "R"
            if self.rect.y < 70:                 # jak chce za wysoko polecieć
                self.rect.y = 72
                self.change_x *= -1
                self.rect.x += self.change_x 
                if self.direction == "R":
                    self.direction = "L"
                else:
                    self.direction = "R"
                
            if self.direction == "R":            # ma się wić i to wić w odpowiednim kierunku z okiem w głowie, a nie w ogonie
                if self.no_frame == 15:
                    self.frame = 1 - self.frame
                    self.image = self.walking_frames_r[self.frame]
                    self.no_frame = 0
                else:
                    self.no_frame += 1
            else:
                if self.no_frame == 15:
                    self.frame = 1 - self.frame
                    self.image = self.walking_frames_l[self.frame]
                    self.no_frame = 0
                else:
                    self.no_frame += 1
                
            #a tutaj sprawdzam, czy player zdeptał zwierzątko
            if (self.rect.y <= self.player.rect.y + self.player.rect.height + self.player.change_y + 2) and (self.rect.y >= self.player.rect.y + self.player.rect.height + self.player.change_y - 10):
                if self.rect.x + 3 < self.player.rect.x + self.player.rect.width and self.rect.x + self.rect.width - 3 > self.player.rect.x:
                    if self.direction == "R":                   # zwierzątko umiera w odpowiednim kierunku
                        self.image = self.walking_frames_r[2]
                    else:
                        self.image = self.walking_frames_l[2]
                    self.change_x = 0                           # i już się więcej nie rusza
                    self.player.level.enemy_list.remove(self)   # i już playerowi nie zagraża
                    self.player.level.deadenemy_list.add(self)  # ale trup ma być widoczny na planszy
                    self.dead = True
                    kill_sound = pygame.mixer.Sound("kill.wav")
                    kill_sound.play()
        else:
            if self.rect.y < const.SCREEN_HEIGHT + 200:
                self.rect.y += 5
                self.change_y = 0
            

        
class Surprise(pygame.sprite.Sprite):
    """
    Klasa reprezentująca niespodzianki wyskakujące z odpowiednich platform (SurprisePlatform).
    """
    def __init__(self, x, y, type_of):
        """ Konstruktor niespodzianki"""
        super().__init__()
        if type_of == 0:
            image = pygame.image.load("mushroomRed.png").convert()
        else:
            image = pygame.image.load("mushroomBrown.png").convert()
        image = pygame.transform.scale(image, (70, 70))
        self.image = image
        self.image.set_colorkey(const.BLACK)
        self.rect = self.image.get_rect()
        self.ile = 0 
        self.rect.x = x
        self.rect.y = y                 
                    
class Coin(pygame.sprite.Sprite):
    """
    Klasa reprezentująca monety do zbierania.
    """
    def __init__(self, x, y):
        """ Konstruktor monety"""
        super().__init__()
        image = pygame.image.load("coinGold.png").convert()
        image = pygame.transform.scale(image, (60, 60))
        self.image = image
        self.image.set_colorkey(const.BLACK)
        self.rect = self.image.get_rect()
        self.ile = 0
        self.rect.x = x
        self.rect.y = y    
        
class Key(pygame.sprite.Sprite):
    """
    Klasa reprezentująca klucze do zamków. 
    """
    def __init__(self, x, y):
        """ Konstruktor klucza"""
        super().__init__()
        image = pygame.image.load("keyYellow.png").convert()
        image = pygame.transform.scale(image, (60, 60))
        self.image = image
        self.image.set_colorkey(const.BLACK)
        self.rect = self.image.get_rect()
        self.ile = 0
        self.rect.x = x
        self.rect.y = y    
        
class Sign(pygame.sprite.Sprite): 
    """
    Klasa do rysowania strzałek na koniec poziomu. 
    """
    def __init__(self, x, y):
        """ Konstruktor strzałki na koniec poziomu."""
        super().__init__()
        image = pygame.image.load("signRight.png").convert()
        image = pygame.transform.scale(image, (70, 70))
        self.image = image
        self.image.set_colorkey(const.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y    

        #niepotrzebna
class Life(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("life3.png").convert()
        self.image.set_colorkey(const.BLACK)
        self.rect = self.image.get_rect()
        self.ile = 0
        self.rect.x = 180
        self.rect.y = 20
        
    def update(self, screen, font, player):
        self.ile = player.life
        #output = "{0}".format(self.ile)
        #text = font.render(output, True, [255,255,51])
        #screen.blit(text, [150, 20])
        

