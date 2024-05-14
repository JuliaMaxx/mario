import pygame
from sys import exit
from random import randint, choice

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
        
        # jump sound
        self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        self.jump_sound.set_volume(0.5)
        
        # score sound
        self.score_sound = pygame.mixer.Sound('sounds/scorering.wav')
        self.score_sound.set_volume(0.5)
        
        # death sound
        self.death_sound = pygame.mixer.Sound('sounds/death.wav')
        self.death_sound.set_volume(0.5)
        
        # right side images
        self.mario = pygame.transform.scale2x(pygame.image.load('graphics/mario.png').convert_alpha())
        self.mario_jump = pygame.transform.scale2x(pygame.image.load('graphics/mario_jump.png').convert_alpha())
        self.mario_walk_0 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move0.png').convert_alpha())
        self.mario_walk_1 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move1.png').convert_alpha())
        self.mario_walk_2 = pygame.transform.scale2x(pygame.image.load('graphics/mario_move2.png').convert_alpha())
        self.mario_death = pygame.transform.scale2x(pygame.image.load('graphics/mario_death.png').convert_alpha())
        self.mario_walk = [self.mario, self.mario_walk_0, self.mario_walk_1, self.mario_walk_2]
        
        # left side images
        self.mario_walk_flip = []
        for i in range(len(self.mario_walk)):
            self.mario_walk_flip.append(pygame.transform.flip(self.mario_walk[i], True, False))
        self.mario_jump_flip = pygame.transform.flip(self.mario_jump, True, False)
          
        # image/rect   
        self.image = self.mario_walk[int(self.player_index)]
        self.rect = self.image.get_rect(midbottom = (640, 610))
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        
        # jump
        if keys[pygame.K_UP] and self.rect.bottom >= 610:
            self.player_gravity = -25
            self.jump_sound.play() 
        
        # left walking
        if keys[pygame.K_LEFT] and self.rect.left >= 0 and not self.fade_out:
            self.rect.x -= 5
            self.direction = 'left'
            self.walk_animation(self.direction)
            self.moving = True
        
        # right walking
        elif keys[pygame.K_RIGHT] and self.rect.right <= 1280 and not self.fade_out:
            self.rect.x += 5
            self.direction = 'right'
            self.walk_animation(self.direction)
            self.moving = True
        else:
            self.moving = False
        
    def jump_animation(self):
        if self.rect.bottom < 610:
            self.jump = True
            if self.direction == 'right':
                self.image = self.mario_jump
            elif self.direction == 'left':
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
                global score
                # kill the enemy
                if self.jump == True and self.rect.bottom > sprite.rect.top and not self.fade_out:
                    self.player_gravity = -20
                    sprite.fade_out = True
                    self.score_sound.play()
                    score += 1
                    
                # player dies
                elif not self.fade_out:
                    self.fade_out = True
                    global bg_music
                    bg_music.stop()
                    self.death_sound.play()
                    self.player_gravity = -20
                                      
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


