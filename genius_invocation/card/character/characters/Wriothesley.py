from genius_invocation.card.character.import_head import *

class ForcefulFistsofFrost(NormalAttack):
    name = 'Forceful Fists of Frost'
    name_ch = "迅烈倾霜拳"
    id: int = 11111
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 1,'cost_type': CostType.CRYO},{'cost_num': 2,'cost_type': CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class IcefangRush(ElementalSkill):
    id = 11102
    name = 'Icefang Rush'
    name_ch = "冰牙突驰"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 3,'cost_type': CostType.CRYO},]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        self.add_status(game, Snappy_Silhouette)

        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Still_Photo_Comprehensive_Confirmation(ElementalBurst):
    id = 11103
    name = 'Still Photo: Comprehensive Confirmation'
    name_ch = "定格·全方位确证"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        }
    ]

    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        for character in self.from_character.from_player.character_list:
            if character.is_alive:
                character.heal(1, game)
        self.generate_summon(game, Newsflash_Field)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Wriothesley(Character):
    id = 1111
    name = 'Wriothesley'
    name_ch = "莱欧斯利"
    element = ElementType.CRYO
    weapon_type = WeaponType.CATALYST
    country = CountryType.FONTAINE

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        Cool_Color_Capture,
        Framing_Freezing_Point_Composition,
        Still_Photo_Comprehensive_Confirmation
    ]
    max_power = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]

class ChillingPenalty(Status):
    name = 'Chilling Penalty'
    name_ch = "寒烈的惩裁"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', talent = False):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.is_

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.from_character == self.from_character:
                if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                    if self.from_character.health_point >= 6:
                        if self.current_usage > 0:
                            if game.current_dice.cost[1]['cost_num'] > 0:
                                game.current_dice.cost[1]['cost_num'] = max(0, game.current_dice.cost[1]['cost_num'] - 1)
                                return True

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    game.current_damage.main_damage += 1
                    self.current_usage -= 1
                    if self.from_character.health_point >= 6:
                        damage = Damage()


    def on_skill(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.current_usage -= 1
            self.is_use = True

    def after_skill(self, game: 'GeniusGame'):




    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]