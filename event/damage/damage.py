from card.character.base import SkillType
from utils import *
from game.game import GeniusGame

class Damage:
    # 伤害基本类
    def __init__(self, damage_type: SkillType, main_damage_element: ElementType, main_damage: int, piercing_damage: int, is_plunging_attack: bool=False, is_charged_attack: bool=False) -> None:
        self.damage_type: SkillType = damage_type
        self.main_damage_element: ElementType = main_damage_element
        self.main_damage: int = main_damage
        self.piercing_damage: int = piercing_damage

        self.is_plunging_attack: bool
        self.is_charged_attack: bool

    @staticmethod
    def create_damage(cls, game: GeniusGame,
                      damage_type: SkillType, main_damage_element: ElementType, 
                      main_damage: int, piercing_damage: int):
        if damage_type == SkillType.NORMAL_ATTACK:
            # TODO: 判断当前角色是否为切换后的第一个战斗行动
            # is_plunging_attack = game.players.
            
            is_charged_attack = len(game.players[game.active_player].dice_zone) % 2 
        else:
            return cls(damage_type, main_damage_element, main_damage, piercing_damage)