from genius_invocation.card.character.import_head import *

class Katzlein_Style(NormalAttack):
    name = "Kätzlein Style"
    name_ch = '猎人射术'
    id: int = 110201
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.CRYO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
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


class Icy_Paws(ElementalSkill):
    name = "Icy Paws"
    name_ch = '猫爪冻冻'
    id = 110202
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)
    
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        self.add_combat_shield(game, Cat_Claw_Shield)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Signature_Mix(ElementalBurst):
    name = "Signature Mix"
    name_ch = '最烈特调'
    id = 110203
    type = SkillType.ELEMENTAL_BURST

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
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.from_character.heal(2, game)
        self.generate_summon(game, Drunken_Mist)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Cat_Claw_Shield(Combat_Shield):
    name = "Cat-Claw Shield"
    name_ch = "猫爪护盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        if self.from_character.talent:
            self.usage = 2
        self.current_usage = self.usage

    def update(self):
        if self.from_character.talent:
            self.usage =2
        self.current_usage = max(self.current_usage, self.usage)

class Drunken_Mist(Summon):
    name = "Drunken Mist"
    name_ch = "酒雾领域"
    removable = True
    element = ElementType.CRYO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage
    def end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                SkillType.SUMMON,
                self.element,
                1,
                0,
                self,
                get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            get_my_active_character(game).heal(2, game)
            self.current_usage -= 1
            if self.current_usage<=0:
                self.on_destroy(game)

class Diona(Character):
    id: int = 1102
    name: str = "Diona"
    name_ch = "迪奥娜"
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
