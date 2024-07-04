from genius_invocation.card.character.import_head import *



class SteelFang(NormalAttack):
    id: int = 14021
    name = "Steel Fang"
    name_ch = "钢脊"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.ELECTRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ClawandThundert(ElementalSkill):
    id: int = 14022
    name = "Claw and Thunder"
    name_ch = "利爪与苍雷"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        if self.from_character.talent and self.from_character.use_round != game.round:
            self.from_character.use_round = game.round
            characters = [get_my_active_character(game)] + get_my_standby_character(game)
            for char in characters:
                if char.element == ElementType.ELECTRO:
                    if char.max_power != char.power:
                        char.get_power(power=1)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class TheWolfWithin(Status):
    name = "The Wolf Within"
    name_ch = "雷狼"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = max(self.max_usage, self.current_usage)

    def on_after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.type == SkillType.NORMAL_ATTACK or game.current_skill.type == SkillType.ELEMENTAL_SKILL:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.ELECTRO,
                    main_damage=2,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                    )
                game.add_damage(dmg)
                game.resolve_damage()

    def on_begin(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_skill),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

class LightningFang(ElementalBurst):
    id: int = 14023
    name = "Lightning Fang"
    name_ch = "雷牙"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_status(game, TheWolfWithin)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Razor(Character):
    id: int = 1402
    name: str = "Razor"
    name_ch = "雷泽"
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [SteelFang, ClawandThundert, LightningFang]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        # 4.2更新
        self.use_round = -1

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.2] = "调整了「七圣召唤」中，角色牌「雷泽」元素爆发所需的充能和伤害：元素爆发所需的充能由3点调整为2点，造成5点雷元素伤害调整为造成3点雷元素伤害"
        return log