# Flake8: noqa
"""
Chrome Levi
"""
import os
from sys import exit
import pygame
from pygame.sprite import Sprite
from pygame.locals import *
from random import randrange, randint, choice
import neat


def display_mensage(mensage, size, color, _font):
    font = pygame.font.SysFont(f'{_font}', size, False, False)
    text = f'{mensage}'
    formated_text = font.render(text, True, color)
    return formated_text


# File path
FILE_PATH = os.path.dirname(__file__)
IMAGES_PATH = os.path.join(FILE_PATH, 'Images')


# Defining constances
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Obstacule choice
obstacle_choice = choice([0, 1])

# AI generation
generation = 0

pygame.init()

# speed_game
speed = 30

# Variable containing collision status
collided = False

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set game name
pygame.display.set_caption('Chrome Levi')

# Load sprite sheets
SPRITE_SHEET = pygame.image.load(os.path.join(
    IMAGES_PATH, 'Levi_spritesheet.png')).convert_alpha()


class Player(Sprite):
    collisions = False
    collided = False

    def __init__(self, sprite_sheet, size, scale, position_y):
        super().__init__()
        self._sprites = []

        for i in range(4):
            sprite = sprite_sheet.subsurface((i * size, 0), (size, size))
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
        self.time = 0
        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        self.is_jump = True
        self.time = 0

    def down(self):
        self.is_down = True

    def update(self):
        if self.list_index > len(self._sprites) - 1:
            self.list_index = 0

        displacement = self.jump_speed * self.time + 1.5 * (self.time**2)

        if self.is_jump:
            self.time = 1

            if self.rect.y <= 218:
                self.down()
                self.is_jump = False

            self.rect.y -= displacement

        if self.is_down == True:
            if self.rect.y + displacement > self.position_y:
                self.rect.y = self.position_y

            if self.rect.y == self.position_y:
                self.is_down = False
            else:
                self.rect.y += displacement

        if self.is_jump or self.is_down:
            self.image = self._sprites[1]
        else:
            self.list_index += 0.2
            self.image = self._sprites[int(self.list_index)]


