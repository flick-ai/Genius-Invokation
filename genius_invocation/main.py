'''
    预计进行运行的接口
'''
from genius_invocation.game.game import GeniusGame
from genius_invocation.game.action import *
import genius_invocation.card.action as action
import inspect
import sys
import genius_invocation.card.character.characters as chars
import genius_invocation.card.action.equipment.talent as talents

from genius_invocation.utils import *
from rich import print
import time
import argparse
import os
import pickle
import numpy as np


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', default=False)
    parser.add_argument('--fix', action='store_true', default=False)
    parser.add_argument('--code', action='store_true', default=False)
    parser.add_argument('--save', action='store_true', default=False)
    parser.add_argument('--omni', action='store_true', default=False)
    parser.add_argument('--seed', type=int, default=2026)
    args = parser.parse_args()
    return args

def test_code():
    code = 'FhHRgm4YFiHxg3YYFzFhhHcYF0FxhXgYF1GBhn4YF2Hhh38YF3HxioAYGKEBfYEXGNAA'
    card = get_card()
    name = code_to_name(code, card)
    character_card = name[0:3]
    action_card = name[3:]
    codes = []
    for i in range(0, 3):
        codes.append(name_to_code(name, [c[0] for c in card], i))
    print(codes)
    exit()

def get_card():
    package_dir = "./card/character/characters"
    available_character_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
    available_character = []
    for name in available_character_name:
        available_character.append((name, eval("chars."+name).name_ch, eval("chars."+name).id, eval("chars."+name).time))
    available_card = []
    ignore = [action.ActionCard, action.EquipmentCard, action.WeaponCard, action.TalentCard, action.ArtifactCard, action.SupportCard, action.FoodCard]
    for names, obj in inspect.getmembers(action):
        if inspect.isclass(obj) and obj not in ignore:
            available_card.append((names, obj.name_ch, obj.id, obj.time))
    card = available_character + available_card
    card = sorted(card, key=lambda x:(x[3] if x[3]>4.2 else 3.3, x[2]))
    print([c[1] for c in card])
    return card

def test_select():
    # 输出所有角色
    package_dir = "./card/character/characters"
    available_character_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
    available_character = []
    for name in available_character_name:
        available_character.append((name, eval("chars."+name).name, eval("chars."+name).name_ch, eval("chars."+name).id))
    print(len(available_character))


    for character in sorted(available_character, key=lambda x:x[-1]):
        print(character[2])

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
        # 测试天赋的归属
        if package_dir == "./card/action/equipment/talent/talents":
            all_talents = [eval('talents.'+talent).character.__name__ for talent in available_name]
            for talent in all_talents:
                if talent not in available_character_name:
                    print("{} not has character".format(talent))
            for character in available_character_name:
                if character not in all_talents:
                    print("{} not has talent".format(character))

    # 测试选择卡函数
    available_card = select_card(['Ganyu', 'Keqing' ,'Lynette'], available_card)
    exit()

def select_card(characters: List['Character'], all_action_card: List['ActionCard']):
    all_weapon_type = {}
    same_country = {}
    same_element = {}
    all_character = []
    available_action_card = defaultdict(list)

    for character in characters:
        character = eval('chars.'+character)
        all_character.append(character.__name__)
        same_element[character.element] = same_element.get(character.element, 0) + 1
        if hasattr(character, 'country_list'):
            for country in character.country_list:
                same_country[country] = same_country.get(country, 0) + 1
        else:
            same_country[character.country] = same_country.get(character.country, 0) + 1
        all_weapon_type[character.weapon_type] = all_weapon_type.get(character.weapon_type, 0) + 1

    all_action_card  = sorted(all_action_card, key=lambda x:x[-1].id)
    for class_name, name, name_ch, action_card in all_action_card:
        match action_card.card_type:
            case ActionCardType.EQUIPMENT_ARTIFACT:
                available_action_card['ARTIFACT'].append((class_name, name, name_ch))
            case ActionCardType.EQUIPMENT_WEAPON:
                if action_card.weapon_type in all_weapon_type:
                    available_action_card['WEAPON_TALENT'].append((class_name, name, name_ch))
            case ActionCardType.EQUIPMENT_TALENT:
                if action_card.character.__name__ in all_character:
                    available_action_card['WEAPON_TALENT'].append((class_name, name, name_ch))
            case ActionCardType.SUPPORT_LOCATION:
                available_action_card['SUPPORT'].append((class_name, name, name_ch))
            case ActionCardType.SUPPORT_ITEM:
                available_action_card['SUPPORT'].append((class_name, name, name_ch))
            case ActionCardType.SUPPORT_COMPANION:
                available_action_card['SUPPORT'].append((class_name, name, name_ch))
            case ActionCardType.EVENT_FOOD:
                available_action_card['EVENT'].append((class_name, name, name_ch))
            case ActionCardType.EVENT:
                available_action_card['EVENT'].append((class_name, name, name_ch))
            case ActionCardType.EVENT_ARCANE_LEGEND:
                available_action_card['ARCANE_LEGEND'].append((class_name, name, name_ch))
            case ActionCardType.EVENT_ELEMENTAL_RESONANCE:
                if same_element.get(action_card.element, 0) >= 2:
                    available_action_card['EVENT'].append((class_name, name, name_ch))
            case ActionCardType.EVENT_COUNTRY:
                if same_country.get(action_card.country, 0) >= 2:
                    available_action_card['EVENT'].append((class_name, name, name_ch))
    return available_action_card

def code_to_deck(code):
    card = get_card()
    name = code_to_name(code, card)
    character_card = name[0:3]
    action_card = name[3:]
    deck = {
        'character': character_card,
        'action_card': action_card
    }
    return deck

if __name__=="__main__":
    args = get_parser()
    if args.fix:
        test_select()
    if args.code:
        test_code()
    deck1 = {
    'character': ['Rhodeia_of_Loch'],
    'action_card': ['Fresh_Wind_of_Freedom','Dunyarzad','Dunyarzad','Chef_Mao','Chef_Mao','Paimon','Paimon',
                    'Rana','Rana','Liben','Liben','Mushroom_Pizza','Mushroom_Pizza','Adeptus_Temptation',
                    'Adeptus_Temptation','Teyvat_Fried_Egg','Sweet_Madame','Sweet_Madame','Mondstadt_Hash_Brown',
                    'Lotus_Flower_Crisp','Lotus_Flower_Crisp','Strategize','Strategize','Leave_it_to_Me','Leave_it_to_Me',
                    'PaidinFull','PaidinFull','Send_Off','Starsigns','Starsigns']
    }
    deck2 = {
    'character': ['Neuvillette', 'Bennett', 'Qiqi'],
    'action_card': ['VourukashasGlow' for i in range(30)]
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
    game = GeniusGame(player0_deck=deck1, player1_deck=deck2, seed=args.seed, is_omni=args.omni)
    with open("save_data.pickle", "wb+") as f:
        pickle.dump(game, f)

    with open("save_data.pickle", "rb+") as f:
        game = pickle.load(f)

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
            if game.incoming_state:
                print(game.incoming_state.encode_message())
            else:
                print(game.encode_message())
            # print(game)
            action = Action.from_input(game, log, mode='w', jump=False)
            game.step(action)
            # save log
            if args.save:
                with open("./action.log", "w") as f:
                    json.dump(log, f, indent=4)
