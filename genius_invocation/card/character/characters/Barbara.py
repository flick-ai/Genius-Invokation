from genius_invocation.card.character.import_head import *

class WhisperofWater(NormalAttack):
    id: int = 12011
    name = "Whisper of Water"
    name_ch = "水之浅唱"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.HYDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class LettheShowBegin(ElementalSkill):
    id: int = 12012
    name = "Let the Show Begin♪"
    name_ch = "演唱，开始♪"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.generate_summon(game, MelodyLoop)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class MelodyLoop(Summon):
    name: str = 'Melody Loop'
    name_ch = "歌声之环"
    element: ElementType = ElementType.HYDRO
    removable = True
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int = 2
        self.current_usage: int = 2
        self.talent_max_usage = 1
        self.talent_usage = 0
        self.talent_round = -1

    def update(self, game: 'GeniusGame'):
        self.current_usage = max(self.current_usage,self.usage)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            character = get_my_active_character(game)
            character.elemental_attach(game, ElementType.HYDRO)
            for char in self.from_player.character_list:
                if char.is_alive:
                    char.heal(heal=1, game=game)
            self.current_usage -= 1
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]
        if self.from_character.talent:
            self.listeners.append((EventType.CALCULATE_DICE, ZoneType.SUMMON_ZONE, self.on_calculate_dice))
            self.listeners.append((EventType.ON_CHANGE_CHARACTER, ZoneType.SUMMON_ZONE, self.on_switch))

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.round != self.talent_round:
            self.talent_round = game.round
            self.talent_usage = self.talent_max_usage
        if game.active_player == self.from_player:
            if game.current_dice.use_type == SwitchType.CHANGE_CHARACTER:
                if self.from_character.is_alive:
                    if game.current_dice.cost[0]['cost_num']>0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
        return False

    def on_switch(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.talent_usage -= 1

class ShiningMiracle(ElementalBurst):
    id: int = 12013
    name = "Shining Miracle♪"
    name_ch = "闪耀奇迹♪"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        for character in self.from_character.from_player.character_list:
            if character.is_alive:
                character.heal(heal=4, game=game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Barbara(Character):
    id: int = 1201
    name: str = "Barbara"
    name_ch = "芭芭拉"
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [WhisperofWater, LettheShowBegin, ShiningMiracle]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]

    def listen_talent_events(self, game: 'GeniusGame'):
        status = self.from_player.summon_zone.has_entity(MelodyLoop)
        if status != None:
            status.listen_event(game, EventType.CALCULATE_DICE, ZoneType.SUMMON_ZONE, status.on_calculate_dice)
            status.listen_event(game, EventType.ON_CHANGE_CHARACTER, ZoneType.SUMMON_ZONE, status.on_switch)

