from enum import Enum

DICENUM = 8
MAX_HANDCARD = 10
MAX_DICE = 16
MAX_ROUND = 15

class CountryType(Enum):
    MONDSTADT = 0 # 蒙德
    LIYUE = 1 # 璃月
    INAZUMA = 2 # 稻妻
    SUNERU = 3 # 须弥
    FONTAINE = 4 # 枫丹
    NATLAN = 5 # 纳塔
    SNEZHNAYA = 6 # 至冬
    FATUI = 7 # 愚人众
    HILICHURL = 8 # 丘丘人
    MONSTER = 9 # 怪物

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
    ANEPMO = 4 # 风
    GEO = 5 # 岩
    DENDRO = 6 # 草
    WHITE = 7 # 任意相同
    BLACK = 8 # 任意

class DiceType(Enum):
    CRYO = 0 # 冰
    HYDRO = 1 # 水
    PYRO = 2 # 火
    ELECTRO = 3 # 雷
    ANEPMO = 4 # 风
    GEO = 5 # 岩
    DENDRO = 6 # 草
    OMNI = 7 # 万能

class ElementType(Enum):
    CRYO = 0 # 冰
    HYDRO = 1 # 水
    PYRO = 2 # 火
    ELECTRO = 3 # 雷
    ANEPMO = 4 # 风
    GEO = 5 # 岩
    DENDRO = 6 # 草
    PHYSICAL = 7 # 物理

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

class ZoneType(Enum):
    CHARACTER_ZONE = 0
    ACTIVE_ZONE = 1
    SUMMON_ZONE = 2
    SUPPORT_ZONE = 3

class EventType(Enum):
    BEGIN_ACTION_PHASE = 0
    DAMAGE_ADD = 1
    CALCULATE_DICE = 2
    BEFORE_CHANGE_CHARACTER = 3
    AFTER_CHANGE_CHARACTER = 4
    AFTER_USE_SKILL = 5
    AFTER_TAKES_DMG = 6
    AFTER_PLAY_CARD = 7
    END_PHASE = 8
    DEALING_DAMAGE = 9 # Mona only right now
    INFUSION = 10




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
from game.game import GeniusGame

# get characters
def get_active_character(
        game: GeniusGame, 
        player_idx: int, 
        require_player_idx: bool=False):
    if require_player_idx:
        return (player_idx, game.players[player_idx].active_idx)
    return game.players[player_idx].active_idx

def get_my_active_character(
        game: GeniusGame,
        require_player_idx: bool=False):
    return get_active_character(game, game.active_player, require_player_idx)

def get_opponent_active_character(
        game: GeniusGame,
        require_player_idx: bool=False):
    return get_active_character(game, not game.active_player, require_player_idx)

def get_standby_character(
        game: GeniusGame, 
        player_idx: int,
        require_player_idx: bool=False):
    player = game.players[player_idx]
    active_idx = game.players[player_idx].active_idx
    standby_charas = []
    for idx in range(player.character_num):
        if idx == active_idx:
            continue
        if player.character_list[idx].is_alive:
            if require_player_idx:
                standby_charas.append((player_idx, idx))
            else:
                standby_charas.append(idx)
    return standby_charas

def get_my_standby_character(
        game: GeniusGame,
        require_player_idx: bool=False):
    return get_standby_character(game, game.active_player, require_player_idx)

def get_opponent_standby_character(
        game: GeniusGame,
        require_player_idx: bool=False):
    return get_standby_character(game, not game.active_player, require_player_idx)