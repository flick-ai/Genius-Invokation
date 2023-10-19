'''
    预计进行运行的接口
'''
from game.game import GeniusGame
from game.action import *
from utils import *

deck1 = {
    'character': ['Rhodeia_of_Loch', 'Nahida', 'Tartaglia'],
    'action_card': ['Liyue_Harbor_Wharf' for i in range(30)]
}
deck2 = {
    'character': ['Shenhe', 'Wanderer', 'Yoimiya'],
    'action_card': ['Paimon' for i in range(30)]
}

game = GeniusGame(player0_deck=deck1, player1_deck=deck2)
information = []

while not game.is_end:
    print(game.encode_message())
    action = Action.from_input(game)
    game.step(action)

print_information(information)
