from players import Player, Field, Computer


field = [[' ']*10]
for i in range(9):
    field += [[' '] * 10]

pl = Player()
cm = Computer()
Field.print_field(cm.field, pl.field)
while len(pl.storage) > 0 and len(cm.storage) > 0:
    pl.strike(cm)
    cm.strike(pl)
    Field.print_field(cm.field, pl.field)


if len(cm.storage) is 0:
    print('Player wins')
elif len(pl.storage) is 0:
    print('Computer wins')
