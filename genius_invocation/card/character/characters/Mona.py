from genius_invocation.card.character.import_head import *

class Ripple_of_Fate(NormalAttack):
# 因果点破
    name = 'Ripple of Fate'
    name_ch = '因果点破'
    id = 120301
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


class Mirror_Reflection_of_Doom(ElementalSkill):
# 水中幻愿
    name = 'Mirror Reflection of Doom'
    name_ch = '水中幻愿'
    id = 120302
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 1
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
        self.generate_summon(game, Reflection)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Stellaris_Phantasm(ElementalBurst):
# 星命定轨
    name = 'Stellaris Phantasm'
    name_ch = '星命定轨'
    id = 120303
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 4
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
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, Illusory_Bubble)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Reflection(Summon):
    '''虚影'''
    name = 'Reflection'
    name_ch = '虚影'
    element = ElementType.HYDRO
    removable = False
    id = 120311

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

            status = self.from_player.team_combat_status.has_status(Shield_from_Refrection)
            if status is not None:
                status.on_destroy(game)
            self.on_destroy(game)

    def update(self, game:'GeniusGame'):
        if self.current_usage == 0:
            self.current_usage = self.usage
            assert self.from_player.team_combat_status.has_status(Shield_from_Refrection) is None
            status = Shield_from_Refrection(game, self.from_player, self.from_character, self)
            self.from_player.team_combat_status.add_entity(status)
        else:
            pass
            #No Need to Update

    def add_usage(self, game: 'GeniusGame', count: int):
        self.current_usage += count
        if self.current_usage == count:
            status = Shield_from_Refrection(game, self.from_player, self.from_character, self)
            self.from_player.team_combat_status.add_entity(status)

        self.from_player.team_combat_status.has_status(Shield_from_Refrection).update()

    def minus_usage(self, game: 'GeniusGame', count: int):
        if self.current_usage == 0: return
        self.current_usage -= count
        self.current_usage = max(0, self.current_usage)
        if self.current_usage == 0:
            self.from_player.team_combat_status.has_status(Shield_from_Refrection).on_destroy(game)

    def on_destroy(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status(Shield_from_Refrection)
        if status is not None:
            status.on_destroy(game)
        super().on_destroy(game)

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = self.usage
        assert self.from_player.team_combat_status.has_status(Shield_from_Refrection) is None
        status = Shield_from_Refrection(game, self.from_player, self.from_character, self)
        self.from_player.team_combat_status.add_entity(status)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.ACTIVE_ZONE, self.on_end_phase),
        ]

class Shield_from_Refrection(Combat_Status):
    name = 'Shield from Refrection'
    name_ch = '虚影之盾'
    id = 120331
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


class Illusory_Bubble(Combat_Status):
    # 泡影
    name = 'Illusory Bubble'
    name_ch = '泡影'
    id = 120332
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.usage = 1

    def on_dealing_damage(self, game: 'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character):
            if game.current_damage.damage_from.from_player == self.from_player:
                game.current_damage.damage_multiply += 1
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DEALING_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_dealing_damage)
        ]

class Mona(Character):
    id = 1203
    name = 'Mona'
    name_ch = '莫娜'

    element = ElementType.HYDRO
    weapon_type = WeaponType.CATALYST
    country: CountryType = CountryType.MONDSTADT

    init_health_point = 10
    max_health_point = 10
    skill_list = [Ripple_of_Fate, Mirror_Reflection_of_Doom, Stellaris_Phantasm]
    max_power = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.last_round = -1
        self.talent_skill = self.skills[2]

    def on_change(self, game:'GeniusGame'):
        # 虚实流动
        if self.last_round != game.round:
            if game.active_player == self.from_player:
                if game.active_player.active_idx == self.index:
                    if game.is_change_player:
                        # active player is Mona
                        game.is_change_player = False
                        self.last_round = game.round

    def on_dmg_after_reation(self, game:'GeniusGame'):
        if self.talent:
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.reaction in [ElementalReactionType.Frozen,
                                                ElementalReactionType.Vaporize,
                                                ElementalReactionType.Bloom,
                                                ElementalReactionType.Electro_Charged] \
                    or game.current_damage.swirl_crystallize_type == ElementType.HYDRO:
                    game.current_damage.main_damage += 2

    def update_listener_list(self):
        super().update_listener_list()
        self.listeners += [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_change),
        ]
        if self.talent:
            self.listeners.append((EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.CHARACTER_ZONE, self.on_dmg_after_reation))

    def listen_talent_events(self, game:'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.CHARACTER_ZONE, self.on_dmg_after_reation)
