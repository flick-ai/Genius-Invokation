from genius_invocation.card.character.import_head import *



class Rapid_Ritesword(NormalAttack):
    id = 15081
    name = "Rapid Ritesword"
    name_ch = "迅捷礼刺剑"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ANEMO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.resolve_damage(game)
        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Enigmatic_Feint(ElementalSkill):
    id = 15082
    name = "Enigmatic Feint"
    name_ch = "谜影障身法"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 3
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        if self.usage_this_round == 2 and self.from_character.talent:
            self.resolve_damage(game, add_main_damage=2)
            self.from_character.need_to_switch = True
        else:
            self.resolve_damage(game)

        if self.usage_this_round == 1:
            if self.from_character.health_point <=8:
                self.from_character.heal(2, game)
                self.add_status(game, Overawing_Assault)

        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Overawing_Assault(Status):
    name = "Overawing Assault"
    name_ch = "攻袭余威"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    
    def end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            if self.from_character.health_point >= 6:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage=2,
                    main_damage_element=ElementType.PIERCING,
                    piercing_damage=0,
                    damage_from=self.from_character,
                    damage_to=self.from_character,
                )
                game.add_damage(dmg)
                game.resolve_damage()
            self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.end_phase)
        ]

class Bogglecat_Box(Summon):
    name = "Bogglecat Box"
    name_ch = "惊奇猫猫盒"
    removable = True
    element = ElementType.ANEMO

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.infuse_element = ElementType.ANEMO

    def begin_round(self, game: 'GeniusGame'):
        if self.from_player.team_combat_status.has_status(Shield_from_Booglecat_Box) is None:
            status = Shield_from_Booglecat_Box(game, self.from_player, self.from_character, self)
            self.from_player.team_combat_status.add_entity(status)

    def update(self, game:'GeniusGame'):
        self.current_usage = max(self.current_usage, self.usage)
        if self.from_player.team_combat_status.has_status(Shield_from_Booglecat_Box) is None:
            status = Shield_from_Booglecat_Box(game, self.from_player, self.from_character, self)
            self.from_player.team_combat_status.add_entity(status)

    def on_excuete_dmg(self, game:'GeniusGame'):
        if self.infuse_element == ElementType.ANEMO:
            if game.current_damage.damage_to.from_player == self.from_player \
                and game.current_damage.main_damage_element in [ElementType.CRYO, ElementType.HYDRO, ElementType.PYRO, ElementType.ELECTRO]:
                self.infuse_element = game.current_damage.main_damage_element
                

    def end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage=1,
                main_damage_element=self.infuse_element,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_destroy(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status(Shield_from_Booglecat_Box)
        if status is not None:
            status.on_destroy(game)

        super().on_destroy(game)
    

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.SUMMON_ZONE, self.on_excuete_dmg),
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.end_phase),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUMMON_ZONE, self.begin_round)
        ]

class Shield_from_Booglecat_Box(Combat_Status):
    name = 'Shield from Booglecat Box'
    name_ch = '猫猫盒之盾'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, from_summon:'Summon' = None):
        super().__init__(game, from_player, from_character)
        # USAGE SHOULD ALWAYS SAME WITH SUMMON
        self.from_summon = from_summon
        self.current_usage = self.from_summon.current_usage
        self.usage = self.from_summon.usage

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, from_summon:'Summon' = None):
        super().__init__(game, from_player, from_character)
        # USAGE SHOULD ALWAYS 1
        self.from_summon = from_summon
        self.current_usage = 1
        self.usage = 1

    def on_execute_dmg(self, game:"GeniusGame"):
        if self.from_character.is_active: return
        if game.current_damage.damage_to != self.from_player: return
        if game.current_damage.main_damage <= 0: return
        if game.current_damage.main_damage_element == ElementType.PIERCING: return
        game.current_damage.main_damage -= 1
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_execute_dmg)
        ]
    def update(self):
        self.current_usage = 1

class Magic_Trick_Astonishing_Shift(ElementalBurst):
    id = 15083
    name = "Magic Trick: Astonishing Shift"
    name_ch = "魔术·运变惊奇"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
        }
    ]

    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Bogglecat_Box)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Lynette(Character):
    id: int = 1508
    name: str = "Lynette"
    name_ch = "琳妮特"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.FONTAINE
    country_list: List[CountryType] = [CountryType.FONTAINE, CountryType.FATUI]
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Rapid_Ritesword, Enigmatic_Feint, Magic_Trick_Astonishing_Shift]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        self.need_to_switch = False
        if self.talent:
            self.listen_talent_events(game)

    def special_switch(self, game: 'GeniusGame'):
        if self.need_to_switch:
            self.need_to_switch = False
            opponent = get_opponent(game) # During special_switch, the active player is always me.
            opponent.change_to_previous_character()

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.SPECIAL_SWITCH, ZoneType.CHARACTER_ZONE, self.special_switch)
