from genius_invocation.card.character.import_head import *


class WaterBall(NormalAttack):
    id: int = 22021
    name = "Water Ball"
    name_ch = "水弹"
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

class InfluxBlast(ElementalSkill):
    id: int = 22022
    name = "Influx Blast"
    name_ch = "潋波绽破"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)

        target = get_opponent_active_character(game)
        status = target.character_zone.has_entity(Refraction)
        self.from_character.refraction_target = target
        if not status:
            target.character_zone.add_entity(Refraction(game, from_player=get_opponent(game), from_character=target, belong_to=self.from_character))
        else:
            status.update()
        for char in get_opponent_standby_character(game):
            if char.character_zone.has_entity(Refraction):
                char.character_zone.remove_entity(Refraction)

        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Refraction(Status):
    name = "Refraction"
    name_ch = "水光破镜"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character', belong_to:'Character'):
        super().__init__(game, from_player, from_character)
        self.belong_to = belong_to
        self.max_usage = 2
        self.current_usage = 2
        if self.belong_to.talent:
            self.max_usage += 1
            self.current_usage += 1

    def update(self):
        if self.belong_to.talent:
            self.max_usage = 3
        self.current_usage = self.max_usage

    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element == ElementType.HYDRO:
                game.current_damage.main_damage += 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_destroy(self, game):
        super().on_destroy(game)
        self.belong_to.refraction_target = None

    def on_calculate_dice(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            if game.current_dice.from_character == self.from_character:
                game.current_dice.cost[0]['cost_num'] += 1

    def on_switch(self, game):
        self.on_calculate_dice(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]
        if self.from_character.talent:
            self.listeners.append(EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice)
            self.listeners.append(EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_switch)


class RippledReflection(ElementalBurst):
    id: int = 22023
    name = "Rippled Reflection"
    name_ch = "粼镜折光"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 5
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class MirrorMaiden(Character):
    id: int = 2202
    name: str = "Mirror Maiden"
    name_ch = "愚人众·藏镜仕女"
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [WaterBall, InfluxBlast, RippledReflection]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        self.refraction_target: Character = None

    def listen_talent_events(self, game: 'GeniusGame'):
        if self.refraction_target != None:
            status = self.refraction_target.character_zone.has_entity(Refraction)
            status.listen_event(game, EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, status.on_calculate_dice)
            status.listen_event(game, EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, status.on_switch)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.7] = "调整了「七圣召唤」中，角色牌「愚人众·藏镜仕女」元素战技造成的水元素伤害：造成3水元素伤害改为造成2水元素伤害"
        return log