from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.base import ActionCard


class BloodBondedShadow(CharacterSkill):
    id = 210404
    name = 'Blood-Bonded Shadow'
    name_ch = '血契掠影'
    def on_call(self, game:'GeniusGame', damage:int):
        usage = min(5, damage-2)
        target_zone = get_opponent_active_character(game).character_zone
        target_zone.add_entity(BondofLife(game, get_opponent(game), get_opponent_active_character(game), usgae=usage),
                               usage=usage)
        if self.from_character.talent:
            status = get_opponent_active_character(game).character_zone.has_entity(BondofLife)
            status.usage *= 2

class SwiftPoint(NormalAttack):
    id: int = 210401
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Swift Point"
    name_ch = "迅捷剑锋"
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{
            'cost_num': 1,
            'cost_type': CostType.CRYO
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
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class FrostyInterjection(ElementalSkill):
    id: int = 210402
    name = "Frosty Interjection"
    name_ch = "霜刃截击"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1
    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class OnslaughtStance(Status):
    id = 210421
    name = "Onslaught Stance"
    name_ch = "掠袭之势"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            for character in get_opponent(game).character_list:
                if character.is_alive:
                    if character.character_zone.has_entity(BondofLife) is not None:
                        dmg = Damage.create_damage(
                            game,
                            SkillType.OTHER,
                            main_damage_element=ElementType.PIERCING,
                            main_damage=1,
                            piercing_damage=0,
                            damage_from=self,
                            damage_to=get_opponent_active_character(game),
                        )
                        game.add_damage(dmg)
                        game.resolve_damage()

    def on_end(self, game: 'GeniusGame'):
        self.usage -= 1
        if self.usage == 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
        ]

class ThornyOnslaught(ElementalBurst):
    id = 210403
    name: str = "Thorny Onslaught"
    name_ch = "掠袭之刺"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_status(game, OnslaughtStance)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class FrostOperative(Character):
    id = 2104
    name = "Frost Operative"
    name_ch = "愚人众·霜役人"
    time = 4.8
    element = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    country_list: List[CountryType] = [CountryType.MONSTER, CountryType.FATUI]

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [SwiftPoint, FrostyInterjection, ThornyOnslaught]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_use_skill)
        self.listen_event(game, EventType.EXCUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_excute)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
        self.passive_skill = BloodBondedShadow(self)
        self.skill_damage = 0

    def on_excute(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self:
            self.skill_damage = game.current_damage.max_main_damage

    def after_use_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self:
            self.passive_skill(game, self.skill_damage)
