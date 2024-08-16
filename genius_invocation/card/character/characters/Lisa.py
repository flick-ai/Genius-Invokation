from genius_invocation.card.character.import_head import *

class Conductive(Status):
    name: str = "Conductive"
    name_ch: str = "引雷"
    id = 140921
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        '''
        from_player: the player this status is attached to
        from_character: the character this status is attached to
        '''
        super().__init__(game, from_player, from_character)
        self.max_usage = 4
        self.current_usage = 2

    @staticmethod
    def check_status(game: 'GeniusGame', from_character: 'Character'=None):
        if from_character is None:
            from_character = get_opponent_active_character(game)
        return from_character.character_zone.has_entity(Conductive)


    @staticmethod
    def add_status(game: 'GeniusGame', from_character: 'Character'=None, status: 'Status'=None):
        if status is not None:
            status.update()
            return

        # if status is not provided
        status = Conductive.check_status(game, from_character)
        if from_character is None:
            from_character = get_opponent_active_character(game)
        if status is None:
            status = Conductive(game, get_opponent(game), from_character)
            from_character.character_zone.add_entity(status)
        else:
            status.update()

    def update(self):
        self.current_usage = min(self.current_usage+1, self.max_usage)

    def on_add_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_to != self.from_character:
            return
        if isinstance(game.current_skill,Violet_Arc):
            game.current_damage.main_damage += self.current_usage
            self.on_destroy(game)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            self.update()
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]


class Lightning_Touch(NormalAttack):
    id: int = 140901
    name = "Lightning Touch"
    name_ch = "指尖风暴"
    type: SkillType = SkillType.NORMAL_ATTACK

    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage = 0

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
        self.resolve_damage(game)
        if self.is_charged_attack:
            Conductive.add_status(game)

        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Violet_Arc(ElementalSkill):
    id: int = 140902
    name = "Violet Arc"
    name_ch = "苍雷"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        status = Conductive.check_status(game)
        self.resolve_damage(game)
        if status is None:
            Conductive.add_status(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Lightning_Rose_Summon(Summon):
    name: str = "Lightning Rose"
    name_ch: str = "蔷薇雷光"
    main_damage: int = 2
    id = 140911
    element: ElementType = ElementType.ELECTRO
    removable: bool = True
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=self.main_damage,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1

        if (self.current_usage <= 0):
            self.on_destroy(game)

    def update(self):
        self.current_usage = max(self.usage, self.current_usage)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]


class Lightning_Rose(ElementalBurst):
    id: int = 140903
    name = "Lightning Rose"
    name_ch = "蔷薇的雷光"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        status = Conductive.check_status(game)
        self.resolve_damage(game)
        if status is None:
            Conductive.add_status(game)
        self.generate_summon(game, Lightning_Rose_Summon)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Lisa(Character):
    id: int = 1409
    name: str = "Lisa"
    name_ch = "丽莎"
    time = 4.0
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [
        Lightning_Touch, # Normal Attack
        Violet_Arc, # Elemental Skill
        Lightning_Rose, # Elemental Burst
    ]
    max_power: int = 2
    talent_on: int = 0

    def on_switched_to(self):
        super().on_switched_to()
        if self.talent:
            if self.talent_on:
                self.talent_on -= 1
                Conductive.add_status(self.from_player.game)

    def on_begin(self, game: 'GeniusGame'):
        super().on_begin(game)
        if self.talent:
            self.talent_on = 1

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_on = 1

    def balance_adjustment():
        log = {}
        log[4.8] = "调整了角色牌「丽莎」元素爆发的效果：增加了效果“使敌方出战角色附属引雷”"
        return log