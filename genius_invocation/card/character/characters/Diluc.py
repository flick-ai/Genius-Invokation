from genius_invocation.card.character.import_head import *

class TemperedSword(NormalAttack):
    id: int = 13011
    name = "Tempered Sword"
    name_ch = "淬炼之剑"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.PYRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SearingOnslaught(ElementalSkill):
    id: int = 13012
    name = "Searing Onslaught"
    name_ch = "逆焰之刃"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.from_character.use_element_skill += 1
        if self.from_character.use_element_skill == 3:
            self.resolve_damage(game, add_main_damage=2)
        else:
            self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Dawn(ElementalBurst):
    d: int = 13013
    name = "Dawn"
    name_ch = "黎明"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 8
    piercing_damage: int = 0
    cost = [{'cost_num':4, 'cost_type':CostType.PYRO}]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.add_status(game, PYROElementalInfusion)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class PYROElementalInfusion(Combat_Status):
    name = "PYRO Elemental Infusion"
    name_ch = "火元素附魔"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.max_usage

    def on_infuse(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.PYRO

    def on_begin(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.ACTIVE_ZONE, self.on_infuse),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin)
        ]

class Diluc(Character):
    id: int = 1301
    name: str = "Diluc"
    name_ch = "迪卢克"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [TemperedSword, SearingOnslaught, Dawn]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.use_element_skill = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
    
    def on_begin(self, game: 'GeniusGame'):
        super().on_begin(game)
        self.use_element_skill = 0

    def on_calculate_dice(self, game:'GeniusGame'):
        if game.current_dice.from_character == self:
            if game.current_dice.use_type == SkillType.ELEMENTAL_SKILL:
                if self.use_element_skill == 1:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1

    def on_use_skill(self, game:'GeniusGame'):
        self.on_calculate_dice(game)

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice)
        self.listen_event(game, EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_use_skill)
                    