from genius_invocation.card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from genius_invocation.entity.character import Character
from genius_invocation.entity.entity import Entity
from genius_invocation.entity.summon import Summon
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple


if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.game.zone import CharacterZone
    
from genius_invocation.event.damage import Damage
from genius_invocation.entity.status import Status

class ElectroCrystalProjection(NormalAttack):
    '''
        雷晶投射
    '''
    id: int = 0
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Electro Crystal Projection"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ELECTRO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class RockPaperScissorsCombo_Paper(ElementalSkill):
    '''
        猜拳三连击·布
    '''
    name = 'Rock-Paper-Scissors Combo: Paper'
    id: int = 11
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.from_character.from_player.prepared_skill = None


class PreparePaper(Status):
    '''
        准备技能: 猜拳三连击·布
    '''
    name = 'Prepare for Paper'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.skill = RockPaperScissorsCombo_Paper(from_character=from_character)

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)

    def on_destroy(self, game):
        return super().on_destroy(game)


class RockPaperScissorsCombo_Scissors(ElementalSkill):
    '''
        猜拳三连击·剪刀
    '''
    name = 'Rock-Paper-Scissors Combo: Scissors'
    id: int = 12
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        prepare_paper = PreparePaper(game=game,
                                     from_player=self.from_character.from_player,
                                     from_character=self.from_character)
        self.from_character.character_zone.add_entity(prepare_paper)
        self.from_character.from_player.prepared_skill = prepare_paper
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class PrepareScissors(Status):
    '''
        准备技能: 猜拳三连击·剪刀
    '''
    name = 'Prepare for Scissors'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.skill = RockPaperScissorsCombo_Scissors(from_character=from_character)

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)

    def on_destroy(self, game):
        return super().on_destroy(game)




class RockPaperScissorsCambo(ElementalSkill):
    '''
        猜拳三连击
    '''
    id: int = 1
    type: SkillType = SkillType.ELEMENTAL_SKILL
    name = 'Rock-Paper-Scissors Combo'
    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 5,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        prepare_scissors = PrepareScissors(game=game,
                                     from_player=self.from_character.from_player,
                                     from_character=self.from_character)
        self.from_character.character_zone.add_entity(prepare_scissors)
        self.from_character.from_player.prepared_skill = prepare_scissors
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class ChainsOfWardingThunder(Summon):
    '''
        雷锁镇域
    '''
    name = 'Chains of Warding Thunder'
    element: ElementType = ElementType.ELECTRO
    usage: int = 2
    max_usage: int = 2
    removable = True
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.usage
        self.used_this_round = 1

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == 1 - self.from_player.index:
            if self.used_this_round > 0:
                if game.current_dice.use_type == 'change character':
                    game.current_dice.cost[0]['cost_num'] += 1

    def on_change(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.used_this_round -= 1

    def update(self):
        self.current_usage = self.usage

    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成1点雷元素伤害
            结束阶段分先后手两次调用on_end_phase, 所以需要判断
        '''
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if(self.current_usage <= 0):
            '''
                Entity在被移除时, 调用on_destroy移除监听并执行对应的移除操作(在对应区域中移除此entity等)
            '''
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUMMON_ZONE, self.on_change),
            (EventType.CALCULATE_DICE, ZoneType.SUMMON_ZONE, self.on_calculate),
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]



class LightningLockdown(ElementalBurst):
    '''
        元素爆发
        雳霆镇锁
    '''
    id: int = 2
    type: SkillType = SkillType.ELEMENTAL_BURST
    name = 'Lightning Lockdown'
    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 消耗能量
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        self.generate_summon(game, ChainsOfWardingThunder)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ElectroCrystalCore(Status):
    '''
        雷晶核心
    '''
    name = 'Electro Crystal Core'
    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时
        '''
        if not self.from_character.is_alive:
            self.from_character.is_alive = True
            self.from_character.health_point = 1
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        ]

class ElectroHypostasis(Character):
    '''
        无相之雷
    '''
    id: int = 2401
    name: str = 'Electro Hypostasis'
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 8
    max_health_point: int = 8
    skill_list: List = [ElectroCrystalProjection, RockPaperScissorsCambo, LightningLockdown]

    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        '''
            被动技能: 战斗开始时, 初始附属雷晶核心
        '''
        electro_crystal_core = ElectroCrystalCore(game=game,
                                                  from_player=self.from_player,
                                                  from_character=self)
        self.character_zone.add_entity(electro_crystal_core)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent