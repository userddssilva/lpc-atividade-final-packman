import time

import pygame
from pygame import Vector2

import random

from game_object import GameObject
from settings import *


class Enemy(GameObject):
    def __init__(self, app, pos, number):
        super().__init__(app, pos)

        self.number = number
        self.colour = self.set_colour()
        self.personality = self.set_personality()

        self.sprites = []
        self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_up_1.png'))
        self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_up_2.png'))
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.radius = self.image.get_width() / 2

        self.direction = Vector2(0, 0)
        self.target = None
        self.speed = self.set_speed()

        self.first_time = time.time()
        self.second_time = None

    def update(self):
        self.change_speed()
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1

        # sprites animation
        if self.direction == (0, -1):
            self.sprites.clear()
            self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_up_1.png'))
            self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_up_2.png'))

        if self.direction == (0, 1):
            self.sprites.clear()
            self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_down_1.png'))
            self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_down_2.png'))

        if self.direction == (-1, 0):
            self.sprites.clear()
            self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_left_1.png'))
            self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_left_2.png'))

        if self.direction == (1, 0):
            self.sprites.clear()
            self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_right_1.png'))
            self.sprites.append(pygame.image.load('Sprites/Ghosts/' + self.colour + '_right_2.png'))

        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

    def change_speed(self):
        # check if is red ghost and change him speed
        if self.number == 0 and self.speed < 2:
            self.second_time = time.time()
            if self.second_time - self.first_time >= 10:
                self.first_time = self.second_time
                self.speed = 2
                print(self.speed)

    def draw(self):
        self.app.screen.blit(self.image, ((int(self.pix_pos.x) - self.radius), (int(self.pix_pos.y) - self.radius)))

    def set_speed(self):
        # if self.number == 0:
        #     return 1
        # elif self.number == 1:
        #     return 1
        # elif self.number == 2:
        #     return 1
        # elif self.number == 3:
        #     return 1
        # elif self.number == 4:
        return 1

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return Vector2(1, 1)
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] < ROWS // 2:
                return Vector2(1, ROWS - 2)
            if self.app.player.grid_pos[0] < COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return Vector2(COLS - 2, 1)
            else:
                return Vector2(COLS - 2, ROWS - 2)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0) or self.direction == Vector2(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1) or self.direction == Vector2(0, 0):
                return True

        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]

        return Vector2(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])

        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for _ in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1

        queue = [start]
        path = []
        visited = []

        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])

        return shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1

            next_pos = Vector2(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)

            if next_pos not in self.app.walls:
                break
            
        return Vector2(x_dir, y_dir)

    def get_pix_pos(self):
        return Vector2((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 +
                   self.app.cell_height // 2)

    def set_colour(self):
        if self.number == 0:
            return 'red'
        if self.number == 1:
            return 'pink'
        if self.number == 2:
            return 'blue'
        if self.number == 3:
            return 'orange'

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"         
        else:
            return "scared"
