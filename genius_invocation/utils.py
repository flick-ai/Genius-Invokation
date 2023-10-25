from enum import Enum
from typing import List
DICENUM = 8
MAX_SUMMON = 4
MAX_SUPPORT = 4
MAX_HANDCARD = 10
MAX_DICE = 16
MAX_ROUND = 15

class CountryType(Enum):
    MONDSTADT = 0 # 蒙德
    LIYUE = 1 # 璃月
    INAZUMA = 2 # 稻妻
    SUMERU = 3 # 须弥
    FONTAINE = 4 # 枫丹
    NATLAN = 5 # 纳塔
    SNEZHNAYA = 6 # 至冬
    FATUI = 7 # 愚人众
    HILICHURL = 8 # 丘丘人
    MONSTER = 9 # 怪物
    OTHER = 10 # 其他

class WeaponType(Enum):
    SWORD = 0 # 单手剑
    CATALYST = 1 # 法器
    CLAYMORE = 2 # 双手剑
    BOW = 3 # 弓
    POLEARM = 4 # 长柄武器
    OTHER = 5 # 其他武器

class CostType(Enum):
    CRYO = 0 # 冰
    HYDRO = 1 # 水
    PYRO = 2 # 火
    ELECTRO = 3 # 雷
    ANEMO = 4 # 风
    GEO = 5 # 岩
    DENDRO = 6 # 草
    WHITE = 7 # 任意相同
    BLACK = 8 # 任意

class DiceType(Enum):
    CRYO = 0 # 冰
    HYDRO = 1 # 水
    PYRO = 2 # 火
    ELECTRO = 3 # 雷
    ANEMO = 4 # 风
    GEO = 5 # 岩
    DENDRO = 6 # 草
    OMNI = 7 # 万能

class ElementType(Enum):
    CRYO = 0 # 冰
    HYDRO = 1 # 水
    PYRO = 2 # 火
    ELECTRO = 3 # 雷
    ANEMO = 4 # 风
    GEO = 5 # 岩
    DENDRO = 6 # 草
    PHYSICAL = 7 # 物理
    PIERCING = 8 # 穿透

class Status_Counting_Type(Enum):
    TURNS = 0 # 回合开始时计数
    ATTACKS = 1 # 攻击时计数
    SUFFER = 2 # 被攻击时计数
    DAMAGES = 3 # 基于伤害计数

class SkillType(Enum):
    NORMAL_ATTACK = 0
    ELEMENTAL_SKILL = 1
    ELEMENTAL_BURST = 2
    PASSIVE_SKILL = 3
    SUMMON = 4
    OTHER = 5

class GamePhase(Enum):
    SET_CARD = 0
    SET_CHARACTER = 1
    ROLL_PHASE = 2
    ACTION_PHASE = 3
    END_PHASE = 4

class ActionChoice(Enum):
    HAND_CARD = 0
    CHARACTER_SKILL = 1
    CHANGE_CHARACTER = 2
    PASS = 3
    NONE = 4

class ActionTarget(Enum):
    OPPONENT = 0
    MYSELF = 1
    MY_CHARACTER = 2
    OPPONENT_SUMMON = 3
    MY_SUPPORT_REGION = 4
    DICE_REGION = 5
    CARD_REGION = 6


class ActionCardType(Enum):
    EQUIPMENT_TALENT = 0
    EQUIPMENT_WEAPON = 1
    EQUIPMENT_ARTIFACT = 2
    SUPPORT_LOCATION = 3
    SUPPORT_ITEM = 4
    SUPPORT_COMPANION = 5
    EVENT = 6
    EVENT_FOOD = 7
    EVENT_ELEMENTAL_RESONANCE = 8
    EVENT_ARCANE_LEGEND = 9
    EVENT_COUNTRY = 10

class ZoneType(Enum):
    CHARACTER_ZONE = 0
    ACTIVE_ZONE_SHIELD = 1
    ACTIVE_ZONE = 2
    SUMMON_ZONE = 3
    SUPPORT_ZONE = 4

class EventType(Enum):
    BEGIN_ROLL_PHASE = 0
    BEGIN_ACTION_PHASE = 1
    CALCULATE_DICE = 2
    ON_PLAY_CARD= 3
    AFTER_PLAY_CARD = 4
    ON_USE_SKILL = 5
    AFTER_USE_SKILL = 6
    ON_CHANGE_CHARACTER = 7
    AFTER_CHANGE_CHARACTER = 8
    END_PHASE = 9

    AFTER_TAKES_DMG = 10
    DAMAGE_ADD = 11
    DAMAGE_ADD_AFTER_REACTION = 12 #AFTER REACTION, DMG ADD
    DEALING_DAMAGE = 13 # Mona only right now
    INFUSION = 14
    # ON_REACTION = 14 # Elemental Reaction based event. Maybe trigger sth, or just add DMG.
    DIVIDE_DAMAGE = 21 # 诺艾尔!
    EXECUTE_DAMAGE = 15
    CHARACTER_DIE = 16
    CHARACTER_WILL_DIE = 17

    BEFORE_ANY_ACTION = 18
    AFTER_ANY_ACTION = 19
    ON_SUMMON_REMOVE = 20

    ELEMENTAL_APPLICATION_REATION = 21
    AFTER_HEAL = 22

