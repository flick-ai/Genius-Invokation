'''
    预计进行运行的接口
'''
from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *
from genius_invocation.utils import *
from rich import print

deck1 = {
    'character': ['Rhodeia_of_Loch', 'Nahida', 'Tartaglia'],
    'action_card': ['Gandharva_Ville' for i in range(30)]
}
deck2 = {
    'character': ['Cyno', 'Wanderer', 'Yoimiya'],
    'action_card': ['Favonius_Cathedral' for i in range(30)]
}

game = GeniusGame(player0_deck=deck1, player1_deck=deck2)
information = []

while not game.is_end:
    print(game.encode_message())
    action = Action.from_input(game)
    game.step(action)

print_information(information)
