import neat
import os
import pygame
import pygame.freetype
import pickle
import random

from math import atan2
from GameFile import Snake
from GameFile import Food

pygame.init()

WIDTH = 30 
HEIGHT = 30
DIMENSION = 20


WIN = pygame.display.set_mode((WIDTH * DIMENSION, HEIGHT * DIMENSION))
pygame.display.set_caption("AI Plays Snake")

FONT = pygame.font.SysFont('Comic Sans MS', 30)


def draw(players, foods, show):
    WIN.fill((0, 0, 0))

    for food in foods:
        food.draw(WIN)

    for player in players:
        player.draw(WIN)

    if show:
        score = len(players[0].body) - 3
        text = FONT.render("Score: " + str(score), False, (220, 0, 0))
        WIN.blit(text, (10, 10))

    pygame.display.update()

def draw_single(player, food):
    WIN.fill((0, 0, 0))

    player.draw(WIN)
    food.draw(WIN)

    pygame.display.update()


def update(players, foods, networks, genomes, counter, show):

    # 1 can i move front?
    # 2 can i move left?
    # 3 can i move right?
    # angle to food

    # 1-3 distance to wall for each direction
    # 4-6 distance to self for each direction
    # 7-8 x and y difference

    # 1 turn left
    # 2 turn right

    for i, player in enumerate(players):

        f_dist = 0
        l_dist = 0
        r_dist = 0

        temp_x = player.x
        temp_y = player.y

        # forward
        if player.move == "UP":  # facing up
            temp_y -= 1
            while not detect_wall_collision(temp_x, temp_y):
                f_dist += 1
                temp_y -= 1
        elif player.move == "DOWN":  # facing down
            temp_y += 1
            while not detect_wall_collision(temp_x, temp_y):
                f_dist += 1
                temp_y += 1
        elif player.move == "LEFT":  # facing left
            temp_x -= 1
            while not detect_wall_collision(temp_x, temp_y):
                f_dist += 1
                temp_x -= 1
        else:                        # facing right
            temp_x += 1
            while not detect_wall_collision(temp_x, temp_y):
                f_dist += 1
                temp_x += 1

        temp_x = player.x
        temp_y = player.y
        # leftward
        if player.move == "RIGHT":  # facing right
            temp_y -= 1
            while not detect_wall_collision(temp_x, temp_y):
                l_dist += 1
                temp_y -= 1
        elif player.move == "LEFT":  # facing left
            temp_y += 1
            while not detect_wall_collision(temp_x, temp_y):
                l_dist += 1
                temp_y += 1
        elif player.move == "UP":  # facing up
            temp_x -= 1
            while not detect_wall_collision(temp_x, temp_y):
                l_dist += 1
                temp_x -= 1
        else:                        # facing down
            temp_x += 1
            while not detect_wall_collision(temp_x, temp_y):
                l_dist += 1
                temp_x += 1

        temp_x = player.x
        temp_y = player.y
        # rightward
        if player.move == "LEFT":  # facing left
            temp_y -= 1
            while not detect_wall_collision(temp_x, temp_y):
                r_dist += 1
                temp_y -= 1
        elif player.move == "RIGHT":  # facing right
            temp_y += 1
            while not detect_wall_collision(temp_x, temp_y):
                r_dist += 1
                temp_y += 1
        elif player.move == "DOWN":  # facing down
            temp_x -= 1
            while not detect_wall_collision(temp_x, temp_y):
                r_dist += 1
                temp_x -= 1
        else:  # facing up
            temp_x += 1
            while not detect_wall_collision(temp_x, temp_y):
                r_dist += 1
                temp_x += 1

        f_self = 0
        l_self = 0
        r_self = 0

        temp_x = player.x
        temp_y = player.y

        # forward
        if player.move == "UP":  # facing up
            temp_y -= 1
            while temp_y >= 0 and not player.detect_self_collision(temp_x, temp_y):
                f_self += 1
                temp_y -= 1
        elif player.move == "DOWN":  # facing down
            temp_y += 1
            while temp_y < HEIGHT and not player.detect_self_collision(temp_x, temp_y):
                f_self += 1
                temp_y += 1
        elif player.move == "LEFT":  # facing left
            temp_x -= 1
            while temp_x >= 0 and not player.detect_self_collision(temp_x, temp_y):
                f_self += 1
                temp_x -= 1
        else:  # facing right
            temp_x += 1
            while temp_x < WIDTH and not player.detect_self_collision(temp_x, temp_y):
                f_self += 1
                temp_x += 1

        temp_x = player.x
        temp_y = player.y
        # leftward
        if player.move == "RIGHT":  # facing right
            temp_y -= 1
            while temp_y >= 0 and not player.detect_self_collision(temp_x, temp_y):
                l_self += 1
                temp_y -= 1
        elif player.move == "LEFT":  # facing left
            temp_y += 1
            while temp_y < HEIGHT and not player.detect_self_collision(temp_x, temp_y):
                l_self += 1
                temp_y += 1
        elif player.move == "UP":  # facing up
            temp_x -= 1
            while temp_x >= 0 and not player.detect_self_collision(temp_x, temp_y):
                l_self += 1
                temp_x -= 1
        else:  # facing down
            temp_x += 1
            while temp_x < WIDTH and not player.detect_self_collision(temp_x, temp_y):
                l_self += 1
                temp_x += 1

        temp_x = player.x
        temp_y = player.y
        # rightward
        if player.move == "LEFT":  # facing left
            temp_y -= 1
            while temp_y >= 0 and not player.detect_self_collision(temp_x, temp_y):
                r_self += 1
                temp_y -= 1
        elif player.move == "RIGHT":  # facing right
            temp_y += 1
            while temp_y < HEIGHT and not player.detect_self_collision(temp_x, temp_y):
                r_self += 1
                temp_y += 1
        elif player.move == "DOWN":  # facing down
            temp_x -= 1
            while temp_x >= 0 and not player.detect_self_collision(temp_x, temp_y):
                r_self += 1
                temp_x -= 1
        else:  # facing up
            temp_x += 1
            while temp_x < WIDTH and not player.detect_self_collision(temp_x, temp_y):
                r_self += 1
                temp_x += 1



        # #experiment 1
        # angle = getAngle(player.x, player.y, foods[i].x, foods[i].y)
        # output = networks[i].activate((f_dist, l_dist, r_dist, angle))

        # #experiment 2
        # xDiff = foods[i].x - player.x
        # yDiff = foods[i].y - player.y

        # if not death and player == rand:
        #     print("xDiff: " + str(xDiff))
        #     print("yDiff: " + str(yDiff))

        # experiment 3
        food_u = 1
        food_d = 1
        food_l = 1
        food_r = 1
        food_ul = 1
        food_dl = 1
        food_ur = 1
        food_dr = 1

        food_x = foods[i].x
        food_y = foods[i].y

        if player.move == "UP":
            temp_x = player.x
            temp_y = player.y

            # check forward
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_y < 0:
                    food_u = 0
                    break
                food_u += 1
                temp_y -= 1

            temp_x = player.x
            temp_y = player.y

            # check backward
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_y >= HEIGHT:
                    food_d = 0
                    break
                food_d += 1
                temp_y += 1

            temp_x = player.x
            temp_y = player.y

            # check leftward
            temp_x -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0:
                    food_l = 0
                    break
                food_l += 1
                temp_x -= 1

            temp_x = player.x
            temp_y = player.y

            # check rightward
            temp_x += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH:
                    food_r = 0
                    break
                food_r += 1
                temp_x += 1

            # check up-left
            temp_x = player.x
            temp_y = player.y

            temp_x -= 1
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0 or temp_y < 0:
                    food_ul = 0
                    break
                food_ul += 1
                temp_x -= 1
                temp_y -= 1

            # check down-left
            temp_x = player.x
            temp_y = player.y

            temp_x -= 1
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0 or temp_y >= HEIGHT:
                    food_dl = 0
                    break
                food_dl += 1
                temp_x -= 1
                temp_y += 1

            # check up-right
            temp_x = player.x
            temp_y = player.y

            temp_x += 1
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH or temp_y < 0:
                    food_ur = 0
                    break
                food_ur += 1
                temp_x += 1
                temp_y -= 1

            # check down-right
            temp_x = player.x
            temp_y = player.y

            temp_x += 1
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH or temp_y >= HEIGHT:
                    food_dr = 0
                    break
                food_dr += 1
                temp_x += 1
                temp_y += 1

        elif player.move == "DOWN":
            temp_x = player.x
            temp_y = player.y

            # check backward
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_y < 0:
                    food_d = 0
                    break
                food_d += 1
                temp_y -= 1

            temp_x = player.x
            temp_y = player.y

            # check forward
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_y >= HEIGHT:
                    food_u = 0
                    break
                food_u += 1
                temp_y += 1

            temp_x = player.x
            temp_y = player.y

            # check rightward
            temp_x -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0:
                    food_r = 0
                    break
                food_r += 1
                temp_x -= 1

            temp_x = player.x
            temp_y = player.y

            # check left
            temp_x += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH:
                    food_l = 0
                    break
                food_l += 1
                temp_x += 1

            # check down-right
            temp_x = player.x
            temp_y = player.y

            temp_x -= 1
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0 or temp_y < 0:
                    food_dr = 0
                    break
                food_dr += 1
                temp_x -= 1
                temp_y -= 1

            # check up-right
            temp_x = player.x
            temp_y = player.y

            temp_x -= 1
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0 or temp_y >= HEIGHT:
                    food_ur = 0
                    break
                food_ur += 1
                temp_x -= 1
                temp_y += 1

            # check down-left
            temp_x = player.x
            temp_y = player.y

            temp_x += 1
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH or temp_y < 0:
                    food_dl = 0
                    break
                food_dl += 1
                temp_x += 1
                temp_y -= 1

            # check up-left
            temp_x = player.x
            temp_y = player.y

            temp_x += 1
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH or temp_y >= HEIGHT:
                    food_ul = 0
                    break
                food_ul += 1
                temp_x += 1
                temp_y += 1

        elif player.move == "LEFT":
            temp_x = player.x
            temp_y = player.y

            # check rightward
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_y < 0:
                    food_r = 0
                    break
                food_r += 1
                temp_y -= 1

            temp_x = player.x
            temp_y = player.y

            # check leftward
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_y >= HEIGHT:
                    food_l = 0
                    break
                food_l += 1
                temp_y += 1

            temp_x = player.x
            temp_y = player.y

            # check forward
            temp_x -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0:
                    food_u = 0
                    break
                food_u += 1
                temp_x -= 1

            temp_x = player.x
            temp_y = player.y

            # check backward
            temp_x += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH:
                    food_d = 0
                    break
                food_d += 1
                temp_x += 1

            # check up-right
            temp_x = player.x
            temp_y = player.y

            temp_x -= 1
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0 or temp_y < 0:
                    food_ur = 0
                    break
                food_ur += 1
                temp_x -= 1
                temp_y -= 1

            # check up-left
            temp_x = player.x
            temp_y = player.y

            temp_x -= 1
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0 or temp_y >= HEIGHT:
                    food_ul = 0
                    break
                food_ul += 1
                temp_x -= 1
                temp_y += 1

            # check down-right
            temp_x = player.x
            temp_y = player.y

            temp_x += 1
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH or temp_y < 0:
                    food_dr = 0
                    break
                food_dr += 1
                temp_x += 1
                temp_y -= 1

            # check down-left
            temp_x = player.x
            temp_y = player.y

            temp_x += 1
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH or temp_y >= HEIGHT:
                    food_dl = 0
                    break
                food_dl += 1
                temp_x += 1
                temp_y += 1
        else:
            temp_x = player.x
            temp_y = player.y

            # check leftward
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_y < 0:
                    food_l = 0
                    break
                food_l += 1
                temp_y -= 1

            temp_x = player.x
            temp_y = player.y

            # check rightward
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_y >= HEIGHT:
                    food_r = 0
                    break
                food_r += 1
                temp_y += 1

            temp_x = player.x
            temp_y = player.y

            # check backward
            temp_x -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0:
                    food_d = 0
                    break
                food_d += 1
                temp_x -= 1

            temp_x = player.x
            temp_y = player.y

            # check forward
            temp_x += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH:
                    food_u = 0
                    break
                food_u += 1
                temp_x += 1

            # check down-left
            temp_x = player.x
            temp_y = player.y

            temp_x -= 1
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0 or temp_y < 0:
                    food_dl = 0
                    break
                food_dl += 1
                temp_x -= 1
                temp_y -= 1

            # check down-right
            temp_x = player.x
            temp_y = player.y

            temp_x -= 1
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x < 0 or temp_y >= HEIGHT:
                    food_dr = 0
                    break
                food_dr += 1
                temp_x -= 1
                temp_y += 1

            # check up-left
            temp_x = player.x
            temp_y = player.y

            temp_x += 1
            temp_y -= 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH or temp_y < 0:
                    food_ul = 0
                    break
                food_ul += 1
                temp_x += 1
                temp_y -= 1

            # check up-right
            temp_x = player.x
            temp_y = player.y

            temp_x += 1
            temp_y += 1
            while temp_x != food_x or temp_y != food_y:
                if temp_x >= WIDTH or temp_y >= HEIGHT:
                    food_ur = 0
                    break
                food_ur += 1
                temp_x += 1
                temp_y += 1

        output = networks[i].activate((f_dist, l_dist, r_dist, f_self, l_self, r_self, food_u, food_d, food_l, food_r,
                                       food_ul, food_dl, food_ur, food_dr))

        direction = "FORWARD"

        if 0.5 < output[0]:
            direction = "LEFT"
        elif 0.5 < output[1]:
            direction = "RIGHT"

        if player.food_collision(foods[i]):
            if not show:
                genomes[i].fitness += 50
                counter[i] = 0
            foods[i].spawn(player)
            player.grow_to(direction)
        else:
            player.move_to(direction)


