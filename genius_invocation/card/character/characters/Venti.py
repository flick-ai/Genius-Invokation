from genius_invocation.card.character.import_head import *


class Divine_Marksmanship(NormalAttack):
    name = "Divine Marksmanship"
    name_ch = "神代射术"
    id = 15031
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


class Stormzone(Combat_Status):
    name = "Stormzone"
    name_ch = "风域"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.is_triggered = False


    def update(self, game: 'GeniusGame'):
        self.current_usage = max(self.current_usage, self.usage)

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            if game.current_dice.use_type == SwitchType.CHANGE_CHARACTER:
                if game.current_dice.cost[0]['cost_num'] > 0:
                    game.current_dice.cost[0]['cost_num'] -= 1
                    return 1
            if self.from_character.talent and self.is_triggered:
                if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return 2
        return False
    
    def on_use(self, game:'GeniusGame'):
        use_type = self.on_calculate(game)
        if use_type == 1:
            self.current_usage -= 1
            self.is_triggered
            if self.current_usage <= 0:
                self.on_destroy(game)
        elif use_type == 2:
            self.is_triggered = False
    
    def on_begin(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.is_triggered = False

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate),
            (EventType.ON_USE_SKILL, ZoneType.ACTIVE_ZONE, self.on_use),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.ACTIVE_ZONE, self.on_use),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin)
        ]
    



class Skyward_Sonnet(ElementalSkill):
    name = "Skyward Sonnet"
    name_ch = "高天之歌"
    id = 15032
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 2
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
        self.add_combat_status(game, Stormzone)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Stormeye(Summon):
    name = "Stormeye"
    name_ch = "暴风之眼"
    removable = True
    element = ElementType.ANEMO

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.infuse_element = ElementType.ANEMO
        self.need_to_switch = False

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_reaction(self, game:'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character) or isinstance(game.current_damage.damage_from, Summon):
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.reaction == ElementalReactionType.Swirl:
                    if self.infuse_element == ElementType.ANEMO:
                        self.infuse_element = game.current_damage.swirl_crystallize_type
    def special_switch(self, game:'GeniusGame'):
        if self.need_to_switch:
            self.need_to_switch = False
            opponent = get_opponent(self.from_player.index)
            opponent.change_to_previous_character(game)

    def end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
           dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.infuse_element,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
           game.add_damage(dmg)
           self.need_to_switch = True
           game.resolve_damage()
           self.current_usage -= 1
           if self.current_usage <= 0:
               self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.SUMMON_ZONE, self.on_reaction),
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.end_phase),
            (EventType.SPECIAL_SWITCH, ZoneType.SUMMON_ZONE, self.special_switch)
        ]
    
    



class Wind_s_Grand_Ode(ElementalBurst):
    name = "Wind's Grand Ode"
    name_ch = "风神之诗"
    id = 15033
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 2
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
        self.generate_summon(game, Stormeye)
        self.resolve_damage(game)
        
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Venti(Character):
    id: int = 1503
    name: str = "Venti"
    name_ch = "温迪"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Divine_Marksmanship, Skyward_Sonnet, Wind_s_Grand_Ode]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent