import random


class Participants(object):
    def __init__(self):
        self.storage = []
        self.storage_limit = 0
        self.name = ''

    def presentation(self):
        view = ''
        for card in self.storage:
            view += '/{}/ '.format(card.label())
        print("{} has: {}".format(self.name, view))

    def get_card(self, cards):
        if len(self.storage) < self.storage_limit:
            self.storage += cards
        else:
            print('You are trying to get too many cards ')


class Desk(Participants):

    def __init__(self):
        super().__init__()
        self.storage_limit = 5
        self.name = 'Desk'


class Player(Participants):
    def __init__(self, name):
        super().__init__()
        self.storage_limit = 2
        self.name = name
        self.combination = ()


class Card(object):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def label(self):
        suits = {'hearts': '♥', 'spades': '♠', 'diamonds': '♦', 'clubs': '♣'}
        values = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: '10', 9: 'Jack', 10: 'Queen',
                  11: 'King', 12: 'Ace'}

        if self.value in values and self.suit in suits:
            return '{} {}'. format(values[self.value], suits[self.suit])


class Deck(object):
    def __init__(self):
        self.cards = []
        self.suits = ['hearts', 'spades', 'diamonds', 'clubs']

    def generate(self):
        for suits in self.suits:
            for i in range(13):
                c = Card(suits, i)
                self.cards += [c]

    def shake(self):
        random.shuffle(self.cards)

    def pass_off_card(self, q=1):
        res = []
        while q > 0:
            res += [self.cards.pop(0)]
            q = q - 1
        return res


def combination_checker(player, desk):

    cards = []
    suits = []
    for card in player.storage + desk.storage:
        cards += card.value
        suits += card.suit

    for suit in Deck().suits:
        for card_suit in suits:
            if card_suit == suit:
                suits += card.sut
            if len(suits) > 5:
                for val in list(range(8, 13)):
                    if val not in cards:

                    player.combination = 11, 'Royal Flush'
                elif







