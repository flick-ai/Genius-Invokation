from genius_invocation.card.character.import_head import *


class Guhua_Style(NormalAttack):
    id: int = 120201
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Guhua Style"
    name_ch = "古华剑法"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
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


class Fatal_Rainscreen(ElementalSkill):
    '''
    行秋
    元素战技
    '''
    id: int = 120202
    name = "Stellar Restoration"
    name_ch = "画雨笼山"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        #附着水元素
        self.from_character.elemental_attach(game, ElementType.HYDRO)
        # 获得能量
        self.gain_energy(game)
        self.add_combat_status(game, Rain_Sword)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Raincutter(ElementalBurst):
    '''
    行秋
    元素爆发
    '''
    id: int = 120203
    name = "Fatal Rainscreen"
    name_ch = "裁雨留虹"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.from_character.elemental_attach(game, ElementType.HYDRO)
        self.add_combat_status(game, Rainbow_Bladework)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Rain_Sword(Combat_Status):
    name = "Rain Sword"
    name_ch = "雨帘剑"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        if self.from_character.talent:
            self.usage = 3
        self.current_usage = self.usage

        self.current_usage = self.usage
    def update(self):
        if self.from_character.talent:
            self.usage = 3
        self.current_usage = max(self.current_usage, self.usage)

    def on_execute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_to.from_player == self.from_player:
            if game.current_damage.damage_to.is_active:
                if game.current_damage.main_damage_element != ElementType.PIERCING:
                    if game.current_damage.main_damage >= 3:
                        game.current_damage.main_damage -= 1
                        self.current_usage -= 1
                        if self.current_usage <=0:
                            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_execute_dmg)
        ]

class Rainbow_Bladework(Combat_Status):
    name = "Rainbow Bladework"
    name = "虹剑势"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = self.usage

    def after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                dmg = Damage.create_damage(
                    game=game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.HYDRO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()

                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]

class Xingqiu(Character):
    id = 1202
    name = 'Xingqiu'
    name_ch = "行秋"
    element = ElementType.HYDRO
    weapon_type = WeaponType.SWORD
    country = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Guhua_Style, Fatal_Rainscreen, Raincutter]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]