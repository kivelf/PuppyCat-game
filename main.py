# main.py

import pygame
from utils import get_background
from sprites.player import Player
from sprites.object import Block, Fire
from settings import WIDTH, HEIGHT, FPS, PLAYER_VEL, TITLE  # import settings from settings.py

pygame.init()  # initialise all imported pygame modules

pygame.display.set_caption(TITLE)  # set the caption for the game window using TITLE from settings.py
window = pygame.display.set_mode((WIDTH, HEIGHT))  # create the game window with specified dimensions


def draw(window, background, bg_image, player, objects, offset_x):
    """
    draw all game elements on the screen
    :param window: the game window surface
    :param background: list of background tiles
    :param bg_image: the background image
    :param player: the player object
    :param objects: list of all other game objects
    :param offset_x: horizontal offset for scrolling effect
    """
    for tile in background:
        window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window, offset_x)
    player.draw(window, offset_x)
    pygame.display.update()  # update the display


def handle_vertical_collision(player, objects, dy):
    """
    handle vertical collisions between the player and objects
    :param player: the player object
    :param objects: list of all other game objects
    :param dy: change in player's vertical position
    :return: list of objects the player has collided with
    """
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)
    return collided_objects


def collide(player, objects, dx):
    """
    check for collisions in the horizontal direction
    :param player: the player object
    :param objects: list of all other game objects
    :param dx: change in player's horizontal position
    :return: the object collided with (if any)
    """
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    """
    handle player movement and collisions
    :param player: the player object
    :param objects: list of all other game objects
    """
    keys = pygame.key.get_pressed()  # get the state of all keyboard buttons
    player.x_vel = 0  # reset horizontal velocity
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
        player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
        player.move_right(PLAYER_VEL)
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


def main():
    """
    the main game loop
    """
    clock = pygame.time.Clock()
    background, bg_image = get_background("Pink.png", WIDTH, HEIGHT)
    block_size = 96

    player = Player(100, 100, 50, 50)
    fire = Fire(200, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)  # ensure the game runs at the specified FPS
        for event in pygame.event.get():  # handle events
            if event.type == pygame.QUIT:  # check if the user wants to quit
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)  # update the player state
        fire.loop()  # update the fire/traps state
        handle_move(player, objects)  # handle player movement
        draw(window, background, bg_image, player, objects, offset_x)  # draw everything on the screen

        # handles scrolling
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()  # quit pygame


if __name__ == "__main__":
    main()  # start the game
