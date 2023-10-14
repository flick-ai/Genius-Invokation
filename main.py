'''
    预计进行运行的接口
'''

from game.game import GeniusGame
from game.action import *

deck1 = {
    'character': ['Tartaglia', 'Nahida', 'Yoimiya'],
    'action_card': ['RavenBow' for i in range(30)]
}
deck2 = {
    'character': ['Tartaglia', 'Nahida', 'Yoimiya'],
    'action_card': ['RavenBow' for i in range(30)]
}

game = GeniusGame(player0_deck=deck1, player1_deck=deck2)
print(game.encode_message())

action = choose_card([0, 4])
game.step(action)
print(game.encode_message())

action = choose_card([0, 4])
game.step(action)
print(game.encode_message())

action = choose_character(0)
game.step(action)
print(game.encode_message())

action = choose_character(1)
game.step(action)
print(game.encode_message())

action = choose_dice([2,3,4,5,6,7])
game.step(action)
print(game.encode_message())

