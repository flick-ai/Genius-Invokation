from genius_invocation.card.character.import_head import *


class KhandaBarrierBuster(NormalAttack):
    id: int = 17021
    name = "Khanda Barrier-Buster"
    name_ch = "藏蕴破障"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.ELECTRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class VijnanaPhalaMine(ElementalSkill):
    id: int = 17022
    name = "Vijnana-Phala Mine"
    name_ch = "识果种雷"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        if self.from_character.talent:
            characters = [get_my_active_character(game)] + get_my_standby_character(game)
            for char in characters:
                if char.element == ElementType.ELECTRO:
                    if char.max_power != char.power:
                        char.get_power(power=1)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class VijnanaSuffusion(Status):
    name = "Vijnana Suffusion"
    name_ch = " 通塞识"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = max(self.max_usage, self.current_usage)

    def on_after_skill(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK or game.current_damage.damage_type == SkillType.ELEMENTAL_SKILL:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.ELECTRO,
                    main_damage=2,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                    )
                game.add_damage(dmg)
                game.resolve_damage()

    def on_begin(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_skill),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

class FashionersTanglevineShaft(ElementalBurst):
    id: int = 17023
    name = "Fashioner's Tanglevine Shaft"
    name_ch = "造生缠藤箭"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_status(TheWolfWithin(game, self.from_character.from_player, self.from_character))
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Tighnari(Character):
    id: int = 1702
    name: str = "Tighnari"
    name_ch = "提纳里"
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.SUNERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
