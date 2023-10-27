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
import os

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', default=False)
    parser.add_argument('--fix', action='store_true', default=False)
    args = parser.parse_args()
    return args

def test_select():
    # 输出所有角色
    package_dir = "./card/character/characters"
    available_character_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
    available_character = []
    for name in available_character_name:
        available_character.append((name, eval("chars."+name).name, eval("chars."+name).name_ch, eval("chars."+name)))
    print(len(available_character))

    # 输出所有行动牌
    available_card = []
    ignore = [action.ActionCard, action.EquipmentCard, action.WeaponCard, action.TalentCard, action.ArtifactCard, action.SupportCard, action.FoodCard]
    for name, obj in inspect.getmembers(action):
        if inspect.isclass(obj) and obj not in ignore:
            available_card.append((name, obj.name, obj.name_ch, obj))
    print(len(available_card))

    # 输出每个类行动牌数量
    package_dirs = ["./card/character/characters","./card/action/support/companion",
                    "./card/action/support/item","./card/action/support/location",
                    "./card/action/event/events","./card/action/event/foods",
                    "./card/action/event/elemental_resonance", "./card/action/event/arcane_legend",
                    "./card/action/equipment/artifact/artifacts",
                    "./card/action/equipment/talent/talents",
                    "./card/action/equipment/weapon/weapons"]
    for package_dir in package_dirs:
        available_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        print(package_dir, len(available_name))

    # 测试选择卡函数
    available_card = select_card(['Ganyu', 'Keqing' ,'Qiqi'], available_card)
    print(available_card['SPECIAL EVENT'])
    exit()


if __name__=="__main__":
    args = get_parser()
    if args.fix:
        test_select()
    deck1 = {
    'character': ['Rhodeia_of_Loch', 'Yae_Miko' ,'Fatui_Pyro_Agent'],
    'action_card': ['Fresh_Wind_of_Freedom','Dunyarzad','Dunyarzad','Chef_Mao','Chef_Mao','Paimon','Paimon',
                    'Rana','Rana','Liben','Liben','Mushroom_Pizza','Mushroom_Pizza','Adeptus_Temptation',
                    'Adeptus_Temptation','Teyvat_Fried_Egg','Sweet_Madame','Sweet_Madame','Mondstadt_Hash_Brown',
                    'Lotus_Flower_Crisp','Lotus_Flower_Crisp','Strategize','Strategize','Leave_it_to_Me','Leave_it_to_Me',
                    'PaidinFull','PaidinFull','Send_Off','Starsigns','Starsigns']
    }
    deck2 = {
    'character': ['Klee', 'Lisa', 'Qiqi'],
    'action_card': ['PulsatingWitch' for i in range(30)]
    }
    # deck2 = {
    # 'character': ['Arataki_Itto', 'Dehya', 'Noelle'],
    # 'action_card': ['TenacityoftheMillelith','TenacityoftheMillelith','TheBell','TheBell','Paimon','Paimon',
    #                 'Chef_Mao','Chef_Mao','Liben','Liben','Dunyarzad','Dunyarzad','Fresh_Wind_of_Freedom',
    #                 'Woven_Stone','Woven_Stone','Enduring_Rock','Enduring_Rock','Strategize','Strategize',
    #                 'Leave_it_to_Me','Send_Off','Heavy_Strike','Heavy_Strike','Adeptus_Temptation',
    #                 'Lotus_Flower_Crisp','Lotus_Flower_Crisp','Sweet_Madame','Mondstadt_Hash_Brown',
    #                 'Mushroom_Pizza','Mushroom_Pizza']
    # }
    game = GeniusGame(player0_deck=deck1, player1_deck=deck2, seed=2026, is_omni=False)

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
