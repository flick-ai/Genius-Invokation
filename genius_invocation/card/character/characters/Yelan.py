from genius_invocation.card.character.import_head import *


class Stealthy_Bowshot(NormalAttack):
    id: int = 12091
    name = "Stealthy Bowshot"
    name_ch = "潜形隐曜弓"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.HYDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        breakthrough = self.from_character.character_zone.has_entity(Breakthrough)
        if breakthrough.current_usage>=2:
            game.add_damage(Damage.create_damage(game, self.damage_type, ElementType.HYDRO,
                              self.main_damage,
                              self.piercing_damage,
                              self.from_character, get_opponent_active_character(game),
                              self.is_plunging_attack, self.is_charged_attack))
            game.resolve_damage()
            breakthrough.current_usage -= 2
            self.from_player.get_card(1)
        else:
            self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Lingering_Lifeline(ElementalSkill):
    id: int = 12092
    name = "Lingering Lifeline"
    name_ch = "萦络纵命索"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        self.from_character.character_zone.has_entity(Breakthrough).gain(2)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Breakthrough(Status):
    name = "Breakthrough"
    name_ch = "破局"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 0
        self.usage = 3

    def gain(self, num):
        self.current_usage = min(self.current_usage + num, self.usage)

    def update(self):
        '''Should not have update'''
        pass

    def on_begin_phase(self, game:'GeniusGame'):
        if game.active_playe == self.from_player:
            self.gain(1)
                    


class DepthClarion_Dice(ElementalBurst):
    id: int = 12093
    name = "Depth-Clarion Dice"
    name_ch = "渊图玲珑骰"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 3
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, Exquisite_Throw)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Exquisite_Throw(Combat_Status):
    name = "Exquisite Throw"
    name_ch = "adsfasd"

    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.HYDRO,
                    main_damage=2,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                    is_plunging_attack=False,
                    is_charged_attack=False
                )
                game.add_damage(dmg)
                game.resolve_damage()

    def on_begin_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_character.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin_phase),
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]

class Yelan(Character):
    id: int = 1209
    name: str = "Yelan"
    name_ch = "夜兰"
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Stealthy_Bowshot, Lingering_Lifeline, DepthClarion_Dice]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        if self.talent:
            self.listen_talent_events(game)


    def init_state(self, game: 'GeniusGame'):
        assert self.character_zone.has_entity(Breakthrough) is None
        status = Breakthrough(game, self.from_player, self)
        self.character_zone.add_entity(status)
    
    def revive(self, game: 'GeniusGame'):
        super().revive(game)
        self.init_state(game)

    def on_begin(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dice_type = DiceType.OMNI
            self.from_player.fix_dice += [dice_type.value] * len(self.from_player.element_set)
    
    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.BEGIN_ROLL_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
