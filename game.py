import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))

def toggle_fullscreen():
    fullscreen = not screen.get_flags() & pygame.FULLSCREEN
    pygame.display.set_mode((800, 600), pygame.FULLSCREEN if fullscreen else 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
     
    pygame.display.update()   