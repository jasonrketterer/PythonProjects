import sys
import os
import pygame
import neat
from math import hypot as dist
from pygame import *
import game_elements
from game_elements import *

# start a pygame module and
pygame.init()
screen = pygame.display.set_mode(SCREEN.size)
pygame.display.set_caption("MAN VS. MACHINE")

# set fonts for the different uses in game, then the winning message when you beat the computer
pygame.font.init()
win_font = pygame.font.SysFont(None, 65)
menu_font = pygame.font.SysFont(None, 100)
button_font = pygame.font.SysFont(None, 50)
win_msg = win_font.render('Win!', True, (0, 128, 0))
info_font = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 20)
smaller_font = pygame.font.SysFont(None, 10)

game_elements.ai_score = 0
game_elements.player_score = 0

# set path and load images for menu icons
script_dir = os.path.dirname(__file__)
human_img_path = os.path.join(script_dir, 'user.png')
ai_img_path = os.path.join(script_dir, 'bot.png')
human_img = pygame.image.load(human_img_path)
ai_img = pygame.image.load(ai_img_path)

# set some simple colors for use later on with buttons and whatnot
red = (200, 0, 25)
lightred = (255, 0, 50)
green = (0, 128, 0)
lightgreen = (0, 175, 0)
blue = (0, 0, 125)
lightblue = (0,0,200)
mid_blue= (90, 140, 240)
lighter_blue = (100, 240, 250)
white = (255, 255, 255)

# function to create the counters for score while the game plays
def scoreboard(player_score, ai_score):

    # creates the exit button in the top right corner
    make_button("Menu", button_font, white, mid_blue, lighter_blue, SCREEN.width - 100, 0, 100, 50, "menu")

    # place border and background
    pygame.draw.rect(screen, white, (5, 5, 150, 100))
    pygame.draw.rect(screen, (0,0,0), (10, 10, 140, 90))

    # Add title of scoreboard
    text_surf, text_rect = text_objects("Score", info_font, white)
    text_rect.center = (77, 22)
    screen.blit(text_surf, text_rect)

    # add rectangles to house the points
    pygame.draw.rect(screen, (47, 79, 79), (20, 34, 50, 62))
    pygame.draw.rect(screen, (47, 79, 79), (90, 34, 50, 62))

    # add score titles
    # human title first
    text_surf, text_rect = text_objects("Human", small_font, white)
    text_rect.center = (44, 42)
    screen.blit(text_surf, text_rect)
    # ai title second
    text_surf, text_rect = text_objects("AI", small_font, white)
    text_rect.center = (115, 42)
    screen.blit(text_surf, text_rect)

    # add scores in the boxes
    # player score first
    text_surf, text_rect = text_objects(str(player_score), button_font, white)
    text_rect.center = (44, 75)
    screen.blit(text_surf, text_rect)
    # ai score second
    text_surf, text_rect = text_objects(str(ai_score), button_font, white)
    text_rect.center = (115, 75)
    screen.blit(text_surf, text_rect)

# output the information screen
def game_info():

    info = True

    # loop ensuring the objects remain created
    while info:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # paint a black background that matches the game
        screen.fill((0,0,0))

        # Title block at the top of the screen
        text_surf, text_rect = text_objects('Man vs. Machine', menu_font, lightblue)
        text_rect.center = (int(SCREEN.width / 2), 50)
        screen.blit(text_surf, text_rect)

        # lines 383 - 432 simply output text explanations to the screen
        text_surf, text_rect = text_objects('Man vs. Machine is a small-scale platforming game', info_font, white)
        text_rect.center = (int(SCREEN.width / 3), 125)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('It has been developed to implement and test basic AI', info_font, white)
        text_rect.center = (int(SCREEN.width / 3) + 10, 150)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('How it works:', win_font, lightred)
        text_rect.center = (int(SCREEN.width / 4.7) + 10, 210)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('The AI get a headstart of sorts and run through the program a few preliminary times', info_font, white)
        text_rect.center = (int(SCREEN.width / 2.05) + 10, 250)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Users then choose a level of difficulty: easy, medium, or hard', info_font, white)
        text_rect.center = (int(SCREEN.width / 2.45) + 10, 275)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('The difficulty level corresponds to a set number of AIs the player will be up against', info_font, white)
        text_rect.center = (int(SCREEN.width / 1.925) + 10, 300)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Essentially, the more AI trying to win, the tougher it will be for you', info_font, white)
        text_rect.center = (int(SCREEN.width / 2.49) + 10, 325)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('If you reach the finish before the AI, you win!', info_font, white)
        text_rect.center = (int(SCREEN.width / 3.43) + 10, 350)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('If any of the AI beat you there, they win!', info_font, white)
        text_rect.center = (int(SCREEN.width / 3.77) + 10, 375)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('As soon as you finish a level, you\'ll continue on to a new one', info_font, white)
        text_rect.center = (int(SCREEN.width / 2.71) + 10, 400)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('There are more AI than there are of you, so multiple AI could beat you in one round!', info_font, white)
        text_rect.center = (int(SCREEN.width / 2.06) + 10, 425)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Good luck!', win_font, lightgreen)
        text_rect.center = (int(SCREEN.width / 2) + 10, 525)
        screen.blit(text_surf, text_rect)

        # make a lil button to get back to the menu
        make_button('Back', score_font, white, lightblue, mid_blue, SCREEN.width - 200, SCREEN.height - 100, 100, 50, "menu")

        pygame.display.update()


