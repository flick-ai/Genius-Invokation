from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.equipment.specialskill import SpecialSkillCard
from genius_invocation.entity.status import Frozen_Status, SpecialSkill

class DriftcloudWave(Status):
    name = 'Driftcloud Wave'
    name_ch = "闲云冲击波"
    id = 151021
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.max_usage = 2

    def update(self):
        self.usage = min(self.max_usage, self.usage + 1)

    def after_change_character(self, game: 'GeniusGame'):
        if game.current_switch.to_character == self.from_character:
            damage = Damage(damage_type=None,
                            main_damage_element=ElementType.ANEMO,
                            main_damage=1,
                            piercing_damage=0,
                            damage_from=self,
                            damage_to=get_opponent_active_character(game))
            game.add_damage(damage)
            game.resolve_damage()
            self.usage -= 1
            if self.usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change_character)
        ]

class Skyladder(Combat_Status):
    name = "Skyladder"
    name_ch = "步天梯"
    id = 151031
    def __init__(self, game:'GeniusGame', from_player:'GeniusPlayer', from_character:'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.max_usage = 2

    def update(self):
        self.usage = min(self.max_usage, self.usage + 1)

    def on_change_character(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.usage -= 1
            if self.usage <= 0:
                self.on_destroy(game)

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.current_dice.from_player == self.from_player:
            if game.current_dice.use_type == SwitchType.CHANGE_CHARACTER:
                if game.current_dice.cost[0]['cost_num'] > 0:
                    game.current_dice.cost[0]['cost_num'] -= 1
                    return True
        return False

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_change_character),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice)
        ]

class AdeptalAssistance(SpecialSkill):
    name: str = "Adeptal Assistance"
    name_ch = "仙力助推"
    id = "1510s1"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.begin_invoke = False
        self.has_used = False

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.from_character.heal(2)
        self.begin_invoke = True
        self.check_usage()
        game.manager.invoke(EventType.AFTER_USE_SPECIAL, game)

    def on_use_skill(self, game: 'GeniusGame'):
        if self.begin_invoke:
            if game.current_skill.from_character == self.from_character:
                if game.current_skill.type == SkillType.NormalAttack:
                    game.current_skill.is_plunging_attack = True
                    self.has_used = True

    def on_add_damage(self, game: 'GeniusGame'):
        if self.has_used:
            game.current_damage.main_damage += 1

    def after_skill(self, game: 'GeniusGame'):
        if self.has_used:
            damage = Damage(damage_type=None,
                            main_damage_element=ElementType.ANEMO,
                            main_damage=1,
                            piercing_damage=0,
                            damage_from=self,
                            damage_to=get_opponent_active_character(game))
            game.add_damage(damage)
            game.resolve_damage()

            self.has_used = False
            self.begin_invoke = False

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_use_skill),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill)
        ]

class Starwicker(SpecialSkillCard):
    id: int = 151071
    name: str = "Starwicker"
    name_ch = "竹星"
    time: float = 5.0
    cost_num: int = 0
    cost_type: CostType = None

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = AdeptalAssistance

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)


class WordofWindandFlower(NormalAttack):
    name = 'Word of Wind and Flower'
    name_ch = "清风散花词"
    id: int = 151001
    type: SkillType = SkillType.NORMAL_ATTACK

    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
    piercing_damage: int = 0

    cost = [{'cost_num': 1,'cost_type': CostType.ANEMO},{'cost_num': 2,'cost_type': CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class WhiteCloudsatDawn(ElementalSkill):
    id = 151002
    name = 'White Clouds at Dawn'
    name_ch = "朝起鹤云"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [{'cost_num': 3,'cost_type': CostType.ANEMO},]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)

        self.add_combat_status(Skyladder(game, self.from_player))
        self.add_status(DriftcloudWave(game, self.from_player, self.from_character))

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class StarsGatheratDusk(ElementalBurst):
    id = 151003
    name = "Stars Gather at Dusk"
    name_ch = "暮集竹星"
    type: SkillType = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
    piercing_damage: int = 0

    cost = [{'cost_num': 3, 'cost_type': CostType.ANEMO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)

        for character in self.from_character.from_player.character_list:
            if character.is_alive:
                character.heal(1, game)
        self.from_character.from_player.hand_zone.add([Starwicker()])

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Xianyun(Character):
    id = 1510
    name = "Xianyun"
    name_ch = "闲云"
    time = 5.0
    element = ElementType.ANEMO
    weapon_type = WeaponType.CATALYST
    country = CountryType.LIYUE

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        WordofWindandFlower,
        WhiteCloudsatDawn,
        StarsGatheratDusk
    ]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
        self.talent_usage = 2
        self.stormpinion = 0

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_final_end)
        self.listen_event(game, EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_change_character)
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)

    def on_change_character(self, game: 'GeniusGame'):
        if game.current_switch.from_player == self.from_player:
            if self.talent_usage > 0:
                self.stormpinion += 1

    def on_final_end(self, game: 'GeniusGame'):
        self.talent_usage = 2

    def on_add_damage(self, game: 'GeniusGame'):
        if self.talent:
            if game.current_damage.damage_from == self:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    game.current_damage.main_damage += self.stormpinion
                    self.stormpinion = 0
