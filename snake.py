import pygame
import math
import random 
import time
import sys

WIDTH = 642
HIGHT = 640
PIXELS = 40
SQUARES = int(WIDTH/PIXELS)
BG1 = (0, 0, 0)
BG2 = (0, 0, 0)
#APPLE_COLOR_1 = (0, 193, 174)
#APPLE_COLOR_2 = (234, 255, 0)
SNAKE_COLOR = (255, 2, 255)
BODY_COLOR = (110, 0, 90)
LABEL_COLOR = (255, 255, 255)
class Snake:
    def __init__(self):
        self.color = SNAKE_COLOR
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HIGHT, PIXELS)
        self.state = 'STOP'
        self.bodies = []
        self.body_color = 102
    def move(self):
        if self.state == 'UP':
            self.headY -= PIXELS
        elif self.state == 'DOWN':
            self.headY += PIXELS
        elif self.state == 'RIGHT':
            self.headX += PIXELS
        elif self.state == 'LEFT':
            self.headX -= PIXELS
    def move_body(self):
        if len(self.bodies) > 0:
            for i in range (len(self.bodies)-1 , -1 , -1):
                if i == 0:
                    self.bodies[0].posX = self.headX 
                    self.bodies[0].posY = self.headY 
                else: 
                    self.bodies[i].posX = self.bodies[i-1].posX 
                    self.bodies[i].posY = self.bodies[i-1].posY
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.headX, self.headY, PIXELS, PIXELS))
        if len(self.bodies) > 0:
            for body in self.bodies:
                pygame.draw.rect(surface, body.color, (body.posX, body.posY, PIXELS, PIXELS))

    def add_body(self):
        self.body_color += 5
        body = Body((255, self.body_color , 186), self.headX, self.headY)
        self.bodies.append(body)
    def die(self): 
        self.state = 'STOP'
        self.bodies = []
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HIGHT, PIXELS)
        self.body_color = 50

class Apple:
    def __init__(self):
        self.color = (random.randint(150,255),random.randint(150,255),random.randint(150,255))
    def spawn(self):
        self.color = (random.randint(150,255),random.randint(150,255),random.randint(150,255))
        self.posX = random.randrange(0, WIDTH, PIXELS)
        self.posY = random.randrange(0, HIGHT, PIXELS)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))   

class Background:
    def draw(self, surface):
        surface.fill(BG1)
        counter = 0
        for row in range(SQUARES):
            for col in range(SQUARES):
                if counter % 2 == 0:
                    pygame.draw.rect( surface, BG2 , (col*PIXELS, row*PIXELS, PIXELS, PIXELS))
                if col != SQUARES-1:
                    counter += 1

class Body:
    def __init__(self, color, posX, posY):
        self.color = color
        self.posX = posX 
        self.posY = posY
    def draw(self, surface):
        pygame.draw.rect (surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))

class Colission:
    def between_head_and_body(self, snake):
        for body in snake.bodies:
            distance = math.sqrt( math.pow(snake.headX - body.posX, 2 ) + math.pow(snake.headY - body.posY , 2))
            if distance < PIXELS:
                return True
        return False
    def between_snake_and_walls(self, snake):
        if snake.headX < 0 or snake.headX > WIDTH- PIXELS or snake.headY < 0 or snake.headY > HIGHT - PIXELS:
            return True
        return False
    def between_snake_and_apple(self, snake, apple):
        distance = math.sqrt( math.pow(snake.headX - apple.posX, 2 ) + math.pow(snake.headY - apple.posY , 2))
        return distance < PIXELS

class Score:
    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont('monospace', 30, bold=False)
    def increase(self):
        self.points += 1
    def reset(self):
        self.points = 0
    def show(self, surface):
        lbl = self.font.render('Score: ' + str(self.points), 1, LABEL_COLOR)
        surface.blit(lbl, (5,5))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HIGHT))
    pygame.display.set_caption("snake")

    background = Background()
    apple = Apple()
    snake = Snake()
    score = Score()
    colission = Colission()
    apple.spawn()
    #main loop:
    while True:
        background.draw(screen)
        apple.draw(screen)
        snake.draw(screen)
        score.show(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.state != 'DOWN':
                    snake.state = 'UP'
                if event.key == pygame.K_DOWN and snake.state != 'UP':
                    snake.state = 'DOWN'
                if event.key == pygame.K_RIGHT and snake.state != 'LEFT':
                    snake.state = 'RIGHT'
                if event.key == pygame.K_LEFT and snake.state != 'RIGHT':
                    snake.state = 'LEFT'
                if event.key == pygame.K_p:
                    snake.state = 'STOP'
        
        if colission.between_snake_and_apple(snake, apple):
            apple.spawn()
            snake.add_body()
            score.increase()
        if snake.state != 'STOP':
            snake.move_body()
            snake.move()
        if colission.between_snake_and_walls(snake):
            snake.die()
            apple.spawn() 
            score.reset()
        if colission.between_head_and_body(snake):
            snake.die()
            apple.spawn()
            score.reset()
        pygame.time.delay(120)
        pygame.display.update()

main()