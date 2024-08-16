from genius_invocation.card.character.import_head import *

class Sward_of_the_Radiant_Path(NormalAttack):
    id: int = 110901
    name = "Sward of the Radiant Path"
    name_ch = "熠辉轨度剑"
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
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
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Nights_of_Formal_Focus(ElementalSkill):
    '''
        垂裳端凝之夜
        元素战技
    '''
    id: int = 110902
    name="Nights of Formal Focus"
    name_ch = "垂裳端凝之夜"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 不造成伤害

        # 召唤物/状态生成
        self.add_combat_status(game, Shooting_Star)
        self.add_combat_shield(game, Curtain_of_Slumber)
        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Curtain_of_Slumber(Combat_Shield):
    name = "Curtain of Slumber Shield"
    name_ch = "安眠帷幕护盾"
    id = 110951
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)


class Shooting_Star(Combat_Status):
    name = "Shooting Stars"
    name_ch = "飞星"
    id = 110931
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 4
        self.current_usage = 0

    def gain_night_star(self, num):
        self.current_usage += num
        if self.current_usage>=self.usage:
            dmg = Damage.create_damage(
                self.game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.CRYO,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(self.game),
            )
            self.game.add_damage(dmg)
            self.game.resolve_damage()
            self.current_usage -= self.usage
            if self.from_character.talent:
                self.from_player.get_card(1)


    def update(self):
        self.gain_night_star(2)


    def after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            self.gain_night_star(1)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]

class Dream_of_the_StarStream_Shaker(ElementalBurst):
    '''
        星流摇床之梦
        元素爆发
    '''
    id: int = 110903
    name = " Dream of the Star-Stream Shaker"
    name_ch = "星流摇床之梦"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        # 召唤物/状态生成
        self.generate_summon(game, Celestial_Dreamsphere)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Celestial_Dreamsphere(Summon):
    name = "Celestial Dreamsphere"
    name_ch = "饰梦天球"
    id:int = 110911
    element: ElementType = ElementType.ELECTRO
    removable: bool = True

    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = max(self.usage, self.current_usage)

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

            shooting_star = self.from_player.team_combat_status.has_status(Shooting_Star)
            if shooting_star is not None:
                shooting_star.gain_night_star(1)

            if self.current_usage <= 0:
                self.on_destroy(game)


    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]

class Layla(Character):
    '''莱依拉'''
    id: int = 1109
    name: str = 'Layla'
    name_ch = "莱依拉"
    time = 4.3
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.SUMERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Sward_of_the_Radiant_Path, Nights_of_Formal_Focus, Dream_of_the_StarStream_Shaker]

    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]


