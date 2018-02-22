from random import randint, shuffle
from functools import reduce


def get_point(some):
    point = (randint(0, 9), randint(0, 9))
    if point in some:
        return get_point(some)
    return point


class Battleship:
    name = 'Battleship'
    label = 'B'
    length = 4

    def __init__(self, abandoned):

        self.coordinates = self.builder(abandoned)
        if self.coordinates is not False:
            self.abandoned_coordinates = self.abandoned_checker()
            self.is_alive = True

    def abandoned_checker(self):
        res = []
        x_max, y_max = max(self.coordinates)
        x_min, y_min = min(self.coordinates)
        for x in range(x_min - 1, x_max + 2):
            for y in range(y_min - 1, y_max + 2):
                res += [(x, y)]
        res = list(filter(lambda point: -1 < point[0] < 10 and -1 < point[1] < 10, res))
        return res

    def builder(self, abandoned):
        if self.length is 1:
            res = [get_point(abandoned)]
            # print(self.name, 'have been created in ', res)
            return res

        first_p = get_point(abandoned)
        finish_point_and_way = [
            #           x                   y                       gen                                   way
            ((first_p[0] + self.length, first_p[1]), map(lambda x: first_p[0] + x, range(0, self.length)), 'v'),
            ((first_p[0] - self.length, first_p[1]), map(lambda x: first_p[0] - x, range(0, self.length)), 'v'),
            ((first_p[0], first_p[1] + self.length), map(lambda y: first_p[1] + y, range(0, self.length)), 'h'),
            ((first_p[0], first_p[1] - self.length), map(lambda y: first_p[1] - y, range(0, self.length)), 'h')
        ]
        finish_point_and_way = list(filter(lambda fpnw: fpnw[0] not in abandoned, finish_point_and_way))
        finish_point_and_way = list(filter(lambda fpnw: -1 < fpnw[0][0] < 10 and -1 < fpnw[0][1] < 10,
                                           finish_point_and_way))
        if len(finish_point_and_way) < 1:
            return self.builder(abandoned)
        else:
            shuffle(finish_point_and_way)
            fp, gen, way = finish_point_and_way.pop()
            if way == 'v':
                res = list(zip(gen, [first_p[1]] * self.length))
            elif way == 'h':
                res = list(zip([first_p[0]] * self.length, gen))
            # print(self.name, 'have been created in ', res)
            return res

    def alive_checker(self, moves, opponent):
        if reduce(lambda a, b: a and b, map(lambda t: t in moves, self.coordinates)):
            self.is_alive = False
            print('{} have been destroyed'.format(self.name))
            for coordinate in self.abandoned_coordinates:
                opponent.field[coordinate[0]][coordinate[1]] = 'x'
                moves.update([coordinate])
                # print(moves)
            for coordinate in self.coordinates:
                opponent.field[coordinate[0]][coordinate[1]] = 'X'


class Cruiser(Battleship):

    name = 'Cruiser'
    label = 'C'
    length = 3


class Destroyer(Battleship):

    name = 'Destroyer'
    label = 'D'
    length = 2


class Submarine(Battleship):

    name = 'Submarine'
    label = 'S'
    length = 1
