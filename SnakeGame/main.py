import pygame
import random
import os

# Inicializar Pygame
pygame.init()

# Tamaño de la pantalla
screen_width = 800
screen_height = 600

# Crear la pantalla del juego
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Definir colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Configuración del reloj y velocidad de la serpiente
clock = pygame.time.Clock()
initial_snake_speed = 15

# Definir el tamaño de los bloques de la serpiente
snake_block = 10
font_style = pygame.font.SysFont(None, 50)

# Añadir variables de puntaje y nivel
score = 0
high_score = 0
level = 1
snake_speed = initial_snake_speed

# Función para mostrar el puntaje y nivel en la pantalla
def show_score(score, high_score, level):
    value = font_style.render("Score: " + str(score) + " High Score: " + str(high_score) + " Level: " + str(level), True, white)
    screen.blit(value, [0, 0])

# Función para dibujar la serpiente
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

# Función para mostrar mensajes en la pantalla
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

# Función para cargar el puntaje más alto desde un archivo
def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as f:
            return int(f.read())
    return 0

# Función para guardar el puntaje más alto en un archivo
def save_high_score(high_score):
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

# Cargar el puntaje más alto al iniciar el juego
high_score = load_high_score()

# Función principal del juego
def gameLoop():
    global score, high_score, level, snake_speed  # Añadir global para poder modificar las variables

    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    score = 0  # Reiniciar el puntaje al comenzar un nuevo juego
    level = 1  # Reiniciar el nivel al comenzar un nuevo juego
    snake_speed = initial_snake_speed  # Reiniciar la velocidad al comenzar un nuevo juego

    while not game_over:

        while game_close:
            screen.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(blue)
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        show_score(score, high_score, level)  # Mostrar el puntaje y el nivel
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 10  # Incrementar el puntaje cada vez que la serpiente come comida

            if score > high_score:
                high_score = score  # Actualizar el puntaje más alto si el puntaje actual es mayor

            # Incrementar el nivel y la velocidad cada 50 puntos
            if score % 50 == 0:
                level += 1
                snake_speed += 5

        clock.tick(snake_speed)

    save_high_score(high_score)  # Guardar el puntaje más alto al finalizar el juego
    pygame.quit()
    quit()

# Ejecutar el juego
gameLoop()