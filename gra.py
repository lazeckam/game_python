import pygame
import os
import constants as const

from player import Player
from levels import Level, Level_01, Level_02, Level_03
from timer import Timer
 
def main():
    """ Główny program """
    pygame.init()
 
    size = [const.SCREEN_WIDTH, const.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_visible(False)
 
    font = pygame.font.SysFont("verdana", 30, True, False)
    font2 = pygame.font.SysFont("verdana", 15, True, False)
    click = pygame.mixer.Sound("click.wav")
    
    pygame.display.set_caption("Ekstra Marian Jedynak")
    timer = Timer()
    
    done = False
    clock = pygame.time.Clock()
    game_started = False
    game_over = False
    
    high_score_txt = open("high_score.txt", "r")
    high_score_odczytane = list(map(int, high_score_txt.readlines()))
    high_score_txt.close()
    
    high_score = high_score_odczytane[0]
    
    menu_bar = [[250, 300, 300, 40],
               [250, 350, 300, 40],
               [250, 400, 300, 40],
               [250, 450, 300, 40]]
    names_bar = ["START GRY",
                "LICZBA ŻYĆ",
                "POZIOM",
                "KONIEC"]
    index_menu_bar = 0
    life = 3
    poziom = 0
    while not game_started and not done:
        screen.fill(const.WHITE)
        screen.blit(pygame.image.load("background_menu.png").convert(), [0,0,800,600])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    index_menu_bar += 1
                    index_menu_bar = index_menu_bar % len(menu_bar)
                    click.play()
                if event.key == pygame.K_UP:
                    index_menu_bar -= 1
                    index_menu_bar = index_menu_bar % len(menu_bar)
                    click.play()
                if index_menu_bar == 1:
                    if event.key == pygame.K_LEFT:
                        if life > 1:
                            click.play()
                            life -= 1
                    elif event.key == pygame.K_RIGHT:
                        if life < 5:
                            life += 1
                            click.play()
                if index_menu_bar == 0:
                    if event.key == pygame.K_SPACE:
                        game_started = True
                if index_menu_bar == 2:
                    if event.key == pygame.K_LEFT:
                        if poziom > 0:
                            poziom -= 1
                            click.play()
                    elif event.key == pygame.K_RIGHT:
                        if poziom < 2:
                            poziom += 1
                            click.play()
                if index_menu_bar == 3:
                    if event.key == pygame.K_SPACE:
                        done = True
                       
        for i in menu_bar:    
            pygame.draw.rect(screen, const.CIEMNYBEZOWY, i, 0)
        for i in range(len(names_bar)):  
            wspolrzedne = menu_bar[i]
            screen.blit(font.render(names_bar[i], True, const.JASNYBEZOWY), [wspolrzedne[0] + 7, wspolrzedne[1] + 4])
        pygame.draw.rect(screen, const.JASNYBEZOWY, menu_bar[index_menu_bar], 5)
        
        pygame.draw.rect(screen, const.JASNYBEZOWY, [555, 350, 40, 40], 0)
        screen.blit(font.render(str(life), True, const.CIEMNYBEZOWY), [570, 350 + 4])
        pygame.draw.rect(screen, const.JASNYBEZOWY, [555, 400, 40, 40], 0)
        screen.blit(font.render(str(poziom + 1), True, const.CIEMNYBEZOWY), [570, 400 + 4])
        screen.blit(font2.render("Spacja potwierdza wybór START/KONIEC. Sterowanie kosmitą za pomocą strzałek.", True, const.CIEMNYBEZOWY), [34, 580])
        pygame.display.flip()
        
    player = Player()
 
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
 
    current_level_no = poziom
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    collide_enemy = current_level.enemy_list
    player.level = current_level
    player.life = life
    player.rect.x = 340
    player.rect.y = const.SCREEN_HEIGHT - player.rect.height - 200
    player.collected_coins = 0
    
    active_sprite_list.add(player)
        
    while (not done and game_started) and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
  
        current_level.update()
        active_sprite_list.update()
 
        # Gracz idzie w prawo
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # Gracz idzie w lewo
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
 
        # Gracz przechodzi poziom
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 320
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                game_over = True
 
        # RYSOWANIE PONIŻEJ
        current_level.draw(screen)
        active_sprite_list.draw(screen)
             
        # górny panel wyświetaljący się w trakcie gry
        pygame.draw.rect(screen, const.CIEMNYBEZOWY, [5, 5, const.SCREEN_WIDTH - 10, 50])
        serce = pygame.transform.scale(pygame.image.load("life.png").convert(),[40, 40])
        timer.update(screen, font, 10, 12)  
        for i in range(player.life):
            screen.blit(serce, [100 + i*50 + 20,10,40,40])
        moneta = pygame.transform.scale(pygame.image.load("coinGold.png").convert(),[50, 50])  
        moneta.set_colorkey(const.BLACK)
        screen.blit(moneta, [400, 5, 50, 50])
        screen.blit(font.render(str(player.collected_coins), True, const.JASNYBEZOWY), [450, 12])
        klucz = pygame.transform.scale(pygame.image.load("keyYellow.png").convert(),[50, 50])
        klucz.set_colorkey(const.BLACK)
        screen.blit(klucz, [500, 5, 50, 50])
        screen.blit(font.render(str(player.collected_keys), True, const.JASNYBEZOWY), [550, 12])
        screen.blit(font.render("LEVEL: " + str(current_level_no + 1), True, const.JASNYBEZOWY), [600, 12])
        
        # Przegrywanie
        if player.rect.y >= const.SCREEN_HEIGHT + 10:
            game_over = True    
        if player.life <= 0:
            game_over = True
            
        pygame.display.flip()

    while (game_over and not done) and game_started:
        screen.blit(pygame.image.load("background_menu.png").convert(), [0,0,800,600])
        pobity_rekord = False

        screen.blit(font.render("Twój wynik to: " + str(player.collected_coins), True, const.CIEMNYBEZOWY), [30, 360])
        if player.collected_coins > high_score:
            pobity_rekord = True
            high_score_file = open("high_score.txt", "w")
            high_score_file.write(str(player.collected_coins))
            high_score_file.close()
        if pobity_rekord:
            screen.blit(font.render("Gratulacje! Pobiłeś rekord!", True, const.CIEMNYBEZOWY), [30, 280])
                
        screen.blit(font.render("Najlepszy wynik to: " + str(max(player.collected_coins, high_score)), True, const.CIEMNYBEZOWY), [30, 440])
        screen.blit(font.render("Aby zagrać jeszcze raz kliknij Spację.", True, const.CIEMNYBEZOWY), [30, 520])
 
        # koniec RYSOWANIA
    
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    main()
        
    clock.tick(60)
    
    pygame.display.quit()
    pygame.quit()
    
if __name__ == "__main__":
    main()