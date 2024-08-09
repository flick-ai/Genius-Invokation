from genius_invocation.card.character.import_head import *
from genius_invocation.entity.status import Crystallize_Shield

class CloudGrazingStrike(NormalAttack):
    id: int = 16071
    name = "Cloud-Grazing Strike"
    name_ch = "拂云出手"
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

class OpeningFlourish(ElementalSkill):
    id: int = 16072
    name = "Opening Flourish"
    name_ch = "旋云开相"
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
        self.gain_energy(game)
        self.add_combat_status(game, FlyingCloudFlagFormation, usage=1)

        Next_Skill = self.from_character.next_skill
        prepare_status = ShieldofSwirlingClouds(game, self.from_character.from_player, self.from_character, Next_Skill)
        assert self.from_character.character_zone.has_entity(ShieldofSwirlingClouds) is None
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class ShieldofSwirlingClouds(Shield):
    name = "Shield of Swirling Clouds"
    name_ch = "旋云护盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', Next_Skill: 'CharacterSkill'):
        super().__init__(game, from_player, from_character)
        self.skill = Next_Skill
        self.current_usage = 2

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)
        #Check when the shield disappear. Answer: the same point of damage, even the shield is 0.
        #In this implement, the prepare_status is destroy after the stage of after_skill in the process of on_call.
    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_execute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element != ElementType.PIERCING:
                if game.current_damage.main_damage >= self.current_usage:
                    game.current_damage.main_damage -= self.current_usage
                    self.current_usage = 0
                else:
                    self.current_usage -= game.current_damage.main_damage
                    game.current_damage.main_damage = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg),
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]

class SpearFlourish(ElementalSkill):
    id = 16074
    name = 'Spear Flourish'
    name_ch = '长枪开相'
    type = SkillType.ELEMENTAL_SKILL

    damage_type= SkillType.ELEMENTAL_SKILL
    main_damage_element = ElementType.GEO
    main_damage = 2
    piercing_damage = 0
    is_prepared_skill = True

    cost =[]
    energy_cost = 0
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        add_main_damage = 0
        if self.from_character.from_player.round_discard_cards + self.from_character.from_player.round_tune_cards > 0:
            add_main_damage = 1
        self.resolve_damage(game, add_main_damage=add_main_damage)
        self.from_character.from_player.prepared_skill = None


class FlyingCloudFlagFormation(Combat_Status):
    name = "Flying Cloud Flag Formation"
    name_ch = "飞云旗阵"
    max_usage = 4
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, usage=1):
        super().__init__(game, from_player, from_character)
        self.current_usage = usage
        self.is_use = False

    def update(self, usage=1):
        self.current_usage = min(self.max_usage, self.current_usage + usage)

    def after_any_action(self, game: 'GeniusGame'):
        self.is_use = False

    def on_calculate_dice(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                if self.from_player.is_after_change:
                    if game.current_dice.cost[1]['cost_num'] > 0:
                        game.current_dice.cost[1]['cost_num'] -= 1
                        return True
        return False

    def on_use_skill(self, game:'GeniusGame'):
        if self.on_calculate_dice(game):
            self.current_usage -= 1

    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from.from_player == self.from_player:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                if self.is_use:
                    if self.from_character.talent and self.from_player.hand_zone.num()==0:
                        game.current_damage.main_damage += 2
                if self.current_usage == 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_add_damage),
            (EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate_dice),
            (EventType.ON_USE_SKILL, ZoneType.ACTIVE_ZONE, self.on_use_skill),
            (EventType.AFTER_ANY_ACTION, ZoneType.ACTIVE_ZONE, self.after_any_action),
        ]

class CliffbreakersBanner(ElementalBurst):
    id: int = 16073
    name = "Cliffbreaker's Banner"
    name_ch = "破嶂见旌仪"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, FlyingCloudFlagFormation, usage=3)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Yunjin(Character):
    id: int = 1607
    name: str = "Yun jin"
    name_ch = "云堇"
    time = 4.7
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [CloudGrazingStrike, OpeningFlourish, CliffbreakersBanner]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]
        self.next_skill = SpearFlourish(self)

    def balance_adjustment():
        log = {}
        log[4.8] = "调整了角色牌「云堇」出战状态「飞云旗阵」的效果：移除了效果“造成的伤害+1”"
        return log