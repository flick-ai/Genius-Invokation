from genius_invocation.card.character.characters.import_head import *


class RangedStance(Status):
    '''
        远程状态
    '''
    name = "Ranged Stance"
    name_ch= "远程状态"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def show(self):
        return str(MAX_ROUND)

class MeleeStance(Status):
    '''
        近战状态
    '''
    name = "Melee Stance"
    name_ch = "近战状态"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.opponent = None
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def infuse(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.HYDRO

    def find_next_alive_character(self, current_character: 'Character'):
        '''
            找到下一个活着的角色
        '''
        current_idx = current_character.index
        while True:
            current_idx = (current_idx + 1) % current_character.from_player.character_num
            if current_idx == current_character.index:
                break
            if current_character.from_player.character_list[current_idx].is_alive:
                return current_character.from_player.character_list[current_idx]
        return None


    def on_use_skill(self, game: 'GeniusGame'):
        '''
            用于在使用技能后，判断角色是否有断流
            目前on_use_skill仅用于达达利亚
        '''
        active_index = game.active_player.active_idx
        if self.from_character == game.active_player.character_list[active_index]:
            opponent = get_opponent_active_character(game)
            if opponent.character_zone.has_entity(Riptide) is not None:
                '''
                    当前攻击的角色具有断流
                '''
                self.opponent = opponent


    def on_after_use_skill(self, game: 'GeniusGame'):
        '''
            近战状态的达达利亚对已附属有断流的角色使用技能后:
            对下一个敌方后台角色造成1点穿透伤害
        '''
        if self.opponent:
            next_character = self.find_next_alive_character(self.opponent)
            if next_character:
                game.add_damage(Damage.create_damage(game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.PIERCING,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self.from_character,
                    damage_to=next_character,
                    is_plunging_attack=False,
                    is_charged_attack=False))
                game.resolve_damage()
            self.opponent = None



    def on_begin_phase(self, game: 'GeniusGame'):
        '''
            开始阶段, 可用次数减1
        '''
        if game.active_player == self.from_character.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)
                self.from_character.is_melee_stance = False
                # 切换成远程模式
                ranged_stance = RangedStance(game=game,
                                            from_player=self.from_player,
                                            from_character=self.from_character)
                self.from_character.character_zone.add_entity(ranged_stance)


    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_use_skill),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_use_skill),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infuse)
        ]


