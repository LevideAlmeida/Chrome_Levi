import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from sys import exit
import os


pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FILE_PATH = os.path.dirname(__file__)
IMAGES_PATH = os.path.join(FILE_PATH, 'Images')
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

position = 0
selection_font = pygame.font.SysFont('', 40, False, False)
selection_text = selection_font.render('CHOOSE YOUR CHARACTER', True, BLACK)

class Player(Sprite):
    def __init__(self, sprite_sheet, size, scale):
        super().__init__()
        self._sprites = []

        for i in range(4):
            sprite = sprite_sheet.subsurface((i * size,0), (size, size))
            sprite = pygame.transform.scale(sprite, (size*scale, size*scale))
            self._sprites.append(sprite)

        self.list_index = 0
        self.image = self._sprites[self.list_index]

        self.rect = self.image.get_rect()
        self.position_y = SCREEN_HEIGHT - 112
        self.rect.topleft = (70, self.position_y)


while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                if position >= 6:
                    position = 0
                else:
                    position += 1
            if event.key == K_LEFT:
                if position == 0:
                    position = 6
                else:
                    position -= 1

    if position == 0:
        pygame.draw.rect(screen, RED, (25,195, 70, 80), width=4)
    elif position == 1:
        pygame.draw.rect(screen, RED, (95,195, 70, 80), width=4)
    elif position == 2:
        pygame.draw.rect(screen, RED, (165,195, 80, 80), width=4)
    elif position == 3:
        pygame.draw.rect(screen, RED, (250,195, 100, 80), width=4)
    elif position == 4:
        pygame.draw.rect(screen, RED, (360,195, 100, 80), width=4)
    elif position == 5:
        pygame.draw.rect(screen, RED, (465,195, 75, 80), width=4)
    elif position == 6:
        pygame.draw.rect(screen, RED, (540,195, 80, 80), width=4)

    screen.blit(LEVI, (30,200))
    screen.blit(DUDA, (100,200))
    screen.blit(LUZIA, (170, 201))
    screen.blit(ANNE, (255, 201))
    screen.blit(VITORIA, (360, 201))
    screen.blit(VK, (470, 200))
    screen.blit(EMIMI, (550, 200))
    screen.blit(selection_text, (140, 40))

    pygame.display.flip()
