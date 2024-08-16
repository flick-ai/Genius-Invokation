from genius_invocation.card.character.import_head import *

class Ceremonial_Bladework(NormalAttack):
    name = 'Ceremonial Bladework'
    name_ch = "仪典剑术"
    id: int = 110301
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

class Frostgnaw(ElementalSkill):
    id = 110302
    name = "Frostgnaw"
    name_ch = "霜袭"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 3
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
        self.heal_round = -1
    
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        if self.from_character.talent:
            if self.heal_round!=game.round:
                self.from_character.heal(2, game)
                self.heal_round = game.round

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Glacial_Waltz(ElementalBurst):
    name = "Glacial Waltz"
    name_ch = "凛冽轮舞"
    id: int = 110303
    type = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 4,
            'cost_type': CostType.CRYO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, Icicle)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Icicle(Combat_Status):
    name = "Icicle"
    name_ch = "寒冰之棱"
    id = 110331
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = self.usage

    def on_switch(self, game: 'GeniusGame'):
        if game.active_player != self.from_player: return
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.OTHER,
            main_damage_element=ElementType.CRYO,
            main_damage=2,
            piercing_damage=0,
            damage_from=self,
            damage_to=get_opponent_active_character(game)
        )
        game.add_damage(dmg)
        game.resolve_damage()
        self.current_usage -= 1
        if self.current_usage<=0:
            self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.ACTIVE_ZONE, self.on_switch)
        ]
class Kaeya(Character):
    id: int = 1103
    name: str = "Kaeya"
    name_ch = "凯亚"
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Ceremonial_Bladework, Frostgnaw, Glacial_Waltz]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
