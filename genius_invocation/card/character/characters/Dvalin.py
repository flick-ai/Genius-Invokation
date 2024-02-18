from genius_invocation.card.character.import_head import *

class LaceratingSlash(NormalAttack):
    id: int = 25021
    name = "Lacerating Slash"
    name_ch = "裂爪横击"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.ANEMO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class TempestuousBarrage(ElementalSkill):
    id: int = 25022
    name = "Tempestuous Barrage"
    name_ch = "暴风轰击"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ANEMO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        opponent = get_opponent_active_character(game)
        state = opponent.character_zone.has_entity(TotalCollapse)
        if state != None:
            state.update()
        else:
            opponent.character_zone.add_entity(TotalCollapse(game, from_player=get_opponent(game), from_character=opponent, dvalin=self.from_character))
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class TotalCollapse(Status):
    name = "Total Collapse"
    name_ch = "坍毁"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, dvalin: Dvalin = None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
        self.dvalin = dvalin
    
    def update(self):
        self.current_usage = self.usage

    def on_add_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element in [ElementType.PHYSICAL, ElementType.ANEMO]:
                game.current_damage.main_damage += 2
                self.on_destroy(game)
    
    def on_destroy(self, game: 'GeniusGame'):
        super().on_destroy(game)
        if self.dvalin.talent:
            if self.dvalin.talent_round != game.round:
                self.dvalin.talent_round = game.round
                targets = get_standby_character(game, self.from_player.index)
                if len(targets):
                    opponent = targets[0]
                    opponent = get_opponent_active_character(game)
                    state = opponent.character_zone.has_entity(TotalCollapse)
                    if state != None:
                        state.update()
                    else:
                        opponent.character_zone.add_entity(TotalCollapse(game, from_player=get_opponent(game), from_character=opponent, dvalin=self.from_character))
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_dmg)
        ]


class DvalinsCleansing(ElementalSkill):
    id: int = 25023
    name = "Dvalin's Cleansing"
    name_ch = "风龙涤流"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':5, 'cost_type':CostType.ANEMO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        
        prepare_Perpetual_Cleansing = Prepare_PerpetualCleansing(game, self.from_character, self.from_character)
        self.from_character.character_zone.add_entity(prepare_Perpetual_Cleansing)
        self.from_character.from_player.prepared_skill = prepare_Perpetual_Cleansing
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class PerpetualCleansing(ElementalSkill):
    id = 250231
    name = 'Perpetual Cleansing'
    name_ch = '长延涤流'
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
    piercing_damage: int = 0
    is_prepared_skill = True
    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        targets = get_opponent_standby_character(game)
        if len(targets):
            target = targets[0]
            game.add_damage(Damage.create_damage(game, self.damage_type, self.main_damage_element, 
                                                 self.main_damage,
                                                 self.piercing_damage,
                                                 self.from_character,
                                                 target))
            game.resolve_damage()
        else:   
            self.resolve_damage(game)
        prepare_Ultimate_Cleansing = Prepare_UltimateCleansing(game=game,
                                     from_player=self.from_character.from_player,
                                     from_character=self.from_character)
        self.from_character.character_zone.add_entity(prepare_Ultimate_Cleansing)
        self.from_character.from_player.prepared_skill = prepare_Ultimate_Cleansing


class Prepare_PerpetualCleansing(Status):
    name = "Prepare for Perpetual Cleansing"
    name_ch = "准备技能: 长延涤流"
    current_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.skill = PerpetualCleansing(from_character=from_character)

    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]
    def on_destroy(self, game):
        return super().on_destroy(game)

class UltimateCleansing(ElementalSkill):
    id = 250232
    name = "Ultimate Cleansing"
    name_ch = "终幕涤流"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 2
    piercing_damage: int = 0
    is_prepared_skill = True
    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        targets = get_opponent_standby_character(game)
        if len(targets):
            target = targets[-1]
            game.add_damage(Damage.create_damage(game, self.damage_type, self.main_damage_element, 
                                                 self.main_damage,
                                                 self.piercing_damage,
                                                 self.from_character,
                                                 target))
            game.resolve_damage()
        else:   
            self.resolve_damage(game)
        self.from_character.from_player.prepared_skill = None

class Prepare_UltimateCleansing(Status):
    name = "Prepare for Ultimate Cleansing"
    name_ch = '准备技能：终幕涤流'
    current_usage = 1

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.skill = UltimateCleansing(from_character=from_character)

    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]
    def on_destroy(self, game):
        return super().on_destroy(game)


class CaelestinumFinaleTermini(ElementalBurst):
    id: int = 25024
    name = "Caelestinum Finale Termini"
    name_ch = "终天闭幕曲"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 5
    piercing_damage: int = 0
    cost = [{'cost_num':4, 'cost_type':CostType.ANEMO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        targets = get_opponent_standby_character(game)
        for opponent in targets:
            state = opponent.character_zone.has_entity(TotalCollapse)
            if state != None:
                state.update()
            else:
                opponent.character_zone.add_entity(TotalCollapse(game, from_player=get_opponent(game), from_character=opponent, dvalin=self.from_character))
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Dvalin(Character):
    id: int = 2502
    name: str = "Maguu Kenki"
    name_ch = "魔偶剑鬼"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [LaceratingSlash, TempestuousBarrage, DvalinsCleansing, CaelestinumFinaleTermini]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        self.talent_round = -1
