from instances import Deck, Desk, Player
from croupier import combination_checker, input_number


desk = Desk()
deck = Deck()


deck.generate()
deck.shake()
players = []

total_players = input_number('How many players would play: ')
while len(players) < total_players:
    players += [Player(input('Player #{}, input your name: '.format(len(players) + 1)))]

list(map(lambda player: player.get_card(deck.pass_off_card(2)), players))     # раздаем всем игрокам карты

list(map(lambda player: player.presentation(), players))                      # показываем карты

list(map(lambda player: player.keep_playing(), players))                      # спрашиваем

players = list(filter(lambda player: player.in_game is True, players))        # убираем тех, кто отказался

desk.get_card(deck.pass_off_card(3))                                          # выкладываем 3 карты


def action():
    desk.presentation()
    list(map(lambda player: player.presentation(), players))
    for player in players:
        if len(players) > 1:
                player.keep_playing()
        elif len(players) == 1:
            print('{} wins'.format(player.name))
            break


while len(desk.storage) < 5:
    action()
    if len(players) < 1:
        break
    else:
        desk.get_card(deck.pass_off_card(1))
action()


if len(players) > 1:
    for player in players:
        player.combination = combination_checker(player, desk)           # проверяем комбинации всех игроков
    players = sorted(players, key=lambda player: player.combination[1], reverse=True)  # сортируем по "весу" комбинации
    if players[0].combination[1] == players[1].combination[1]:  # если >1 со старшей комбинацией, сортируем из по карте
        players = list(filter(lambda player: player.combination[1] == players[0].combination[1], players))
        players = sorted(players, key=lambda player: player.combination[2], reverse=True)
        print('{} wins with {} and highest card'.format(players[0].name, players[0].combination[0]))
    else:
        print('{} wins with {}'.format(players[0].name, players[0].combination[0]))
