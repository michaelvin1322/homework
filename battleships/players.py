from random import randint
from functools import reduce
from ships import Battleship, Cruiser, Destroyer, Submarine


class Field:

    @staticmethod
    def print_field(computer_field, player_field):
        row = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
        header = '|' + '|'.join(map(lambda n: ' ' + str(n) + ' ', list(range(1, 10)))) + '| 10|'
        intercourse = '+---' * 10 + '++-++' + '---+' * 10

        print(header + '| |' + header)
        print(intercourse)
        for l in range(0, 10):
            print('| ' + ' | '.join(computer_field[l]) + ' ||' + row[l] + '|| ' + ' | '.join(player_field[l]) + ' |')
            print(intercourse)


class Participant:
    def __init__(self):
        self.storage = []
        self.abandoned = set()
        self.moves = set()
        self.field = [[' '] * 10]
        for i in range(9):
            self.field += [[' '] * 10]

        self.get_ship(Battleship, 1)
        self.get_ship(Cruiser, 2)
        self.get_ship(Destroyer, 3)
        self.get_ship(Submarine, 4)
        self.ships = reduce(lambda a, b: a + b, map(lambda ship: ship.coordinates, self.storage))
        self.name = 'Noname'

    def get_ship(self, ship_class, quantity):
        for i in range(quantity):
            ship = ship_class(self.abandoned)

            self.storage += [ship]
            ab_in_total = ship.abandoned_coordinates + ship.coordinates
            for p in ab_in_total:
                self.abandoned.update([p])

    def view(self):
        for ship in self.storage:
            for coordinates in ship.coordinates:
                x, y = coordinates
                self.field[x][y] = ship.label

    def input_coordinates(self):
        pass

    def strike(self, opponent):
        p = self.input_coordinates()
        self.moves.update([p])
        print('{} strikes in {}'.format(self.name, p))

        if p in opponent.ships:
            print('GOT! ')
            opponent.field[p[0]][p[1]] = 'X'
            for i, ship in enumerate(opponent.storage):
                ship.alive_checker(self.moves, opponent)
                if ship.is_alive is False:
                    opponent.storage.pop(i)
            Field.print_field(opponent.field, self.field)
            if len(opponent.storage) == 0:
                pass
            else:
                self.strike(opponent)
        else:
            print('Past..')
            opponent.field[p[0]][p[1]] = 'x'


class Player(Participant):
    an_t = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}

    def __init__(self):
        super().__init__()
        self.view()
        self.name = 'Human'

    def input_coordinates(self):
        def inp_num():
            try:
                y = int(input('Type column: ').lower().replace(' ', ''))
                while y not in range(1, 11):
                    y = int(input('Type column: ').lower().replace(' ', ''))
            except:
                print('Must be a integer number!')
                return inp_num()
            return y

        x = input('Type line: ').lower().replace(' ', '')
        while x not in self.an_t.keys():
            x = input('Type line: ').lower().replace(' ', '')
        if x in self.an_t.keys():
            x = self.an_t[x]

        y = inp_num()

        p = (x, y-1)

        while p in self.moves:
            print("You've strike in this point. Try other!")
            p = self.input_coordinates()

        return p


class Computer(Participant):
    def __init__(self):
        super().__init__()
        self.name = 'Computer'

    def input_coordinates(self):
        p = (randint(0, 9), randint(0, 9))
        while p in self.moves:
            p = (randint(0, 9), randint(0, 9))
        return p