def getAngle(x1, y1, x2, y2):
    xDiff = x2 - x1
    yDiff = y2 - y1

    return atan2(yDiff, xDiff)


def detect_wall_collision(x, y):
    if x < 0:
        return True
    if x >= WIDTH:
        return True
    if y < 0:
        return True
    if y >= HEIGHT:
        return True

    return False


def main(genomes, config):
    run = True

    #parallel arrays

    players = []
    foods = []
    networks = []
    snake_genomes = []
    counter = []

    for id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(net)
        players.append(Snake())
        foods.append(Food())
        snake_genomes.append(genome)
        counter.append(0)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        update(players, foods, networks, snake_genomes, counter, False)
        # draw(players, foods, False)

        #game status
        for player in players:
            index = players.index(player)
            if snake_genomes[index].fitness >= 5000:
                outFile = open("best_snake.pickle", 'wb')
                pickle.dump(networks[index], outFile)
                outFile.close()

                run = False
                break

            if player.wall_collision() or player.self_collision() or counter[index] >= 300:
                del foods[index]
                del networks[index]
                del snake_genomes[index]
                del counter[index]
                del players[index]
            else:
                counter[index] += 1

        if len(players) <= 0:
            run = False



def show_case(network):
    run = True

    players = [Snake()]
    foods = [Food()]
    networks = [network]

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # **************** update ******************
        update(players, foods, networks, None, None, True)
        draw(players, foods, True)

        for player in players:

            if player.wall_collision() or player.self_collision():
                run = False
                break


def run(config_path):
    best = pickle.load(open("best_snake.pickle", 'rb'))

    show_case(best)

    # config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    #
    # population = neat.Population(config)
    #
    # population.add_reporter(neat.StdOutReporter(True))
    # population.add_reporter(neat.StatisticsReporter())
    #
    # winner = population.run(main, 1000)
    #
    # print('\nBest genome:\n{!s}'.format(winner))
    #
    # pygame.quit()
    # quit()

if __name__ == '__main__':
    dir = os.path.dirname(__file__)
    config_path = os.path.join(dir, 'config-feedforward.txt')
    run(config_path)