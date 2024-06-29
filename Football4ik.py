import pygame
import pygame_menu
from pygame.locals import *
import random
import math

WIDTH = 800
HEIGHT = 400

PLAYER_WIDTH = 10
PLAYER_HEIGHT = 60

PLAYER_SPEED = 5

BALL_RADIUS = 6
BALL_SPEED_X = 6
BALL_SPEED_Y = 6

GRAVITY_STRENGTH = 0.1
GRAVITY_CHANGE_INTERVAL = 5000  

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Футбольчик')
icon = pygame.image.load("image/img1.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

hit_sound = pygame.mixer.Sound("hit_sound.mp3")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

font = pygame.font.Font(None, 36)
game_over_text = font.render("Ты продул, ты нуб!!!", True, (255, 255, 255))

player1_speed = 0
player2_speed = 0
player1_pos = [10, HEIGHT // 2 - PLAYER_HEIGHT // 2]
player2_pos = [WIDTH - 10 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2]
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_dir = [-1 if random.choice([True, False]) else 1, 1]
player1_score = 0
player2_score = 0
running_game = False
music_playing = True  

background_image = pygame.image.load("background.jpg")

def exit_game():
    pygame.mixer.music.stop()
    pygame.quit()
    quit()

def reset_game():
    global player1_speed, player2_speed, player1_pos, player2_pos
    global ball_pos, ball_dir, player1_score, player2_score

    player1_speed = 0
    player2_speed = 0

    player1_pos = [10, HEIGHT // 2 - PLAYER_HEIGHT // 2]
    player2_pos = [WIDTH - 10 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2]

    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_dir = [-1 if random.choice([True, False]) else 1, 1]

    player1_score = 0
    player2_score = 0

def start_the_game():
    global running_game, player1_speed, player2_speed, player1_pos, player2_pos
    global ball_pos, ball_dir, player1_score, player2_score

    reset_game()
    running_game = True
    main_menu.disable()
    while running_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                running_game = False
                exit_game()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                elif event.key == pygame.K_r and (player1_score == 10 or player2_score == 10):
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running_game = False
                    main_menu.enable()
               
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_speed = -PLAYER_SPEED
        elif keys[pygame.K_s]:
            player1_speed = PLAYER_SPEED
        else:
            player1_speed = 0

        if keys[pygame.K_UP]:
            player2_speed = -PLAYER_SPEED
        elif keys[pygame.K_DOWN]:
            player2_speed = PLAYER_SPEED
        else:
            player2_speed = 0

        player1_pos[1] += player1_speed
        player2_pos[1] += player2_speed

        if player1_pos[1] < 0:
            player1_pos[1] = 0
        elif player1_pos[1] > HEIGHT - PLAYER_HEIGHT:
            player1_pos[1] = HEIGHT - PLAYER_HEIGHT

        if player2_pos[1] < 0:
            player2_pos[1] = 0
        elif player2_pos[1] > HEIGHT - PLAYER_HEIGHT:
            player2_pos[1] = HEIGHT - PLAYER_HEIGHT

        ball_pos[0] += BALL_SPEED_X * ball_dir[0]
        ball_pos[1] += BALL_SPEED_Y * ball_dir[1]

        if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - BALL_RADIUS:
            ball_dir[1] = -ball_dir[1]
            hit_sound.play()

        if ball_pos[0] <= player1_pos[0] + PLAYER_WIDTH and \
                player1_pos[1] <= ball_pos[1] <= player1_pos[1] + PLAYER_HEIGHT:
            ball_dir[0] = 1
            hit_sound.play()

        elif ball_pos[0] >= player2_pos[0] - BALL_RADIUS and \
                player2_pos[1] <= ball_pos[1] <= player2_pos[1] + PLAYER_HEIGHT:
            ball_dir[0] = -1
            hit_sound.play()

        if ball_pos[0] < 0:
            player2_score += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_dir = [-1 if random.choice([True, False]) else 1, 1]

        elif ball_pos[0] > WIDTH - BALL_RADIUS:
            player1_score += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_dir = [-1 if random.choice([True, False]) else 1, 1]

        if player1_score == 10 or player2_score == 10:
            window.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 18))
            pygame.display.flip()
            pygame.time.delay(3000)

        
        window.blit(background_image, (0, 0))

        pygame.draw.rect(window, (255, 255, 255), (player1_pos[0], player1_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))
        pygame.draw.rect(window, (255, 255, 255), (player2_pos[0], player2_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))
        pygame.draw.circle(window, (255, 255, 255), (ball_pos[0], ball_pos[1]), BALL_RADIUS)
        pygame.draw.aaline(window, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        player1_score_text = font.render(str(player1_score), True, (2, 170, 255))
        player2_score_text = font.render(str(player2_score), True, (255, 0, 81))
        window.blit(player1_score_text, (WIDTH // 2 - 50, 10))
        window.blit(player2_score_text, (WIDTH // 2 + 40, 10))


        pygame.display.flip()
        clock.tick(55)

    pygame.mixer.music.stop()

def gravity_pong():
    global running_game

    
    player1_pos = [10, HEIGHT // 2 - PLAYER_HEIGHT // 2]
    player2_pos = [WIDTH - 10 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2]
    player1_speed = 0
    player2_speed = 0

    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

    gravity_point = [WIDTH // 2, HEIGHT // 2]
    last_gravity_change = pygame.time.get_ticks()

    player1_score = 0
    player2_score = 0

    while running_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                running_game = False
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_game = False
                    main_menu.enable()
                    pygame.mixer.music.unpause()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_speed = -PLAYER_SPEED
        elif keys[pygame.K_s]:
            player1_speed = PLAYER_SPEED
        else:
            player1_speed = 0

        if keys[pygame.K_UP]:
            player2_speed = -PLAYER_SPEED
        elif keys[pygame.K_DOWN]:
            player2_speed = PLAYER_SPEED
        else:
            player2_speed = 0

        player1_pos[1] += player1_speed
        player2_pos[1] += player2_speed

        if player1_pos[1] < 0:
            player1_pos[1] = 0
        elif player1_pos[1] > HEIGHT - PLAYER_HEIGHT:
            player1_pos[1] = HEIGHT - PLAYER_HEIGHT

        if player2_pos[1] < 0:
            player2_pos[1] = 0
        elif player2_pos[1] > HEIGHT - PLAYER_HEIGHT:
            player2_pos[1] = HEIGHT - PLAYER_HEIGHT

        
        current_time = pygame.time.get_ticks()
        if current_time - last_gravity_change > GRAVITY_CHANGE_INTERVAL:
            gravity_point = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
            last_gravity_change = current_time

        
        direction = [gravity_point[0] - ball_pos[0], gravity_point[1] - ball_pos[1]]
        distance = math.hypot(direction[0], direction[1])
        if distance != 0:  
            direction = [d / distance for d in direction]

            
            ball_speed[0] += direction[0] * GRAVITY_STRENGTH
            ball_speed[1] += direction[1] * GRAVITY_STRENGTH

        
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        
        if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - BALL_RADIUS:
            ball_speed[1] = -ball_speed[1]
            hit_sound.play()

        if ball_pos[0] <= player1_pos[0] + PLAYER_WIDTH and \
                player1_pos[1] <= ball_pos[1] <= player1_pos[1] + PLAYER_HEIGHT:
            ball_speed[0] = -ball_speed[0]
            hit_sound.play()

        elif ball_pos[0] >= player2_pos[0] - BALL_RADIUS and \
                player2_pos[1] <= ball_pos[1] <= player2_pos[1] + PLAYER_HEIGHT:
            ball_speed[0] = -ball_speed[0]
            hit_sound.play()

        
        if ball_pos[0] < 0:
            player2_score += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

        elif ball_pos[0] > WIDTH - BALL_RADIUS:
            player1_score += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

        if player1_score == 10 or player2_score == 10:
            window.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 18))
            pygame.display.flip()
            pygame.time.delay(3000)
            running_game = False
            main_menu.enable()

        
        window.blit(background_image, (0, 0))

        pygame.draw.rect(window, (255, 255, 255), (player1_pos[0], player1_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))
        pygame.draw.rect(window, (255, 255, 255), (player2_pos[0], player2_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))
        pygame.draw.circle(window, (255, 255, 255), (ball_pos[0], ball_pos[1]), BALL_RADIUS)
        pygame.draw.circle(window, (255, 0, 0), (gravity_point[0], gravity_point[1]), 5)

        
        player1_score_text = font.render(str(player1_score), True, (2, 170, 255))
        player2_score_text = font.render(str(player2_score), True, (255, 0, 81))
        window.blit(player1_score_text, (WIDTH // 2 - 50, 10))
        window.blit(player2_score_text, (WIDTH // 2 + 40, 10))


        pygame.display.flip()
        clock.tick(55)

def start_gravity_pong():
    global running_game
    running_game = True
    main_menu.disable()
    gravity_pong()

def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    music_playing = not music_playing

main_menu = pygame_menu.Menu('Футбольчик', 600, 400, theme=pygame_menu.themes.THEME_DARK)

main_menu.add.button('Играть', start_the_game)
main_menu.add.button("DLC", start_gravity_pong)
main_menu.add.button('Музыка', toggle_music)
main_menu.add.button('Выйти', pygame_menu.events.EXIT)

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit_game()

        if main_menu.is_enabled():
            main_menu.update(events)
            main_menu.draw(window)
            if music_playing:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()

        pygame.display.update()
