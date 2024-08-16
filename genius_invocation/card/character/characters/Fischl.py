from genius_invocation.card.character.import_head import *


class Oz(Summon):
    '''奥兹'''
    id: int = 140111
    name: str = 'Oz'
    name_ch = "奥兹"
    element: ElementType = ElementType.ELECTRO
    removable: bool = True

    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成1点雷元素伤害
            结束阶段分先后手两次调用on_end_phase, 所以需要判断
        '''
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
        self.usage = 2
        self.current_usage = 2

class BoltsOfDownfall(NormalAttack):
    '''
        菲谢尔
        普通攻击
        罪灭之矢
    '''
    id: int = 140101
    name = "Bolts of Downfall"
    name_ch = "罪灭之矢"
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
            'cost_type': CostType.ELECTRO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        if self.from_character.talent:
            oz = self.from_character.from_player.summon_zone.has_entity(Oz)
            if oz is not None:
                oz.current_usage -= 1
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.SUMMON,
                    main_damage_element=oz.element,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=oz,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()
                if oz.current_usage <= 0:
                    oz.on_destroy(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Nightrider(ElementalSkill):
    '''
        菲谢尔
        元素战技
        夜巡影翼
    '''
    id: int = 140102
    name = "Nightrider"
    name_ch = "夜巡影翼"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
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
    energy_cost: int = 0
    energy_gain: int = 1


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.generate_summon(game, Oz)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class MidnightPhantasmagoria(ElementalBurst):
    '''
        菲谢尔
        元素爆发
        至夜幻现
    '''
    id: int = 140103
    type: SkillType = SkillType.ELEMENTAL_BURST
    name = "Midnight Phantasmagoria"
    name_ch = "至夜幻现"
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 4
    piercing_damage: int = 2

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Fischl(Character):
    '''菲谢尔'''
    id: int = 1401
    name: str = 'Fischl'
    name_ch = "菲谢尔"
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [BoltsOfDownfall, Nightrider, MidnightPhantasmagoria]

    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