# output the starting menu
def game_menu():

    intro = True

    screen.fill((0, 0, 0))

    # add some dope icons in the menu to make it pretty
    screen.blit(human_img, (int(SCREEN.width/3), int(SCREEN.height/5)))
    text_surf, text_rect = text_objects('VS', button_font, white)
    text_rect.center = (int(SCREEN.width / 2), int(SCREEN.height / 3.5))
    screen.blit(text_surf, text_rect)
    screen.blit(ai_img, (int(SCREEN.width*2/3 - 80), int(SCREEN.height/5)))

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # title words
        text_surf, text_rect = text_objects('Welcome to Man vs. Machine', menu_font, lighter_blue)
        text_rect.center = (int(SCREEN.width / 2), int(SCREEN.height / 2))
        screen.blit(text_surf, text_rect)

        # call functions to create buttons to move to other screens or quit
        make_button('Start', button_font, white, lightblue, mid_blue, 150, SCREEN.height - 200, 200, 100, "sett")
        make_button('Quit', button_font, white, lightblue, mid_blue, SCREEN.width - 100, SCREEN.height-50, 100, 50, "quit")
        make_button('Info', button_font, white, lightblue, mid_blue, SCREEN.width - 200 - 150, SCREEN.height - 200, 200, 100, "info")

        pygame.display.update()


# once user starts the game, let them select the difficulty with this menu
def game_settings():

    sett = True

    while sett:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))

        text_surf, text_rect = text_objects('Man vs. Machine', menu_font, lightblue)
        text_rect.center = (int(SCREEN.width / 2), 50)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Difficulty', win_font, lightred)
        text_rect.center = (int(SCREEN.width / 2) + 10, 125)
        screen.blit(text_surf, text_rect)

        make_button('Easy', button_font, white, green, lightgreen, SCREEN.width/4 - 100, SCREEN.height/2, 200, 100, "easy")
        make_button('Medium', button_font, white, blue, lightblue, SCREEN.width/2 - 100, SCREEN.height/2, 200, 100, "med")
        make_button('Hard', button_font, white, red, lightred, SCREEN.width*3/4 - 100, SCREEN.height/2, 200, 100, "hard")

        pygame.display.update()


# button creator function
def make_button (text, font, textcolor, color_off, color_on, x_pos, y_pos, width, height, action = None):
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    if x_pos + width > mouse[0] > x_pos and y_pos + height > mouse[1] > y_pos:
        pygame.draw.rect(screen, color_on, (int(x_pos), int(y_pos), int(width), int(height)))
        if click[0] == 1 and action is not None:
            if action == 'sett':
                # start game action
                game_settings()
            elif action == 'quit':
                pygame.quit()
                quit()
            elif action == 'menu':
                game_menu()
            elif action == 'info':
                game_info()
            elif action == 'easy':
                run(config_easy)
            elif action == 'med':
                run(config_med)
            elif action == 'hard':
                run(config_hard)
    else:
        pygame.draw.rect(screen, color_off, (int(x_pos), int(y_pos), int(width), int(height)))

    text_surf, text_rect = text_objects(text, font, textcolor)
    text_rect.center = (int(x_pos) + int(width / 2), int(y_pos) + int(height / 2))

    screen.blit(text_surf, text_rect)


# helper function to create text blocks
def text_objects(text, font, color):

    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# Run A.I. simulation of the game - calculates the fitness function
