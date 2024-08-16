from genius_invocation.card.character.import_head import *


class Favonius_Bladework_Edel(NormalAttack):
    name = 'Favonius Bladework-Edel'
    name_ch = "西风剑术·宗室"
    id: int = 110601
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
        summon = self.from_character.from_player.summon_zone.has_entity(Lightfall_Sword)
        if summon is None:
            self.gain_energy(game)
        else:
            summon.add_usage(game, 2)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Icetide_Veortex(ElementalSkill):
    id = 110602
    name = "Icetide Vortex"
    name_ch = "冰潮的涡旋"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
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
        status =  self.from_character.character_zone.has_entity(Grimheart)
        if status is None:
            self.resolve_damage(game)
            self.add_status(game, Grimheart)
        else:
            status.on_destroy(game)
            self.resolve_damage(game, add_main_damage=3)
        # 获得能量
        summon = self.from_character.from_player.summon_zone.has_entity(Lightfall_Sword)
        if summon is None:
            self.gain_energy(game)
        else:
            if self.from_character.talent:
                summon.add_usage(game, 3)
            else:
                summon.add_usage(game, 2)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Glacial_Illumination(ElementalBurst):
    id = 110603
    name = 'Glacial Illumination'
    name_ch = "凝浪之光剑"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
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
        self.generate_summon(game, Lightfall_Sword)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Grimheart(Status):
    name = "Grimheart"
    name_ch = "冷酷之心"
    id = 110621
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    

class Lightfall_Sword(Summon):
    name = "Lightfall Sword"
    name_ch = "光降之剑"
    element = ElementType.PHYSICAL
    removable = False
    id = 110611

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 0
        self.usage = 0
    
    def update(self):
        pass # NO UPDATE

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=3 + self.current_usage,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

class Eula(Character):
    id: int = 1106
    name: str = "Eula"
    name_ch = "优菈"
    time = 3.5
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Favonius_Bladework_Edel, Icetide_Veortex, Glacial_Illumination]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.8] = "调整了「七圣召唤」中，角色牌「优菈」元素战技伤害，元素爆发伤害：元素战技的冷酷之心，”使本次伤害+2“效果调整为”使本次伤害+3“；元素爆发的光降之剑，”结束阶段：弃置此牌，造成2点物理伤害“调整为”结束阶段：弃置此牌，造成3点物理伤害“"
        return log