import pygame
import random

WIDTH = 30
HEIGHT = 30
DIMENSION = 20

pygame.init()

WIN = pygame.display.set_mode((WIDTH * DIMENSION, HEIGHT * DIMENSION))
pygame.display.set_caption("AI Plays Snake")


class Snake:

    def __init__(self):
        #tile coordinates
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.body = []

        self.move = "RIGHT"

        #add three cubes to the body
        self.body.append(Cube(self.x, self.y))
        self.body.append(Cube(self.x - 1, self.y))
        self.body.append(Cube(self.x - 2, self.y))

    def move_to(self, direction):
        if direction == "LEFT":
            if self.move == "UP":
                temp = Cube(self.x - 1, self.y)
                self.body.insert(0, temp)
                self.x -= 1
                self.move = "LEFT"
            elif self.move == "DOWN":
                temp = Cube(self.x + 1, self.y)
                self.body.insert(0, temp)
                self.x += 1
                self.move = "RIGHT"
            elif self.move == "LEFT":
                temp = Cube(self.x, self.y + 1)
                self.body.insert(0, temp)
                self.y += 1
                self.move = "DOWN"
            else:
                temp = Cube(self.x, self.y - 1)
                self.body.insert(0, temp)
                self.y -= 1
                self.move = "UP"
        elif direction == "RIGHT":
            if self.move == "UP":
                temp = Cube(self.x + 1, self.y)
                self.body.insert(0, temp)
                self.x += 1
                self.move = "RIGHT"
            elif self.move == "DOWN":
                temp = Cube(self.x - 1, self.y)
                self.body.insert(0, temp)
                self.x -= 1
                self.move = "LEFT"
            elif self.move == "LEFT":
                temp = Cube(self.x, self.y - 1)
                self.body.insert(0, temp)
                self.y -= 1
                self.move = "UP"
            else:
                temp = Cube(self.x, self.y + 1)
                self.body.insert(0, temp)
                self.y += 1
                self.move = "DOWN"
        else:
            if self.move == "UP":
                temp = Cube(self.x, self.y - 1)
                self.body.insert(0, temp)
                self.y -= 1
            elif self.move == "DOWN":
                temp = Cube(self.x, self.y + 1)
                self.body.insert(0, temp)
                self.y += 1
            elif self.move == "LEFT":
                temp = Cube(self.x - 1, self.y)
                self.body.insert(0, temp)
                self.x -= 1
            else:
                temp = Cube(self.x + 1, self.y)
                self.body.insert(0, temp)
                self.x += 1

        del self.body[len(self.body) - 1]

    # change direction only if next move is different and not the opposite of move
    def translate(self):
        if self.move == "UP":
            # temp = Cube(self.x, self.y - 1)
            # self.body.insert(0, temp)
            # self.y -= 1
            if not self.anti_gliche():
                temp = Cube(self.x, self.y - 1)
                self.body.insert(0, temp)
                self.y -= 1
            else:
                self.move = "DOWN"

        if self.move == "DOWN":
            # temp = Cube(self.x, self.y + 1)
            # self.body.insert(0, temp)
            # self.y += 1
            if not self.anti_gliche():
                temp = Cube(self.x, self.y + 1)
                self.body.insert(0, temp)
                self.y += 1
            else:
                self.move = "UP"
                temp = Cube(self.x, self.y - 1)
                self.body.insert(0, temp)
                self.y -= 1

        if self.move == "LEFT":
            # temp = Cube(self.x - 1, self.y)
            # self.body.insert(0, temp)
            # self.x -= 1
            if not self.anti_gliche():
                temp = Cube(self.x - 1, self.y)
                self.body.insert(0, temp)
                self.x -= 1
            else:
                self.move = "RIGHT"

        if self.move == "RIGHT":
            # temp = Cube(self.x + 1, self.y)
            # self.body.insert(0, temp)
            # self.x += 1
            if not self.anti_gliche():
                temp = Cube(self.x + 1, self.y)
                self.body.insert(0, temp)
                self.x += 1
            else:
                self.move = "LEFT"
                temp = Cube(self.x - 1, self.y)
                self.body.insert(0, temp)
                self.x -= 1

        del self.body[len(self.body)-1]

    def grow_to(self, direction):
        if direction == "LEFT":
            if self.move == "UP":
                temp = Cube(self.x - 1, self.y)
                self.body.insert(0, temp)
                self.x -= 1
            elif self.move == "DOWN":
                temp = Cube(self.x + 1, self.y)
                self.body.insert(0, temp)
                self.x += 1
            elif self.move == "LEFT":
                temp = Cube(self.x, self.y + 1)
                self.body.insert(0, temp)
                self.y += 1
            else:
                temp = Cube(self.x, self.y - 1)
                self.body.insert(0, temp)
                self.y -= 1
        elif direction == "RIGHT":
            if self.move == "UP":
                temp = Cube(self.x + 1, self.y)
                self.body.insert(0, temp)
                self.x += 1
            elif self.move == "DOWN":
                temp = Cube(self.x - 1, self.y)
                self.body.insert(0, temp)
                self.x -= 1
            elif self.move == "LEFT":
                temp = Cube(self.x, self.y - 1)
                self.body.insert(0, temp)
                self.y -= 1
            else:
                temp = Cube(self.x, self.y + 1)
                self.body.insert(0, temp)
                self.y += 1
        else:
            if self.move == "UP":
                temp = Cube(self.x, self.y - 1)
                self.body.insert(0, temp)
                self.y -= 1
            elif self.move == "DOWN":
                temp = Cube(self.x, self.y + 1)
                self.body.insert(0, temp)
                self.y += 1
            elif self.move == "LEFT":
                temp = Cube(self.x - 1, self.y)
                self.body.insert(0, temp)
                self.x -= 1
            else:
                temp = Cube(self.x + 1, self.y)
                self.body.insert(0, temp)
                self.x += 1

    def grow(self):
        if self.move == "UP":
            temp = Cube(self.x, self.y - 1)
            self.body.insert(0, temp)
            self.y -= 1

        if self.move == "DOWN":
            temp = Cube(self.x, self.y + 1)
            self.body.insert(0, temp)
            self.y += 1

        if self.move == "LEFT":
            temp = Cube(self.x - 1, self.y)
            self.body.insert(0, temp)
            self.x -= 1

        if self.move == "RIGHT":
            temp = Cube(self.x + 1, self.y)
            self.body.insert(0, temp)
            self.x += 1

    def anti_gliche(self):
        if self.move == "UP":
            if self.x == self.body[1].xPos and self.y - 1 == self.body[1].yPos:
                return True

        if self.move == "DOWN":
            if self.x == self.body[1].xPos and self.y + 1 == self.body[1].yPos:
                return True

        if self.move == "LEFT":
            if self.x - 1 == self.body[1].xPos and self.y == self.body[1].yPos:
                return True

        if self.move == "RIGHT":
            if self.x + 1 == self.body[1].xPos and self.y == self.body[1].yPos:
                return True

        return False

    def detect_self_collision(self, x, y):
        for i in range(len(self.body)):
            if x == self.body[i].xPos and y == self.body[i].yPos:
                return True
        return False

    def wall_collision(self):
        if self.x < 0:
            return True
        if self.x >= WIDTH:
            return True
        if self.y < 0:
            return True
        if self.y >= HEIGHT:
            return True
        return False

    def self_collision(self):
        for i in range(1, len(self.body)):
            if self.x == self.body[i].xPos and self.y == self.body[i].yPos:
                return True
        return False

    def food_collision(self, food):
        if self.x == food.x and self.y == food.y:
            return True
        return False

    def draw(self, frame):
        for cube in self.body:
            cube.draw(frame)

    def up(self):
        self.move = "UP"

    def down(self):
        self.move = "DOWN"

    def left(self):
        self.move = "LEFT"

    def right(self):
        self.move = "RIGHT"


class Food:

    def __init__(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(0, HEIGHT - 1)
        self.color = (255, 0, 0)

    def spawn(self, player):
        onSnake = True

        while onSnake:
            onSnake = False

            self.x = random.randint(0, WIDTH - 1)
            self.y = random.randint(0, HEIGHT - 1)

            for cube in player.body:
                if self.x == cube.xPos and self.y == cube.yPos:
                    onSnake = True

    def draw(self, frame):
        pygame.draw.rect(frame, self.color, (self.x * DIMENSION, self.y * DIMENSION, DIMENSION, DIMENSION))


class Cube:

    def __init__(self, x, y, c = (0, 50, 255)):
        #tiles
        self.xPos = x
        self.yPos = y
        self.color = c

    def draw(self, frame):
        pygame.draw.rect(frame, self.color, (self.xPos * DIMENSION, self.yPos * DIMENSION, DIMENSION, DIMENSION))
