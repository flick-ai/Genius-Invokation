from genius_invocation.card.character.import_head import *

class HurtlingBolts(NormalAttack):
    name = 'Hurtling Bolts'
    name_ch = "轰闪落雷"
    id = 24041
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
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
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class MistyCall(ElementalSkill):
    name = 'Misty Call'
    name_ch = '雾虚之召'
    id = 24042
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
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

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.generate_summon(game, ElectroCicin)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class ThunderingShield(ElementalBurst):
    name = 'Thundering Shield'
    name_ch = '霆雷之护'
    id = 24043
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        }
    ]

    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        self.from_character.elemental_attach(game, ElementType.ELECTRO)
        self.add_combat_shield(game, ElectroCicinShield)

        Next_Skill = self.from_character.next_skill
        prepare_status = PrepareSurgingThunder(game, self.from_character.from_player, self.from_character, Next_Skill)
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SurgingThunder(ElementalBurst):
    name = "Surging Thunder"
    name_ch = "霆电迸发"
    id = 22034
    type = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element = ElementType.ELECTRO
    main_damage: int = 2
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

class PrepareSurgingThunder(Status):
    name = "Prepare Surging Thunder"
    name_ch = "准备技能: 霆电迸发"
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


class ElectroCicin(Summon):
    name = 'Electro Cicin'
    name_ch = '雷萤'
    removable = True
    element = ElementType.ELECTRO
    max_usage = 3
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.max_usage
        self.count = 0
        self.opponent = game.players[1 - from_player.index]

    def on_end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.ELECTRO,
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

    def after_play_card(self, game: 'GeniusGame'):
        if game.active_player == self.opponent:
            self.count += 1
            if self.count >= 3:
                self.count = 0
                self.current_usage = min(self.current_usage + 1, self.max_usage)

    def before_action(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.from_character.is_alive and self.from_character.talent:
                if self.current_usage >= self.max_usage:
                    dmg = Damage.create_damage(
                        game,
                        damage_type=SkillType.SUMMON,
                        main_damage_element=ElementType.ELECTRO,
                        main_damage=1,
                        piercing_damage=0,
                        damage_from=self,
                        damage_to=get_opponent_active_character(game)
                    )
                    game.add_damage(dmg)
                    game.resolve_damage()
                    self.current_usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
            (EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.SUMMON_ZONE, self.on_reaction),
            (EventType.AFTER_PLAY_CARD, ZoneType.SUMMON_ZONE, self.after_play_card),
        ]
        if self.from_character.talent:
            self.listeners.append((EventType.BEFORE_ANY_ACTION, ZoneType.SUMMON_ZONE, self.before_action))


class ElectroCicinShield(Combat_Shield):
    name = 'Electro Cicin Shield'
    name_ch = '雷萤护罩'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        cicin = self.from_player.summon_zone.has_entity(ElectroCicin)
        if cicin is not None:
            self.current_usage = self.usage + min(cicin.current_usage,3)
        else:
            self.current_usage = self.usage

    def update(self):
        cicin = self.from_player.summon_zone.has_entity(ElectroCicin)
        if cicin is not None:
            self.current_usage = max(self.current_usage, self.usage + min(cicin.current_usage,3))
        else:
            self.current_usage = max(self.current_usage, self.usage)

class FatuiElectroCicinMage(Character):
    id: int = 2404
    name: str = "Fatui Electro Cicin Mage"
    name_ch = "愚人众·雷萤术士"
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [HurtlingBolts, MistyCall, ThunderingShield]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        self.next_skill = SurgingThunder(self)

    def listen_talent_events(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status()
        if status is not None:
            status.listen_event(game, EventType.BEFORE_ANY_ACTION, ZoneType.SUMMON_ZONE, status.before_action)


