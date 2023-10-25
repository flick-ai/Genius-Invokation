from genius_invocation.card.character.import_head import *

class Liutian_Archery(NormalAttack):
    name = 'Liutian Archery'
    name_ch = "流天射术"
    id: int = 0
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


class Trail_of_the_Qilin(ElementalSkill):
    id = 1
    name = 'Trail of the Qilin'
    name_ch = "山泽麟迹"
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
        # 处理伤害
        self.resolve_damage(game)
        self.add_combat_status(game, Ice_Lotus)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Frostflake_Arrow(NormalAttack):
    name = 'Frostflake Arrow'
    name_ch = "霜华矢"
    id: int = 2
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 2

    # cost
    cost = [
        {
            'cost_num': 5,
            'cost_type': CostType.CRYO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.from_character.usage_frostflake_arrow += 1
        # 处理伤害
        if self.from_character.talent and self.from_character.usage_frostflake_arrow>=2:
            self.resolve_damage(game, add_piercing_damage=1)
        else:
            self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Celestial_Shower(ElementalBurst):
    id = 3
    name = 'Celestial Shower'
    name_ch = "降众天华"
    type = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 1

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        }
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Sacred_Cryo_Pearl)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Ice_Lotus(Combat_Status):
    name = 'Ice Lotus'
    name_ch = "冰莲"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def on_execute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to.from_player == self.from_player:
            if game.current_damage.main_damage_element == ElementType.PIERCING:
                return
            if game.current_damage.damage_to.is_active:
                if game.current_damage.main_damage >0:
                    game.current_damage.main_damage -= 1
                    self.current_usage -=1
                    if self.current_usage <=0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_execute_dmg),
        ]

class Sacred_Cryo_Pearl(Summon):
    name = "Sacred Cryo Pearl"
    name_ch = "冰灵珠"
    element = ElementType.CRYO
    usage = 2
    max_usage = 2
    removable = True

    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成1点冰元素伤害, 1点穿透伤害
            结束阶段分先后手两次调用on_end_phase, 所以需要判断
        '''
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=1,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if(self.current_usage <= 0):
            '''
                Entity在被移除时, 调用on_destroy移除监听并执行对应的移除操作(在对应区域中移除此entity等)
            '''
            self.on_destroy(game)

    def update(self):
        self.current_usage = max(self.usage, self.current_usage)

    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)


class Ganyu(Character):
    id = 1101
    name = "Ganyu"
    name_ch = "甘雨"
    element = ElementType.CRYO
    weapon_type = WeaponType.BOW
    country = CountryType.LIYUE

    init_health_point = 10
    max_health_point = 10
    skill_list = [Liutian_Archery, Trail_of_the_Qilin, Frostflake_Arrow, Celestial_Shower]
    
    max_power = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.usage_frostflake_arrow = 0
        self.talent_skill = self.skills[2]
