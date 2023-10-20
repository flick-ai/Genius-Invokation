'''
    预计进行运行的接口
'''
from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *
from genius_invocation.utils import *
from rich import print

deck1 = {
    'character': ['Rhodeia_of_Loch', 'Nahida', 'Tartaglia'],
    'action_card': ['ElegyForTheEnd' for i in range(15)] + ['Golden_House' for i in range(15)]
}
deck2 = {
    'character': ['Cyno', 'Rhodeia_of_Loch', 'Yoimiya'],
    'action_card': ['RavenBow' for i in range(15)] + ['Golden_House' for i in range(15)]
}

game = GeniusGame(player0_deck=deck1, player1_deck=deck2)
information = []

while not game.is_end:
    print(game.encode_message())
    action = Action.from_input(game)
    game.step(action)

print_information(information)
