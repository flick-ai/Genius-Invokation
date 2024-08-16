from genius_invocation.card.character.import_head import *

class Weiss(NormalAttack):
    id: int = 160401
    name = "Favonius Bladework - Weiss"
    name_ch = "西风剑术·白"
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


class Abiogenesis(ElementalSkill):
    id: int = 160402
    name = "Abiogenesis: Solar Isotoma"
    name_ch = "创生法·拟造阳华"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.generate_summon(game, SolarIsotoma)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SolarIsotoma(Summon):
    name: str = 'Solar Isotoma'
    name_ch = "阳华"
    id = 160411
    element: ElementType = ElementType.GEO
    removable = True
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'):
        super().__init__(game, from_player, from_character)
        self.usage: int = 3
        self.current_usage: int = 3
        self.round = -1

    def update(self):
        self.current_usage = self.usage

    def on_end(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            if self.current_usage > 0:
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
                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)

    def on_calculate_dice(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                if self.from_player.is_after_change:
                    if game.current_dice.cost[1]['cost_num'] > 0:
                        game.current_dice.cost[1]['cost_num'] -= 1
                        return True
        return False

    def on_use_skill(self, game:'GeniusGame'):
        self.on_calculate_dice(game)

    def on_change(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.round != game.round:
                self.round = game.round
                self.from_player.is_quick_change == True

    def on_add_damage(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            if self.from_character.is_alive:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    if self.from_player.is_after_change:
                        game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUMMON_ZONE, self.on_change),
        ]
        if self.from_character.talent:
            self.listeners.append((EventType.DAMAGE_ADD, ZoneType.SUMMON_ZONE, self.on_add_damage))
            self.listeners.append((EventType.CALCULATE_DICE, ZoneType.SUMMON_ZONE, self.on_calculate_dice))
            self.listeners.append((EventType.ON_USE_SKILL, ZoneType.SUMMON_ZONE, self.on_use_skill))

class RiteofProgeniture(ElementalBurst):
    id: int = 160403
    name = "Rite of Progeniture: Tectonic Tide"
    name_ch = "诞生式·大地之潮"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 4
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        if self.from_character.from_player.summon_zone.has_entity(SolarIsotoma):
            self.resolve_damage(game, 2)
        else:
            self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Albedo(Character):
    id: int = 1604
    name: str = "Albedo"
    name_ch = "阿贝多"
    time = 4.0
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Weiss, Abiogenesis, RiteofProgeniture]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]

    def listen_talent_events(self, game: 'GeniusGame'):
        status = self.from_player.summon_zone.has_entity(SolarIsotoma)
        if status != None:
            status.listen_event(game, EventType.DAMAGE_ADD, ZoneType.SUMMON_ZONE, status.on_add_damage)
            status.listen_event(game, EventType.CALCULATE_DICE, ZoneType.SUMMON_ZONE, status.on_calculate_dice)
            status.listen_event(game, EventType.ON_USE_SKILL, ZoneType.SUMMON_ZONE, status.on_use_skill)

    def balance_adjustment():
        log = {}
        log[4.8] = "调整了角色牌「阿贝多」召唤「阳华」的效果：效果“此召唤物在场时：我方角色进行下落攻击时少花费一个无色元素”调整为“此召唤物在场，我方执行「切换角色」行动时：将此次切换视为「快速行动」而非「战斗行动」”"
        return log