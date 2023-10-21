'''
    预计进行运行的接口
'''
from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *
from genius_invocation.utils import *
from rich import print

if __name__=="__main__":
    deck1 = {
    'character': ['Rhodeia_of_Loch', 'Nahida', 'Fischl'],
    'action_card': ['Fresh_Wind_of_Freedom','Toss_up','Toss_up','Dunyarzad','Dunyarzad','Chef_Mao','Chef_Mao','Paimon','Paimon',
                    'Rana','Rana','Liben','Liben','Timmie','Timmie','Mushroom_Pizza','Mushroom_Pizza','Adeptus_Temptation','Adeptus_Temptation',
                    'Teyvat_Fried_Egg','Teyvat_Fried_Egg','Sweet_Madame','Sweet_Madame','Mondstadt_Hash_Brown','Mondstadt_Hash_Brown',
                    'Treasure_Seeking_Seelie','Treasure_Seeking_Seelie','Vanarana','Lotus_Flower_Crisp','Lotus_Flower_Crisp']
    }
    deck2 = {
    'character': ['Xingqiu', 'Ganyu', 'Shenhe'],
    'action_card': ['Fresh_Wind_of_Freedom','Toss_up','Toss_up','Dunyarzad','Dunyarzad','Chef_Mao','Chef_Mao','Paimon','Paimon',
                    'Rana','Rana','Liben','Liben','Timmie','Timmie','Mushroom_Pizza','Mushroom_Pizza','Adeptus_Temptation','Adeptus_Temptation',
                    'Teyvat_Fried_Egg','Teyvat_Fried_Egg','Sweet_Madame','Sweet_Madame','Mondstadt_Hash_Brown','Mondstadt_Hash_Brown',
                    'Treasure_Seeking_Seelie','Treasure_Seeking_Seelie','Vanarana','Lotus_Flower_Crisp','Lotus_Flower_Crisp']
    }
    game = GeniusGame(player0_deck=deck1, player1_deck=deck2)

    while not game.is_end:
        print(game.encode_message())
        action = Action.from_input(game, jump=False)
        game.step(action)
