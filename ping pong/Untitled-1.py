import pygame
import random
import arabic_reshaper
from bidi.algorithm import get_display
pygame.display.init()
pygame.font.init()

HEIGHT = 500
WIDTH = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font_ar = pygame.font.Font('font.ttf', 60)
font_num = pygame.font.Font('font_num.ttf', 60)
font_start = pygame.font.Font(None, 36)

player_score, opponent_score = 0, 0
 
title_image = pygame.image.load("title.png")
title_image = pygame.transform.scale(title_image, (600, 100))
title_rect = title_image.get_rect()
title_rect.center = (WIDTH / 2, HEIGHT / 4)

def draw_dashed_line(surface, color, start_pos, end_pos, dash_length=10, gap_length=10, thickness=5):
    x_diff = end_pos[0] - start_pos[0]
    y_diff = end_pos[1] - start_pos[1]
    line_length = (x_diff ** 2 + y_diff ** 2) ** 0.5
    unit_x = x_diff / line_length
    unit_y = y_diff / line_length
    num_segments = int(line_length / (dash_length + gap_length))
    for i in range(num_segments):
        segment_start = (int(start_pos[0] + unit_x * (dash_length + gap_length) * i),
                         int(start_pos[1] + unit_y * (dash_length + gap_length) * i))
        segment_end = (int(start_pos[0] + unit_x * (dash_length + gap_length) * i + dash_length * unit_x),
                       int(start_pos[1] + unit_y * (dash_length + gap_length) * i + dash_length * unit_y))
        pygame.draw.line(surface, color, segment_start, segment_end, thickness)

def start_menu():
    classic_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 50, 200, 50)
    fog_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50)
    
    classic_text = font_start.render("Classic Mode", True, (255, 255, 255))
    fog_text = font_start.render("Fog Mode", True, (255, 255, 255))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if classic_button.collidepoint(mouse_pos):
                    return "classic"
                elif fog_button.collidepoint(mouse_pos):
                    return "fog"
        
        title_rect.y = HEIGHT / 4 + 5 * (int(pygame.time.get_ticks() / 100) % 5 - 15)

        screen.fill((0, 0, 0))
        screen.blit(title_image, title_rect)
        
        pygame.draw.rect(screen, (0, 255, 0), classic_button)
        pygame.draw.rect(screen, (0, 255, 0), fog_button)
        screen.blit(classic_text, (WIDTH / 2 - classic_text.get_width() / 2, HEIGHT / 2 - 35))
        screen.blit(fog_text, (WIDTH / 2 - fog_text.get_width() / 2, HEIGHT / 2 + 65))
        
        pygame.display.update()
        clock.tick(60)

selected_mode = start_menu()

player = pygame.Rect(0, 0, 10, 110)
player.center = (WIDTH - 30, HEIGHT / 2)

opp = pygame.Rect(0, 0, 10, 110)
opp.center = (30, HEIGHT / 2)

ball = pygame.Rect(0, 0, 20, 20)
ball.center = (WIDTH / 2 - 5, HEIGHT / 2)
x_speed, y_speed = 2.5, 2.5

fog_area = pygame.Rect(264.6, 0, 170.9, 500)

class Particle:
    def __init__(self):
        self.x = random.uniform(264.6, 435.5)
        self.y = random.uniform(0, 500)
        self.radius = random.randint(1, 3)
        self.color = (200, 200, 200)
        self.speed = random.uniform(0.1, 1)

    def move(self):
        self.x -= self.speed
        if self.x < 264.6:
            self.x = 435.5
            self.y = random.uniform(0, 500)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

particles = [Particle() for _ in range(100)]

def countdown():
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        countdown_text = font_ar.render(str(i), True, (255, 255, 255))
        if i == 3:
            screen.blit(countdown_text, (WIDTH / 2 - countdown_text.get_width() / 2, 50))
        elif i == 2:
            screen.blit(countdown_text, (WIDTH / 2 - countdown_text.get_width() / 2, HEIGHT / 2 - countdown_text.get_height() / 2))
        else:
            screen.blit(countdown_text, (WIDTH / 2 - countdown_text.get_width() / 2, HEIGHT - 50 - countdown_text.get_height()))
        pygame.display.update()
        pygame.time.wait(1000)

def spawn_ball():
    ball.center = (WIDTH / 2 - 5, HEIGHT / 2)
    x_speed, y_speed = 3.5, 3.5

while True:
    keys_pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if keys_pressed[pygame.K_UP]:
        if player.top > 0:
            player.top -= 7
    if keys_pressed[pygame.K_DOWN]:
        if player.bottom < HEIGHT:
            player.bottom += 7

    if keys_pressed[pygame.K_s]:
        if opp.top > 0:
            opp.top -= 7
    if keys_pressed[pygame.K_x]:
        if opp.bottom < HEIGHT:
            opp.bottom += 7

    ball.x += x_speed  # Update ball's x-coordinate
    ball.y += y_speed  # Update ball's y-coordinate

    if ball.y + 20 >= HEIGHT:
        y_speed = -3.5
    if ball.y <= 0:
        y_speed = 3.5
    if ball.x <= 0:
        opponent_score += 1
        spawn_ball()
        countdown()
    if ball.x >= WIDTH:
        player_score += 1
        spawn_ball()
        countdown()
    if player.x - ball.width <= ball.x <= player.right and ball.y in range(player.top - ball.width,
                                                                           player.bottom + ball.width):
        x_speed = -2.5
    if opp.x - ball.width <= ball.x <= opp.right and ball.y in range(opp.top - ball.width, opp.bottom + ball.width):
        x_speed = 2.5

    screen.fill((0, 0, 0))
    
    if selected_mode == "fog":
        pygame.draw.rect(screen, (100, 100, 100), fog_area)
        for particle in particles:
            particle.move()
            particle.draw(screen)
    
    if not (selected_mode == "fog" and fog_area.collidepoint(ball.center)):
        pygame.draw.circle(screen, "white", ball.center, 10)

    player_score_text = font_num.render(str(player_score), True, "white")
    opponent_score_text = font_num.render(str(opponent_score), True, "white")
    
    draw_dashed_line(screen, 'white', (345, 0), (345, 500), dash_length=10, gap_length=10, thickness=5)
    
    screen.blit(player_score_text, (290, 0))
    screen.blit(opponent_score_text, (368, 0))

    pygame.draw.rect(screen, "white", player)
    pygame.draw.rect(screen, "white", opp)

    pygame.display.update()
    clock.tick(60)
