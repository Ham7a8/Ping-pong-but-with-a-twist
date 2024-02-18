import pygame
import sys
import random

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # player score    
    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()

    # opponent score    
    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0: 
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    if not is_2_player_mode:
        if opponent.top < ball.y:
            opponent.y += opponent_speed
        if opponent.bottom > ball.y:
            opponent.y -= opponent_speed

        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= screen_height:
            opponent.bottom = screen_height
    else:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_s]:
            if opponent.top > 0:
                opponent.top -= 7
        if keys_pressed[pygame.K_x]:
            if opponent.bottom < screen_height:
                opponent.bottom += 7

def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2-5, screen_height/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, white)
        screen.blit(number_three, (screen_width/2 , screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_number = game_font.render("2", False, white)
        screen.blit(number_number, (screen_width/2, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, white)
        screen.blit(number_one, (screen_width/2 , screen_height/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


def draw_dashed_line(surface, color, start_pos, end_pos, dash_length=10, gap_length=10, thickness=5):
    # Calculate the vector between start and end points
    x_diff = end_pos[0] - start_pos[0]
    y_diff = end_pos[1] - start_pos[1]
    # Calculate the length of the line
    line_length = (x_diff ** 2 + y_diff ** 2) ** 0.5
    # Calculate the unit vector components
    unit_x = x_diff / line_length
    unit_y = y_diff / line_length
    # Calculate the number of segments
    num_segments = int(line_length / (dash_length + gap_length))
    # Draw each segment
    for i in range(num_segments):
        # Calculate the start and end points of the segment
        segment_start = (int(start_pos[0] + unit_x * (dash_length + gap_length) * i),
                         int(start_pos[1] + unit_y * (dash_length + gap_length) * i))
        segment_end = (int(start_pos[0] + unit_x * (dash_length + gap_length) * i + dash_length * unit_x),
                       int(start_pos[1] + unit_y * (dash_length + gap_length) * i + dash_length * unit_y))
        # Draw the segment
        pygame.draw.line(surface, color, segment_start, segment_end, thickness)


def start_menu():
    title_font = pygame.font.Font(None, 50)
    menu_font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if one_player_button.collidepoint(mouse_pos):
                    return False
                elif two_player_button.collidepoint(mouse_pos):
                    return True

        screen.fill((0, 0, 0))
        title_text = title_font.render("Ping Pong", True, (255, 255, 255))
        one_player_text = menu_font.render("1 Player", True, (255, 255, 255))
        two_player_text = menu_font.render("2 Players", True, (255, 255, 255))

        title_rect = title_text.get_rect(center=(screen_width/2, 100))
        one_player_button = pygame.Rect(screen_width/2 - 100, 200, 200, 50)
        two_player_button = pygame.Rect(screen_width/2 - 100, 300, 200, 50)

        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, (0, 255, 0), one_player_button)
        pygame.draw.rect(screen, (0, 255, 0), two_player_button)
        screen.blit(one_player_text, (screen_width/2 - one_player_text.get_width()/2, 215))
        screen.blit(two_player_text, (screen_width/2 - two_player_text.get_width()/2, 315))

        pygame.display.flip()
        clock.tick(60)

# normal game set up
pygame.mixer.pre_init()
pygame.init()
clock = pygame.time.Clock()

# to set the screen size of the main window
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Rectangles for the game
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color(0, 0, 0)
ball_color = (255, 255, 255)
line_color = (132, 132, 130)
player_color = (255, 179, 179)
opponent_color = (153, 204, 255)
white = (255, 255, 255)

# game variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# score timer
score_time = True

# text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 32)
score_font = pygame.font.Font('font_num.ttf', 65)

is_2_player_mode = start_menu()

# condition for the game to run
while True:
    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
            
            if event.key == pygame.K_ESCAPE:  # Check for Escape key press
                is_2_player_mode = start_menu()  # Return to start menu
                player_score = 0  # Reset scores
                opponent_score = 0
                ball_speed_x = 7 * random.choice((1, -1))  # Reset ball speed
                ball_speed_y = 7 * random.choice((1, -1))
                player_speed = 0  # Reset player speed
                opponent_speed = 7  # Reset opponent speed
                score_time = True 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7



    ball_animation()
    player_animation()
    opponent_animation()
    
    #game visuals
    screen.fill(bg_color)
    draw_dashed_line(screen, 'grey', (345, 0), (345, 500), dash_length=10, gap_length=10, thickness=5)
    pygame.draw.rect(screen, player_color, player)
    pygame.draw.rect(screen, opponent_color, opponent)

    # Instead of drawing a sharp ellipse, we'll create a smoother surface for the ball
    smooth_ball_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(smooth_ball_surface, ball_color, (15, 15), 15)

    # Then, blit this smoother surface onto the main screen
    screen.blit(smooth_ball_surface, ball)

    #pygame.draw.aaline(screen, line_color, (screen_width/2,0), (screen_width/2, screen_height))



    if score_time:
        ball_start()

    player_text = score_font.render(f"{player_score}", False, white)
    screen.blit(player_text, (365, 10))

    opponent_text = score_font.render(f"{opponent_score}", False, white)
    screen.blit(opponent_text, (290, 10))

    #updating the game window
    pygame.display.flip()
    clock.tick(75)