class Clouds(Sprite):
    def __init__(self):
        super().__init__()
        self.image = SPRITE_SHEET.subsurface((32*9, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 151, 50)
        self.rect.x = SCREEN_WIDTH - randrange(0, 450, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = randrange(50, 200, 50)

        self.rect.x -= speed/2


class Ground(Sprite):
    def __init__(self, position_x):
        super().__init__()

        if position_x == 0:
            self.image = SPRITE_SHEET.subsurface((32*8, 0), (32, 32))
        else:
            self.image = SPRITE_SHEET.subsurface((32*7, 0), (32, 32))

        self.image = pygame.transform.scale(self.image, (32*4, 32*4))
        self.rect = self.image.get_rect()
        self.rect.x = position_x * 128
        self.rect.y = SCREEN_HEIGHT - 32*4

    def update(self):
        self.rect.x -= speed
        if self.rect.x <= -128:
            self.rect.x = SCREEN_WIDTH


class Cactus(Sprite):
    def __init__(self):
        super().__init__()
        self.image = SPRITE_SHEET.subsurface((32*6, 0), (32, 32))
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

            self.rect.x -= speed


class Pterodactyl(Sprite):
    def __init__(self):
        super().__init__()
        self._sprites = []
        for i in range(4, 6):
            img = SPRITE_SHEET.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self._sprites.append(img)

        self.list_index = 0
        self.image = self._sprites[self.list_index]

        self.rect = self.image.get_rect()
        self.rect.x = -96
        self.rect.y = SCREEN_HEIGHT - 200

        self.mask = pygame.mask.from_surface(self.image)

        self.choice = obstacle_choice
        self.rng = randint(0, 2)

    def update(self):
        if self.choice == 0:

            if self.rect.topright[0] <= 0:
                self.rect.x = SCREEN_WIDTH + 60

            if self.rng == 0:
                self.rect.y = SCREEN_HEIGHT - 200
            elif self.rng == 1:
                self.rect.y = SCREEN_HEIGHT - 170
            else:
                self.rect.y = SCREEN_HEIGHT - 250

            self.list_index += 0.2

            if self.list_index >= 2:
                self.list_index = 0

            self.image = self._sprites[int(self.list_index)]

            self.rect.x -= speed

# fitness function
def main(genomes, config):
    global generation
    speed = 30
    generation += 1
    generation_text = display_mensage(
        f"Generation: {generation}", 40, BLACK, '')

    # Obstacule choice
    obstacle_choice = choice([0, 1])

    # Score variable
    score = 0

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

    # Create cactus instance
    cactus = Cactus()
    obstacles_group.add(cactus)
    all_sprites.add(cactus)

    # Create Pterodactyl instance
    pterodactyl = Pterodactyl()
    obstacles_group.add(pterodactyl)
    all_sprites.add(pterodactyl)

    players = []
    networks = []
    genomes_list = []
    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        genome.fitness = 0
        genomes_list.append(genome)
        players.append(Player(SPRITE_SHEET, 32, 2.5, 368))

    for player in players:
        all_sprites.add(player)

    clock = pygame.time.Clock()
    fps = 20

    while True:
        if not players:
            break

        clock.tick(fps)

        screen.fill(WHITE)

        # Event LOOP🔄
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        for i, player in enumerate(players):
            player_height = player.image.get_height()
            if obstacle_choice == 0:
                obstacle_distance = pterodactyl.rect.x - \
                    player.rect.bottomright[0]
                obstacle_width = pterodactyl.image.get_width()
                obstacle_height = pterodactyl.image.get_height()
                obstacle_position_y = pterodactyl.rect.topleft[1]
            else:
                obstacle_distance = cactus.rect.bottomleft[0] - \
                    player.rect.bottomright[0]
                obstacle_width = cactus.image.get_width()
                obstacle_height = pterodactyl.image.get_height()
                obstacle_position_y = cactus.rect.topleft[1]

            inputs = (player_height,
                      obstacle_distance,
                      obstacle_width,
                      obstacle_height,
                      obstacle_position_y,
                      speed,)

            outputs = networks[i].activate(inputs)

            if outputs[0] > 0:
                if not player.is_jump and not player.is_down:
                    player.jump()

        # Colisions list
        for player in players:
            player.collisions = pygame.sprite.spritecollide(
                player, obstacles_group, False, pygame.sprite.collide_mask)

        # Resetting obstacles position attributes
        if cactus.rect.topright[0] <= 0 or pterodactyl.rect.topright[0] <= 0:
            obstacle_choice = choice([0, 1])
            cactus.rect.x = SCREEN_WIDTH
            pterodactyl.rect.x = SCREEN_WIDTH
            cactus.choice = obstacle_choice
            pterodactyl.choice = obstacle_choice
            pterodactyl.rng = randint(0, 1)

        all_sprites.draw(screen)

        for player in players:
            if player.collisions and player.collided == False:
                player.collided = True

        for i, player in enumerate(players):
            if player.collided == True:
                genomes_list[i].fitness -= 30
                players.pop(i)
                all_sprites.remove(player)
                genomes_list.pop(i)
                networks.pop(i)
            else:
                genomes_list[i].fitness += 0.1
                player.update()
                score_text = display_mensage(
                    f'{score}'.zfill(5), 40, BLACK, '')

        score += 1

        if score % 100 == 0:
            if speed <= 1000:
                speed += 10

        all_sprites.update()

        screen.blit(score_text, (550, 40))
        screen.blit(generation_text, (generation_text.get_width(), 40))

        pygame.display.flip()


def run(config_path):
    config = neat.Config(neat.DefaultGenome,
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,
                         neat.DefaultStagnation,
                         config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    population.run(main)


if __name__ == "__main__":
    CONFIG_PATH = os.path.join(FILE_PATH, "config.txt")
    run(CONFIG_PATH)
