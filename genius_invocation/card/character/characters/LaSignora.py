from genius_invocation.card.character.import_head import *

class Frostblade_Hailstorm(NormalAttack):
    id: int = 21021
    name = "Frostblade Hailstorm"
    name_ch = "霜锋霰舞"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.CRYO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Biting_Shards(ElementalSkill):
    id: int = 21022
    name = "Biting Shards"
    name_ch = "凛冽之刺"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.CRYO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        opponent = get_opponent_active_character(game)
        state = opponent.character_zone.has_entity(Sheer_Cold)
        if state != None:
            state.update()
        else:
            opponent.character_zone.add_entity(Sheer_Cold(game, from_player=get_opponent(game), from_character=opponent))
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Sheer_Cold(Status):
    name = "Sheer Cold"
    name_ch = "严寒"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1

    def update(self):
        self.current_usage = self.usage

    def on_end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                SkillType.OTHER,
                ElementType.CRYO,
                1,
                0,
                self,
                self.from_character
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]

class Blazing_Heat(Status):
    name = "Blazing Heat"
    name_ch = "炽热"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        status = self.from_character.character_zone.has_entity(Sheer_Cold)
        if status is not None:
            status.on_destroy(game)
        self.usage = 1
        self.current_usage = 1

    def update(self):
        self.current_usage = self.usage

    def on_end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                SkillType.OTHER,
                ElementType.PYRO,
                1,
                0,
                self,
                self.from_character
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]

class Carmine_Chrysalis(ElementalBurst):
    id: int = 21023
    name = "Carmine Chrysalis"
    name_ch = "红莲冰茧"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 4
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.CRYO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.from_character.heal(2, game)
        status = self.from_character.character_zone.has_entity(IceSealed_Crimson_Witch_of_Embers)
        assert status is not None
        status.on_destroy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        

class LaSignora(Character):
    id: int = 2102
    name: str = "La Signora"
    name_ch = "「女士」"
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Frostblade_Hailstorm, Biting_Shards, Carmine_Chrysalis]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        rebirth = IceSealed_Crimson_Witch_of_Embers(game, self.from_player, self)
        self.character_zone.add_entity(rebirth)

    def equip_talent(self, game: 'GeniusGame', is_action=False):
        self.from_player.dice_zone.add([DiceType.CRYO.value]*3)
        if not self.talent:
            self.listen_talent_events(game)
            self.talent = True
        self.talent_round = -1
        game.is_change_player = False


    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_round = -1
        if self.talent:
            self.listen_talent_events(game)
        

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg)
    
    def on_execute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self:
            if game.current_damage.main_damage >= 3 and self.talent_round!=game.round:
                self.talent_round = game.round
                game.current_damage.main_damage -= 1
                opponent_player = game.players[1-self.from_player.index]
                opponent = get_active_character(game, 1-self.from_player.index)
                state = opponent.character_zone.has_entity(Sheer_Cold)
                if state != None:
                    state.update()
                else:
                    opponent.character_zone.add_entity(Sheer_Cold(game, from_player=opponent_player, from_character=opponent))

    

    def change_to_Crimson_Witch_of_Ember(self, game:'GeniusGame'):
        # Create new character, move everything in the character Zone into the new character.

        # TODO: Check which part of states are maintained the same through this process.
        new_char = Crimson_Witch_of_Embers(
            game = game,
            zone = self.character_zone,
            from_player = self.from_player,
            index = self.index,
            from_character = None,
            talent = self.talent,
            power = self.power,
            health_point=self.health_point,
            is_active = self.is_active,
            is_alive = self.is_alive,
            is_frozen = self.is_frozen,
            is_satisfy = self.is_satisfy,
            elemental_application = self.elemental_application)

        for status in self.character_zone.status_list:
            status.from_character = new_char
        
        self.from_player.character_list[self.index] = new_char
        self.from_player.update_element_list()

        # Only remove the events.
        for action in self.registered_events:
            action.remove()         

class IceSealed_Crimson_Witch_of_Embers(Status):
    name = "Ice-Sealed Crimson Witch of Embers"
    name_ch = "冰封的炽炎魔女"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
    
    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时
        '''
        if not self.from_character.is_alive:
            self.from_character.is_alive = True
            self.from_character.health_point = 0
            self.from_character.heal(1, game)
            #TODO: check whether this operation is belongs to heal?
            self.on_destroy(game)
    
    def on_begin_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            if self.from_character.health_point <=4:
                self.on_destroy(game)
    
    def on_destroy(self, game:'GeniusGame'):
        super().on_destroy(game)
        self.from_character.change_to_Crimson_Witch_of_Ember(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase)
        ]



class Crimson_Lotus_Moth(NormalAttack):
    id: int = 21024
    name = "Crimson Lotus Moth"
    name_ch = "红莲之蛾"
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

class Decimating_Lash(ElementalSkill):
    id: int = 21025
    name = "Decimating Lash"
    name_ch = "烬灭之鞭"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        opponent = get_opponent_active_character(game)
        state = opponent.character_zone.has_entity(Blazing_Heat)
        if state != None:
            state.update()
        else:
            opponent.character_zone.add_entity(Blazing_Heat(game, from_player=get_opponent(game), from_character=opponent))
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Whirling_Blaze(ElementalBurst):
    id: int = 21026
    name = "Whirling Blaze"
    name_ch = "燃焰旋织"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 6
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Crimson_Witch_of_Embers(Character):
    id: int = 2102 # MAYBE WRONG
    name = "Crimson Witch of Embers"
    name_ch = "「焚尽的炽炎魔女」"

    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Crimson_Lotus_Moth, Decimating_Lash, Whirling_Blaze]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False, power= 0, health_point = 10, is_active=False, is_alive= True, is_frozen = False, is_satisfy = False, elemental_application = []):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = power
        self.talent = talent
        self.health_point = health_point
        self.is_active = is_active
        self.is_alive = is_alive
        self.is_frozen = is_frozen
        self.is_satisfy = is_satisfy
        self.elemental_application = elemental_application
        if self.talent:
            self.listen_talent_events(game)


    def equip_talent(self, game: 'GeniusGame', is_action=False):
        self.from_player.dice_zone.add([DiceType.PYRO.value]*3)
        if not self.talent:
            self.listen_talent_events(game)
            self.talent = True
        self.talent_round = -1
        game.is_change_player = False
    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg)
    
    def on_execute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self:
            if game.current_damage.main_damage >= 3 and self.talent_round!=game.round:
                self.talent_round = game.round
                game.current_damage.main_damage -= 1
                opponent_player = game.players[1-self.from_player.index]
                opponent = get_active_character(game, 1-self.from_player.index)
                state = opponent.character_zone.has_entity(Blazing_Heat)
                if state != None:
                    state.update()
                else:
                    opponent.character_zone.add_entity(Blazing_Heat(game, from_player=opponent_player, from_character=opponent))

    