def eval_genomes(genomes, config):

    # lists to hold the players, the genomes, and the neural net associated with that genome and player
    neural_nets = []
    genome = []
    players = []

    # this tracks the user beating the AI
    win = False

    # initialize neural nets and genomes
    for _, g in genomes:
        g.fitness = 0
        nn = neat.nn.FeedForwardNetwork.create(g, config)
        neural_nets.append(nn)
        bot = Player((800, 1540), Color(255, 80, 80))
        bot.isBot = True
        players.append(bot)
        genome.append(g)

    # initialize the game
    player = Player((800, 1540), Color(255, 255, 255))
    screen = pygame.display.set_mode(SCREEN.size)
    clock = pygame.time.Clock()

    # Set background
    local_dir = os.path.dirname(__file__)
    background_path = os.path.join(local_dir, 'background.png')
    background = pygame.image.load(background_path).convert()
    screen.blit(background, [0,0])

    # Set game objects
    objects = pygame.sprite.Group()
    tiles = []
    camera = Camera(SCREEN)

    # Build world
    world = World(player, players, tiles, objects)

    # Set up keys
    left = right = space = up = False
    left2 = right2 = space2 = up2 = False

    # GAME LOOP
    run_simulation = True
    while run_simulation and len(players) > 0:
        clock.tick(60)
        
        for e in pygame.event.get():
            if e.type == QUIT: 
                run_simulation = False
                pygame.quit()
                sys.exit()
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
        
        
        # SET UP AI PLAYER
        '''
            -----------------------------------------------------------------------------------------------------------
        '''
        for i, p in enumerate(players):
            x = players[i].rect.x
            y = players[i].rect.y
            from_goal = dist(p.goalX - x, p.goalY - y)

            output = neural_nets[players.index(p)].activate((x, y, from_goal))

            # set values to allow the computer to jump
            if output[1] > 0.5:
                space2 = True
                up2 = True

            # blocks to choose character's movement left and right
            if output[0] > 0.5:
                left2 = False
                right2 = True
            else:
                left2 = True
                right2 = False


            p.move(left2, right2, space2, up2, world)

            # get new position
            x2 = players[i].rect.x
            y2 = players[i].rect.y
            new_from_goal = dist(p.goalX - x2, p.goalY - y2)

            # find if we backtracked from our cur_goal
            if new_from_goal < from_goal:
                genome[players.index(p)].fitness -= 2

            # see if we are any closer to our goal
            if new_from_goal > from_goal:
                genome[players.index(p)].fitness += 2

            # did we achieve the goal?
            if new_from_goal > from_goal == 0:
                # if we achieved the goal, we will take this instance out and its fitness will increase
                genome[players.index(p)].fitness += 15
                neural_nets.pop(players.index(p))
                genome.pop(players.index(p))
                players.pop(players.index(p))
            else:
                # decrease exist counter for this player
                p.life_counter -= 1

            if p.life_counter < 0:
                # remove this player and neural net
                genome[players.index(p)].fitness -= 5  # remove some fitness for not making it to the goal
                genome[players.index(p)].fitness += 0.002 * new_from_goal  # add some fitness back proportional to how close it got to the goal
                neural_nets.pop(players.index(p))
                genome.pop(players.index(p))
                players.pop(players.index(p))
        '''
            -----------------------------------------------------------------------------------------------------------
        '''

        # reset the winner, so it doesn't mess up the loop's dependencies
        if player.win and player.isBot:
            player.win = False  # reset win

        # case for human landing on the correct goal obstacle
        if player.win and not player.isBot:
            win = True

        # increment user score and end the iteration once you make it to the end
        if win:
            players.clear()

        # at the end of the loop make sure everything updates constantly
        for obj in world.objects:
            screen.blit(obj.image, camera.apply(obj))

        # add the scoreboard
        scoreboard(game_elements.player_score, game_elements.ai_score)

        pygame.display.update()


# implements the run method according to the neat configuration
def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # creates the population to run the top-level simulation
    p = neat.Population(config)

    # output statistics to console
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # run the simulation
    num_generations = 100


    # eventually change this to be called in main -- the menu will launch the rest
        # commented out, but left for testing and logging purposes
    # game_menu()
    results = p.run(eval_genomes, num_generations)

    # show stats
    print(results)
    

if __name__ == "__main__":
    # set file paths to respective difficulty levels
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-neat.txt')
    config_easy = os.path.join(local_dir, 'config-neat-easy.txt')
    config_med = os.path.join(local_dir, 'config-neat-medium.txt')
    config_hard = os.path.join(local_dir, 'config-neat-hard.txt')

    game_menu()