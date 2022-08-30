import pygame
from pygame import *
import random

SCREEN = pygame.Rect((0, 0, 960, 640))
LEVEL = pygame.Rect((0, 0, 1600, 1600))

# global variables to track the player and ai scores
ai_score = 0
player_score = 0

'''
    Player class, Camera, and other GameObjects

    Reference: https://stackoverflow.com/questions/14354171/
'''

class Camera(object):
    def __init__(self, level_size):
        self.state = level_size

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        l = target.rect.left
        t = target.rect.top
        self.state = pygame.Rect((SCREEN.centerx-l, SCREEN.centery-t, self.state.width, self.state.height))

class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos, length, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((length, width))
        self.rect = pygame.Rect((pos), (length, width))

    def update(self):
        pass

class Tile(GameObject):
    def __init__(self, pos):
        super().__init__(pos, 20, 20)
        self.image.fill(Color("#000000"))

class Goal(GameObject):
    def __init__(self, pos):
        super().__init__(pos, 20, 20)
        self.image.fill(Color("#0033FF"))
        
class Wall(GameObject):
    def __init__(self, pos, length, width):
        super().__init__(pos, length, width)
        self.image.fill(Color("#000000"))

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = pygame.Rect((pos), (40, 40))
        self.speed = 0
        self.vert = 0
        self.grounded = False
        self.life_counter = 700
        self.win = False
        self.isBot = False
        self.goalX = 200
        self.goalY = 170

    def get_position(self):
        return self.rect.left, self.rect.top

    def move(self, left, right, space, up, world):
        # Process key input results:
        # Moving left or right
        if left:
            self.speed = -10
        if right:
            self.speed = 10
        # Jumping
        if space or up:
            if self.grounded:
                self.vert -= 12
        # Falling
        if not self.grounded:
            self.vert += 0.5
        if not left and not right:
            self.speed = 0

        # Update position
        self.rect.left += self.speed
        self.collision(self.speed, 0, world)

        self.rect.top += self.vert
        self.grounded = False
        self.collision(0, self.vert, world)

    def collision(self, speed, vert, world):
        global ai_score
        global player_score
        for tile in world.tiles:
            if pygame.sprite.collide_rect(self, tile):
                # Reached goal object
                if isinstance(tile, Goal):
                    self.vert = 0
                    self.speed = 0
                    self.win = True
                    if self.win and self.isBot:
                        ai_score += 1
                    if self.win and not self.isBot:
                        player_score += 1
                    world.createWorld(self, self, world.tiles, world.objects)
                # Left and right collisions
                if speed < 0:
                    self.rect.left = tile.rect.right
                if speed > 0:
                    self.rect.right = tile.rect.left
                # Top and bottom collisions
                if vert < 0:
                    self.rect.top = tile.rect.bottom
                if vert > 0:
                    self.rect.bottom = tile.rect.top
                    self.vert = 0
                    self.grounded = True

'''
    SolutionPath class generates scheme for a beatable level

    Random Level Generation, modeled after Spelunky
    Reference: http://tinysubversions.com/spelunkyGen/

    This algorithm creates a 4x4 matrix of rooms and assigns
    each a value, 0-3
        0 rooms are not part of solution path
        1 rooms can be passed through left and right
        2 rooms can be passed through left, right, and bottom
        3 rooms can be passed through left, right, and top

    Upon generation, the sequence of rooms is guaranteed to have
    a continuous path from the top row to the bottom row
'''
class SolutionPath(object):
    def __init__(self):
        self.findSolution()

    def findSolution(self):
        # Level is the final level scheme
        self.level = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        i = 0
        j = random.randint(0,3)

        # Make random room in top row a 1
        self.level[i][j] = 1

        # Decide where to go next randomly
        # 1 or 2 = Left; 3 or 4 = Right; 5 = Down
        # Moving left into left edge or right into right edge
        # calls for moving down instead
        while i < 3:
            go = random.randint(1,5)
            dropped = False
            if go == 1 or go==2:
                if j - 1 < 0:
                    if self.level[i][j] == 3:
                        continue
                    dropped = True
                    self.level[i][j] = 2
                    i += 1
                else:
                    j -= 1
            elif go==3 or go==4:
                if j + 1 > 3:
                    if self.level[i][j] == 3:
                        continue
                    dropped = True
                    self.level[i][j] = 2
                    i += 1
                else:
                    j += 1
            else:
                if self.level[i][j] == 3:
                    continue
                dropped = True
                self.level[i][j] = 2
                i += 1
            # Place next room
            if dropped or self.level[i][j] == 3:
                self.level[i][j] = 3
            else:
                self.level[i][j] = 1 

