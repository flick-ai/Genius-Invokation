from card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from entity.character import Character
from entity.entity import Entity
from game.player import GeniusPlayer
from utils import *
from game.game import GeniusGame
from typing import TYPE_CHECKING, List, Tuple

from utils import GeniusGame

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import ListenerNode
    from game.player import GeniusPlayer
    from event.damage import Damage
from entity.status import Status

class RangedStance(Status):
    '''
        远程状态
    '''


class MeleeStance(Status):
    '''
        近战状态
    '''
    def on_after_skill(self, game: GeniusGame):
        '''
            近战状态的达达利亚对已附属有断流的角色使用技能后: 
            对下一个敌方后台角色造成1点穿透伤害
        '''

    def update_listener_list(self):
        return super().update_listener_list()
    

class Riptide(Status):
    '''
        断流
        实现逻辑:
        当角色死亡时, 会调用on_distroy, 这时候先建一个新的断流
    '''
    def __init__(self, game: GeniusGame, from_player: GeniusPlayer, from_character=None):
        super().__init__(game, from_player, from_character)
        self.attached = False # 是否附着

    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_switch_character)
        ]

    def on_damage_add(self, game: GeniusGame):
        '''
            近战状态下的达达利亚对附属有断流的角色造成的伤害+1
        '''
        if game.players[0] == self.from_player:
            tartaglia_player = game.players[1]
        else:
            tartaglia_player = game.players[0]
        tartaglia = get_character_with_name(tartaglia_player, Tartaglia)
        if game.current_damage.damage_from == tartaglia:
            game.current_damage.main_damage += 1

    def on_distroy(self, game):
        super().on_destroy()
        # 新的断流
        new_riptide = Riptide(game=game,
                          from_player=self.from_player,
                          from_character=None)

    def on_switch_character(self, game: GeniusGame):
        if not self.attached:
            # 附着到新的出战角色上
            new_character = self.from_player.character_list[self.from_player.active_idx]
            new_character.add_entity(self)
            self.from_character = new_character
            self.attached = True
    
    def on_end_phase(self, game: GeniusGame):
        if game.players[0] == self.from_player:
            tartaglia_player = game.players[1]
        else:
            tartaglia_player = game.players[0]
        tartaglia = get_character_with_name(tartaglia_player, Tartaglia)
        if tartaglia.talent and tartaglia.character_zone.is_alive:
            Damage.resolve_damage(game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.PIERCING,
                main_damage=1,
                piercing_damage=0,
                damage_from=None,
                damage_to=get_opponent_active_character(game),
                is_plunging_attack=False,
                is_charged_attack=False)


class CuttingTorrent(NormalAttack):
    '''
        达达利亚
        普通攻击
        断雨
    '''
    id: int = 0
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.HYDRO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 消耗骰子
        self.on_dice(game)
        # 处理伤害
        self.resolve_damage(game)

        # 如果达达利亚的攻击为重击：对目标角色附属断流
        if self.is_charged_attack:

            # 如果目标角色没有附属断流，则附属断流
            status = game.current_damage.damage_to.character_zone.has_entity(Riptide)
            if not status:
                riptide = Riptide(game=game,
                                  from_player=game.current_damage.damage_to.from_player,
                                  from_character=game.current_damage.damage_to)
                game.current_damage.damage_to.character_zone.add_entity(riptide)

        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class FoulLegacy_RagingTide(ElementalSkill):
    '''
        达达利亚
        元素战技
        魔王武装：狂澜
    '''
    id: int = 1
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call():
        pass


class FlashOfHavoc(ElementalBurst):
    '''
        达达利亚
        远程状态元素爆发
    '''
    id: int = 3
    type: SkillType = SkillType.ELEMENTAL_BURST

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost: int = 3
    energy_gain: int = 2

    def on_call(self, game: GeniusGame):
        pass
    
class LightOfHavoc(ElementalBurst):
    '''
        达达利亚
        近战状态元素爆发
    '''
    id: int = 4
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 7
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: GeniusGame):
        pass

class Havoc_Obliteration(ElementalBurst):
    '''
    '''
    id: int = 2
    def __init__(self, from_character: Character) -> None:
        self.from_character = from_character
        self.flash_of_havoc = FlashOfHavoc(from_character)
        self.light_of_havoc = LightOfHavoc(from_character)

    def on_call(self, game: GeniusGame):
        if self.from_character.is_melee_stance:
            self.light_of_havoc.on_call(game)
        else:
            self.flash_of_havoc.on_call(game)
        

class Tartaglia(Character):
    '''达达利亚'''
    id: int = 2
    name: str = 'Tartaglia'
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.FATUI
    health_point: int = 10
    max_health_point: int = 10
    skill_list: [CuttingTorrent, FoulLegacy_RagingTide, Havoc_Obliteration]

    power: int = 0
    max_power: int = 3

    def init_state(self, game: GeniusGame):
        '''
            被动技能：战斗开始时, 附属远程状态
        '''
        range_stance = RangedStance(game=game,
                                    from_player=self.from_player,
                                    from_character=self)
        self.character_zone.append()


    def __init__(self, game: GeniusGame, from_player: GeniusPlayer, from_character = None, talent = False):
        super().__init__(game, from_character, from_player)
        self.talent = talent
        self.is_melee_stance = False # 是否为近战状态