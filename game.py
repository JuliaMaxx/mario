import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Function to toggle fullscreen mode
def toggle_fullscreen():
    screen = pygame.display.get_surface()
    fullscreen = not screen.get_flags() & pygame.FULLSCREEN
    pygame.display.set_mode((800, 600), pygame.FULLSCREEN if fullscreen else 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
     
    pygame.display.update()   