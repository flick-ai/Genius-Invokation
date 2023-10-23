from genius_invocation.card.character.characters.import_head import *

class Spiritfox_SinEater(NormalAttack):
    id = 0
    type = SkillType.NORMAL_ATTACK
    name = "Spiritfox Sin-Eater"
    name_ch = "狐灵食罪式"
    # damage
    damage_type = SkillType.NORMAL_ATTACK
    main_damage_element = ElementType.ELECTRO
    main_damage = 1
    piercing_damage = 0

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
    energy_cost = 0
    energy_gain = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Yakan_Evocation_Sesshou_Sakura(ElementalSkill):
    id = 1
    name = "Yakan Evocation: Sesshou Sakura"
    name_ch = "野干役咒·杀生樱"
    type = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type = SkillType.ELEMENTAL_SKILL
    main_damage_element = ElementType.ELECTRO
    main_damage = 0
    piercing_damage = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        },
    ]
    energy_cost = 0
    energy_gain = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 召唤杀生樱
        self.generate_summon(game, Sesshou_Sakura)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Great_Secret_Art_Tenko_Kenshin(ElementalBurst):
    id = 2
    name = "Great Secret Art: Tenko Kenshin"
    name_ch = "大密法·天狐显真"
    type = SkillType.ELEMENTAL_BURST

    damage_type = SkillType.ELEMENTAL_BURST
    main_damage_element = ElementType.ELECTRO
    main_damage = 4
    piercing_damage = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        },
    ]

    energy_cost = 2
    energy_gain = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        summon = self.from_character.from_player.summon_zone.has_entity(Sesshou_Sakura)
        if summon is not None:
            summon.on_destroy(game)
            assert(self.from_character.from_player.team_combat_status.has_status(Tenko_Thunderbolts) is None)
            self.from_character.from_player.team_combat_status.add_entity(Tenko_Thunderbolts(game, self.from_character.from_player, self.from_character))
            if self.from_character.talent:
                self.from_character.character_zone.add_entity(SaveDice_Sakura(game, self.from_character.from_player, self.from_character))
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Yae_Miko(Character):
    id = 1408
    name = 'Yae Miko'
    name_ch = "八重神子"
    element = ElementType.ELECTRO
    weapon_type = WeaponType.CATALYST
    country = CountryType.INAZUMA
    init_health_point = 10
    max_health_point = 10
    skill_list = [Spiritfox_SinEater, Yakan_Evocation_Sesshou_Sakura, Great_Secret_Art_Tenko_Kenshin]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0

class Sesshou_Sakura(Summon):
    name = "Sesshou Sakura"
    name_ch = "杀生樱"
    removable = True
    element = ElementType.ELECTRO
    usage = 3
    max_usage = 6
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.usage
    def update(self):
        self.current_usage = max(self.current_usage, min(self.max_usage, self.current_usage + 3)) # TODO: Check update
    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if(self.current_usage <= 0):
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

class Tenko_Thunderbolts(Combat_Status):
    name = "Tenko Thunderbolts"
    name_ch = "天狐霆雷"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    def update(self):
        assert False # Should no update!

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage=3,
                main_damage_element=ElementType.ELECTRO,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEFORE_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

class SaveDice_Sakura(Status):
    name = "Save Dice for Sakura"
    name_ch = "神篱之御荫-效果"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
        self.max_usage = 1

    def update(self):
        assert False
        # Should no update.

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type is SkillType.ELEMENTAL_SKILL:
                if game.current_dice.from_character == self.from_character:  #Yae Miko use elemental skill, no action card.
                    if self.usage > 0:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] -= 2
                            game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num'])
                            return True

        return False

    def on_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)
    def end_phase(self, game:'GeniusGame'):
        if self.from_player == game.active_player:
            self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.end_phase),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill)
        ]
