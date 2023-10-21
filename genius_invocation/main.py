'''
    预计进行运行的接口
'''
from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *
from genius_invocation.utils import *
from rich import print

if __name__=="__main__":
    deck1 = {
        'character': ['Cyno', 'Wanderer', 'Yoimiya'],
        'action_card': ['Chang_the_Ninth' for i in range(30)]
    }
    deck2 = {
        'character': ['Candace', 'Shenhe', 'Qiqi'],
        'action_card': ['Dunyarzad' for i in range(30)]
    }

    game = GeniusGame(player0_deck=deck1, player1_deck=deck2)

    while not game.is_end:
        print(game.encode_message())
        action = Action.from_input(game, jump=True)
        game.step(action)
