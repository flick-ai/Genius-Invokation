from genius_invocation.card.character.import_head import *



class Whirlwind_Thrust(NormalAttack):
    name = "Whirlwind Thrust"
    name_ch = "卷积微尘"
    id = 150401
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ANEMO
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


class Lemniscatic_Wind_Cycling(ElementalSkill):
    name = "Lemniscatic Wind Cycling"
    name_ch = "风轮两立"
    id = 150402
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 3
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
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



class Yaksha_s_Mask(Status):
    name = "Yaksha's Mask"
    name_ch = "夜叉傩面"
    
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.used_this_round = False
        self.usage_this_entity = 2


    def damage_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.is_plunging_attack:
                game.current_damage.main_damage += 2
            if game.current_damage.main_damage_element == ElementType.ANEMO:
                game.current_damage.main_damage += 1

    def update(self, game: 'GeniusGame'):
        self.current_usage = max(self.current_usage, self.usage)
        self.usage_this_entity = self.usage_this_entity

    def infusion(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.ANEMO
    
    def on_calculate(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            if self.from_character.is_active and game.current_dice.use_type == SwitchType.CHANGE_CHARACTER and not self.used_this_round:
                if game.current_dice.cost[0]['cost_num'] > 0:
                    game.current_dice.cost[0]['cost_num'] -= 1
                    return 1
            elif self.from_character.talent and game.current_dice.use_type == SkillType.ELEMENTAL_SKILL:
                if self.usage_this_entity > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return 2
        return False
                
    def on_use(self, game:'GeniusGame'):
        use_tyoe = self.on_calculate(game)
        if use_tyoe == 1:
            self.used_this_round = True
        elif use_tyoe == 2:
            self.usage_this_entity -= 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.used_this_round = False
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.damage_add),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_use),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_use),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin),
        ]

class Bane_of_All_Evil(ElementalBurst):
    name = "Bane of All Evil"
    name_ch = "靖妖傩舞"
    id = 150403
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 4
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
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
        self.generate_summon(game, Yaksha_s_Mask)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Xiao(Character):
    id: int = 1504
    name: str = "Xiao"
    name_ch = "魈"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Whirlwind_Thrust, Lemniscatic_Wind_Cycling, Bane_of_All_Evil]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent