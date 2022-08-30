import pygame
from pygame import *
import game_elements
from game_elements import *
import neat



if __name__ == "__main__":
    # Initialize window
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption("MAN VS. MACHINE")
    clock = pygame.time.Clock()

    # Set background
    background = pygame.image.load("background.png").convert()
    screen.blit(background, [0,0])

    # Set game objects
    objects = pygame.sprite.Group()
    tiles = []
    camera = Camera(SCREEN)
    player = Player((800, 1540), Color(255, 255, 255))
    ai_players = []

    # Build world
    world = World(player, ai_players, tiles, objects)

    # Set up keys
    left = right = space = up = False

    # GAME LOOP
    while 1:
        clock.tick(60)
        
        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                space = True
            if e.type == KEYDOWN and e.key == K_UP:
                up = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                space = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
        
        screen.blit(background, [0,0])
        camera.update(player)

        player.move(left, right, space, up, world)

        for obj in world.objects:
            screen.blit(obj.image, camera.apply(obj))

        pygame.display.update()