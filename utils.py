# utils.py

import pygame
from os import listdir
from os.path import isfile, join


def flip(sprites):
    """
    flip sprites horizontally
    :param sprites: list of sprite images
    :return: list of flipped sprite images
    """
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """
    load sprite sheets from the assets directory
    :param dir1: first directory name
    :param dir2: second directory name
    :param width: width of each sprite
    :param height: height of each sprite
    :param direction: whether to load directional sprites
    :return: dictionary of loaded sprites
    """
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites


def get_block(size):
    """
    get a block image of the specified size
    :param size: size of the block
    :return: block image
    """
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 128, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


def get_background(name, width, height):
    """
    get the background image and tiles
    :param name: name of the background image file
    :param width: width of the game window
    :param height: height of the game window
    :return: list of background tiles and the background image
    """
    image = pygame.image.load(join("assets", "Background", name))
    _, _, img_width, img_height = image.get_rect()
    tiles = []
    for i in range(width // img_width + 1):
        for j in range(height // img_height + 1):
            pos = (i * img_width, j * img_height)
            tiles.append(pos)
    return tiles, image
