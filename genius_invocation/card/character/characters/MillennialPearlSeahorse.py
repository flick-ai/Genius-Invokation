from genius_invocation.card.character.import_head import *


class TailSweep(NormalAttack):
    '''
        旋尾扇击
    '''
    id: int = 24031
    type: SkillType = SkillType.NORMAL_ATTACK
    name: str = "Tail Sweep"
    name_ch = "旋尾扇击"

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

class SwirlingSchoolOfFish(ElementalSkill):
    '''
        霰舞鱼群
    '''
    id: int = 24032
    type: SkillType = SkillType.ELEMENTAL_SKILL
    name: str = "Swirling School of Fish"
    name_ch = "霰舞鱼群"

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    is_prepared_skill = False

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: Character) -> None:
        super().__init__(from_character)
        self.add_usage_this_round = 0

    def on_call(self, game: 'GeniusGame'):
        '''
            造成3点雷元素伤害
            如果本角色已附属原海明珠，则使其可用次数+1. (每回合1次)
        '''
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # 如果本角色已附属原海明珠，则使其可用次数+1
        pearl_armor = self.from_character.character_zone.has_entity(PearlArmor)
        if pearl_armor and self.add_usage_this_round < 1:
            pearl_armor.current_usage += 1
            self.add_usage_this_round += 1
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class FontemerHoarthunder(ElementalBurst):
    '''
        元素爆发
        原海古雷
        造成1点雷元素伤害，本角色附属原海明珠，召唤共鸣珊瑚珠
    '''
    id: int = 24033
    type: SkillType = SkillType.ELEMENTAL_BURST
    name: str = "Fontemer Hoarthunder"
    name_ch = "原海古雷"
    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
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
        # 消耗能量
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        # 本角色附属原海明珠
        self.add_status(game, PearlArmor)
        # 召唤共鸣珊瑚珠
        self.generate_summon(game, ResonantCoralOrb)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class PearlArmor(Status):
    name = "Pearl Armor"
    name_ch = "原海明珠"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None, equip_talent=False):
        super().__init__(game, from_player, from_character)
        self.max_usage = 10000
        self.usage = 2
        self.summon_used_this_round = 0
        if equip_talent:
            self.current_usage = 1
        else:
            self.current_usage = self.usage

    def update(self):
        self.summon_used_this_round = 0
        self.current_usage = self.usage

    def on_execute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element != ElementType.PIERCING:
                if game.current_damage.main_damage > 0:
                    game.current_damage.main_damage -= 1
                    if game.current_damage.damage_type == SkillType.SUMMON:
                        self.summon_used_this_round += 1
                        if self.from_character.talent:
                            # 装备有此牌的千年珍珠骏麟所附属的原海明珠抵消召唤物伤害时，改为每回合2次不消耗可用次数
                            if self.summon_used_this_round > 2:
                                self.current_usage -= 1
                        else:
                            # 每回合1次，抵消来自召唤物的伤害时不消耗可用次数
                            if self.summon_used_this_round > 1:
                                self.current_usage -= 1
                    else:
                        self.current_usage -= 1
                    if self.current_usage <= 0:
                        self.on_destroy(game)

    def after_action(self, game: 'GeniusGame'):

        if game.active_player == self.from_player:
            if game.active_player.is_pass:
                if get_my_active_character(game) == self.from_character:
                    self.from_player.get_card(1)

    def on_begin(self, game: 'GeniusGame'):
        self.summon_used_this_round = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg),
            (EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.after_action)
        ]

class ResonantCoralOrb(Summon):
    '''
        共鸣珊瑚珠
    '''
    name: str = "Resonant Coral Orb"
    name_ch = "共鸣珊瑚珠"
    element: ElementType = ElementType.ELECTRO
    removable: bool = True

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成1点雷元素伤害
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
            self.on_destroy(game)

    def update(self):
        self.current_usage = max(self.usage, self.current_usage)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]



class MillennialPearlSeahorse(Character):
    '''
        千年珍珠骏麟
    '''
    id: int = 2403
    name: str = 'Millennial Pearl Seahorse'
    name_ch = '千年珍珠骏麟'
    time = 4.4
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 8
    max_health_point: int = 8
    skill_list: List = [TailSweep, SwirlingSchoolOfFish, FontemerHoarthunder]

    max_power: int = 2



    def init_state(self, game: 'GeniusGame'):
        '''
            被动技能: 战斗开始时，本角色附属原海明珠。
        '''
        pearl_armor = PearlArmor(game=game,
                                    from_player=self.from_player,
                                    from_character=self)
        self.character_zone.add_entity(pearl_armor)

    def on_begin(self, game: 'GeniusGame'):
        # 重载on_begin函数
        super().on_begin(game)
        self.skill_list[1].add_usage_this_round = 0

    def equip_talent(self, game:'GeniusGame', is_action=True, talent_card=None):
        # 重载装备天赋函数
        self.talent = True
        self.character_zone.talent_card = talent_card
        pearl_armor = self.character_zone.has_entity(PearlArmor)
        if pearl_armor:
            pearl_armor.usage += 1
        else:
            pearl_armor = PearlArmor(game=game,
                                    from_player=self.from_player,
                                    from_character=self,
                                    equip_talent=True)
            self.character_zone.add_entity(pearl_armor)