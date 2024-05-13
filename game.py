import pygame
from sys import exit
from random import randint

# initialization
pygame.init()
pygame.display.set_caption("Mario")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # variables
        self.player_gravity = 0
        self.player_index = 0
        self.moving = False
        self.direction = 'right'
        self.jump = False
        
        # fade variables
        self.alpha = 255  
        self.fade_speed = 3
        self.fade_out = False

        # right side
        self.mario = pygame.transform.scale2x(pygame.image.load('graphics/mario.png').convert_alpha())
        self.mario_jump = pygame.transform.scale2x(pygame.image.load('graphics/mario_jump.png').convert_alpha())
        self.mario_walk_0 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move0.png').convert_alpha())
        self.mario_walk_1 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move1.png').convert_alpha())
        self.mario_walk_2 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move2.png').convert_alpha())
        self.mario_death = pygame.transform.scale2x(pygame.image.load('graphics/mario_death.png').convert_alpha())
        self.mario_walk = [self.mario, self.mario_walk_0, self.mario_walk_1, self.mario_walk_2]
        
        # left side
        self.mario_walk_flip = []
        for i in range(len(self.mario_walk)):
            self.mario_walk_flip.append(pygame.transform.flip(self.mario_walk[i], True, False))
        self.mario_jump_flip = pygame.transform.flip(self.mario_jump, True, False)
          
        # image/rect   
        self.image = self.mario_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom = (30, 610))
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        
        # jump
        if keys[pygame.K_UP] and self.rect.bottom >= 610:
            self.player_gravity = -25 
        
        # left walking
        if keys[pygame.K_LEFT] and self.rect.left >= 0 :
            self.rect.x -= 5
            self.direction = 'left'
            self.walk_animation(self.direction)
            self.moving = True
        
        # right walking
        elif keys[pygame.K_RIGHT] and self.rect.right <= 1280:
            self.rect.x += 5
            self.direction = 'right'
            self.walk_animation(self.direction)
            self.moving = True
        else:
            self.moving = False
        
    def jump_animation(self):
        if self.rect.bottom < 610:
            self.jump = True
            if self.moving and self.direction == 'right':
                self.image = self.mario_jump
            elif self.moving and self.direction == 'left':
                self.image = self.mario_jump_flip
        else: self.jump = False
         
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
        
    def fade_out_animation(self):
        if self.fade_out:
            self.image = self.mario_death
            self.rect.y -= 5
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                global game_active
                game_active = False
        
    def collision(self):
        collision_sprites = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
        if collision_sprites:
            for sprite in collision_sprites:
                if self.jump == True and self.rect.bottom > sprite.rect.top:
                    sprite.fade_out = True
                    self.player_gravity = -20
                else:
                    self.fade_out = True
                    

    def update(self):
        self.player_input()
        self.jump_animation()
        self.apply_gravity()
        self.collision()
        self.fade_out_animation()
        
        # fade_out
        if self.alpha < 255:
            self.image.set_alpha(self.alpha)
        
        # jump fliping animation
        if not self.moving and self.rect.bottom >= 610:
            if self.direction == "left":
                self.image = self.mario_walk_flip[0]
            elif self.direction == "right":
                self.image = self.mario_walk[0]
           
           
class Goombas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # variables
        self.obstactle_index = 0
        
        # fade out variables
        self.alpha = 255  
        self.fade_speed = 10
        self.fade_out = False
        
        # images
        goombas_0 = pygame.image.load('graphics/goombas_0.png').convert_alpha()
        goombas_1 = pygame.image.load('graphics/goombas_1.png').convert_alpha()
        self.dead = pygame.image.load('graphics/goombas_dead.png').convert_alpha()
        self.frames = [goombas_0, goombas_1]
        
        # image/rect
        self.image = self.frames[self.obstactle_index]
        self.rect = self.image.get_rect(midbottom = (randint(1300, 1600), 610))
        
    def animation(self):
        self.obstactle_index += 0.1
        if self.obstactle_index > len(self.frames): self.obstactle_index = 0
        self.image = self.frames[int(self.obstactle_index)]
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            
    def fade_out_animation(self):
        if self.fade_out:
            self.image = self.dead
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                self.kill()
                     
    def update(self):
        self.animation()
        self.rect.x -= 2
        self.destroy()
        self.fade_out_animation()
        if self.alpha < 255:
            self.image.set_alpha(self.alpha)
            

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

# obstacle
obstacle_group = pygame.sprite.Group()

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 4000)

# player
player = pygame.sprite.GroupSingle()
player.add(Player())


# function to toggle fullscreen mode
def toggle_fullscreen():
    fullscreen = not screen.get_flags() & pygame.FULLSCREEN
    pygame.display.set_mode((800, 600), pygame.FULLSCREEN if fullscreen else 0)
    
# game reset function
def game_reset():
    obstacle_group.empty()
    player.sprite.rect.x = 30
    player.sprite.alpha = 255
    player.sprite.fade_out = False
    player.sprite.image = player.sprite.mario_walk[0]

while True:
    for event in pygame.event.get():
        # quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()   
        if game_active:
            # add obstacles
            if event.type == obstacle_timer:
                obstacle_group.add(Goombas())
        else:
            # restart the game with ENTER
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
                game_active = True
                start_time = pygame.time.get_ticks()
                game_reset()
                
                    
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
        
        # player
        player.draw(screen)
        player.update()
        
        # obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()
    
    else:
        screen.fill('#c84c0c')
        screen.blit(super_mario_bros_surf, super_mario_bros_rect)
        screen.blit(game_instruction_surf, game_instruction_rect)
        
    pygame.display.update()
    clock.tick(60)   