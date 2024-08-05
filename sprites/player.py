# sprites/player.py

import pygame
from utils import load_sprite_sheets


class Player(pygame.sprite.Sprite):
    """
    class for the player character
    """
    COLOUR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.count = None
        self.jump_count = 0
        self.sprite = None
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.hit = False
        self.hit_count = 0

        # load sprite sheets here after display has been initialised
        self.SPRITES = load_sprite_sheets("MainCharacter", "PuppyCat", 32, 32, True)

    def jump(self):
        """
        make the player jump
        """
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        """
        move the player by the specified amount
        :param dx: change in horizontal position
        :param dy: change in vertical position
        """
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        """
        mark the player as hit
        """
        self.hit = True
        self.hit_count = 0

    def move_left(self, vel):
        """
        move the player left
        :param vel: velocity of movement
        """
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        """
        move the player right
        :param vel: velocity of movement
        """
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        """
        update the player state every frame
        :param fps: frames per second
        """
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        """
        handle landing after a jump
        """
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        """
        handle hitting the head
        """
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        """
        update the player's sprite based on its current state
        """
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = self.animation_count // self.ANIMATION_DELAY % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        """
        update the player's position and mask
        """
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        """
        draw the player on the window
        :param win: the game window surface
        :param offset_x: horizontal offset for scrolling effect
        """
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
