'''
    预计进行运行的接口
'''
from game.game import GeniusGame
from game.action import *
from utils import *

deck1 = {
    'character': ['Tartaglia', 'Nahida', 'Yoimiya'],
    'action_card': ['RavenBow' for i in range(15)] + ['Paimon' for i in range(15)]
}
deck2 = {
    'character': ['Tartaglia', 'Nahida', 'Yoimiya'],
    'action_card': ['RavenBow' for i in range(15)] + ['Paimon' for i in range(15)]
}

game = GeniusGame(player0_deck=deck1, player1_deck=deck2)
information = []
# while not game.is_end:
#     action = Action.from_input()
#     game.step(action)
#     print(game.encode_message())

action = choose_card([0, 4])
game.step(action)
action = choose_card([0, 4])
game.step(action)

action = choose_character(0)
game.step(action)
action = choose_character(1)
game.step(action)

action = choose_dice([2,3,4,5,6,7])
game.step(action)
action = choose_dice([2,3,4,5,6,7])
game.step(action)

action = choose_character(1)
game.step(action)
action = choose_character(2)
game.step(action)

while not game.is_end:
    print(game.encode_message())
    action = Action.from_input()
    game.step(action)

print_information(information)
