'''
    预计进行运行的接口
'''

from game.game import GeniusGame

deck1 = {
    'character': [],
    'action_card': []
}
deck2 = {
    'character': [],
    'action_card': []
}

game = GeniusGame(seed=2023, player0_deck=deck1, player1_deck=deck2)

