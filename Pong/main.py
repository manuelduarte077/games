import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurar la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Configurar la raqueta y la pelota
paddle_width = 10
paddle_height = 100
ball_size = 10

# Posiciones iniciales
paddle_x = 50
paddle_y = (screen_height // 2) - (paddle_height // 2)
ball_x = screen_width // 2
ball_y = screen_height // 2

# Velocidades iniciales
paddle_speed = 6
ball_speed_x = 4
ball_speed_y = 4

# Número de vidas
lives = 3

# Estado del juego
running = True
paused = False

# Fuente para mostrar el puntaje y las vidas
font = pygame.font.Font(None, 74)
menu_font = pygame.font.Font(None, 50)

def draw_menu():
    screen.fill(BLACK)
    menu_text = ["Pong Game Menu", "1. Continue", "2. Restart", "3. Quit"]
    for i, text in enumerate(menu_text):
        menu_surface = menu_font.render(text, True, WHITE)
        screen.blit(menu_surface, (screen_width // 4, screen_height // 4 + i * 60))
    pygame.display.flip()

def reset_game():
    global paddle_y, ball_x, ball_y, ball_speed_x, ball_speed_y, lives
    paddle_y = (screen_height // 2) - (paddle_height // 2)
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_speed_x = 4
    ball_speed_y = 4
    lives = 3

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            if paused:
                if event.key == pygame.K_1:
                    paused = False
                elif event.key == pygame.K_2:
                    reset_game()
                    paused = False
                elif event.key == pygame.K_3:
                    running = False

    if paused:
        draw_menu()
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_y > 0:
        paddle_y -= paddle_speed
    if keys[pygame.K_s] and paddle_y < screen_height - paddle_height:
        paddle_y += paddle_speed

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Colisión con la pared superior e inferior
    if ball_y <= 0 or ball_y >= screen_height - ball_size:
        ball_speed_y = -ball_speed_y

    # Colisión con la raqueta
    if paddle_x < ball_x < paddle_x + paddle_width and paddle_y < ball_y < paddle_y + paddle_height:
        ball_speed_x = -ball_speed_x

    # Puntuación y vidas
    if ball_x <= 0:
        lives -= 1
        ball_x, ball_y = screen_width // 2, screen_height // 2
    if ball_x >= screen_width - ball_size:
        ball_speed_x = -ball_speed_x

    if lives <= 0:
        paused = True

    # Dibujar todo
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))
    pygame.draw.aaline(screen, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height))

    text = font.render(f'Lives: {lives}', True, WHITE)
    screen.blit(text, (screen_width // 4, 20))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()