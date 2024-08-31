from genius_invocation.card.character.import_head import *
from genius_invocation.card.character.characters.EremiteScorchingLoremaster import SpiritofOmensPower
from genius_invocation.card.action.equipment.specialskill import SpecialSkillCard
from genius_invocation.entity.status import Frozen_Status, SpecialSkill


class SpiritSerpentsBlessing(Combat_Status):
    name = "Spirit Serpent's Blessing"
    name_ch = "灵蛇祝福"
    id = 270331
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1

    def update(self, usage:int = 1):
        self.usage += usage

    def on_add_damage(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.name == "Viny Razorscale":
                game.current_damage.main_damage += 1
                self.usage -= 1
                if self.usage <= 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_add_damage),
        ]

class VinyRazorscale(SpecialSkill):
    name: str = "Viny Razorscale"
    name_ch = "藤蔓锋鳞"
    id = "2703s1"
    cost = [{'cost_num': 1,'cost_type': CostType.WHITE}]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_call(self, game: 'GeniusGame'):
        if self.from_player.team_combat_status.has_status(SpiritSerpentsBlessing):
            not_use = True
        damage = Damage(damage_type=None,
                        main_damage_element=ElementType.DENDRO,
                        main_damage=1,
                        piercing_damage=0,
                        damage_from=self,
                        damage_to=get_opponent_active_character(game))
        game.add_damage(damage)
        game.resolve_damage()
        if not not_use:
            self.check_usage(game)
        game.manager.invoke(EventType.AFTER_USE_SPECIAL, game)


class SpiritofOmenDendroSpiritSerpent(SpecialSkillCard):
    id: int = 270371
    name: str = "Spirit of Omen: Dendro Spirit Serpent"
    name_ch = "厄灵·草之灵蛇"
    time: float = 5.1
    cost_num: int = 0
    cost_type: CostType = None
    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity =  VinyRazorscale

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

class FloralRingCaress(NormalAttack):
    name = "Floral Ring Caress"
    name_ch = "叶轮轻扫"
    id = 270301
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.DENDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class SpiralingWhirl(ElementalSkill):
    name = "Spiraling Whirl"
    name_ch = "蔓延旋舞"
    id = 270302
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        self.add_combat_status(game, SpiritSerpentsBlessing, usage=1)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SpiritofOmensAwakeningDendroSpiritSerpent(ElementalBurst):
    name = "Spirit of Omen's Awakening: Dendro Spirit Serpent"
    name_ch = "厄灵苏醒·草之灵蛇"
    id = 270304
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 4
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        if not self.from_character.has_brust:
            self.from_character.has_brust = True
            self.from_character.from_player.hand_zone.add([SpiritofOmenDendroSpiritSerpent()])
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class EremiteFloralRingDancer(Character):
    id: int = 2703
    name: str = "Eremite Floral Ring Dancer"
    name_ch = "镀金旅团·叶轮舞者"
    time = 5.1
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.EREMITES
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [FloralRingCaress, SpiralingWhirl, SpiritofOmensAwakeningDendroSpiritSerpent]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        self.listen_event(game, EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.on_excute_damage)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]
        self.talent_usage = 1

        self.passive_skill = SpiritofOmensPower(self)
        self.passive_round_usage = 1

        self.has_brust = False


    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.passive_round_usage = 1
            if self.talent:
                self.talent_usage = 1

    def on_excute_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self:
            self.passive_skill.on_call(game)

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_change_character)

    def on_change_character(self, game: 'GeniusGame'):
        if game.current_switch.to_character.from_player == self.from_player:
            if isinstance(game.current_switch.to_character.character_zone.special_skill, VinyRazorscale):
                if self.talent:
                    if self.talent_usage > 0:
                        self.talent_usage -= 1
                        dmg = Damage(
                            damage_type=None,
                            main_damage_element=ElementType.DENDRO,
                            main_damage=1,
                            piercing_damage=0,
                            damage_from=None,
                            damage_to=get_opponent_active_character(game)
                        )
                        game.add_damage(dmg)
                        game.resolve_damage()

