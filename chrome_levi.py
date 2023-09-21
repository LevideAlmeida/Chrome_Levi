"""
Chrome Levi
"""
import os
from sys import exit
import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from random import randrange, randint, choice

def display_mensage(mensage, size, color, _font):
    font = pygame.font.SysFont(f'{_font}', size, False, False)
    text = f'{mensage}'
    formated_text = font.render(text, True, color)
    return formated_text

# File path
FILE_PATH = os.path.dirname(__file__)
IMAGES_PATH = os.path.join(FILE_PATH, 'Images')
SOUNDS_PATH = os.path.join(FILE_PATH, 'sounds')


# Defining constances
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

pygame.init()
pygame.mixer.init()

# Define sounds
collision_sound = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'roblox-death-sound-effect.mp3'))
collision_sound.set_volume(1)

score_sound = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'score_sound.wav'))
score_sound.set_volume(1)

# Variable containing collision status
collided = False

# Support variables for the Menu
in_selection_menu = True
menu_position = 0
selection_text = display_mensage('CHOOSE YOUR CHARACTER', 40, BLACK, '')
press_text = display_mensage('Press SPACE to select', 35, BLACK, '')

# Obstacule choice
obstacle_choice = choice([0,1])

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set game name
pygame.display.set_caption('Chrome Levi')

# Load sprite sheets
LEVI_SPRITE_SHEET = pygame.image.load(os.path.join(IMAGES_PATH, 'Levi_spritesheet.png')).convert_alpha()
DUDA_SPRITE_SHEET = pygame.image.load(os.path.join(IMAGES_PATH, 'dudinha_sprite_sheet.png')).convert_alpha()
LUZIA_SPRITE_SHEET = pygame.image.load(os.path.join(IMAGES_PATH, 'luzia_sprite_sheet.png')).convert_alpha()
ANNE_SPRITE_SHEET = pygame.image.load(os.path.join(IMAGES_PATH, 'anne_sprite_sheet.png')).convert_alpha()
VITORIA_SPRITE_SHEET = pygame.image.load(os.path.join(IMAGES_PATH, 'vitoria_sprite_sheet.png')).convert_alpha()
VK_SPRITE_SHEET = pygame.image.load(os.path.join(IMAGES_PATH, 'vk_sprite_sheet.png')).convert_alpha()
EMIMI_SPRITE_SHEET = pygame.image.load(os.path.join(IMAGES_PATH, 'emimi_sprite_sheet.png')).convert_alpha()

LEVI = LEVI_SPRITE_SHEET.subsurface((7, 0), (15,16))
LEVI = pygame.transform.scale(LEVI, (60,64))
DUDA = DUDA_SPRITE_SHEET.subsurface((21,6), (20,22))
DUDA = pygame.transform.scale(DUDA, (60, 66))
LUZIA = LUZIA_SPRITE_SHEET.subsurface((18,4), (23,21))
LUZIA = pygame.transform.scale(LUZIA, (69, 63))
ANNE = ANNE_SPRITE_SHEET.subsurface((15,0), (29,21))
ANNE = pygame.transform.scale(ANNE, (87, 63))
VITORIA = VITORIA_SPRITE_SHEET.subsurface((3,0),(23,12))
VITORIA = pygame.transform.scale(VITORIA, (100, 60))
VK = VK_SPRITE_SHEET.subsurface((21,7), (22,20))
VK = pygame.transform.scale(VK, (66, 60))
EMIMI = EMIMI_SPRITE_SHEET.subsurface((16, 0), (27,26))
EMIMI = pygame.transform.scale(EMIMI, (61, 58))

# Initializing score
score = 0



def reset_game():
    global score, obstacle_choice, fps, collided
    score = 0
    collided = False
    pterodactyl.rect.x = SCREEN_WIDTH
    cactus.rect.x = SCREEN_WIDTH
    player.rect.y = POSITION_Y
    player.is_jump = False
    obstacle_choice = choice([0,1])
    fps = 20

def selection_menu():
    global in_selection_menu, menu_position
    while in_selection_menu:
        screen.fill(WHITE)
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:

                if event.key == K_RIGHT:

                    if menu_position >= 6:
                        menu_position = 0
                    else:
                        menu_position += 1

                if event.key == K_LEFT:

                    if menu_position == 0:
                        menu_position = 6
                    else:
                        menu_position -= 1

                if event.key == K_SPACE:
                    in_selection_menu = False


        if menu_position == 0:
            pygame.draw.rect(screen, RED, (25,195, 70, 80), width=4)
        elif menu_position == 1:
            pygame.draw.rect(screen, RED, (95,195, 70, 80), width=4)
        elif menu_position == 2:
            pygame.draw.rect(screen, RED, (165,195, 80, 80), width=4)
        elif menu_position == 3:
            pygame.draw.rect(screen, RED, (250,195, 100, 80), width=4)
        elif menu_position == 4:
            pygame.draw.rect(screen, RED, (360,195, 100, 80), width=4)
        elif menu_position == 5:
            pygame.draw.rect(screen, RED, (465,195, 75, 80), width=4)
        elif menu_position == 6:
            pygame.draw.rect(screen, RED, (540,195, 80, 80), width=4)


        screen.blit(LEVI, (30,200))
        screen.blit(DUDA, (100,200))
        screen.blit(LUZIA, (170, 201))
        screen.blit(ANNE, (255, 201))
        screen.blit(VITORIA, (360, 201))
        screen.blit(VK, (470, 200))
        screen.blit(EMIMI, (550, 200))
        screen.blit(selection_text, (140, 40))
        screen.blit(press_text, (180, 380))

        pygame.display.flip()

    if menu_position == 0:
        menu_position = 0
        return 0
    elif menu_position == 1:
        menu_position = 0
        return 1
    elif menu_position == 2:
        menu_position = 0
        return 2
    elif menu_position == 3:
        menu_position = 0
        return 3
    elif menu_position == 4:
        menu_position = 0
        return 4
    elif menu_position == 5:
        menu_position = 0
        return 5
    elif menu_position == 6:
        menu_position = 0
        return 6


