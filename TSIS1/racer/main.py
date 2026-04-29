import pygame
import sys
import time
import random
from pygame.locals import *


import persistence as db
import ui
import racer


pygame.init() #create
pygame.mixer.init() #sound

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock() #Manage FPS

font_title = pygame.font.SysFont("Verdana", 40, bold=True) #Shrift для заголовков
font_ui = pygame.font.SysFont("Verdana", 18) #Shrift for coins and etc
game_over_font = pygame.font.SysFont("Verdana", 60) #Shrift for end game


C_BG = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)



background = pygame.image.load("AnimatedStreet.png")


settings = db.load_settings() #load from json file
username = "Player 1"

def play_sound(sound_file):
    if settings["sound"]: #Check sound is work or not?
        try: # Пробуем запустить звук (try защищает игру от вылета, если файла нет)
            pygame.mixer.Sound(sound_file).play() # load the song
        except:
            pass #just skip

def main_menu():
    global username
    btn_play = ui.Button(100, 200, 200, 50, "PLAY", (0, 150, 0), (0, 200, 0))
    btn_lead = ui.Button(100, 270, 200, 50, "LEADERBOARD", (0, 100, 200), (0, 150, 250))
    btn_sett = ui.Button(100, 340, 200, 50, "SETTINGS", (150, 150, 0), (200, 200, 0))
    btn_quit = ui.Button(100, 410, 200, 50, "QUIT", RED, (255, 50, 50))
    
    input_name = ui.TextInput(100, 130, 200, 40) #create some space to enter username
    input_name.text = username

    while True:
        DISPLAYSURF.fill(C_BG)
        title = font_title.render("RACER GAME", True, WHITE)
        DISPLAYSURF.blit(title, (title.get_rect(center=(200, 50))))
        
        lbl = font_ui.render("Enter Name:", True, WHITE)
        DISPLAYSURF.blit(lbl, (100, 105))
        
        input_name.draw(DISPLAYSURF)
        btn_play.draw(DISPLAYSURF)
        btn_lead.draw(DISPLAYSURF)
        btn_sett.draw(DISPLAYSURF)
        btn_quit.draw(DISPLAYSURF)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            input_name.handle_event(event)
            
            if btn_play.is_clicked(event):
                username = input_name.text if input_name.text else "Anonymous"
                game_loop() #Start the game
            if btn_lead.is_clicked(event):
                leaderboard_screen()
            if btn_sett.is_clicked(event):
                settings_screen()
            if btn_quit.is_clicked(event):
                pygame.quit()
                sys.exit()
                
        pygame.display.update()
        clock.tick(60) #limit fps to 60

def settings_screen():
    global settings
    while True:
        DISPLAYSURF.fill(C_BG)
        title = font_title.render("SETTINGS", True, WHITE) # Готовим заголовок
        DISPLAYSURF.blit(title, (title.get_rect(center=(200, 50)))) # Рисуем заголовок
        
        sound_text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        diff_text = f"Difficulty: {settings['difficulty']}"
        color_text = f"Car: {settings['car_color']}"
        
        btn_sound = ui.Button(100, 150, 200, 40, sound_text, (100, 100, 100), (150, 150, 150))
        btn_diff = ui.Button(100, 210, 200, 40, diff_text, (100, 100, 100), (150, 150, 150))
        btn_color = ui.Button(100, 270, 200, 40, color_text, (100, 100, 100), (150, 150, 150))
        btn_back = ui.Button(100, 450, 200, 50, "BACK", (0, 0, 150), (0, 0, 200))
        
        btn_sound.draw(DISPLAYSURF)
        btn_diff.draw(DISPLAYSURF)
        btn_color.draw(DISPLAYSURF)
        btn_back.draw(DISPLAYSURF) #draw button on the screen
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if btn_sound.is_clicked(event):
                settings["sound"] = not settings["sound"]
                db.save_settings(settings)
            if btn_diff.is_clicked(event):
                diffs = ["Easy", "Normal", "Hard"]
                settings["difficulty"] = diffs[(diffs.index(settings["difficulty"]) + 1) % 3]
                db.save_settings(settings)
            if btn_color.is_clicked(event):
                colors = ["Red", "Blue", "Green"]
                settings["car_color"] = colors[(colors.index(settings["car_color"]) + 1) % 3]
                db.save_settings(settings)
            if btn_back.is_clicked(event):
                return #quit of our function
                
        pygame.display.update() # update the screen
        clock.tick(60)

