from genius_invocation.card.character.import_head import *

class Flame_of_Salvation(NormalAttack):
    name = "Flame of Salvation"
    name_ch = "振救之焰"
    id = 23021
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


class Searing_Precept(ElementalSkill):
    name = "Searing Precept"
    name_ch = "炽烈箴言"
    id = 23022
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

class Ominous_Star(ElementalBurst):
    name = "Ominous Star"
    name_ch = "天陨预兆"
    id = 23023
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':4, 'cost_type':CostType.PYRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Darkfire_Furnace)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Darkfire_Furnace(Summon):
    name = "Darkfire Furnace"
    name_ch = "渊火熔炉"
    removable = True
    element  = ElementType.PYRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.usage = 2
    def end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=1,
                damage_from=self,
                damage_to = get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.end_phase)
        ]

class Fiery_Rebirth(Status):
    name = "Fiery Rebirth"
    name_ch = "火之新生"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.set_talent = False
    
    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时
        '''
        if not self.from_character.is_alive:
            self.from_character.is_alive = True
            self.from_character.health_point = 3
            #TODO: check whether this operation is belongs to heal?
            if self.set_talent:
                shield = Aegis_of_Abyssal_Flame(game, self.from_player, self.from_character)
                self.from_character.character_zone.add_entity(shield)
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        ]
    
class Aegis_of_Abyssal_Flame(Shield):
    name = "Aegis of Abyssal Flame"
    name_ch = "渊火加护"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 3
        self.usage = 3
    def dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            assert game.current_damage.main_damage_element == ElementType.PYRO
            game.current_damage.main_damage += 1
    def update_listener_list(self):
        super().update_listener_list()
        self.listeners.append((EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.dmg_add))

class AbyssLectorFathomlessFlames(Character):
    id: int = 2302
    name: str = "Abyss Lector: Fathomless Flames"
    name_ch = "深渊咏者·渊火"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 6
    max_health_point: int = 6
    skill_list: List = [Flame_of_Salvation, Searing_Precept, Ominous_Star]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        rebirth = Fiery_Rebirth(game, self.from_player, self)
        self.character_zone.add_entity(rebirth)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        if self.talent:
            self.character_zone.has_entity(Fiery_Rebirth).set_talent = True
    
    def equip_talent(self, game: 'GeniusGame', is_action=True):
        rebirth = self.character_zone.has_entity(Fiery_Rebirth)
        if rebirth is not None:
            rebirth.set_talent = True
        else:
            shield = self.character_zone.has_entity(Aegis_of_Abyssal_Flame)
            if shield is not None:
                shield.update()
            else:
                shield = Aegis_of_Abyssal_Flame(game, self.from_player, self)
                self.character_zone.add_entity(shield)

        game.is_change_player = is_action


