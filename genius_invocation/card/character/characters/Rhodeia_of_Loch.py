from genius_invocation.card.character.import_head import *


class Squirrel(Summon):
    '''
        花鼠
    '''
    id: int = 0
    name: str = 'Squirrel'
    name_ch = "花鼠"
    element: ElementType = ElementType.HYDRO
    removable = True

    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成2点水元素伤害
            结束阶段分先后手两次调用on_end_phase, 所以需要判断
        '''
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=2,
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

    def update(self, game: 'GeniusGame'):
        #TODO: Check if the usage maybe decrease by update.
        self.current_usage = max(self.current_usage,self.usage)

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


class Raptor(Summon):
    '''
        飞鸢
    '''
    id: int = 1
    name: str = 'Raptor'
    name_ch = "飞鸢"
    element: ElementType = ElementType.HYDRO
    removable = True
    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成1点水元素伤害
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

    def update(self, game: 'GeniusGame'):
        #TODO: Check if the usage maybe decrease by update.
        self.current_usage = max(self.current_usage,self.usage)

    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int = 3
        self.current_usage: int = 3


class Frog(Summon):
    '''
        蛙
    '''
    id: int = 2
    name: str = 'Frog'
    name_ch = "蛙"
    element: ElementType = ElementType.HYDRO
    removable = False
    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成2点水元素伤害
            结束阶段分先后手两次调用on_end_phase, 所以需要判断
        '''
        if game.active_player == self.from_player and self.current_usage==0:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.on_destroy(game)


    def update(self, game: 'GeniusGame'):
        #TODO: Check if the usage maybe decrease by update.
        #TODO: Check when usage=0, refresh the frog, where the shield in combat_status will lie in. The same place or the tail of list?
        if self.current_usage == 0:
            self.current_usage = self.usage
            status = Shield_from_Frog(game,self.from_player,self.from_character,self)
            self.from_player.team_combat_status.add_entity(status)
        else:
            self.current_usage = max(self.current_usage,self.usage)
            self.from_player.team_combat_status.has_status(Shield_from_Frog).update()

    def add_usage(self, game: 'GeniusGame', count: int):
        self.current_usage += count
        if self.current_usage==count:
            status = Shield_from_Frog(game,self.from_player,self.from_character,self)
            self.from_player.team_combat_status.add_entity(status)

        self.from_player.team_combat_status.has_status(Shield_from_Frog).update()

    def minus_usage(self, game: 'GeniusGame', count: int):
        if self.current_usage == 0: return
        self.current_usage -= count
        self.current_usage = max(0, self.current_usage)
        if self.current_usage == 0:
            self.from_player.team_combat_status.has_status(Shield_from_Frog).on_destroy(game)

    def on_destroy(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status(Shield_from_Frog)
        if status is not None:
            status.on_destroy(game)
        super().on_destroy(game)

    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int = 2
        self.current_usage = 2
        status = Shield_from_Frog(game,self.from_player,self.from_character,self)
        self.from_player.team_combat_status.add_entity(status)



class Surge(NormalAttack):
    '''
        至尊翻涌！
    '''
    id = 22011
    name = "Surge"
    name_ch = "翻涌"
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 1
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

Summon_list = [Squirrel,Raptor,Frog]

def choose_one_summon(Skill: ElementalSkill, game: 'GeniusGame'):
    un_summon_list = []
    for summon in Summon_list:
        if Skill.from_character.from_player.summon_zone.has_entity(summon) is None:
            un_summon_list.append(summon)
    if len(un_summon_list) == 0:
        x = Summon_list[game.random.randint(0,2)]
        Skill.from_character.from_player.summon_zone.has_entity(x).update(game)
    else:
        x = un_summon_list[game.random.randint(0,len(un_summon_list))]
        summon = x(game,Skill.from_character.from_player,Skill.from_character)
        Skill.from_character.from_player.summon_zone.add_entity(summon)

class Oceanid_Mimic_Summoning(ElementalSkill):
    '''
        小e
    '''
    id = 22012
    name = "Oceanid Mimic Summoning"
    name_ch = "纯水幻造"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 0
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

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        choose_one_summon(self, game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class The_Myriad_Wilds(ElementalSkill):
    '''
        大e
    '''
    id = 22013
    name = "The Myriad Wilds"
    name_ch = "林野百态"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 0
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 5,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        for _ in range(2):
            choose_one_summon(self, game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Tide_and_Torrent(ElementalBurst):
    id = 22014
    name = "Tide and Torrent"
    name_ch = "潮涌与激流"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]

    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        main_dmg = self.main_damage + self.from_character.from_player.summon_zone.num()*2
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.ELEMENTAL_BURST,
            main_damage_element=self.main_damage_element,
            main_damage=main_dmg,
            piercing_damage=self.piercing_damage,
            damage_from=self.from_character,
            damage_to=get_opponent_active_character(game),
        )
        game.add_damage(dmg)
        game.resolve_damage()

        if self.from_character.talent:
            for summon in self.from_character.from_player.summon_zone.space:
                summon.add_usage(game, 1)

        self.consume_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
class Rhodeia_of_Loch(Character):
    id = 2201
    name = "Rhodeia of Loch"
    name_ch = "纯水精灵·洛蒂娅"
    element = ElementType.HYDRO
    weapon_type = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER

    init_health_point = 1
    max_health_point = 10
    skill_list = [Surge,Oceanid_Mimic_Summoning,The_Myriad_Wilds,Tide_and_Torrent]
    max_power = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[3]


class Shield_from_Frog(Combat_Status):
    name="Shield from Frog"
    name_ch = "蛙之盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, from_summon:'Summon' = None):
        super().__init__(game, from_player, from_character)
        # USAGE SHOULD ALWAYS SAME WITH SUMMON
        self.from_summon = from_summon
        self.current_usage = self.from_summon.current_usage
        self.usage = self.from_summon.usage

    def on_damage_execute(self, game:'GeniusGame'):
        if self.from_summon.current_usage <=0: return
        if game.current_damage.main_damage <=0: return
        if game.current_damage.main_damage_element==ElementType.PIERCING: return
        if game.current_damage.damage_to.from_player == self.from_player:
            if game.current_damage.damage_to.is_active:
                game.current_damage.main_damage -= 1
                self.from_summon.current_usage -= 1
                self.current_usage = self.from_summon.current_usage
                if self.from_summon.current_usage ==0:
                    self.on_destroy(game) # Only destroy the combat_status here

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_damage_execute)
        ]
    def update(self):
        self.current_usage = self.from_summon.current_usage
