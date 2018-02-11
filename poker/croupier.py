from functools import reduce
from instances import Deck


def input_number(text):
    while True:
        try:
            n = int(input(text))
            while 0 <= n > 10:
                print('Wrong input, too much or too less')
                n = int(input(text))
            return n
        except ValueError as err:
            print('Wrong input: ', err, '\n try again')


def sequence_gen(largest_num):
    x = largest_num
    while x > 0:
        yield x, x + 5
        x -= 1


def combination_checker(player, desk):
    total = player.storage + desk.storage
# ищем комбинации Флеша
    for suit in Deck().suits:
        cards_with_same_suits = list(filter(lambda card: card.suit == suit, total))
        if len(cards_with_same_suits) > 5:
            val_with_same_suits = list(map(lambda card: card.value, cards_with_same_suits))
            if sorted(val_with_same_suits[:5]) == list(range(8, 13)):
                return 'Royal Flush', 11, 12  # название комбинации, ее старшинство и старшая карта
            for seq in sequence_gen(12):
                if reduce(lambda a, b: a and b, map(lambda val: val in val_with_same_suits, range(*seq))):
                    return 'Straight Flush', 10, max(val_with_same_suits)
                else:
                    return 'Flush', 7, max(val_with_same_suits)
# ищем Каре и Фулхаус
    for val_first in range(13):
        cards_with_same_value = list(filter(lambda card: card.value is val_first, total))
        if len(cards_with_same_value) == 4:
            return 'Four of a Kind', 9, val_first
        elif len(cards_with_same_value) == 3:
            for val_second in range(13):
                if len(list(filter(lambda card: card.value is val_second, total))) == 2:
                    return 'Full House', 8, val_first
# ищем стрит
    for seq in sequence_gen(13):
        if reduce(lambda a, b: a and b, map(lambda val: val in list(map(lambda card: card.value, total)), range(*seq))):
            return 'Straight', 6, max(*seq)
# ищем тройку
    for val in range(13):
        cards_with_same_value = list(filter(lambda card: card.value is val, total))
        if len(cards_with_same_value) == 3:
            return 'Three of a Kind', 5, val
# ищем две пары или пару
    for val_first in range(13):
        first_pair = list(filter(lambda card: card.value is val_first, total))
        if len(first_pair) == 2:
            for val_second in range(13):
                second_pair = list(filter(lambda card: card.value is val_second, total))
                if len(second_pair) == 2 and val_second != val_first:
                    return 'Two-pair', 4, max(val_first, val_second)
            return 'One-pair', 3, val_first
# если ничего нет, возвращаем старшую карту
    return 'High-card', 2, max(map(lambda card: card.value is val_first, total))
