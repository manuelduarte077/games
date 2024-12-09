import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Configuración de la plataforma y la pelota
paddle_width = 100
paddle_height = 10
ball_radius = 10

# Variables del juego
paddle_speed = 10
ball_speed = [5, -5]
lives = 3
score = 0
difficulty = 1  # 1: Fácil, 2: Medio, 3: Difícil

# Crear la plataforma
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - paddle_height - 10, paddle_width, paddle_height)

# Crear la pelota
ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius, ball_radius)

# Crear bloques
block_width = 75
block_height = 20
blocks = []

def create_blocks():
    global blocks
    blocks = []
    for row in range(5):
        for col in range(10):
            block = pygame.Rect(col * (block_width + 10) + 35, row * (block_height + 10) + 50, block_width, block_height)
            blocks.append(block)

create_blocks()

# Sistema de puntaje y fuente
font = pygame.font.Font(None, 36)

# Estados del juego
menu = True
running = False
paused = False
game_over = False

def draw_menu():
    screen.fill(black)
    title_text = font.render("Breakout", True, white)
    start_text = font.render("Presiona '1' para Fácil, '2' para Medio, '3' para Difícil", True, white)
    quit_text = font.render("Presiona 'Q' para salir", True, white)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()

def draw_pause_menu():
    screen.fill(black)
    pause_text = font.render("Juego Pausado", True, white)
    resume_text = font.render("Presiona 'C' para continuar", True, white)
    reset_text = font.render("Presiona 'R' para resetear", True, white)
    quit_text = font.render("Presiona 'Q' para salir", True, white)
    screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 4))
    screen.blit(resume_text, (screen_width // 2 - resume_text.get_width() // 2, screen_height // 2))
    screen.blit(reset_text, (screen_width // 2 - reset_text.get_width() // 2, screen_height // 2 + 50))
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 100))
    pygame.display.flip()

def draw_game_over():
    screen.fill(black)
    game_over_text = font.render("Juego Terminado", True, white)
    score_text = font.render("Puntaje: " + str(score), True, white)
    reset_text = font.render("Presiona 'R' para resetear", True, white)
    quit_text = font.render("Presiona 'Q' para salir", True, white)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(reset_text, (screen_width // 2 - reset_text.get_width() // 2, screen_height // 2 + 50))
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 100))
    pygame.display.flip()

def reset_game():
    global paddle, ball, blocks, score, running, game_over, lives, ball_speed
    paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - paddle_height - 10, paddle_width, paddle_height)
    ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius, ball_radius)
    create_blocks()
    score = 0
    running = False
    game_over = False
    lives = 3
    ball_speed = [5 * difficulty, -5 * difficulty]

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                difficulty = 1
                reset_game()
                running = True
                menu = False
            if event.key == pygame.K_2:
                difficulty = 2
                reset_game()
                running = True
                menu = False
            if event.key == pygame.K_3:
                difficulty = 3
                reset_game()
                running = True
                menu = False
            if event.key == pygame.K_r:
                reset_game()
                menu = True
            if event.key == pygame.K_q:
                pygame.quit()
                exit()
            if event.key == pygame.K_c and paused:
                paused = False
                running = True
            if event.key == pygame.K_p and running:
                paused = True
                running = False

    if menu:
        draw_menu()
        continue

    if paused:
        draw_pause_menu()
        continue

    if running:
        # Mover la plataforma
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < screen_width:
            paddle.right += paddle_speed

        # Mover la pelota
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Colisiones con los bordes de la pantalla
        if ball.left <= 0 or ball.right >= screen_width:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        if ball.bottom >= screen_height:
            lives -= 1
            if lives > 0:
                ball.x, ball.y = screen_width // 2, screen_height // 2
                ball_speed[1] = -ball_speed[1]
            else:
                game_over = True
                running = False  # Fin del juego si la pelota toca el fondo

        # Colisiones con la plataforma
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        # Colisiones con los bloques
        for block in blocks[:]:
            if ball.colliderect(block):
                ball_speed[1] = -ball_speed[1]
                blocks.remove(block)
                score += 10

        # Dibujar todo
        screen.fill(black)
        pygame.draw.rect(screen, blue, paddle)
        pygame.draw.ellipse(screen, white, ball)
        for block in blocks:
            pygame.draw.rect(screen, red, block)

        # Dibujar el puntaje y vidas
        score_text = font.render("Puntaje: " + str(score), True, white)
        lives_text = font.render("Vidas: " + str(lives), True, white)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (screen_width - 120, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    if game_over:
        draw_game_over()