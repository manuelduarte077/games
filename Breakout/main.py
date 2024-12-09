import pygame

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

# Dimensiones de la plataforma
paddle_width = 100
paddle_height = 10
paddle_speed = 10

# Dimensiones de la pelota
ball_radius = 10
ball_speed = [5, -5]

# Crear la plataforma
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - paddle_height - 10, paddle_width, paddle_height)

# Crear la pelota
ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius, ball_radius)

# Crear bloques
block_width = 75
block_height = 20
blocks = []
for row in range(5):
    for col in range(10):
        block = pygame.Rect(col * (block_width + 10) + 35, row * (block_height + 10) + 50, block_width, block_height)
        blocks.append(block)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        running = False  # Fin del juego si la pelota toca el fondo

    # Colisiones con la plataforma
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # Colisiones con los bloques
    for block in blocks[:]:
        if ball.colliderect(block):
            ball_speed[1] = -ball_speed[1]
            blocks.remove(block)

    # Dibujar todo
    screen.fill(black)
    pygame.draw.rect(screen, blue, paddle)
    pygame.draw.ellipse(screen, white, ball)
    for block in blocks:
        pygame.draw.rect(screen, red, block)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()