'''
    World class handles level creation and reset
    upon contact with the goal
'''
class World(object):
    def __init__(self, player, ai_players, tiles, objects):
        self.player = player
        self.ai_players = ai_players
        for bot in ai_players:
            bot.rect = pygame.Rect((800, 1520), (40, 40))
            bot.win = False
        self.player.rect = pygame.Rect((800, 1520), (40, 40))
        self.player.win = False
        self.tiles = tiles
        self.objects = objects
        self.room1 = [
            "                    ",
            "      XXXXXXXXXXXX  ",
            "XXXXXXXXXXXXXXXXXXXX",
            "                    ",
            "                    ",
            "         XXXXX      ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "          XXXXXXXX  ",
            "                    ",
            "                    ",
            "  XXXXXXX           ",
            "                    ",
            "                    ",
            "XXXXXXX   XXXXXXXXXX",
            "     XXXXXXXXXXXXXX ",
            "                    "
        ]

        self.room1_2 = [
            "                    ",
            "  XXXXXXXXXXXXX   XX",
            "XXXXXXXXXXXXXXXXXXXX",
            "          XXXX      ",
            "               XX   ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            " XXXXXX             ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "         XXXXXXXXXXX",
            "      XXXXXXXXX  XXX",
            "   XXX    XX  XXXX  ",
            "XXXXXXXX            ",
            "                    "
        ]

        self.room2 = [
            "                    ",
            "  XXXXXXXXXXXXX   XX",
            "XXXXXXXXXXXXXXXXXXXX",
            "          XXXX      ",
            "                    ",
            "                    ",
            "            XXX     ",
            "                    ",
            "                    ",
            "    XXX             ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "               XXXXX",
            "                    ",
            "XXXX                ",
            "   XXX        XXXX  ",
            "                    "
        ]

        self.room2_2 = [
            "                    ",
            "  XXXXXXXXXXXXX   XX",
            "XXXXXXXXXXXXXXXXXXXX",
            "                    ",
            "                    ",
            "                    ",
            "   XXXXXXXXXX       ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "       XXX          ",
            "                    ",
            "                    ",
            "                XX  ",
            "                    ",
            "XXXXX               ",
            "   XXX          XXXX",
            "                    "
        ]

        self.room3 = [
            "                    ",
            "  XXX             XX",
            "XXXXXX          XXXX",
            "                    ",
            "           XXXXXX   ",
            "         XXXXX      ",
            "                    ",
            "                    ",
            "                    ",
            " XXXXXX             ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "         XXXXXXXXXXX",
            "                    ",
            " XXXX XXXXXXXXX     ",
            "   XXX    XX  XXXX X",
            "                    "
        ]

        self.room3_2 = [
            "                    ",
            "  XXXXX           XX",
            "XXXXX           XXXX",
            "          XXXX      ",
            "               XX   ",
            "       XX           ",
            "                    ",
            "                    ",
            "                    ",
            " XXXXXX             ",
            "                    ",
            "                    ",
            "           XXX      ",
            "                    ",
            "                    ",
            "         XXXXXXXXXXX",
            "XXXXXXXXX           ",
            "      XXXXXXXXX     ",
            "   XXX    XX  XXXX  ",
            "                    "
        ]

        self.room0 = [
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "       XXXXXXXX     ",
            "                    ",
            "                    ",
            "                    ",
            "            XX      ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "   XXX              ",
            "               X    ",
            "                    ",
            "                    ",
            "                    ",
            "                    "
        ]

        self.room0_2 = [
            "                    ",
            "                    ",
            "                    ",
            "    XXX             ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "        XXXXXXXXX   ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "   XXXXXXXX         ",
            "                    ",
            "                    ",
            "                    ",
            "                    "
        ]

        self.goalRoom = [
            "                    ",
            "  XXXXXXXXXXXXX   XX",
            "XXXXXXXXXXXXXXXXXXXX",
            "          XXXX      ",
            "                    ",
            "         GG         ",
            "         GG         ",
            "         GG         ",
            "         GG         ",
            "       XXXXXX       ",
            "     XX      XX     ",
            "                    ",
            "                    ",
            "                    ",
            "                    ",
            "               XXXXX",
            "                    ",
            "XXXX                ",
            "   XXX        XXXX  ",
            "                    "
        ]
        self.createWorld(player, ai_players, tiles, objects)

    '''
        createWorld function takes in solution scheme as input
        and generates playable world as output

        The playable world is 1600 x 1600 pixels in area. Each
        400 x 400 pixel section corresponds to a solution scheme
        room. This sequence creates each playable level section
        according to the solution scheme by following the appropriate
        room instructions.

        Room instructions are an array of strings with Xs or ' '
        A tile is placed where every X is to create the section.
    '''
    def createWorld(self, player, ai_players, tiles, objects):
        self.tiles.clear()
        self.objects.empty()
        self.player.rect = pygame.Rect((800, 1520), (40, 40))
        self.player.win = False
        
        soln = SolutionPath().level
        goalRoom = True

        for i in range(0, 4):
            for j in range(0, 4):
                choice = random.randint(0, 1)
                if soln[i][j] == 0:
                    if choice:
                        soln[i][j] = self.room0
                    else:
                        soln[i][j] = self.room0_2
                if soln[i][j] == 1:
                    if choice:
                        soln[i][j] = self.room1
                    else:
                        soln[i][j] = self.room1_2
                if soln[i][j] == 2:
                    if choice:
                        soln[i][j] = self.room2
                    else:
                        soln[i][j] = self.room2_2
                    if goalRoom:
                        soln[i][j] = self.goalRoom
                        goalRoom = False
                        for bot in self.ai_players:
                            bot.goalX = (j * 400) + 200
                if soln[i][j] == 3:
                    if choice:
                        soln[i][j] = self.room3
                    else:
                        soln[i][j] = self.room3_2

        x = y = 0
        x2 = y2 = 0
        for i in range(0, 4):
            for j in range(0, 4):
                for row in soln[i][j]:
                    for col in row:
                        if col == "X":
                            tile = Tile((x, y))
                            tiles.append(tile)
                            objects.add(tile)
                        if col == "G":
                            goal = Goal((x, y))
                            tiles.append(goal)
                            objects.add(goal)
                        x += 20
                    y += 20
                    x = x2
                x2 += 400
                y -= 400
            y += 400
            x2 = 0

        wall = Wall((0, 0), 20, 1600)
        tiles.append(wall)
        objects.add(wall)

        wall = Wall((1580, 0), 20, 1600)
        tiles.append(wall)
        objects.add(wall)

        wall = Wall((20, 0), 1560, 20)
        tiles.append(wall)
        objects.add(wall)

        wall = Wall((20, 1580), 1560, 20)
        tiles.append(wall)
        objects.add(wall)

        objects.add(self.player)
        for bot in self.ai_players:
            bot.win = False
            bot.rect = pygame.Rect((800, 1520), (40, 40))
            objects.add(bot)

        self.tiles = tiles
        self.objects = objects