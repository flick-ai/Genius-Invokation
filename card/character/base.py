from utils import *
from typing import List, TYPE_CHECKING
from event.damage.damage import Damage
from event.Action_Effect import *

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import EventNode

class CharacterSkill:
    # 角色技能基本类
    id: int
    name: str
    type: SkillType
    # character: CharacterCard

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

class NormalAttackSkill(CharacterSkill):

    def on_call(self, game: GeniusGame):
        is_plunging_attack = False
        is_charged_attack = False
        game.manager.invoke('before_skill', game)

        # TODO: 消耗骰子
        # TODO: 判断技能是否有伤害
        # 生成伤害
        game.current_damage = Damage.create_damage(self.damage_type, self.main_damage_element, self.main_damage, self.piercing_damage, is_plunging_attack, is_charged_attack)

        # 伤害计算
        game.manager.invoke('on_damage', game)

        # 伤害执行
        game.current_damage.execute()

        # 治疗执行

        # 召唤物/状态生成

        # TODO: 获得能量
        # 大概吧，叹气，不确定是不是“active”类中，我觉得应该是的
        game.manager.register('after_skill', 'active', GainEnergyForActive(self.energy_gain))
        
        game.manager.invoke('after_skill', game)






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


        
