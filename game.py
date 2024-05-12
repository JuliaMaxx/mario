import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_gravity = 0
        self.player_index = 0
        self.moving = False
        self.direction = 'right'
        
        # right side
        self.mario = pygame.transform.scale2x(pygame.image.load('graphics/mario.png').convert_alpha())
        self.mario_jump = pygame.transform.scale2x(pygame.image.load('graphics/mario_jump.png').convert_alpha())
        self.mario_walk_0 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move0.png').convert_alpha())
        self.mario_walk_1 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move1.png').convert_alpha())
        self.mario_walk_2 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move2.png').convert_alpha())
        self.mario_walk = [self.mario, self.mario_walk_0, self.mario_walk_1, self.mario_walk_2]
        
        # left side
        self.mario_walk_flip = []
        for i in range(len(self.mario_walk)):
            self.mario_walk_flip.append(pygame.transform.flip(self.mario_walk[i], True, False))
        self.mario_jump_flip = pygame.transform.flip(self.mario_jump, True, False)
             
        self.image = self.mario_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom = (30, 610))
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 610:
            self.player_gravity = -25 
        
        if keys[pygame.K_LEFT] and self.rect.left >= 0 :
            self.rect.x -= 5
            self.direction = 'left'
            self.walk_animation(self.direction)
            self.moving = True
            
        elif keys[pygame.K_RIGHT] and self.rect.right <= 1280:
            self.rect.x += 5
            self.direction = 'right'
            self.walk_animation(self.direction)
            self.moving = True
        else:
            self.moving = False
        
    def jump_animation(self):
        if self.rect.bottom < 610:
            if self.moving and self.direction == 'right':
                self.image = self.mario_jump
            elif self.moving and self.direction == 'left':
                self.image = self.mario_jump_flip
         
    def walk_animation(self, direction):
        self.player_index += 0.2
        if self.player_index >= len(self.mario_walk): self.player_index = 0
        
        if direction == 'left':
            self.image = self.mario_walk_flip[int(self.player_index)]
        else:
            self.image = self.mario_walk[int(self.player_index)]
                            
    def apply_gravity(self):
        self.player_gravity += 1
        self.rect.y += self.player_gravity
        if self.rect.bottom > 610: self.rect.bottom = 610
    
    def update(self):
        self.player_input()
        self.jump_animation()
        self.apply_gravity()
        if not self.moving and self.rect.bottom >= 610:
            if self.direction == "left":
                self.image = self.mario_walk_flip[0]
            elif self.direction == "right":
                self.image = self.mario_walk[0]

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