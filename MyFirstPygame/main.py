import pygame # pygame.init() to initialize the game
import sys  # sys.exit() to quit the game

# Initialize the game
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('My Game')


# Run the game loop
background_color = (0, 0, 0) # black

while True:
  for event in pygame.event.get(): # check for any events that are happening
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  screen.fill(background_color) # fill the screen with the background color

  pygame.display.flip() # update the display