from genius_invocation.card.character.import_head import *


class KhandaBarrierBuster(NormalAttack):
    id: int = 17021
    name = "Khanda Barrier-Buster"
    name_ch = "藏蕴破障"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.DENDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class VijnanaPhalaMine(ElementalSkill):
    id: int = 17022
    name = "Vijnana-Phala Mine"
    name_ch = "识果种雷"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':2, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        self.add_status(game, VijnanaSuffusion)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class VijnanaSuffusion(Status):
    name = "Vijnana Suffusion"
    name_ch = " 通塞识"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = max(self.max_usage, self.current_usage)

    def on_infuse(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                if game.current_damage.is_charged_attack:
                    if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                        game.current_damage.main_damage_element = ElementType.CRYO
                        self.current_usage -= 1
                        self.is_use = True
    
    def on_after_any(self, game:'GeniusGame'):
        if self.is_use:
            self.from_player.summon_zone.add_entity(ClusterbloomArrow(game, from_player=self.from_player, from_character=self.from_character))
            self.is_use = False
            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_calculate_dice(self, game:'GeniusGame'):
        if self.from_player.dice_zone.num()%2 != 0:
            return False
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                if game.current_dice.from_character == self.from_character:
                    if self.usage > 0:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] -= 1
                            return True
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False
    
    def on_skill(self, game:"GeniusGame"):
        self.on_calculation(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.on_infuse),
            (EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.on_after_any)
        ]
        if self.from_character.talent:
            self.listeners.append(
                (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
                (EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.on_skill),
            )


class ClusterbloomArrow(Summon):
    name = "Clusterbloom Arrow"
    name_ch = "藏蕴花矢"
    removable = True
    element = ElementType.DENDRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 1

    def update(self):
        if self.current_usage < self.usage:
            self.current_usage += 1
        else:
            self.current_usage = self.current_usage

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
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
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class FashionersTanglevineShaft(ElementalBurst):
    id: int = 17023
    name = "Fashioner's Tanglevine Shaft"
    name_ch = "造生缠藤箭"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 4
    piercing_damage: int = 1
    cost = [{'cost_num':3, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Tighnari(Character):
    id: int = 1702
    name: str = "Tighnari"
    name_ch = "提纳里"
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.SUMERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [KhandaBarrierBuster, VijnanaPhalaMine, FashionersTanglevineShaft]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.init_skill[1]
    
    def listen_talent_events(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status(VijnanaSuffusion)
        if status is not None:
            status.listen_event(game, EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, status.on_calculate_dice)
            status.listen_event(game, EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, status.on_skill)
