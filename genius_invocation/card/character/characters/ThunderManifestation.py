from genius_invocation.card.character.import_head import *

class ThunderousWingslash(NormalAttack):
    id: int = 24021
    name = "Thunderous Wingslash"
    name_ch = "轰霆翼斩"
    type: SkillType = SkillType.NORMAL_ATTACK

    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage = 0

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
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class LightningStrikeProbe(Combat_Status):
    name = "Lightning Strike Probe"
    name_ch = "雷霆探知"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', thunder: 'Character'): 
        # from_character here is None
        super().__init__(game, from_player, from_character)
        self.triggered = False
        self.thunder = thunder # The Thunder Manifestation who generate this Probe
        self.lightningrod = None

    def show(self):
        if self.triggered:
            return "-x-"
        else:
            return "^v^"
    
    def on_begin_action(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.triggered = False
    
    def after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player and not self.triggered:
            if self.lightningrod is not None:
                self.lightningrod.on_destroy(game)
            
            lightningrod = Lightning_Rod(game, self.from_player, game.current_skill.from_character, self.thunder)
            self.lightningrod = lightningrod
            self.thunder.target = game.current_skill.from_character

            self.triggered = True

    
class Lightning_Rod(Status):
    name = "Lightning Rod"
    name_ch = "雷鸣探知"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', thunder: 'Character'):
        super().__init__(game, from_player, from_character)
        self.thunder = thunder # The Thunder Manifestation who generate this Probe
    def on_destroy(self, game: 'GeniusGame'):
        self.thunder.target = None
        super().on_destroy(game)

    def dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_to == self.from_character and \
              (game.current_damage.damage_from == self.thunder or game.current_damage.damage_from.from_character == self.thunder):
            game.current_damage.main_damage += 1
            if self.thunder.talent and self.thunder.round != game.round:
                self.thunder.from_player.get_card(1)
                self.thunder.round = game.round
            self.on_destroy(game)
    
    def on_execute_dmg(self, game:'GeniusGame'):
        if self.thunder.talent and self.thunder.round != game.round:
            if game.current_damage.damage_to == self.from_character or \
                (game.current_damage.piercing_damage > 0 and game.current_damage.damage_to.from_player == self.from_player):
                self.thunder.from_player.get_card(1)
                self.thunder.round = game.round
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.dmg_add),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg)
        ]

class StrifefulLightning(ElementalSkill):
    id: int = 24022
    name = "Strifeful Lightning"
    name_ch = "雷墙倾轧"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0
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
        if self.from_character.target is not None:
            game.add_damage(Damage.create_damage(game, self.damage_type, self.main_damage_element,
                              self.main_damage,
                              self.piercing_damage,
                              self.from_character, self.from_character.target,
                            ))
            game.resolve_damage()
        else:
            self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Thundering_Shackles(Summon):
    name: str = "Thundering Shackles"
    name_ch: str = "轰雷禁锢"
    main_damage: int = 3
    element: ElementType = ElementType.ELECTRO
    removable: bool = True
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = self.usage
    
    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            if self.from_character.target is not None:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.SUMMON,
                    main_damage_element=self.element,
                    main_damage=self.main_damage,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=self.from_character.target,
                )
            else:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.SUMMON,
                    main_damage_element=self.element,
                    main_damage=self.main_damage,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1

        if (self.current_usage <= 0):
            self.on_destroy(game)

    def update(self):
        self.current_usage = max(self.usage, self.current_usage)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]


class ThunderingShackles(ElementalBurst):
    id: int = 24023
    name = "Thundering Shackles"
    name_ch = "轰雷禁锢"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
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
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Thundering_Shackles)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class ThunderManifestation(Character):
    id: int = 2402
    name: str = "Thunder Manifestation"
    name_ch = "雷音权现"
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [
        ThunderousWingslash, # Normal Attack
        StrifefulLightning, # Elemental Skill
        ThunderingShackles, # Elemental Burst
    ]
    max_power: int = 2
    talent_on: int = 0

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.target = None
        self.round = -1
        self.listen_event(game, EventType.BEFORE_ANY_ACTION, self.before_action)
        self.talent_skill = self.skills[1]

    def before_action(self, game:'GeniusGame'):
        target_player = game.players[1-self.from_player.index]
        status = LightningStrikeProbe(game, target_player, None, self)
        target_player.team_combat_status.add_entity(status)

        for action in self.registered_events:
            if action.action == self.before_action:
                action.remove()
    
    
    
