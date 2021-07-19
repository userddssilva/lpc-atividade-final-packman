import pygame
from pygame.math import Vector2

from game_object import GameObject
from settings import *


class Player(GameObject):
    def __init__(self, app, pos):
        super().__init__(app, pos)
        self.sprites = []
        self.sprites.append(pygame.image.load('Sprites/Pacman/idle.png'))
        self.sprites.append(pygame.image.load('Sprites/Pacman/right_1.png'))
        self.sprites.append(pygame.image.load('Sprites/Pacman/right_2.png'))
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.radius = self.image.get_width() / 2

        self.direction = Vector2(1, 0)
        self.stored_direction = None

        self.able_to_move = True

        self.current_score = 0
        self.high_score = 0
        self.speed = 2
        self.lives = 3

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed

        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction

            self.able_to_move = self.can_move()

        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1

        if self.on_coin():
            self.eat_coin()

        # update sprite animation
        self.current_sprite += 0.15
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

    def draw(self):
        self.app.screen.blit(self.image, ((int(self.pix_pos.x) - self.radius), (int(self.pix_pos.y) - self.radius)))

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, (255, 255, 0), (30 + 20 * x, HEIGHT - 15), 7)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0):
                    return True

            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1):
                    return True

        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

        sound = pygame.mixer.Sound('Sounds/munch_1.wav')
        sound.play()
            

    def move(self, direction):
        self.stored_direction = direction

        if direction == (0, -1):
            self.sprites.clear()
            self.sprites.append(pygame.image.load('Sprites/Pacman/idle.png'))
            self.sprites.append(pygame.image.load('Sprites/Pacman/up_1.png'))
            self.sprites.append(pygame.image.load('Sprites/Pacman/up_2.png'))

        if direction == (0, 1):
            self.sprites.clear()
            self.sprites.append(pygame.image.load('Sprites/Pacman/idle.png'))
            self.sprites.append(pygame.image.load('Sprites/Pacman/down_1.png'))
            self.sprites.append(pygame.image.load('Sprites/Pacman/down_2.png'))

        if direction == (-1, 0):
            self.sprites.clear()
            self.sprites.append(pygame.image.load('Sprites/Pacman/idle.png'))
            self.sprites.append(pygame.image.load('Sprites/Pacman/left_1.png'))
            self.sprites.append(pygame.image.load('Sprites/Pacman/left_2.png'))

        if direction == (1, 0):
            self.sprites.clear()
            self.sprites.append(pygame.image.load('Sprites/Pacman/idle.png'))
            self.sprites.append(pygame.image.load('Sprites/Pacman/right_1.png'))
            self.sprites.append(pygame.image.load('Sprites/Pacman/right_2.png'))

    def get_pix_pos(self):
        return Vector2((self.grid_pos[0] * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) +
                   TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == Vector2(1, 0) or self.direction == Vector2(-1, 0) or self.direction == Vector2(0, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == Vector2(0, 1) or self.direction == Vector2(0, -1) or self.direction == Vector2(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if Vector2(self.grid_pos + self.direction) == wall:
                return False
                
        return True