class Obstacle(pygame.sprite.Sprite):
    # dummy code
    obstacle_count = 0
    
    def __init__(self, name, x, direction):
        super().__init__()  
          
        # dummy code
        Obstacle.obstacle_count += 1
                    
        # variables
        self.direction = direction
        self.obstactle_index = 0
        self.name = name
        
        # fade out variables
        self.alpha = 255  
        self.fade_speed = 10
        self.fade_out = False
        
        # images
        self.frame_0 = pygame.image.load(f'graphics/{name}_0.png').convert_alpha()
        self.frame_1 = pygame.image.load(f'graphics/{name}_1.png').convert_alpha()
        self.dead = pygame.image.load(f'graphics/{name}_dead.png').convert_alpha()
        self.frames = [self.frame_0, self.frame_1]
        
        # flipped
        self.frames_flip = []
        for i in range(len(self.frames)):
            self.frames_flip.append(pygame.transform.flip(self.frames[i], True, False))
        
        # image
        if self.name == 'koopa' and self.direction == 'right':
            self.image = self.frames_flip[int(self.obstactle_index)]
        else:
            self.image = self.frames[self.obstactle_index]
         
        # spawn enemies from the right and left
        if self.direction == 'left':
            self.rect = self.image.get_rect(midbottom = (x, 610))
        else:
            self.rect = self.image.get_rect(midbottom = (-x + 1000, 610))
             
    def animation(self):
        self.obstactle_index += 0.1
        if self.obstactle_index > len(self.frames): self.obstactle_index = 0
        if self.name == 'koopa' and self.direction == 'right':
            self.image = self.frames_flip[int(self.obstactle_index)]  
        else: self.image = self.frames[int(self.obstactle_index)]  
    
    def destroy(self):
        # remove enemies if they are out of the screen
        if self.direction == 'left':
            if self.rect.x <= -100:
                self.kill()  
        else:
            if self.rect.x >= 1300:
                self.kill()   
    
    def fade_out_animation(self):
        if self.fade_out:
            self.image = self.dead
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                self.kill() 
    
    def update(self):
        self.animation()
        # move enemies to the screen either from the left or right
        if self.direction == 'left':
            self.rect.x -= 2
        else: self.rect.x += 2
        self.destroy()
        self.fade_out_animation()
        if self.alpha < 255:
            self.image.set_alpha(self.alpha)
                    
    # dummy code  
    @classmethod
    def description(self):
        return f"This is obstacle class with {Obstacle.obstacle_count} obstacles defined."
    def __str__(self):
        return f"Obstacle with the name {self.name} which is moving to the {self.direction}"
   
           
class Goombas(Obstacle):
    def __init__(self, direction):
        super().__init__('goombas', randint(1250, 1400), direction)
        
        
class Koopa(Obstacle):
    def __init__(self, direction):
        super().__init__('koopa', randint(1400, 1650), direction)


# variables
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/emulogic.ttf', 30)
font_1 = pygame.font.Font('fonts/emulogic.ttf', 70)
game_active = False
score = 0
first_game = True

# background music
bg_music = pygame.mixer.Sound('sounds/overworld.wav')
bg_music.set_volume(0.5)
chanel= bg_music.play(loops = -1)

# inactive game surface
super_mario_bros_surf = pygame.image.load('graphics/super_mario_bros.png').convert_alpha()
super_mario_bros_rect = super_mario_bros_surf.get_rect(center = ( (640, 300)))
game_over_surf = font_1.render('GAME OVER', False, 'Black').convert_alpha()
game_over_rect = game_over_surf.get_rect(center = ((640, 330)))
game_instruction_surf = font.render("Press ENTER to run", False, '#fcbcb0')
game_instruction_rect = game_instruction_surf.get_rect(center = (640, 440))

# background
sky_surf = pygame.image.load('graphics/sky.png').convert_alpha()
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()

# obstacle
obstacle_group = pygame.sprite.Group()

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

# player
player = pygame.sprite.GroupSingle()
player.add(Player())

# function to toggle fullscreen mode
def toggle_fullscreen():
    fullscreen = not screen.get_flags() & pygame.FULLSCREEN
    pygame.display.set_mode((800, 600), pygame.FULLSCREEN if fullscreen else 0)
    
# game reset function
def game_reset():
    global score, chanel
    obstacle_group.empty()
    player.sprite.rect.x = 640
    player.sprite.alpha = 255
    player.sprite.fade_out = False
    player.sprite.image = player.sprite.mario_walk[0]
    score = 0
    if not chanel.get_busy():
        chanel = bg_music.play()    

while True:
    for event in pygame.event.get():
        # quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
               
        if game_active:
            # add obstacles
            if event.type == obstacle_timer:
                obstacle_group.add(choice([Goombas('left'), Koopa('left'), Goombas('left'), Goombas('right'), Koopa('right'), Goombas('right')]))
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
    
        first_game = False
    else:
        screen.fill('#c84c0c')
        screen.blit(game_instruction_surf, game_instruction_rect)
        if first_game:
            screen.blit(super_mario_bros_surf, super_mario_bros_rect)
        else:
            screen.blit(game_over_surf, game_over_rect)
                
    if not first_game:
        # display score
        score_surf = font.render(f"Score: {score}", False, 'Black')
        score_rect = score_surf.get_rect(center = (640, 50))
        screen.blit(score_surf, score_rect)
        
    pygame.display.update()
    clock.tick(60)   
    