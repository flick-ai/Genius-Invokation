
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

    @classmethod
    def create_damage(cls, game: GeniusGame,
                      damage_type: SkillType, main_damage_element: ElementType, 
                      main_damage: int, piercing_damage: int, 
                      is_plunging_attack: bool=False, is_charged_attack: bool=False):
        game.current_damage = cls(damage_type, main_damage_element, main_damage, piercing_damage, is_plunging_attack, is_charged_attack)

    @staticmethod
    def resolve_damage(game: GeniusGame,
                    damage_type: SkillType, main_damage_element: ElementType, 
                    main_damage: int, piercing_damage: int, 
                    is_plunging_attack: bool=False, is_charged_attack: bool=False):    
        Damage.create_damage(game, damage_type, main_damage_element, main_damage, piercing_damage, is_plunging_attack, is_charged_attack)
        Damage.cal_damage(game)
        Damage.execute_damage(game)
        Damage.after_damage(game)
    
    def after_damage(self, game: GeniusGame):
        pass
    def execute_damage(self, game: GeniusGame):
        # 打出伤害

        # TODO: 盾
        pass
    def cal_damage(self, game: GeniusGame):
        # 元素类型转化

        # 元素反应
        # TODO: 可能产生新的独立伤害（扩散), 这一部分需要在当前伤害结算完毕后再进行

        # 伤害加算

        pass