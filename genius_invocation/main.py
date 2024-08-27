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

from genius_invocation.user_input import get_rng_mul_sel
from genius_invocation.utils import *
from rich import print
import time
import argparse
import os
import pickle
import numpy as np


def get_parser():
    parser = argparse.ArgumentParser()
    # 特殊测试模块
    parser.add_argument('--fix', action='store_true', default=False, help='是否测试选择卡函数')
    parser.add_argument('--code', action='store_true', default=False, help='是否测试code转换')
    parser.add_argument('--select', action='store_true', default=False, help='是否选卡')

    # 不建议开启游戏参数
    parser.add_argument('--read', action='store_true', default=False, help='是否读取log')
    parser.add_argument('--save', action='store_true', default=False, help='是否保存log')
    parser.add_argument('--old', action='store_true', default=False, help='采用旧输入输出格式')

    # 建议开启游戏参数
    parser.add_argument('--omni', action='store_true', default=False, help='是否开启全万能骰')
    parser.add_argument('--jump', action='store_true', default=False, help='跳过选择手牌和骰子')

    # 固定随机种子，用于复现
    parser.add_argument('--seed', type=int, default=2026)

    args = parser.parse_args()
    return args

def test_code():
    code = 'GEGxiIwYGJHRiY4PGBDh8Y8PGEDx9JAPGWAB9pEYGaERipIZGVEhlZMZGWExlpQWGZAA'
    card = get_card()
    name = code_to_name(code, card)
    character_card = name[0:3]
    action_card = name[3:]
    print(character_card, action_card)
    exit()

def get_card():
    package_dir = "./card/character/characters"
    available_character_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
    available_character = []
    for name in available_character_name:
        available_character.append((name, eval("chars."+name).name_ch, eval("chars."+name).id, eval("chars."+name).time))
    available_card = []
    ignore = [action.ActionCard, action.EquipmentCard, action.WeaponCard, action.TalentCard, action.ArtifactCard, action.SupportCard, action.FoodCard, action.SpecialSkillCard]
    for names, obj in inspect.getmembers(action):
        if inspect.isclass(obj) and obj not in ignore:
            available_card.append((names, obj.name_ch, obj.id, obj.time))
    card = available_character + available_card
    card = sorted(card, key=lambda x:(x[3] if x[3]>4.2 else 3.3, x[2]))
    # print([c[1] for c in card])
    return card

def test_fix(is_select=False):
    # 输出所有角色
    package_dir = "./card/character/characters"
    available_character_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
    available_character = []
    for name in available_character_name:
        available_character.append((name, eval("chars."+name).name, eval("chars."+name).name_ch, eval("chars."+name).id))
    available_character = sorted(available_character, key=lambda x:x[-1])

    # 输出所有行动牌
    available_card = []
    ignore = [action.ActionCard, action.EquipmentCard, action.WeaponCard, action.TalentCard, action.ArtifactCard, action.SupportCard, action.FoodCard, action.SpecialSkillCard]
    for name, obj in inspect.getmembers(action):
        if inspect.isclass(obj) and obj not in ignore:
            available_card.append((name, obj.name, obj.name_ch, obj))

    # 输出每个类行动牌数量
    package_dirs = ["./card/character/characters","./card/action/support/companion",
                    "./card/action/support/item","./card/action/support/location",
                    "./card/action/event/events","./card/action/event/foods",
                    "./card/action/event/elemental_resonance_dice",
                    "./card/action/event/elemental_resonance_event",
                    "./card/action/event/country_resonance",
                    "./card/action/event/arcane_legend",
                    "./card/action/equipment/artifact/artifacts",
                    "./card/action/equipment/talent/talents",
                    "./card/action/equipment/weapon/weapons",
                    "./card/action/equipment/specialskill/skills"]
    for package_dir in package_dirs:
        available_name = [f[:-3] for f in os.listdir(package_dir) if f.endswith(".py") and f != "__init__.py" and f != "import_head.py"]
        # print(package_dir, len(available_name))
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
    if not is_select:
        available_card = select_available_card(['Ganyu', 'Keqing' ,'Lynette'], available_card)
        exit()
    else:
        maps = get_card()
        # select_charcater = select_card(available_character, max_num=3)
        selected_character = ['Ganyu', 'Keqing' ,'Lynette']
        available_card = select_available_card(selected_character, available_card)
        selected_action = select_card(available_card, max_num=30)
        name = selected_character + selected_action
        code = name_to_code(name, [c[0] for c in maps])
        return code

