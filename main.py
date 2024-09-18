import time

import pygame
from pygame.locals import *
import time
import numpy as np
import random
SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.length = 6
        self.block = pygame.image.load('resources/block.jpg').convert()
        self.x = [SIZE]*self.length
        self.y = [SIZE]*self.length
        self.direction = np.random.choice(['left', 'right', 'up', 'down'])

    def draw(self):
        self.parent_screen.fill((110, 110, 5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def increment_length(self):
        self.length += 1
        self.x.append(self.x[0])
        self.y.append(self.y[0])

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'right':
            self.x[0] += SIZE
            self.draw()
        elif self.direction == 'left':
            self.x[0] -= SIZE
            self.draw()
        elif self.direction == 'up':
            self.y[0] -= SIZE
            self.draw()
        elif self.direction == 'down':
            self.y[0] += SIZE
            self.draw()
        else:
            pass
        self.draw()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_down(self):
        self.direction = 'down'

    def move_up(self):
        self.direction = 'up'


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.parent_screen = parent_screen
        self.x = SIZE*random.randint(2, 24)
        self.y = SIZE*random.randint(2, 19)

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = SIZE * random.randint(2, 24)
        self.y = SIZE * random.randint(2, 19)


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.snake.draw()
        self.apple.draw()

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):  # snake collides with apple
            self.apple.move()
            self.snake.increment_length()

        for i in range(3, self.snake.length):  # snake bites itself
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Game Over!\nYour Score is {self.snake.length}', True, (200, 200, 200))
        self.surface.blit(line1, (500, 400))
        pygame.display.flip()

    def is_collision(self, x1, y1, x2, y2):
        if x2 == x1:  # vertical collision
            if (y2 == y1 - SIZE and self.snake.direction == 'up') or (y2 - SIZE == y1 and self.snake.direction == 'down'):
                return True
            elif y2 == y1:
                return True
        elif y2 == y1:  # horizontal collision
            if (x2 == x1 - SIZE and self.snake.direction == 'left') or (x2 -SIZE == x1 and self.snake.direction == 'right'):
                return True
            elif x2 == x1:
                return True
        else:
            return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length-6}', True, (200, 200, 200))
        self.surface.blit(score, (800, 10))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            try:
                self.play()
            except Exception as e:
                self.show_game_over()
                #running = False

            time.sleep(0.3)


if __name__ == '__main__':
    game = Game()
    game.run()
