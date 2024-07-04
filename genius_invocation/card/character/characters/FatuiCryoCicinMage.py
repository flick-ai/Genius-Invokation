from genius_invocation.card.character.import_head import *

class Cicin_Icicle(NormalAttack):
    name = 'Cicin Icicle'
    name_ch = "冰萤棱锥"
    id = 21011
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
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
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        cicins = self.from_character.from_player.summon_zone.has_entity(Cryo_Cicins)
        if cicins is not None:
            cicins.add_one_usage(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Misty_Summons(ElementalSkill):
    name = 'Misty Summons'
    name_ch = '雾虚摇唤'
    id = 21012
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
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
        self.generate_summon(game, Cryo_Cicins)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Blizzard(ElementalBurst):
    name = 'Blizzard'
    name_ch = '冰枝白花'
    id = 21013
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 5
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        }
    ]

    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        self.from_character.elemental_attach(game, ElementType.CRYO)
        self.add_combat_shield(game, Flowing_Cicin_Shield)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Cryo_Cicins(Summon):
    name = 'Cryo Cicins'
    name_ch = '冰萤'
    removable = True
    element = ElementType.CRYO
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 3
        self.current_usage = self.usage

    def update(self, game:'GeniusGame'):
        use = self.current_usage + self.usage
        if use > self.max_usage:
            self.current_usage = self.max_usage
            if self.from_character.talent:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.CRYO,
                    main_damage=2,
                    piercing_damage=0,
                    damage_from=self.from_character,
                    damage_to=get_opponent_active_character(game)
                )
                game.add_damage(dmg)
                game.resolve_damage()
        else:
            self.current_usage = use

    def add_one_usage(self, game:'GeniusGame'):
        if self.current_usage >= self.max_usage:
            if self.from_character.talent:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.CRYO,
                    main_damage=2,
                    piercing_damage=0,
                    damage_from=self.from_character,
                    damage_to=get_opponent_active_character(game)
                )
                game.add_damage(dmg)
                game.resolve_damage()
        else:
            self.current_usage += 1

    def on_end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.CRYO,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)
    def on_reaction(self, game: 'GeniusGame'):
        if game.current_damage.reaction is not None:
            if game.current_damage.damage_to == self.from_character:
                self.current_usage -= 1
                if self.current_usage <=0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
            (EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.SUMMON_ZONE, self.on_reaction),
        ]

class Flowing_Cicin_Shield(Combat_Shield):
    name = 'Flowing Cicin Shield'
    name_ch = '流萤护罩'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        cicin = self.from_player.summon_zone.has_entity(Cryo_Cicins)
        if cicin is not None:
            self.current_usage = self.usage + min(cicin.current_usage,3)
        else:
            self.current_usage = self.usage

    def update(self):
        cicin = self.from_player.summon_zone.has_entity(Cryo_Cicins)
        if cicin is not None:
            self.current_usage = max(self.current_usage, self.usage + min(cicin.current_usage,3))
        else:
            self.current_usage = max(self.current_usage, self.usage)

class FatuiCryoCicinMage(Character):
    id: int = 2101
    name: str = "Fatui Cryo Cicin Mage"
    name_ch = "愚人众·冰萤术士"
    time = 3.7
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Cicin_Icicle, Misty_Summons, Blizzard]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]


