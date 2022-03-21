import pygame
import sys
from pygame import Vector2
import random

pygame.init()
cell_size = 20
cell_number = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))
pygame.display.set_caption("SNAKE")
pygame.display.set_icon(pygame.image.load(r'C:\Users\Divyanshu\Desktop\Snake\snakes.png'))
apple = pygame.image.load(r'C:\Users\Divyanshu\Desktop\Snake\apple.png').convert_alpha()


class Button:
    def __init__(self):
        self.image_reload = pygame.image.load(r'C:\Users\Divyanshu\Desktop\Snake\reload.png')
        self.image_exit = pygame.image.load(r'C:\Users\Divyanshu\Desktop\Snake\exit.png')

    def draw(self):
        screen.blit(self.image_reload, (4*cell_size, 4*cell_size))


class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def random(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1, 0)
        self.grow = False

    def draw(self):
        for block in self.body:
            snake_rect = pygame.Rect(int(block.x*cell_size), int(block.y*cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (196, 112, 160), snake_rect)

    def move(self):
        main.collision()
        if self.grow is True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.grow = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy


class Main:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()
        self.button = Button()
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def update(self):
        self.snake.move()
        self.collision()
        self.check()

    def draw(self):
        self.fruit.draw()
        self.snake.draw()

    def collision(self):
        if 0 > self.snake.body[0].x:
            self.snake.body[0].x = cell_number
        if cell_number < self.snake.body[0].x:
            self.snake.body[0].x = 0
        if 0 > self.snake.body[0].y:
            self.snake.body[0].y = cell_number
        if cell_number < self.snake.body[0].y:
            self.snake.body[0].y = 0
        if self.fruit.pos == self.snake.body[0]:
            self.snake.grow = True
            self.fruit.random()
            self.score += 1
        for block in self.snake.body[2:]:
            if block == self.fruit.pos:
                self.fruit.random()

    def scores(self):
        score = self.font.render("SCORE: " + str(self.score), True, (255, 255, 255))
        screen.blit(score, (0, 0))

    def game_over(self):
        game = self.font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game, (150, 150))

    def check(self):
        for block in self.snake.body[3:]:
            if block == self.snake.body[0]:
                pygame.quit()
                sys.exit()


screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)
main = Main()
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if events.type == screen_update:
            main.update()
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_UP or events.key == pygame.K_w:
                main.snake.direction = Vector2(0, -1)
            if events.key == pygame.K_DOWN or events.key == pygame.K_s:
                main.snake.direction = Vector2(0, 1)
            if events.key == pygame.K_RIGHT or events.key == pygame.K_a:
                main.snake.direction = Vector2(-1, 0)
            if events.key == pygame.K_LEFT or events.key == pygame.K_d:
                main.snake.direction = Vector2(1, 0)

    screen.fill((166, 190, 120))
    main.draw()
    main.scores()
    pygame.display.update()
