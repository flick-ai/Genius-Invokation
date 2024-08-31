from genius_invocation.card.character.import_head import *

class WeavingBlade(NormalAttack):
    name = "Weaving Blade"
    name_ch = "心织刀流"
    id = 160901
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.GEO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class FlutteringHasode(ElementalSkill):
    name = "Fluttering Hasode"
    name_ch = "羽袖一触"
    id = 160902
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        num = 4 if self.from_character.talent else 3
        self.from_character.from_player.select_list = random.sample([Doll1, Doll2, Doll3, Doll4, Doll5, Doll6], num)
        self.from_character.from_player.select_num = 1

        self.now_phase = game.game_phase
        game.game_phase = GamePhase.SELECT
        game.special_phase = self

    def on_finished(self, game: 'GeniusGame'):
        game.game_phase = self.now_phase
        game.special_phase = None
        select_list = game.active_player.select_list
        game.active_player.select_list = None
        game.active_player.select_num = 0
        result = game.active_player.select_result
        game.active_player.select_result = None

        self.generate_summon(game, select_list[result[0]])
        if self.from_character.talent:
            self.generate_summon(game, Doll3)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        game.current_skill = None
        game.resolve_action(None)

class HiyokuTwinBlades(ElementalBurst):
    name = "Hiyoku: Twin Blades"
    name_ch = "二刀之形·比翼"
    id = 160903
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 5
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ChiorisAutomatonDolls(Summon):
    name: str = "Chiori's Automaton Dolls"
    name_ch = "千织的自动制御人形"
    element: ElementType = ElementType.GEO
    removable = True
    id = 160910
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int = 2
        self.current_usage: int = 2

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.GEO,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class Doll1(ChiorisAutomatonDolls):
    name: str = "Doll 1"
    name_ch = "不悦挥刀之袖"
    id = 160911
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.listen_event(game, EventType.INFUSION, ZoneType.SUMMON_ZONE, self.on_infusion)

    def on_infusion(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.GEO

class Doll2(ChiorisAutomatonDolls):
    name: str = "Doll 2"
    name_ch = "无事发生之袖"
    id = 160912
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.round_usage = 1
        self.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.SUMMON_ZONE, self.after_use_skill)

    def after_use_skill(self, game: 'GeniusGame'):
        if self.round_usage <= 0:
            return
        if game.active_player == self.from_player:
            self.from_player.change_to_next_character()
            self.round_usage -= 1

class Doll3(ChiorisAutomatonDolls):
    name: str = "Doll 3"
    name_ch = "平静养神之袖"
    id = 160913
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

class Doll4(ChiorisAutomatonDolls):
    name: str = "Doll 4"
    name_ch = "轻松迎敌之袖"
    id = 160914
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.round_usage = 1
        self.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.SUMMON_ZONE, self.after_use_skill)

    def after_use_skill(self, game: 'GeniusGame'):
        if self.round_usage <= 0:
            return
        if game.active_player == self.from_player:
            if game.current_skill.from_character != self.from_character:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.SUMMON,
                    main_damage_element=ElementType.GEO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()
                self.round_usage -= 1

class Doll5(ChiorisAutomatonDolls):
    name: str = "Doll 5"
    name_ch = "闭目战斗之袖"
    id = 160915
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.round_usage = 2
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.SUMMON_ZONE, self.on_add_damage)

    def on_add_damage(self, game: 'GeniusGame'):
        if self.round_usage <= 0:
            return
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.GEO:
                game.current_damage.main_damage += 1
                self.round_usage -= 1
        if isinstance(game.current_damage.damage_from, ChiorisAutomatonDolls):
            if game.current_damage.main_damage_element == ElementType.GEO:
                game.current_damage.main_damage += 1
                self.round_usage -= 1

class Doll6(ChiorisAutomatonDolls):
    name: str = "Doll 6"
    name_ch = "侧目睥睨之袖"
    id = 160916
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.round_usage = 1
        self.listen_event(game, EventType.CALCULATE_DICE, ZoneType.SUMMON_ZONE, self.on_calculate_dice)
        self.listen_event(game, EventType.ON_USE_SKILL, ZoneType.SUMMON_ZONE, self.on_use_skill)

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.current_dice.from_character == self.from_character:
            if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                if game.current_dice.cost[0]['cost_num'] > 0:
                    game.current_dice.cost[0]['cost_num'] -= 1
                    return True
                elif game.current_dice.cost[1]['cost_num'] > 0:
                    game.current_dice.cost[1]['cost_num'] -= 1
                    return True
        return False

    def on_use_skill(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.round_usage -= 1

class Chiori(Character):
    id: int = 1609
    name: str = "Chiori"
    name_ch = "千织"
    time = 5.1
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [WeavingBlade, FlutteringHasode, HiyokuTwinBlades]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]

