from genius_invocation.card.character.import_head import *
# from genius_invocation.card.character.base import Skill
from .LaSignora import Sheer_Cold

class Icespike_Shot(NormalAttack):
    '''
        冰锥迸射
    '''
    id: int = 210301
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Icespike Shot"
    name_ch = "冰锥迸射"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
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


class IceRingWaltz(ElementalSkill):
    '''
        圆舞冰环
    '''
    name = 'Ice Ring Waltz'
    name_ch = '圆舞冰环'
    id = 210302
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 3
    piercing_damage: int = 0
    is_prepared_skill = True

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        self.add_status(game, OverwhelmingIce)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class OverwhelmingIce(Status):
    name = "Overwhelming Ice"
    name_ch = "四迸冰锥"
    id = 210321
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1

    def update(self):
        self.current_usage = max(self.usage, self.current_usage)

    def dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                game.current_damage.piercing_damage += 1
                self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.dmg_add)
        ]

class PiercingIceridge(Summon):
    '''
        刺击冰棱
    '''
    name = 'Piercing Iceridge'
    name_ch = '刺击冰棱'
    element: ElementType = ElementType.CRYO
    removable = True
    id = 210311
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.usage, self.current_usage)

    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成1点冰元素伤害
            结束阶段分先后手两次调用on_end_phase, 所以需要判断
        '''
        if game.active_player == self.from_player:
            active_idx = self.from_player.active_idx
            oppenent_player = get_opponent(game)
            target = oppenent_player.character_list[active_idx]
            while not target.is_alive:
                active_idx = (active_idx + 1) %3
                target = oppenent_player.character_list[active_idx]


            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=target,
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
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]



class PlungingIceShards(ElementalBurst):
    '''
        元素爆发
        冰棱轰坠
    '''
    id: int = 210303
    type: SkillType = SkillType.ELEMENTAL_BURST
    name = 'PlungingIceShards'
    name_ch = '冰棱轰坠'
    # damage
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
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 消耗能量
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        self.generate_summon(game, PiercingIceridge)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class CryoCrystalCore(Status):
    '''
        冰晶核心
    '''
    name = 'Cryo Crystal Core'
    name_ch = '冰晶核心'
    current_usage = 1
    id = 210322
    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时
        '''
        if not self.from_character.is_alive or self.from_character.health_point<=0:
            self.from_character.is_alive = True
            self.from_character.health_point = 0
            self.from_character.heal(1, game)

            if self.talent:
                opponent_player = game.players[1-self.from_player.index]
                opponent = get_active_character(game, 1-self.from_player.index)
                state = opponent.character_zone.has_entity(Sheer_Cold)
                if state != None:
                    state.update()
                else:
                    opponent.character_zone.add_entity(Sheer_Cold(game, from_player=opponent_player, from_character=opponent))

            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        ]

class CryoHypostasis(Character):
    '''
        无相之冰
    '''
    id: int = 2103
    name: str = 'Cryo Hypostasis'
    name_ch = '无相之冰'
    time = 4.4
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 8
    max_health_point: int = 8
    skill_list: List = [Icespike_Shot, IceRingWaltz, PlungingIceShards]

    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        '''
            被动技能: 战斗开始时, 初始附属冰晶核心
        '''
        cryo_crystal_core = CryoCrystalCore(game=game,
                                                  from_player=self.from_player,
                                                  from_character=self)
        self.character_zone.add_entity(cryo_crystal_core)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent

    def equip_talent(self, game:'GeniusGame', is_action=True, talent_card=None):
        self.talent = True
        # self.character_zone.talent_card = talent_card
        if self.character_zone.has_entity(CryoCrystalCore) is None:
            cryo_crystal_core = CryoCrystalCore(game=game,
                                                  from_player=self.from_player,
                                                  from_character=self)
            self.character_zone.add_entity(cryo_crystal_core)
        game.is_change_player = is_action

