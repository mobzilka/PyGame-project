import os
import sys
import pygame
from pygame.locals import *


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name).replace("\\", "/")
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "levels/" + filename + ".txt"
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


pygame.init()
pygame.display.set_caption('Перемещение героя')
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
fps = 15
clock = pygame.time.Clock()
tile_images = {
    'wall': load_image('box.png')
    # 'empty': load_image('grass.png')
}
player_image = load_image('mar.png')
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


image_sprite = [pygame.image.load("data/Standing.png"),
                pygame.image.load("data/Walking2.png"),
                pygame.image.load("data/Walking3.png"),
                pygame.image.load("data/Walking4.png"),
                pygame.image.load("data/Walking5.png"),
                pygame.image.load("data/Walking6.png"),
                pygame.image.load("data/Walking7.png"),]
image = image_sprite[0]
clock = pygame.time.Clock()
value = 0
backvalue = 6
run = True
movingLEFT = False
movingRIGHT = False
movingUP = False
movingDOWN = False
velocity = 12
x = 100
y = 150
while run:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or
                    event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                movingDOWN = False
                movingRIGHT = False
                movingUP = False
                movingLEFT = False
                value = 0
                backvalue = 6
    key_pressed_is = pygame.key.get_pressed()
    if key_pressed_is[K_LEFT]:
        x -= 8
        movingLEFT = True
    if key_pressed_is[K_RIGHT]:
        x += 8
        movingRIGHT = True
    if key_pressed_is[K_UP]:
        y -= 8
        movingUP = True
    if key_pressed_is[K_DOWN]:
        y += 8
        movingDOWN = True
    if movingLEFT:
        backvalue -= 1
    if movingRIGHT:
        value += 1
    if movingUP:
        backvalue -= 1
    if movingDOWN:
        value += 1
    if value >= len(image_sprite):
        value = 0
    if backvalue <= 0:
        backvalue = 6
    if movingRIGHT:
        image = image_sprite[value]
    elif movingDOWN:
        image = image_sprite[value]
    elif movingLEFT:
        image = image_sprite[backvalue]
    elif movingUP:
        image = image_sprite[backvalue]

    image = pygame.transform.scale(image, (60, 60))
    screen.blit(image, (x, y))
    pygame.display.update()
    screen.fill((0, 0, 0))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        # while self.image.get_rect() !=
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # if level[y][x] == '.':
            #     Tile('empty', x, y)
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                # Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Лабиринт", "",
                  "Играть",
                  "Выйти"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def move_in_map(player, dx, dy, level_map, level_x, level_y):
    pos_x = player.pos_x + dx
    pos_y = player.pos_y + dy
    print(level_map[pos_y][pos_x])
    if (0 <= pos_x <= level_x and 0 <= pos_y <= level_y and
            level_map[pos_y][pos_x] == '.'):
        player.move(pos_x, pos_y)
        level_map[pos_y][pos_x] = '@'
        level_map[pos_y - dy][pos_x - dx] = '.'


if __name__ == '__main__':
    start_screen()
    level_name = input("Введите название уровня: ")
    level_map = load_level(level_name)
    player, level_x, level_y = generate_level(level_map)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                move_in_map(player, 0, -1, level_map, level_x, level_y)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                move_in_map(player, 0, 1, level_map, level_x, level_y)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                move_in_map(player, -1, 0, level_map, level_x, level_y)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                move_in_map(player, 1, 0, level_map, level_x, level_y)
        screen.fill((255, 255, 255))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
