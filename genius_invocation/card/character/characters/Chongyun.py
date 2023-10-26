from genius_invocation.card.character.import_head import *

class Demonbane(NormalAttack):
    id: int = 11041
    name = "Demonbane"
    name_ch = "灭邪四式"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.CRYO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class LayeredFrost(ElementalSkill):
    id: int = 11042
    name = "Chonghua's Layered Frost"
    name_ch = "重华叠霜"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.CRYO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.add_status(game, FrostField)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class FrostField(Combat_Status):
    name = "Chonghua's Layered Frost"
    name_ch = "重华叠霜"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.current_usage = 2
        if self.from_character.talent:
            self.max_usage += 1
            self.current_usage += 1

    def update(self):
        if self.from_character.talent:
            self.max_usage = 3
        self.current_usage = self.max_usage

    def on_infuse(self, game:'GeniusGame'):
        if game.current_damage.damage_from.from_player == self.from_player:
            if game.current_damage.damage_from.from_character.weapon_type in [WeaponType.SWORD, WeaponType.POLEARM, WeaponType.CLAYMORE]:
                if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                    game.current_damage.main_damage_element = ElementType.CRYO

    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from.from_player == self.from_player:
            if game.current_damage.damage_from.from_character.weapon_type in [WeaponType.SWORD, WeaponType.POLEARM, WeaponType.CLAYMORE]:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    game.current_damage.main_damage += 1
    
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
        if self.from_character.talent:
            self.listeners.append(EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_add_damage)

class CloudPartingStar(ElementalBurst):
    id: int = 11043
    name = "Cloud-Parting Star"
    name_ch = "云开星落"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 7
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.CRYO}]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Chongyun(Character):
    id: int = 1104
    name: str = "Chongyun"
    name_ch = "重云"
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Demonbane, LayeredFrost, CloudPartingStar]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
    
    def listen_talent_events(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status(FrostField)
        if status is not None:
            status.listen_event(game, EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, status.on_add_damage)
