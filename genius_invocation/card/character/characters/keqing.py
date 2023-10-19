from genius_invocation.card.character.base import NormalAttack, ElementalSkill, ElementalBurst
from genius_invocation.entity.entity import Entity
from genius_invocation.utils import *
from typing import TYPE_CHECKING, List, Tuple
from genius_invocation.card.action.base import ActionCard
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.event.events import ListenerNode
    from genius_invocation.game.player import GeniusPlayer
    from genius_invocation.event.damage import Damage
from genius_invocation.entity.character import Character
from genius_invocation.entity.status import Status, Combat_Status
from loguru import logger
class Yunlai_Swordsmanship(NormalAttack):
    '''
    刻晴
    普通攻击
    '''
    id: int = 0
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Yunlai Swordsmanship"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
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

class StellarRestoration(ElementalSkill):
    '''
    刻晴
    元素战技
    '''
    id: int = 1
    name = "Stellar Restoration"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def add_status(self, game: 'GeniusGame'):
        char = get_my_active_character(game)
        assert isinstance(char, Keqing)
        status = self.from_character.character_zone.has_entity(Electro_Elemental_Infusion)
        if status is None:
            status = Electro_Elemental_Infusion(game=game,
                    from_player=game.active_player,
                    from_character=char)
            self.from_character.character_zone.add_entity(status)
        else:
            status.update()


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        if isinstance(game.current_card, Lightning_Stiletto) \
                or self.from_character.from_player.hand_zone.has_card(Lightning_Stiletto) is not None:
            self.add_status(game)
            self.from_character.from_player.hand_zone.remove_name(Lightning_Stiletto)
        else:
            self.from_character.from_player.hand_zone.add([Lightning_Stiletto()])
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
class StarwardSword(ElementalBurst):
    '''
    刻晴
    天街巡游!
    '''
    id = 2
    name="Starward Sword"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 4
    piercing_damage: int = 3

    # cost
    cost = [
        {
            'cost_num': 4,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class Keqing(Character):
    id: int = 1403
    name = "Keqing"
    element = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.LIYUE

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Yunlai_Swordsmanship, StellarRestoration, StarwardSword]

    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone, from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0

class Lightning_Stiletto(ActionCard):
    id: int = -1 #TODO: CHECK THE ID
    name: str = 'Lightning Stiletto'
    cost_num = 3
    cost_type = CostType.ELECTRO
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        super().on_played(game)
        char = get_character_with_name(game.active_player, Keqing)
        assert char is not None
        assert char.is_alive
        logger.info("USE Lightning Stiletto")
        idx = char.index
        if game.active_player.active_idx != idx:
            logger.info("Switch to Keqing.")
            game.manager.invoke(EventType.ON_CHANGE_CHARACTER, game)
            game.active_player.change_to_id(idx)
        logger.info("Use Keqing's Elemental Skill from Lightning Stiletto.")

        game.is_change_player = True
        char.skills[1].on_call(game)





class Electro_Elemental_Infusion(Status):
    def __init__(self, game, from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.max_usage = 2
        if self.from_character.talent:
            self.usage = 3
            self.current_usage = 3
            self.max_usage = 3

    def update(self):
        if self.from_character.talent:
            self.usage = 3
        self.current_usage = self.usage

    def infuse(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.ELECTRO

    def on_dmg_add(self, game: 'GeniusGame'):
        if self.from_character.talent:
            if game.current_damage.damage_from == self.from_character:
                if game.current_damage.main_damage_element == ElementType.ELECTRO:
                    game.current_damage.main_damage += 1

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_character.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infuse),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)
        ]
