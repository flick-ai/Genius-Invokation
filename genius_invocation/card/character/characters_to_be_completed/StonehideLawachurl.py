from genius_invocation.card.character.import_head import *
class PlamaLawa(NormalAttack):
    id: int = 26011
    name = "Plama Lawa"
    name_ch = "Plama Lawa"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.GEO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class MovoLawa(ElementalSkill):
    id: int = 26012
    name = "Movo Lawa"
    name_ch = "Movo Lawa"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class UpaShato(ElementalBurst):
    id: int = 26013
    name = "Upa Shato"
    name_ch = "Upa Shato"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 5
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class InfusedStonehide(Combat_Status):
    name = "Infused Stonehide"
    name_ch = "魔化：岩盔"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = self.usage

        self.usage_round = 1
        self.round = 1

    def update(self):
        self.current_usage = self.max_usage

    def on_infuse(self, game:'GeniusGame'):
        if game.current_damage.damage_from== self.from_character:
            if game.current_damage.damage_type == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.GEO

    def on_add_damage(self, game:'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage_round = 1
        if game.current_damage.damage_from == self.from_character:
            if self.usage_round > 0:
                game.current_damage.main_damage += 1
                self.usage_round -= 1

    def on_execute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element != ElementType.PIERCING:
                if game.current_damage.main_damage > 0:
                    game.current_damage.main_damage -= 1
                    self.current_usage -= 1
                    if self.current_usage <=0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.on_infuse)
        ]


class StonehideLawachurl(Character):
    id: int = 2601
    name: str = "Stonehide Lawachurl"
    name_ch = "丘丘岩盔王"
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 8
    max_health_point: int = 8
    skill_list: List = [PlamaLawa, MovoLawa, UpaShato]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]

    def init_state(self, game: 'GeniusGame'):
        status = InfusedStonehide(game, self.from_player, self)
        self.character_zone.add_entity(status)

    def reget_InfusedStonehide(self, game: 'GeniusGame'):
        if self.talent:
            if game.current_skill.from_character == self:
                if not get_opponent_active_character(game).is_alive:
                    status = self.character_zone.has_entity(InfusedStonehide)
                    if status is None:
                        status = InfusedStonehide(game, self.from_player, self)
                        self.character_zone.add_entity(status)
                    else:
                        status.update()

        