from genius_invocation.card.character.import_head import *

class SearingGlare(NormalAttack):
    name = "Searing Glare"
    name_ch = "烧蚀之光"
    id = 23031
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.PYRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class BlazingStrike(ElementalSkill):
    name = "Blazing Strike"
    name_ch = "炎晶迸击"
    id = 23032
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Spirit_of_Omens_Awakening_Pyro_Scorpion(ElementalBurst):
    name = "Spirit of Omen's Awakening: Pyro Scorpion"
    name_ch = "厄灵苏醒·炎之魔蝎"
    id = 23033
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game,  Spirit_of_Omen_Pyro_Scorpion)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Spirit_of_Omen_Pyro_Scorpion(Summon):
    name = " Spirit of Omen: Pyro Scorpion"
    name_ch = "厄灵·炎之魔蝎"
    removable = True
    element  = ElementType.PYRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.usage = 2
        status = self.from_character.character_zone.has_entity(Pyro_Scorpion_Guardian_Stance)
        if status is None:
            status = Pyro_Scorpion_Guardian_Stance(game, self.from_player, self.from_character, self)
            self.from_character.character_zone.add_entity(status)
        else:
            status.update()

    def end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            add_dmg = 0
            if self.from_character.talent and self.from_character.skills[0].usage_this_round + self.from_character.skills[1].usage_this_round >0:
                add_dmg = 1
            dmg = Damage.create_damage(
                game,
                SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage= 1 + add_dmg,
                piercing_damage=0,
                damage_from=self,
                damage_to = get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def begin_round(self, game: 'GeniusGame'):
        status = self.from_character.character_zone.has_entity(Pyro_Scorpion_Guardian_Stance)
        if status is None:
            status = Pyro_Scorpion_Guardian_Stance(game, self.from_player, self.from_character, self)
            self.from_character.character_zone.add_entity(status)
        else:
            status.update()


    def update(self, game:'GeniusGame'):
        self.current_usage = max(self.current_usage, self.usage)
        status = self.from_character.character_zone.has_entity(Pyro_Scorpion_Guardian_Stance)
        if status is None:
            status = Pyro_Scorpion_Guardian_Stance(game, self.from_player, self.from_character, self)
            self.from_character.character_zone.add_entity(status)
        else:
            status.update()

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.end_phase),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUMMON_ZONE, self.begin_round)
        ]

    def on_destroy(self, game: 'GeniusGame'):
        status = self.from_character.character_zone.has_entity(Pyro_Scorpion_Guardian_Stance)
        if status is not None:
            status.on_destroy(game)
        super().on_destroy(game)
    


class Pyro_Scorpion_Guardian_Stance(Status):
    name = 'Pyro Scorpion: Guardian Stance'
    nane_ch = '炎之魔蝎·守势'

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, from_summon:'Summon' = None):
        super().__init__(game, from_player, from_character)
        # USAGE SHOULD ALWAYS 1
        self.from_summon = from_summon

        if self.from_character.talent:
            self.current_usage = 2
            self.usage = 2
        else:
            self.current_usage = 1
            self.usage = 1

    def on_execute_dmg(self, game:"GeniusGame"):
        if game.current_damage.damage_to != self.from_character: return
        if game.current_damage.main_damage <= 0: return
        if game.current_damage.main_damage_element == ElementType.PIERCING: return
        game.current_damage.main_damage -= 1
        self.current_usage -= 1
        if self.current_usage <=0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg)
        ]
    def update(self):
        if self.from_character.talent:
            self.current_usage = 2
            self.usage = 2
        else:
            self.current_usage = 1
            self.usage = 1

class Spirit_of_Omens_Power(Status):
    name = "Spirit of Omen's Power"
    name_ch = "厄灵之能"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        # USAGE SHOULD ALWAYS 1
        self.current_usage = 1
        self.usage = 1
    
    def on_final_dmg(self, game:'GeniusGame'):
        if self.from_character.health_point<=7:
            self.from_character.get_power(1)
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.on_final_dmg)
        ]

class EremiteScorchingLoremaster(Character):
    id: int = 2303
    name: str = "Eremite Scorching Loremaster"
    name_ch = "镀金旅团·炽沙叙事人"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.EREMITES
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [SearingGlare, BlazingStrike, Spirit_of_Omens_Awakening_Pyro_Scorpion]

    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        status = Spirit_of_Omens_Power(game, self.from_player, self)
        self.character_zone.add_entity(status)


    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]
    
    