def leaderboard_screen():
    board = db.load_leaderboard()
    btn_back = ui.Button(100, 520, 200, 45, "BACK", (0, 0, 150), (0, 0, 200)) #create the BACK button
    
    font_board = pygame.font.SysFont("Verdana", 16) # Обычный шрифт для списка
    font_bold = pygame.font.SysFont("Verdana", 16, bold=True) # Жирный шрифт для заголовков таблицы
    
    while True:
        DISPLAYSURF.fill(C_BG)
        title = font_title.render("TOP 10", True, WHITE) # prepare the заголовок
        DISPLAYSURF.blit(title, (title.get_rect(center=(200, 40)))) #draw
        
        col_rank = 30
        col_name = 80
        col_score = 220
        col_dist = 300
        
        h_rank = font_bold.render("Rank", True, (255, 215, 0))
        h_name = font_bold.render("Name", True, (255, 215, 0))
        h_score = font_bold.render("Score", True, (255, 215, 0))
        h_dist = font_bold.render("Dist", True, (255, 215, 0))
        
        DISPLAYSURF.blit(h_rank, (col_rank, 90))
        DISPLAYSURF.blit(h_name, (col_name, 90))
        DISPLAYSURF.blit(h_score, (col_score, 90))
        DISPLAYSURF.blit(h_dist, (col_dist, 90))
        
        pygame.draw.line(DISPLAYSURF, (150, 150, 150), (30, 115), (370, 115), 1) # Рисуем декоративную линию под заголовками
        
        for i, entry in enumerate(board[:10]): #Top 10 
            y_pos = 130 + i * 32 # Считаем координату Y для каждой строчки
            disp_name = entry['name'][:12] # Обрезаем слишком длинные имена
            
            t_rank = font_board.render(f"{i+1}.", True, WHITE)
            t_name = font_board.render(disp_name, True, WHITE)
            t_score = font_board.render(str(entry['score']), True, WHITE)
            t_dist = font_board.render(f"{int(entry['distance'])}m", True, WHITE)
            
            DISPLAYSURF.blit(t_rank, (col_rank, y_pos))
            DISPLAYSURF.blit(t_name, (col_name, y_pos))
            DISPLAYSURF.blit(t_score, (col_score, y_pos))
            DISPLAYSURF.blit(t_dist, (col_dist, y_pos))
            
        btn_back.draw(DISPLAYSURF) #draw back button
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if btn_back.is_clicked(event):
                return
                
        pygame.display.update()
        clock.tick(60)

