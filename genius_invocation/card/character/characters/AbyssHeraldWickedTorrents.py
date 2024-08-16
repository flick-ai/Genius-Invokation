from genius_invocation.card.character.import_head import *


class RipplingSlash(NormalAttack):
    name = "Rippling Slash"
    name_ch = "波刃锋斩"
    id = 22031
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

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

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class VortexEdge(ElementalSkill):
    name = "Vortex Edge"
    name_ch = "洄涡锋刃"
    id = 22032
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]

    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.resolve_damage(game)
        self.gain_energy(game)
        Next_Skill = self.from_character.next_skill
        prepare_status = PrepareRipplingBlades(game, self.from_character.from_player, self.from_character, Next_Skill)
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class RipplingBlades(ElementalSkill):
    name = "Rippling Blades"
    name_ch = "涟锋旋刃"
    id = 22034
    type = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element = ElementType.HYDRO
    main_damage: int = 1
    piercing_damage: int = 0
    is_prepared_skill = True

    cost =[]
    energy_cost = 0
    energy_gain = 0
    def __init__(self, from_character: 'Character') -> None:
        super().on_call(from_character)

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.from_character.from_player.prepared_skill = None


class PrepareRipplingBlades(Status):
    name = "Prepare Rippling Blades"
    name_ch = "准备技能: 涟锋旋刃"
    def __init__(self, game:'GeniusGame', from_player:'GeniusPlayer', from_character:'Character', next_skill: 'CharacterSkill'):
        super().__init__(game, from_player, from_character)
        self.next_skill = next_skill
        self.current_usage = 1

    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.next_skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]


class TorrentialShock(ElementalBurst):
    name = "Torrential Shock"
    name_ch = "激流强震"
    id = 22033
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 3
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
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

        target_zone = get_opponent(game).team_combat_status
        target_zone.add_entity(CurseoftheUndercurrent(game, from_player=get_opponent(game), from_character=None))

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class CurseoftheUndercurrent(Combat_Status):
    name = "Curse of the Undercurrent"
    name_ch = "暗流的诅咒"
    max_usage = 2
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.max_usage

    def update(self):
        self.current_usage = self.max_usage

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in [SkillType.ELEMENTAL_BURST,
                                              SkillType.ELEMENTAL_SKILL]:
                game.current_dice.cost[0]['cost_num'] += 1
                return True

    def on_skill(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)


    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate_dice),
            (EventType.ON_USE_SKILL, ZoneType.ACTIVE_ZONE, self.on_skill)
        ]

class WateryRebirth(Status):
    name = "Watery Rebirth"
    name_ch = "水之新生"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def on_character_die(self, game: 'GeniusGame'):
        if not self.from_character.is_alive:
            self.from_character.is_alive = True
            self.from_character.health_point = 0
            self.from_character.heal(4, game, heal_type=HealType.REVIVE)
            self.from_character.revive_event(game)
            if self.from_character.talent:
                target_zone = get_opponent(game).team_combat_status
                target_zone.add_entity(CurseoftheUndercurrent(game, from_player=get_opponent(game), from_character=None))
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        ]

class AbyssHeraldWickedTorrents(Character):
    id: int = 2203
    name: str = "Abyss Herald: Wicked Torrents"
    name_ch = "深渊使徒·激流"
    time = 4.6
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 6
    max_health_point: int = 6
    skill_list: List = [RipplingSlash, VortexEdge, TorrentialShock]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        rebirth = WateryRebirth(game, self.from_player, self)
        self.character_zone.add_entity(rebirth)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = None
        self.next_skill = RipplingSlash(self)

    def on_dmg_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self:
            if game.current_damage.main_damage_element == ElementType.HYDRO:
                game.current_damage.main_damage += 1

    def infusion(self, game:'GeniusGame'):
        if self.from_character == game.current_damage.damage_from:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.HYDRO

    def revive_event(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)
        self.listen_event(game, EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion)

    def equip_talent(self, game:'GeniusGame', is_action=True, talent_card=None):
        self.talent = True
        self.character_zone.talent_card = talent_card
        if self.character_zone.has_entity(WateryRebirth) is None:
            target_zone = get_opponent(game).team_combat_status
            target_zone.add_entity(CurseoftheUndercurrent(game, from_player=get_opponent(game), from_character=None))
