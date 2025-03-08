from materials import Card, Deck
from regicideAI import RegicideGame_AI

# Card.get_int_value() test 1
# print('Card.get_int_value() test 1')
d = Deck(shuffle=False)

# int_list = [c.get_int_value() for c in d.cards]
# int_list.sort()
# assert int_list == list(range(52)), 'Card missing'
# print('test passed')

from regicide import Player

# # Player.get_bool_list_cards() test 1
# print('Player.get_bool_list_cards() test 1')
# d.shuffle()
# p = Player('jim')
# p.draw_from_deck(d,7)
# print(p.get_bool_list_cards())

# # RegicideGame_AI.get_state() test 1
# print('RegicideGame_AI.get_state() test 1')
# g = RegicideGame_AI()
# print(g.get_state())

# # 2nd pivot RegicideGame_AI.build_action_space()
# print('build_action_space')
# g = RegicideGame_AI()
# print(g.action_space)
# print(g.int_to_icmd)
# print(g.icmd_to_int)

# testing player.get_hand_int_values()
d = Deck()
p = Player('test')
print(p.get_hand_int_values())
p.draw_from_deck(d)
print(p.get_hand_int_values())
p.draw_from_deck(d,2)
print(p.get_hand_int_values())
p.draw_from_deck(d,3)
print(p.get_hand_int_values())
p.draw_from_deck(d,3)
print(p.get_hand_int_values())