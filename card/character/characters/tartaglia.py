from card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from entity.character import Character
from entity.entity import Entity
from utils import *
from typing import TYPE_CHECKING, List, Tuple

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
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.opponent = None

    def find_next_alive_character(self, current_character: 'Character'):
        '''
            找到下一个活着的角色
        '''
        current_idx = current_character.index
        while True:
            current_idx = (current_idx + 1) % current_character.from_player.character_num
            if current_idx == current_character.index:
                break
            if current_character.from_player.character_list[current_idx].is_alive:
                return current_character.from_player.character_list[current_idx]
        return None


    def on_after_use_skill(self, game: 'GeniusGame'):
        '''
            近战状态的达达利亚对已附属有断流的角色使用技能后:
            对下一个敌方后台角色造成1点穿透伤害
        '''
        if self.opponent:
            next_character = self.find_next_alive_character(self.opponent)
            if next_character:
                Damage.resolve_damage(game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.PIERCING,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self.from_character,
                    damage_to=next_character,
                    is_plunging_attack=False,
                    is_charged_attack=False)
            self.opponent = None


    def on_use_skill(self, game: 'GeniusGame'):
        '''
            用于在使用技能后，判断角色是否有断流
            目前on_use_skill仅用于达达利亚
        '''
        active_index = game.players[game.active_player].active_idx
        if self.from_character == game.players[game.active_player].character_list[active_index]:
            opponent = get_opponent_active_character(game)
            if opponent.character_zone.has_entity(Riptide):
                '''
                    当前攻击的角色具有断流
                '''
                self.opponent = opponent

    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_use_skill),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_use_skill),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add)
        ]


class Riptide(Status):
    '''
        断流
        实现逻辑:
        当角色死亡时, 会调用on_distroy, 这时候先建一个新的断流
    '''
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.attached = False # 是否附着

    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_switch_character)
        ]

    def on_damage_add(self, game: 'GeniusGame'):
        '''
            近战状态下的达达利亚对附属有断流的角色造成的伤害+1
        '''
        if game.players[0] == self.from_player:
            tartaglia_player = game.players[1]
        else:
            tartaglia_player = game.players[0]
        tartaglia = get_character_with_name(tartaglia_player, Tartaglia)
        if game.current_damage.damage_from == tartaglia and tartaglia.is_melee_stance:
            game.current_damage.main_damage += 1

    def find_next_alive_character(self, current_character: 'Character'):
        '''
            找到下一个活着的角色
        '''
        current_idx = current_character.index
        while True:
            current_idx = (current_idx + 1) % current_character.from_player.character_num
            if current_idx == current_character.index:
                break
            if current_character.from_player.character_list[current_idx].is_alive:
                return current_character.from_player.character_list[current_idx]
        return None

    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时，先结算未结算的事件
        '''


    # def on_distroy(self, game: 'GeniusGame'):
    #     super().on_destroy()
    #     # 新的断流
    #     new_riptide = Riptide(game=game,
    #                       from_player=self.from_player,
    #                       from_character=None)

    # def on_switch_character(self, game: 'GeniusGame'):
    #     if not self.attached:
    #         # 附着到新的出战角色上
    #         new_character = self.from_player.character_list[self.from_player.active_idx]
    #         new_character.character_zone.add_entity(self)
    #         self.from_character = new_character
    #         self.attached = True

    def on_end_phase(self, game: 'GeniusGame'):
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
    main_damage: int = 5
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

    def on_call(self, game: 'GeniusGame'):
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

    def on_call(self, game: 'GeniusGame'):
        pass

class Havoc_Obliteration(ElementalBurst):
    '''
    '''
    id: int = 2
    def __init__(self, from_character: 'Character') -> None:
        self.from_character = from_character
        self.flash_of_havoc = FlashOfHavoc(from_character)
        self.light_of_havoc = LightOfHavoc(from_character)

    def on_call(self, game: 'GeniusGame'):
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
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [CuttingTorrent, FoulLegacy_RagingTide, Havoc_Obliteration]

    power: int = 0
    max_power: int = 3

    def init_state(self, game: 'GeniusGame'):
        '''
            被动技能：战斗开始时, 附属远程状态
        '''
        range_stance = RangedStance(game=game,
                                    from_player=self.from_player,
                                    from_character=self)
        self.character_zone.append()


    def __init__(self, game: 'GeniusGame', zone, from_player: 'GeniusPlayer', from_character = None, talent = False):
        super().__init__(game, zone, from_character, from_player)
        self.talent = talent
        self.is_melee_stance = False # 是否为近战状态