class Player(Sprite):
    def __init__(self, sprite_sheet, size, scale, position_y):
        super().__init__()
        self._sprites = []

        for i in range(4):
            sprite = sprite_sheet.subsurface((i * size,0), (size,size))
            sprite = pygame.transform.scale(sprite, (size*scale, size*scale))
            self._sprites.append(sprite)

        self.list_index = 0
        self.image = self._sprites[self.list_index]

        self.rect = self.image.get_rect()
        self.position_y = position_y
        self.rect.topleft = (70, self.position_y)

        self.is_jump = False
        self.is_down = False
        self.jump_speed = 10
        self.jump_sound = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'jump_sound.wav'))

        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        self.is_jump = True
        self.jump_sound.play()

    def down(self):
        self.is_down = True

    def update(self):
        if self.list_index > len(self._sprites) - 1:
            self.list_index = 0

        if self.is_jump:

            if self.rect.y <= POSITION_Y - 158:
                self.down()
                self.is_jump = False

            self.rect.y -= self.jump_speed

        if self.is_down == True:
            if self.rect.y == self.position_y:
                self.is_down = False
            else:
                self.rect.y += self.jump_speed


        if self.is_jump or self.is_down:
            self.image = self._sprites[1]
        else:
            self.list_index += 0.2
            self.image = self._sprites[int(self.list_index)]