def game_loop(): #main and crucial part of my game
    diff = settings["difficulty"]
    color_of_car = settings["car_color"]
    
    if diff == "Easy":
        base_speed = 4
        target_enemies = 1
        target_hazards = 1
    elif diff == "Normal":
        base_speed = 5
        target_enemies = 2
        target_hazards = 2
    else:  
        base_speed = 7
        target_enemies = 3
        target_hazards = 3
        
    game_speed = base_speed
    score = 0
    COINS = 0
    distance = 0.0
    TOTAL_DISTANCE = 1000.0  
    active_powerup = None
    powerup_time = 0
    nitro_mult = 1.0
    
    player_speed_mult = 1.0 # Множитель скорости игрока 
    lane_hazard_mult = 1.0
    difficulty_scale = 1.0
    
    player = racer.Player(color_of_car)
    # Создаем группы спрайтов for comtable usage
    enemies = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    road_events = pygame.sprite.Group()
    
    all_sprites = pygame.sprite.Group() #main group
    all_sprites.add(player)
    
    for i in range(target_enemies):
        new_enemy = racer.Enemy(game_speed)
        new_enemy.rect.center = (random.randint(40, 360), -100 - (i * 250))
        enemies.add(new_enemy)
        all_sprites.add(new_enemy) # Добавляем в общую группу
    
    for i in range(3):
        c = racer.Coins()
        coins_group.add(c)
        all_sprites.add(c)
    
    INC_SPEED = pygame.USEREVENT + 1 #create the own event to manage the speed 
    pygame.time.set_timer(INC_SPEED, 2000) # complete this evernt every 2 seconds
    
    running = True
    while running:
        
        current_speed = game_speed * nitro_mult * lane_hazard_mult
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == INC_SPEED:
                game_speed += 0.2
                for spr in enemies:
                    spr.speed = game_speed
                
        player.move(player_speed_mult)
        # Логика генерации новых объектов
        if len(coins_group) < 3 and random.random() < (0.02 * difficulty_scale):
            c = racer.Coins()
            coins_group.add(c)
            all_sprites.add(c)
        if len(powerups) < 1 and not active_powerup and random.random() < (0.005 * difficulty_scale):
            p = racer.PowerUp()
            powerups.add(p)
            all_sprites.add(p)
            
        if len(road_events) < target_hazards and random.random() < (0.01 * difficulty_scale):
            ev_type = random.choice(["Oil", "NitroStrip"])
            ev = racer.RoadEvent(ev_type)
            road_events.add(ev)
            all_sprites.add(ev)
            
       
        for spr in enemies:
            if spr.move(current_speed): # Метод move возвращает True, если враг ушел за нижний край экрана
                score += 1
                if score % 5 == 0:
                    difficulty_scale += 0.2
            
        for c in coins_group: c.move(current_speed)
        for p in powerups: p.move(current_speed)
        for ev in road_events: ev.move(current_speed) #move this object on the down of our screen
        
        distance += current_speed / 60.0 # count our distance
        
        if distance >= TOTAL_DISTANCE:
            db.save_score(username, score, distance)
            game_over_screen(score, distance)
            return
        
        if active_powerup == "Nitro" and time.time() > powerup_time: #if nitro is end
            nitro_mult = 1.0 # go the start speed 
            active_powerup = None # End our nitro 
        elif active_powerup == "Shield" and not player.shielded: # if the shield is saving 
            active_powerup = None 
            
        player_speed_mult = 1.0
        lane_hazard_mult = 1.0
        
        collided_events = pygame.sprite.spritecollide(player, road_events, False) #if i take something on the road
        for ev in collided_events:
            if ev.type == "Oil":
                player_speed_mult = 0.5  # Manage the car is lower than before 
                lane_hazard_mult = 0.7  # speed is decrease
            elif ev.type == "NitroStrip":
                lane_hazard_mult = 1.5 # speed is increase
            
        collected_coins = pygame.sprite.spritecollide(player, coins_group, True) # True mean is delete the coin after taken
        for coin in collected_coins:
            play_sound("get_coin.wav")
            COINS += coin.value
            score += coin.value
            
        collided_p = pygame.sprite.spritecollide(player, powerups, True)
        for p in collided_p:
            if not active_powerup:
                active_powerup = p.type
                if p.type == "Nitro":
                    nitro_mult = 1.8
                    powerup_time = time.time() + 4.0
                elif p.type == "Shield":
                    player.shielded = True
                elif p.type == "Repair":
                    closest_enemy = None
                    min_dist = 9999
                    for e in enemies:
                        dist = ((player.rect.x - e.rect.x)**2 + (player.rect.y - e.rect.y)**2)**0.5
                        if dist < min_dist:
                            min_dist = dist
                            closest_enemy = e
                    if closest_enemy:
                        closest_enemy.reset()
                    active_powerup = None
                    
        collided_e = pygame.sprite.spritecollide(player, enemies, False)
        if collided_e:
            if player.shielded:
                player.shielded = False
                for hit_enemy in collided_e:
                    hit_enemy.reset()
            else:
                play_sound("crash.wav")
                db.save_score(username, score, distance)
                
                DISPLAYSURF.fill(RED)
                game_over_txt = game_over_font.render("Game Over", True, BLACK)
                DISPLAYSURF.blit(game_over_txt, (30, 250))
                pygame.display.update()
                time.sleep(2)
                
                game_over_screen(score, distance)
                return

        DISPLAYSURF.blit(background, (0, 0))
        
        for entity in all_sprites: # draw all objects 
            DISPLAYSURF.blit(entity.image, entity.rect)
        # draw interface
        scores_txt = font_ui.render(f"Score: {score}", True, BLACK)
        DISPLAYSURF.blit(scores_txt, (10, 10))
        amount_coins = font_ui.render(f"Coins: {COINS}", True, BLACK)
        DISPLAYSURF.blit(amount_coins, (290, 10))
        
        dist_txt = font_ui.render(f"Dist: {int(distance)}m / {int(TOTAL_DISTANCE)}m", True, BLACK)
        DISPLAYSURF.blit(dist_txt, (10, 30))
        
        if active_powerup:
            p_text = f"{active_powerup} active!"
            if active_powerup == "Nitro":
                p_text += f" ({int(powerup_time - time.time())}s)"
            hud_pow = font_ui.render(p_text, True, (0, 0, 255))
            DISPLAYSURF.blit(hud_pow, (10, 50))
            
        pygame.display.update()
        clock.tick(60)

def game_over_screen(score, distance):
    btn_retry = ui.Button(100, 300, 200, 50, "RETRY", (0, 150, 0), (0, 200, 0))
    btn_menu = ui.Button(100, 370, 200, 50, "MAIN MENU", (150, 150, 0), (200, 200, 0))
    
    while True:
        DISPLAYSURF.fill(C_BG)
        title = font_title.render("RESULTS", True, RED)
        DISPLAYSURF.blit(title, (title.get_rect(center=(200, 100))))
        
        s_text = font_ui.render(f"Final Score: {score}", True, WHITE)
        d_text = font_ui.render(f"Total Distance: {int(distance)}m", True, WHITE)
        
        DISPLAYSURF.blit(s_text, (s_text.get_rect(center=(200, 180))))
        DISPLAYSURF.blit(d_text, (d_text.get_rect(center=(200, 210))))
        
        btn_retry.draw(DISPLAYSURF)
        btn_menu.draw(DISPLAYSURF)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if btn_retry.is_clicked(event):
                game_loop()
                return
            if btn_menu.is_clicked(event):
                return
                
        pygame.display.update()
        clock.tick(60)

main_menu()