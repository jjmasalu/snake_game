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
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def increment_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

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
        self.x = SIZE*random.randint(0, 24)
        self.y = SIZE*random.randint(0, 19)

    def draw(self):
        self.parent_screen.blit(self.image, (self.x,self.y))

    def move(self):
        self.x = SIZE * random.randint(0, 24)
        self.y = SIZE * random.randint(0, 19)


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

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):  # snake collides/eats apple
            self.apple.move()
            self.snake.increment_length()

        #  collision with the wall
        if self.snake.x[0] > 1000 or self.snake.x[0] < 0 or self.snake.y[0] > 800 or self.snake.y[0] < 0:
            raise Exception("Game Over")

        # snake bites itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Game Over")

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Game Over!\nYour Score is {self.snake.length-6}', True, (200, 200, 200))
        self.surface.blit(line1, (300, 300))
        line2 = font.render(f'press Enter to play again or escape to exit game', True, (200, 200, 200))
        self.surface.blit(line2, (200, 350))
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

    def reset(self):
        self.snake.length = 6
        self.snake.x = [SIZE] * self.snake.length
        self.snake.y = [SIZE] * self.snake.length
        self.snake.direction = 'down'

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        self.reset()
                    if not pause:
                        if self.snake.direction != 'down' and event.key == K_UP:
                            self.snake.move_up()
                        if self.snake.direction != 'up' and event.key == K_DOWN:
                            self.snake.move_down()
                        if self.snake.direction != 'right' and event.key == K_LEFT:
                            self.snake.move_left()
                        if self.snake.direction != 'left' and event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True

            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()
