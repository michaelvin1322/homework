from poker.instances import Card, Deck, Desk, Player


card = Card('hearts', 10)
deck = Deck()
deck.generate()
deck.shake()
pl_1 = Player('Joe')
desk = Desk()
pl_1.get_card(deck.pass_off_card(2))
desk.get_card(deck.pass_off_card(5))



pl_1.presentation()
desk.presentation()

