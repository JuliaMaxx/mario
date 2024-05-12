import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mario = pygame.transform.scale2x(pygame.image.load('graphics/mario.png').convert_alpha())
        self.mario_jump = pygame.transform.scale2x(pygame.image.load('graphics/mario_jump.png').convert_alpha())
        self.image = self.mario
        self.rect = self.image.get_rect(midbottom = (30, 610))
        self.player_gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 610:
            self.player_gravity = -25 
        
        if keys[pygame.K_LEFT] and self.rect.left >= 0 :
            self.rect.x -= 5
            
        if keys[pygame.K_RIGHT] and self.rect.right <= 1280:
            self.rect.x += 5
    
    def animation(self):
        if self.rect.bottom < 610:
            self.image = self.mario_jump
        else:
            self.image = self.mario
          
    def apply_gravity(self):
        self.player_gravity += 1
        self.rect.y += self.player_gravity
        if self.rect.bottom > 610: self.rect.bottom = 610
    
    def update(self):
        self.player_input()
        self.animation()
        self.apply_gravity()

# initialization
pygame.init()
pygame.display.set_caption("Mario")

# variables
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/emulogic.ttf', 30)
game_active = False

# inactive game surface
super_mario_bros_surf = pygame.image.load('graphics/super_mario_bros.png').convert_alpha()
super_mario_bros_rect = super_mario_bros_surf.get_rect(center = ( (640, 300)))
game_instruction_surf = font.render("Press ENTER to run", False, '#fcbcb0')
game_instruction_rect = game_instruction_surf.get_rect(center = (640, 440))

# background
sky_surf = pygame.image.load('graphics/sky.png').convert_alpha()
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()

# function to toggle fullscreen mode
def toggle_fullscreen():
    fullscreen = not screen.get_flags() & pygame.FULLSCREEN
    pygame.display.set_mode((800, 600), pygame.FULLSCREEN if fullscreen else 0)
    
# player
player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
    for event in pygame.event.get():
        # quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()   
                    
        # keydow
        if event.type == pygame.KEYDOWN:
            # quit the game on ESC
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                
            # toggle fullscreen on F11
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                
            # start the game
            if event.key == pygame.K_RETURN:
                game_active = True
                
    if game_active:                
        # background 
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 610))
        player.draw(screen)
        player.update()
    else:
        screen.fill('#c84c0c')
        screen.blit(super_mario_bros_surf, super_mario_bros_rect)
        screen.blit(game_instruction_surf, game_instruction_rect)
        
    pygame.display.update()
    clock.tick(60)   