class SwitchType(Enum):
    CHANGE_CHARACTER = 0

class ElementalReactionType(Enum):
    Frozen = 0
    Melt = 1
    Superconduct = 2
    Vaporize = 3
    Electro_Charged = 4
    Bloom = 5
    Overloaded = 6
    Burning = 7
    Quicken = 8
    Swirl = 9
    Crystallize = 10

DiceToElement = {
    DiceType(i): ElementType(i) for i in range(7)
}

ElementToDice = {
    ElementType(i): DiceType(i) for i in range(7)
}

DiceToCost = {
    DiceType(i): CostType(i) for i in range(7)
}

CostToDice = {
    CostType(i): DiceType(i) for i in range(7)
}

'''
utility functions
'''
from typing import TYPE_CHECKING
from collections import defaultdict
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.entity.character import Character
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.card.action import ActionCard


# get characters
def get_active_character(
        game: 'GeniusGame',
        player_idx: int,
        require_player_idx: bool=False) -> 'Character':
    active_idx = game.players[player_idx].active_idx
    character = game.players[player_idx].character_list[active_idx]
    if require_player_idx:
        return (player_idx, character)
    return character

def get_my_active_character(
        game: 'GeniusGame',
        require_player_idx: bool=False) -> 'Character':
    return get_active_character(game, game.active_player_index, require_player_idx)

def get_opponent_active_character(
        game: 'GeniusGame',
        require_player_idx: bool=False) -> 'Character':
    return get_active_character(game, 1 - game.active_player_index, require_player_idx)

def get_standby_character(
        game: 'GeniusGame',
        player_idx: int,
        require_player_idx: bool=False) -> List['Character']:
    player = game.players[player_idx]
    active_idx = game.players[player_idx].active_idx
    standby_charas = []
    idx = game.players[player_idx].active_idx
    while True:
        idx = (idx + 1) % player.character_num
        if idx == active_idx:
            break
        if player.character_list[idx].is_alive:
            if require_player_idx:
                standby_charas.append((player_idx, game.players[player_idx].character_list[idx]))
            else:
                standby_charas.append(game.players[player_idx].character_list[idx])
    return standby_charas

def get_my_standby_character(
        game: 'GeniusGame',
        require_player_idx: bool=False)->List["Character"]:
    return get_standby_character(game, game.active_player_index, require_player_idx)

def get_opponent_standby_character(
        game: 'GeniusGame',
        require_player_idx: bool=False)->List["Character"]:
    return get_standby_character(game, 1 - game.active_player_index, require_player_idx)

def get_opponent(
        game: 'GeniusGame'
    ):
    return game.players[1 - game.active_player_index]

def get_character_with_name(
        player: 'GeniusPlayer',
        character
):
    # character here is the class name, return an instance.
    for i in range(player.character_num):
        if isinstance(player.character_list[i], character):
            return player.character_list[i]
    return None

def get_player_from_character(
    character: 'Character'
)->'GeniusPlayer':
    return character.from_player


import json
def print_information(log_info, log_file='./debug.json'):
    with open(log_file, 'w') as Fout:
        json.dump(log_info, Fout, indent=4)

def check_duplicate_dice(dice):
    dice_set = set(dice)
    if len(dice) != len(dice_set):
        return True
    return False

def Elementals_to_str(elements: List[ElementType]):
    res = ""
    for element in elements:
        res += str(element.name)+ " "
    if res == "":
        res = "None"
    return res
def Elements_to_color(ele: ElementType):
    match ele:
        case ElementType.CRYO:
            return "rgb(153,255,255)"
        case ElementType.HYDRO:
            return "rgb(128,192,255)"
        case ElementType.PYRO:
            return "rgb(255,153,153)"
        case ElementType.ELECTRO:
            return "rgb(255,172,255)"
        case ElementType.ANEMO:
            return "rgb(128,255,215)"
        case ElementType.GEO:
            return "rgb(255,230,153)"
        case ElementType.DENDRO:
            return "rgb(126,194,54)"
        case ElementType.PHYSICAL:
            return "rgb(255,255,255)"
        case ElementType.PIERCING:
            return "rgb(255,255,255)"
        

from genius_invocation.card.action import *
import genius_invocation.card.character.characters as chars
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
            case ActionCardType.SUPPORT_COMPANION:
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
                available_action_card['SPECIAL_EVENT'].append((class_name, name, name_ch))
            case ActionCardType.EVENT_ELEMENTAL_RESONANCE:
                if same_element.get(action_card.element, 0) > 2:
                    available_action_card['SPECIAL_EVENT'].append((class_name, name, name_ch))
            case ActionCardType.EVENT_COUNTRY:
                if same_country.get(action_card.country, 0) > 2:
                    available_action_card['SPECIAL_EVENT'].append((class_name, name, name_ch))
    return available_action_card


def decode_enum(dct):
    if "enum_type" in dct and "enum_name" in dct:
        enum_type = globals()[dct["enum_type"]]
        return enum_type[dct["enum_name"]]
    return dct
