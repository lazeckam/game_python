import pygame
import os
import constants as const

class SpriteSheet(object):
    """ Wycinanie konkretnych Spritów z arkusza. """
    sprite_sheet = None

    def __init__(self, file_name):
        """ Konstruktor. file_name - nazwa arkusza """
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Wydobywanie konkretnego Sprita. x, y - współrzędne górnego lewego wierzchołka, 
        width, height - szerokość i wysokość wycinanego obrazka """

        # nowy, pusty, o odp. wymiarach
        image = pygame.Surface([width, height]).convert()

        # kopiujemy z dużego arkusza na mniejszy obrazek
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # czarny - przezroczysty
        image.set_colorkey(const.BLACK)

        return image
    
def Enemy_type(type_of_enemy):
    """
    Pobiera odpowiednie wizerunki wrogów, które potem są przekazywane do klasy Enemy lub Flying_Enemy.
    """
    walking_frames_r = []
    walking_frames_l = []
    sprite_sheet = SpriteSheet("spritesheet_enemies.png")
    if type_of_enemy == 0:
        image = sprite_sheet.get_image(6, 215, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(130 + 6, 13 * 130 + 86, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(6, 85, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(6, 215, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        image = pygame.transform.flip(image, True, False)
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(130 + 6, 13 * 130 + 86, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        image = pygame.transform.flip(image, True, False)
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(6, 85, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        image = pygame.transform.flip(image, True, False)
        walking_frames_l.append(image)
        
    if type_of_enemy == 1:
        image = sprite_sheet.get_image(6, 2 * 130 + 86, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(6, 4 * 130 + 86, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(6, 3 * 130 + 86, 116, 44)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(6, 2 * 130 + 86, 116, 44)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(6, 4 * 130 + 86, 116, 44)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(6, 3 * 130 + 86, 116, 44)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (87, 33))
        walking_frames_l.append(image)
        
    if type_of_enemy == 2:
        image = sprite_sheet.get_image(10, 1430 + 60, 108, 68)
        image = pygame.transform.scale(image, (81, 51))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(10, 1040 + 60, 108, 68)
        image = pygame.transform.scale(image, (81, 51))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(10, 1300 + 60, 108, 68)
        image = pygame.transform.scale(image, (81, 51))
        walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(10, 1430 + 60, 108, 68)
        image = pygame.transform.scale(image, (81, 51))
        image = pygame.transform.flip(image, True, False)
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(10, 1040 + 60, 108, 68)
        image = pygame.transform.scale(image, (81, 51))
        image = pygame.transform.flip(image, True, False)
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(10, 1300 + 60, 108, 68)
        image = pygame.transform.scale(image, (81, 51))
        image = pygame.transform.flip(image, True, False)
        walking_frames_l.append(image)

    if type_of_enemy == 3:
        image = sprite_sheet.get_image(390 + 3, 910 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(390 + 3, 650 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(390 + 3, 780 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(390 + 3, 910 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(390 + 3, 650 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(390 + 3, 780 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_l.append(image)
        
    if type_of_enemy == 4:
        image = sprite_sheet.get_image(260 + 3, 1300 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(260 + 3, 1170 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_r.append(image)
        image = sprite_sheet.get_image(260 + 3, 1040 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(260 + 3, 1300 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(260 + 3, 1170 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_l.append(image)
        image = sprite_sheet.get_image(260 + 3, 1040 + 10, 128 - 6, 128 - 20)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (61, 54))
        walking_frames_l.append(image)
    return walking_frames_r, walking_frames_l


    