def select_character(cards, max_num=3):
    print("请选择3个角色")
    print([(i,c[2]) for i,c in enumerate(cards)])
    result = []
    output = []
    while len(result) < max_num:
        input_select = get_rng_mul_sel("您已选择{}张卡：{} 请选择新的卡牌编号和对应数量，如：0 1\n".format(len(output), output),
                                min=0, max=len(cards)-1, assert_fn=lambda x:True, dtype=int)
        result += [cards[input_select[0]][0] for i in range(input_select[1])]
        output += [cards[input_select[0]][2] for i in range(input_select[1])]
    if len(result) > max_num:
        result = result[:max_num]
    return result

def select_card(cards, max_num=30):
    print("请选择30张卡牌")
    keys = list(cards.keys())
    num = 0
    for idx,key in enumerate(cards.keys()):
        print(idx, key)
        print([(i,c[2]) for i,c in enumerate(cards[key])])
        num += len(cards[key])

    result = []
    output = []
    while len(result) < max_num:
        input_select = get_rng_mul_sel("您已选择{}张卡：{} 请选择新的类别编号、卡牌编号和对应数量，如0 1 2\n".format(len(output), output),
                                min=0, max=num, assert_fn=lambda x:True, dtype=int)
        print(input_select)
        result += [cards[keys[input_select[0]]][input_select[1]][0] for i in range(input_select[2])]
        output += [cards[keys[input_select[0]]][input_select[1]][0] for i in range(input_select[2])]
    if len(result) > max_num:
        result = result[:max_num]
    return result


def select_available_card(characters: List['Character'], all_action_card: List['ActionCard']):
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
        test_fix()
    if args.code:
        test_code()

    # 初始化卡组，直接指定或者通过代码获取
    if args.select:
        code = test_fix(is_select=True)
        deck1 = code_to_deck(code)
    else:
        deck1 = code_to_deck('FhHRgm4YFiHxg3YYFzFhhHcYF0FxhXgYF1GBhn4YF2Hhh38YF3HxioAYGKEBfYEXGNAA')
    deck2 = {
        'character': ['Barbara', 'Beidou', 'KaedeharaKazuha'],
        'action_card': ['Koholasaurus', 'Xenochromatic', 'Yumkasaurus']
    }

    # 初始化游戏
    game = GeniusGame(player0_deck=deck1, player1_deck=deck2, seed=args.seed, is_omni=args.omni)

    # 读取和保存游戏
    if args.save:
        with open("save_data.pickle", "wb+") as f:
            pickle.dump(game, f)
    if args.read:
        with open("save_data.pickle", "rb+") as f:
            game = pickle.load(f)


    # 开始游戏
    if args.read:
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
        if args.old:
            log = []
            while not game.is_end:
                if game.incoming_state:
                    print(game.incoming_state.encode_message())
                else:
                    print(game.encode_message())
                action = Action.from_input(game, log, mode='w', jump=args.jump)
                game.step(action)
                # save log
                if args.save:
                    with open("./action.log", "w") as f:
                        json.dump(log, f, indent=4)
        else:
            # 最新分支
            while not game.is_end:
                if game.incoming_state:
                    layout = game.incoming_state.encode_message()
                else:
                    layout = game.encode_message()
                action = Action.from_layout(game, layout, jump=args.jump)
                game.step(action)
