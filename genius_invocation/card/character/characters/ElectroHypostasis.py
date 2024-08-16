from genius_invocation.card.character.import_head import *
# from genius_invocation.card.character.base import Skill


class ElectroCrystalProjection(NormalAttack):
    '''
        雷晶投射
    '''
    id: int = 24011
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Electro Crystal Projection"
    name_ch = "雷晶投射"
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
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class RockPaperScissorsCombo_Paper(ElementalSkill):
    '''
        猜拳三连击·布
    '''
    name = 'Rock-Paper-Scissors Combo: Paper'
    name_ch = '猜拳三连击·布'
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    is_prepared_skill = True

    # cost
    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.from_character.from_player.prepared_skill = None


class PreparePaper(Status):
    '''
        准备技能: 猜拳三连击·布
    '''
    name = 'Prepare for Paper'
    name_ch = '准备技能: 猜拳三连击·布'
    current_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.skill = RockPaperScissorsCombo_Paper(from_character=from_character)

    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)

    def on_destroy(self, game):
        return super().on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]

class RockPaperScissorsCombo_Scissors(ElementalSkill):
    '''
        猜拳三连击·剪刀
    '''
    name = 'Rock-Paper-Scissors Combo: Scissors'
    name_ch = '猜拳三连击·剪刀'
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0
    is_prepared_skill = True
    # cost
    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        prepare_paper = PreparePaper(game=game,
                                     from_player=self.from_character.from_player,
                                     from_character=self.from_character)
        self.from_character.character_zone.add_entity(prepare_paper)
        self.from_character.from_player.prepared_skill = prepare_paper
        # game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class PrepareScissors(Status):
    '''
        准备技能: 猜拳三连击·剪刀
    '''
    name = 'Prepare for Scissors'
    name_ch = '准备技能: 猜拳三连击·剪刀'
    current_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.skill = RockPaperScissorsCombo_Scissors(from_character=from_character)

    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]
    def on_destroy(self, game):
        return super().on_destroy(game)




class RockPaperScissorsCambo(ElementalSkill):
    '''
        猜拳三连击
    '''
    id: int = 24012
    type: SkillType = SkillType.ELEMENTAL_SKILL
    name = 'Rock-Paper-Scissors Combo'
    name_ch = '猜拳三连击'
    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 5,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        prepare_scissors = PrepareScissors(game=game,
                                     from_player=self.from_character.from_player,
                                     from_character=self.from_character)
        self.from_character.character_zone.add_entity(prepare_scissors)
        self.from_character.from_player.prepared_skill = prepare_scissors
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class ChainsOfWardingThunder(Summon):
    '''
        雷锁镇域
    '''
    name = 'Chains of Warding Thunder'
    name_ch = '雷锁镇域'
    element: ElementType = ElementType.ELECTRO
    removable = True
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage
        self.used_this_round = 1

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == 1 - self.from_player.index:
            if self.used_this_round > 0:
                if game.current_dice.use_type == 'change character':
                    game.current_dice.cost[0]['cost_num'] += 1

    def on_change(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.used_this_round -= 1

    def update(self):
        self.current_usage = self.usage

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

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUMMON_ZONE, self.on_change),
            (EventType.CALCULATE_DICE, ZoneType.SUMMON_ZONE, self.on_calculate),
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]



class LightningLockdown(ElementalBurst):
    '''
        元素爆发
        雳霆镇锁
    '''
    id: int = 24013
    type: SkillType = SkillType.ELEMENTAL_BURST
    name = 'Lightning Lockdown'
    name_ch = '雳霆镇锁'
    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
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

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 消耗能量
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        self.generate_summon(game, ChainsOfWardingThunder)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ElectroCrystalCore(Status):
    '''
        雷晶核心
    '''
    name = 'Electro Crystal Core'
    name_ch = '雷晶核心'
    current_usage = 1
    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时
        '''
        if not self.from_character.is_alive or self.from_character.health_point<=0:
            self.from_character.is_alive = True
            self.from_character.health_point = 0
            self.from_character.heal(1, game, heal_type=HealType.REVIVE)
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        ]

class TalentOfElectroHypostasis(CharacterSkill):
    '''
        无向之雷被动技能
    '''
    def on_call(self, game: 'GeniusGame'):
        self.from_character.heal(3, game=game)
        if not self.from_character.character_zone.has_entity(ElectroCrystalCore):
            electro_crystal_core = ElectroCrystalCore(game=game,
                                                    from_player=self.from_character.from_player,
                                                    from_character=self.from_character)
            self.from_character.character_zone.add_entity(electro_crystal_core)


class ElectroHypostasis(Character):
    '''
        无相之雷
    '''
    id: int = 2401
    name: str = 'Electro Hypostasis'
    name_ch = '无相之雷'
    time = 3.7
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 8
    max_health_point: int = 8
    skill_list: List = [ElectroCrystalProjection, RockPaperScissorsCambo, LightningLockdown]

    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        '''
            被动技能: 战斗开始时, 初始附属雷晶核心
        '''
        electro_crystal_core = ElectroCrystalCore(game=game,
                                                  from_player=self.from_player,
                                                  from_character=self)
        self.character_zone.add_entity(electro_crystal_core)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.talent_skill = TalentOfElectroHypostasis(from_character=self)