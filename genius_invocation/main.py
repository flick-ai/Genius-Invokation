'''
    预计进行运行的接口
'''
from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *
import genius_invocation.card.action as action
import inspect
import sys
import genius_invocation.card.character.characters as chars

from genius_invocation.utils import *
from rich import print
import time
import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', default=False)
    args = parser.parse_args()
    return args

if __name__=="__main__":

    available_character_name = ['Arataki_Itto', 'Candace', 'Cyno', 'Dehya', "ElectroHypostasis", 
                           "Fatui_Pyro_Agent", "Fischl", "Ganyu", "Jadeplume_Terrorshroom", "Keqing", 
                           "Mona", "Nahida", "Ningguang", "Noelle", "Qiqi",
                           "Rhodeia_of_Loch", "Shenhe", "Tartaglia", "Xingqiu", "Yae_Miko",
                           "Yoimiya"]
    available_character = []
    for name in available_character_name:
        available_character.append((name, eval("chars."+name).name, eval("chars."+name).name_ch, eval("chars."+name)))

    print(available_character)
    available_card = []
    ignore = [action.ActionCard, action.EquipmentCard, action.WeaponCard, action.TalentCard, action.ArtifactCard, action.SupportCard, action.FoodCard]
    for name, obj in inspect.getmembers(action):
        if inspect.isclass(obj) and obj not in ignore:
            available_card.append((name, obj.name, obj.name_ch, obj))
    print(available_card)

    select_card(['Rhodeia_of_Loch', 'Yae_Miko' ,'Fatui_Pyro_Agent'], available_card)

    args = get_parser()
    deck1 = {
    'character': ['Rhodeia_of_Loch', 'Yae_Miko' ,'Fatui_Pyro_Agent'],
    'action_card': ['Fresh_Wind_of_Freedom','Dunyarzad','Dunyarzad','Chef_Mao','Chef_Mao','Paimon','Paimon',
                    'Rana','Rana','Liben','Liben','Mushroom_Pizza','Mushroom_Pizza','Adeptus_Temptation',
                    'Adeptus_Temptation','Teyvat_Fried_Egg','Sweet_Madame','Sweet_Madame','Mondstadt_Hash_Brown',
                    'Lotus_Flower_Crisp','Lotus_Flower_Crisp','Strategize','Strategize','Leave_it_to_Me','Leave_it_to_Me',
                    'PaidinFull','PaidinFull','Send_Off','Starsigns','Starsigns']
    }
    deck2 = {
    'character': ['Arataki_Itto', 'Dehya', 'Noelle'],
    'action_card': ['TenacityoftheMillelith','TenacityoftheMillelith','TheBell','TheBell','Paimon','Paimon',
                    'Chef_Mao','Chef_Mao','Liben','Liben','Dunyarzad','Dunyarzad','Fresh_Wind_of_Freedom',
                    'Woven_Stone','Woven_Stone','Enduring_Rock','Enduring_Rock','Strategize','Strategize',
                    'Leave_it_to_Me','Send_Off','Heavy_Strike','Heavy_Strike','Adeptus_Temptation',
                    'Lotus_Flower_Crisp','Lotus_Flower_Crisp','Sweet_Madame','Mondstadt_Hash_Brown',
                    'Mushroom_Pizza','Mushroom_Pizza']
    }
    game = GeniusGame(player0_deck=deck1, player1_deck=deck2, seed=2026, is_omni=True)

    if args.test:
        with open("./action.log") as f:
            log = json.load(f)
        for i in log:
            print(game.encode_message())
            action = Action.from_dict(i)
            game.step(action)
        while not game.is_end:
            print(game.encode_message())
            action = Action.from_input(game, log, mode='w', jump=False)
            game.step(action)
    else:
        log = []
        while not game.is_end:
            print(game.encode_message())
            action = Action.from_input(game, log, mode='w', jump=False)
            game.step(action)