class Clouds(Sprite):
    def __init__(self):
        super().__init__()
        self.image = LEVI_SPRITE_SHEET.subsurface((32*9, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 151, 50)
        self.rect.x = SCREEN_WIDTH - randrange(0,450,90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = randrange(50, 200, 50)

        self.rect.x -= 14


class Ground(Sprite):
    def __init__(self, position_x):
        super().__init__()

        if position_x == 0:
            self.image = LEVI_SPRITE_SHEET.subsurface((32*8,0), (32, 32))
        else:
            self.image = LEVI_SPRITE_SHEET.subsurface((32*7,0), (32, 32))

        self.image = pygame.transform.scale(self.image, (32*4, 32*4))
        self.rect = self.image.get_rect()
        self.rect.x = position_x * 128
        self.rect.y = SCREEN_HEIGHT - 32*4

    def update(self):
        self.rect.x -= 32
        if self.rect.x <= -128:
            self.rect.x = SCREEN_WIDTH


class Cactus(Sprite):
    def __init__(self):
        super().__init__()
        self.image = LEVI_SPRITE_SHEET.subsurface((32*6, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))

        self.rect = self.image.get_rect()
        self.rect.y = SCREEN_HEIGHT - 96
        self.rect.x = SCREEN_WIDTH + 60

        self.mask = pygame.mask.from_surface(self.image)
        self.choice = obstacle_choice

    def update(self):
        if self.choice == 1:

            if self.rect.topright[0] <= 0:
                self.rect.x = SCREEN_WIDTH + 60

            self.rect.x -= 32


class Pterodactyl(Sprite):
    def __init__(self):
        super().__init__()
        self._sprites = []
        for i in range(4,6):
            img = LEVI_SPRITE_SHEET.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self._sprites.append(img)

        self.list_index = 0
        self.image = self._sprites[self.list_index]

        self.rect = self.image.get_rect()
        self.rect.x = -96
        self.rect.y = SCREEN_HEIGHT - 150

        self.mask = pygame.mask.from_surface(self.image)

        self.choice = obstacle_choice
        self.rng = randint(0,1)


    def update(self):
        if self.choice == 0:

            if self.rect.topright[0] <= 0:
                self.rect.x = SCREEN_WIDTH + 60

            if self.rng == 0:
                self.rect.y = SCREEN_HEIGHT - 170
            else:
                self.rect.y = SCREEN_HEIGHT - 240


            self.list_index += 0.2

            if self.list_index >= 2:
                self.list_index = 0

            self.image = self._sprites[int(self.list_index)]

            self.rect.x -= 32


# Create sprites group
all_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()

# Create Ground instance
for i in range(6):
    ground = Ground(i)
    all_sprites.add(ground)

# Create cloud instaces
for i in range(4):
    cloud = Clouds()
    all_sprites.add(cloud)

sprite_sheet = selection_menu()

if sprite_sheet == 0:
    POSITION_Y = 368
    player = Player(LEVI_SPRITE_SHEET, 32, 2.5, POSITION_Y)
    all_sprites.add(player)
elif sprite_sheet == 1:
    POSITION_Y = 348
    player = Player(DUDA_SPRITE_SHEET, 64, 1.5, POSITION_Y)
    all_sprites.add(player)
elif sprite_sheet == 2:
    POSITION_Y = 354
    player = Player(LUZIA_SPRITE_SHEET, 64, 1.5, POSITION_Y)
    all_sprites.add(player)
elif sprite_sheet == 3:
    POSITION_Y = 344
    player = Player(ANNE_SPRITE_SHEET, 64, 1.6, POSITION_Y)
    all_sprites.add(player)
elif sprite_sheet == 4:
    POSITION_Y = 368
    player = Player(VITORIA_SPRITE_SHEET, 32, 2.5, POSITION_Y)
    all_sprites.add(player)
elif sprite_sheet == 5:
    POSITION_Y = 348
    player = Player(VK_SPRITE_SHEET, 64, 1.6, POSITION_Y)
    all_sprites.add(player)
elif sprite_sheet == 6:
    POSITION_Y = 358
    player = Player(EMIMI_SPRITE_SHEET, 64, 1.4, POSITION_Y)
    all_sprites.add(player)



# Create cactus instance
cactus = Cactus()
obstacles_group.add(cactus)
all_sprites.add(cactus)

# Create Pterodactyl instance
pterodactyl = Pterodactyl()
obstacles_group.add(pterodactyl)
all_sprites.add(pterodactyl)


clock = pygame.time.Clock()
fps = 20

while True:
    clock.tick(fps)


    screen.fill(WHITE)

    # Event LOOP🔄
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:

            if event.key == K_SPACE or event.key == K_UP and collided == False:
                if player.is_jump or player.is_down:
                    pass
                else:
                    player.jump()

            if event.key == K_r and collided == True:
                reset_game()

            if event.key == K_s and collided == True:
                all_sprites.remove(player)
                in_selection_menu = True
                sprite_sheet = selection_menu()
                if sprite_sheet == 0:
                    POSITION_Y = 368
                    player = Player(LEVI_SPRITE_SHEET, 32, 2.5, POSITION_Y)
                    all_sprites.add(player)
                elif sprite_sheet == 1:
                    POSITION_Y = 348
                    player = Player(DUDA_SPRITE_SHEET, 64, 1.5, POSITION_Y)
                    all_sprites.add(player)
                elif sprite_sheet == 2:
                    POSITION_Y = 354
                    player = Player(LUZIA_SPRITE_SHEET, 64, 1.5, POSITION_Y)
                    all_sprites.add(player)
                elif sprite_sheet == 3:
                    POSITION_Y = 344
                    player = Player(ANNE_SPRITE_SHEET, 64, 1.6, POSITION_Y)
                    all_sprites.add(player)
                elif sprite_sheet == 4:
                    POSITION_Y = 368
                    player = Player(VITORIA_SPRITE_SHEET, 32, 2.5, POSITION_Y)
                    all_sprites.add(player)
                elif sprite_sheet == 5:
                    POSITION_Y = 348
                    player = Player(VK_SPRITE_SHEET, 64, 1.6, POSITION_Y)
                    all_sprites.add(player)
                elif sprite_sheet == 6:
                    POSITION_Y = 358
                    player = Player(EMIMI_SPRITE_SHEET, 64, 1.4, POSITION_Y)
                    all_sprites.add(player)
                reset_game()


    # Colisions list
    collisions = pygame.sprite.spritecollide(player, obstacles_group, False, pygame.sprite.collide_mask)

    # Resetting obstacles position attributes
    if cactus.rect.topright[0] <= 0 or pterodactyl.rect.topright[0] <= 0:
        obstacle_choice = choice([0,1])
        cactus.rect.x = SCREEN_WIDTH
        pterodactyl.rect.x = SCREEN_WIDTH
        cactus.choice = obstacle_choice
        pterodactyl.choice = obstacle_choice
        pterodactyl.rng = randint(0,1)

    all_sprites.draw(screen)

    if collisions and collided == False:
        collision_sound.play()
        collided = True

    if collided == True:
        if score % 100 == 0:
            score += 1
        game_over_text = display_mensage('GAME OVER', 60, BLACK, '')
        screen.blit(game_over_text, (180,220))
        restart_text = display_mensage('Press R to restart', 35, BLACK, '')
        screen.blit(restart_text, (210,260))
        change_character_text = display_mensage('Press S to change character', 35, BLACK, '')
        screen.blit(change_character_text, (0, 0))

    else:
        score += 1
        all_sprites.update()
        player.update()
        score_text = display_mensage(f'{score}'.zfill(5), 40, BLACK, '')

    if (score % 100) == 0:
        score_sound.play()
        if fps >= 35:
            fps += 0
        else:
            fps += 1

    screen.blit(score_text, (550, 40))


    pygame.display.flip()
