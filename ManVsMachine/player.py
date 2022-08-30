import pygame
import game_objects

class Player():
    '''Class for human players and objects'''

    def __init__(self, screen, color = None):
        self.screen = screen
        self.screen_width = screen.get_rect().right
        self.ground = screen.get_height()-5
        self.x = 0
        self.y = 575
        self.speed = 5
        self.width = 40
        self.height = 60
        if color is None:
            self.color = 0, 170, 0
        else:
            self.color = color
        self.moving_left = False
        self.moving_right = False
        self.on_obstacle = False # False = on the "ground"
        self.obstacle = -1 # track the obstacle we are on; ground is considered obstacle '-1'
        self.jumping = False
        self.jump_counter = 10
        self.jump_dir = 1
        self.jump_modifier = 0.5
        self.life_counter = 700

    def get_position(self):
        return self.x, self.y, self.obstacle

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        if (self.moving_left and self.x > self.speed) and not(self.collision_left()):
            self.x -= self.speed

        elif (self.moving_right and self.x < self.screen_width - self.width - self.speed) and not(self.collision_right()):
            self.x += self.speed

        if self.jumping:
            if self.jump_dir > 0: # jumping upward
                jump_dist = (self.jump_counter ** 2) * self.jump_modifier * self.jump_dir
                collision_diff = self.collision_top(jump_dist)
                if collision_diff < 0: # collision?
                    self.y -= jump_dist
                    self.jump_counter -= 1
                    if self.jump_counter == 0: # end of jump
                        self.jump_dir = -1
                else: # move to collision point and start falling
                    self.y -= (jump_dist - collision_diff)
                    self.jump_dir = -1
            else: # falling
                fall_dist = (self.jump_counter ** 2) * self.jump_modifier * self.jump_dir
                collision_diff = self.collision_bottom(fall_dist)
                if collision_diff < 0: # keep falling
                    self.jump_counter += 1
                    self.y -= fall_dist
                else: # we've landed on something
                    self.jumping = False # stop "jumping"
                    self.jump_dir = 1 # reset direction for next jump
                    self.jump_counter = 10 # reset counter for next jump
                    self.y = self.y - fall_dist - collision_diff
        else:
            if self.on_obstacle:
                if self.check_fall(): # did we walk off the end of the obstacle?
                    # start falling
                    self.jumping = True
                    self.jump_counter = 0
                    self.jump_dir = -1
                    self.on_obstacle = False

    def check_fall(self):
        obstacle = game_objects.obstacles[self.obstacle]
        if self.x + self.width < obstacle.x or self.x > obstacle.x + obstacle.width:
            return True
        else:
            return False

    def collision_bottom(self, fall_dist):
        '''Return -1 if no collision, otherwise return collision difference
        Also sets the id number of the block we've landed on (excludes ground).'''
        # check for collision with the ground first
        if self.y + self.height - fall_dist > self.ground: # hit the ground
            self.on_obstacle = False
            self.obstacle = -1
            return self.y + self.height - fall_dist - self.ground
        else: # figure out what obstacle we landed on
            for idx,obstacle in enumerate(game_objects.obstacles):
                if self.y + self.height < obstacle.y:
                    if (self.x >= obstacle.x and self.x <= obstacle.x + obstacle.width) or \
                        (self.x + self.width >= obstacle.x and self.x + self.width <= obstacle.x + obstacle.width):
                        if self.y + self.height - fall_dist >= obstacle.y:
                            self.on_obstacle = True
                            self.obstacle = idx
                            return self.y + self.height - fall_dist - obstacle.y
        return -1

    def collision_top(self, jump_dist):
        '''Return -1 if no collision, otherwise return collision difference'''
        # check for collision with top of screen first
        if self.y - jump_dist <= 0:
            return jump_dist - self.y
        for obstacle in game_objects.obstacles:
            if self.y > obstacle.y + obstacle.height:
                if (self.x >= obstacle.x and self.x <= obstacle.x + obstacle.width) or \
                    (self.x + self.width >= obstacle.x and self.x + self.width <= obstacle.x + obstacle.width):
                    if self.y - jump_dist <= obstacle.y + obstacle.height:
                        return (obstacle.y + obstacle.height) - (self.y - jump_dist)
        return -1

    def collision_left(self):
        for obstacle in game_objects.obstacles:
            if (self.x - self.speed <= obstacle.x + obstacle.width and self.x + self.width - self.speed >= obstacle.x + obstacle.width) and \
                not (self.y + self.height <= obstacle.y or self.y >= obstacle.y + obstacle.height):
                return True
        return False

    def collision_right(self):
        for obstacle in game_objects.obstacles:
            if (self.x + self.width + self.speed >= obstacle.x and self.x + self.width + self.speed <= obstacle.x + obstacle.width) and \
                not (self.y + self.height <= obstacle.y or self.y >= obstacle.y + obstacle.height):
                return True
        return False
