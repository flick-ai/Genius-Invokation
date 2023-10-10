from utils import *
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from game.events import EventNode


class Entity:

    def __init__(self):
        self.registered_events: list(EventNode) = []

    def register_all_events(self, game: GeniusGame):
        game.manager.register('before_skill', 'on_damage', 'after_skill')

    def on_distroy(self):
        for event in self.registered_events:
            event.del_node()


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


    

class CharacterSkill:
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
        game.manager.invoke('before_skill', game)

        # TODO: 消耗骰子
        # TODO: 消耗能量
        # TODO: 判断技能是否有伤害
        # 生成伤害
        game.current_damage = Damage.create_damage(self.damage_type, self.main_damage_element, self.main_damage, self.piercing_damage)

        # 伤害计算
        game.manager.invoke('on_damage', game)

        # 伤害执行
        game.current_damage.execute()

        # 治疗执行

        # 召唤物/状态生成

        # TODO: 获得能量

        game.manager.invoke('after_skill', game)

    # def on_call(self, game: GeniusGame):
        
    #     action = game.current_action
    #     # 消耗骰子
    #     # 降序排列以便于按索引pop
    #     for dice_index in sorted(action.dice, reverse=True):
    #         game.players[game.active_player].dice_zone.pop(dice_index)

    #     damage = Damage(self.damage_type, self.main_damage_element, self.main_damage, self.piercing_damage)
        
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
            无相雷、丘丘等上限修改
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


        
