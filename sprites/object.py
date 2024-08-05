# sprites/object.py

import pygame
from utils import get_block, load_sprite_sheets


class Object(pygame.sprite.Sprite):
    """
    base class for all objects in the game
    """
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        """
        draw the object on the window
        :param win: the game window surface
        :param offset_x: horizontal offset for scrolling effect
        """
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    """
    class for block objects
    """
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    """
    class for fire (trap) objects with animation
    """
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        """
        turn the fire animation on
        """
        self.animation_name = "on"

    def off(self):
        """
        turn the fire animation off
        """
        self.animation_name = "off"

    def loop(self):
        """
        update the fire animation
        """
        sprites = self.fire[self.animation_name]
        sprite_index = self.animation_count // self.ANIMATION_DELAY % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
