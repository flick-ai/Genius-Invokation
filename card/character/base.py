from utils import *
from typing import List
from game.game import GeniusGame
from game.action import Action


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
        




class DamageModify:
    '''
    '''
    pass

class DamageChange(DamageModify):
    '''
    元素转化
    '''
    pass

class DamageAdd(DamageModify):
    '''
    加算区
    '''
    pass
    def effect(game: GeniusGame, damage: Damage):
        pass

class DamageMultiply(DamageModify):
    '''
    乘算区
    '''
    pass



class Settle:
    # 血量结算类

    # damage
    damage_type: SkillType
    main_damage_element: ElementType
    main_damage: int
    piercing_damage: int

    # heal
    heal: int


    def cal_damage(self, game: GeniusGame, action: Action):
        '''
            1. 元素转化
            2. 加算区
            3. 乘算区
        '''
        pass
    
    def build_damage_queue(self, game: GeniusGame) -> list:
        damage_queue = []

    def pre_settle():
        pass

    def on_settle():
        pass
    
    def post_settle():
        pass

    def on_call(self, game: GeniusGame):
        
        damage = Damage.create_damage(self.damage_type, self.main_damage_element, self.main_damage, self.piercing_damage)
        self.pre_settle(game)
        self.on_settle(game, damage)
        self.post_settle(game)
        
        # demage = Damage(self.damage_type, self.main_damage_element, self.main_damage, self.piercing_damage)



class Summon:
    # 召唤物基本类
    id: int
    name: str
    element: ElementType
    usage: int
    max_usage: int
    skills: list

    def __init__(self) -> None:
        self.usages: int # 此处是否需要区分青蛙和花鼠？
        # self.effect_text: str


    

class CharacterSkill(Settle):
    # 角色技能基本类
    id: int
    name: str
    type: SkillType

    # damage
    damage_type: SkillType
    main_damage_element: ElementType
    main_damage: int
    piercing_damage: int

    # heal
    heal: int

    # cost
    cost: list({'cost_num': int, 'cost_type': CostType})
    energy_cost: int
    energy_gain: int

    def __init__(self) -> None:
        pass

    def on_call(self, game: GeniusGame):
        
        action = game.current_action
        # 消耗骰子
        # 降序排列以便于按索引pop
        for dice_index in sorted(action.dice, reverse=True):
            game.players[game.active_player].dice_zone.pop(dice_index)

        damage = Damage(self.damage_type, self.main_damage_element, self.main_damage, self.piercing_damage)
        
class CharacterCard:
    # 角色卡片基本类
    id: int
    name: str
    element: ElementType
    weapon_type: WeaponType
    country: CountryType
    health_point: int
    max_health_point: int
    skills: {'Normal Attack':CharacterSkill, 'Elemental Skill':CharacterSkill, 'Elemental Burst':CharacterSkill, 'Passive Skill':CharacterSkill}
    power: int
    max_power: int

    init_state: list() # 初始状态
    # def __init__(self) -> None:

    def on_game_start(self):
        '''
            角色区初始化
            讨债人被动 潜行
            雷电将军被动 诸愿百眼之轮
        '''
        return self.power, self.health_point, self.init_state
        

    def on_round_start(self, game: GeniusGame):
        '''
            预留
        '''
        pass

    def on_switched(self, game: GeniusGame):
        '''
            passive skill 被动技能 神里绫华
            
        '''
        pass

    
    def use_skill(self, game: GeniusGame):
        '''
            执行使用什么技能的接口
        '''
        pass


        
