'''
    预计进行运行的接口
'''

from game.game import GeniusGame

deck1 = {
    'character': [],
    'action_card': ['RavenBow' for i in range(30)]
}
deck2 = {
    'character': [],
    'action_card': ['RavenBow' for i in range(30)]
}

game = GeniusGame(seed=2023, player0_deck=deck1, player1_deck=deck2)
print(game.encode_message())