class Riptide(Status):
    '''
        断流
        实现逻辑:
        当角色死亡时, 会调用on_distroy, 这时候先建一个新的断流
    '''
    name = 'Riptide'
    name_ch = "断流"
    current_usage = MAX_ROUND
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.CHARACTER_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]


    def on_damage_add(self, game: 'GeniusGame'):
        '''
            近战状态下的达达利亚对附属有断流的角色造成的伤害+1
        '''
        if game.players[0] == self.from_player:
            tartaglia_player = game.players[1]
        else:
            tartaglia_player = game.players[0]
        tartaglia = get_character_with_name(tartaglia_player, Tartaglia)
        if game.current_damage.damage_from == tartaglia and tartaglia.is_melee_stance:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def find_next_alive_character(self, current_character: 'Character'):
        '''
            找到下一个活着的角色
        '''
        current_idx = current_character.index
        while True:
            current_idx = (current_idx + 1) % current_character.from_player.character_num
            if current_idx == current_character.index:
                break
            if current_character.from_player.character_list[current_idx].is_alive:
                return current_character.from_player.character_list[current_idx]
        return None

    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时，先结算未结算的事件
        '''
        if not self.from_character.is_alive:
            next_character = self.find_next_alive_character(self.from_character)
            if next_character:
                new_riptide = Riptide(game=game,
                                    from_player=self.from_player,
                                    from_character=next_character)
                next_character.character_zone.add_entity(new_riptide)
            self.on_destroy(game)

    def on_end_phase(self, game: 'GeniusGame'):
        if not self.from_character.is_active: return
        if game.players[0] == self.from_player:
            tartaglia_player = game.players[1]
        else:
            tartaglia_player = game.players[0]
        if game.active_player == tartaglia_player:
            tartaglia = get_character_with_name(tartaglia_player, Tartaglia)
            if tartaglia.talent and tartaglia.is_alive:
                game.add_damage(Damage.create_damage(game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.PIERCING,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=None,
                    damage_to=get_opponent_active_character(game),
                    is_plunging_attack=False,
                    is_charged_attack=False))
                game.resolve_damage()


class CuttingTorrent(NormalAttack):
    '''
        普通攻击
        断雨
    '''
    id: int = 0
    name = 'Cutting Torrent'
    name_ch = "断雨"
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
            'cost_type': CostType.HYDRO
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
        # 处理伤害
        # 记录一下target
        target = get_opponent_active_character(game)
        self.resolve_damage(game)

        # 如果达达利亚的攻击为重击：对目标角色附属断流
        if self.is_charged_attack:

            if target.is_alive:
                status = target.character_zone.has_entity(Riptide)
                if not status:
                    riptide = Riptide(game=game,
                                    from_player=target.from_player,
                                    from_character=target)
                    target.character_zone.add_entity(riptide)

        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class FoulLegacy_RagingTide(ElementalSkill):
    '''
        元素战技
        魔王武装：狂澜
    '''
    id: int = 1
    name='Foul Legacy: Raging Tide'
    name_ch = "魔王武装：狂澜"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def add_status(self, game: 'GeniusGame'):
        status = self.from_character.character_zone.has_entity(MeleeStance)
        if status is not None:
            status.update()
        else:
            melee_stance = MeleeStance(game=game,
                                 from_player=self.from_character.from_player,
                                 from_character=self.from_character)
            self.from_character.character_zone.add_entity(melee_stance)
            status = self.from_character.character_zone.has_entity(RangedStance)
            status.on_destroy(game)
            self.from_character.is_melee_stance = True

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        # 切换为近战状态,在主伤害打出前
        self.add_status(game)
        # 记录一下target
        target = get_opponent_active_character(game)
        # 处理伤害
        self.resolve_damage(game)
        # 使目标角色附属断流
        if target.is_alive:
            status = target.character_zone.has_entity(Riptide)
            if not status:
                riptide = Riptide(game=game,
                                  from_player=target.from_player,
                                  from_character=target)
                target.character_zone.add_entity(riptide)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class FlashOfHavoc(ElementalBurst):
    '''
        达达利亚
        远程状态元素爆发
    '''
    id: int = 3
    name = 'Flash of Havoc'
    name_ch = "远程状态·魔弹一闪"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 5
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost: int = 3
    energy_gain: int = 2

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 消耗能量
        self.consume_energy(game)

        # 记录一下target
        target = get_opponent_active_character(game)
        # 处理伤害
        self.resolve_damage(game)
        # 返还2点能量
        self.gain_energy(game)

        # target附属断流
        if target.is_alive:
            status = target.character_zone.has_entity(Riptide)
            if not status:
                riptide = Riptide(game=game,
                                  from_player=target.from_player,
                                  from_character=target)
                target.character_zone.add_entity(riptide)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class LightOfHavoc(ElementalBurst):
    '''
        达达利亚
        近战状态元素爆发
    '''
    id: int = 4
    name = 'Light of Havoc'
    name_ch = "近战状态·尽灭水光"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 7
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 消耗能量
        self.consume_energy(game)

        # 处理伤害
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Havoc_Obliteration(ElementalBurst):
    '''
    '''
    id: int = 2
    name = 'Havoc: Obliteration'
    name_ch = "极恶技·尽灭闪"
    type: SkillType = SkillType.ELEMENTAL_BURST
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    def __init__(self, from_character: 'Character') -> None:
        self.from_character = from_character
        self.flash_of_havoc = FlashOfHavoc(from_character)
        self.light_of_havoc = LightOfHavoc(from_character)

    def on_call(self, game: 'GeniusGame'):
        if self.from_character.is_melee_stance:
            self.light_of_havoc.on_call(game)
        else:
            self.flash_of_havoc.on_call(game)


class Tartaglia(Character):
    '''
        达达利亚
    '''
    id: int = 1204
    name: str = 'Tartaglia'
    name_ch = "达达利亚"
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [CuttingTorrent, FoulLegacy_RagingTide, Havoc_Obliteration]

    max_power: int = 3

    def init_state(self, game: 'GeniusGame'):
        '''
            被动技能：战斗开始时, 附属远程状态
        '''
        range_stance = RangedStance(game=game,
                                    from_player=self.from_player,
                                    from_character=self)
        self.character_zone.add_entity(range_stance)

    def __init__(self, game: 'GeniusGame', zone:'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power= 0

        self.is_melee_stance = False # 是否为近战状态

    def revive(self, game: 'GeniusGame'):
        super().revive(game)
        self.init_state(game)
        self.is_melee_stance = False