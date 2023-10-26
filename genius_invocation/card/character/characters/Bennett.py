from genius_invocation.card.character.import_head import *

class Strike_of_Fortune(NormalAttack):
    name = 'Strike of Fortune'
    name_ch = '好运剑术'
    id = 130301
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
            'cost_type': CostType.PYRO
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


class Passion_Overload(ElementalSkill):
    name = 'Passion Overload'
    name_ch = '热情过载'
    id = 130302
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.PYRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Fantastic_Voyage(ElementalBurst):
    name = 'Fantastic Voyage'
    name_ch = '美妙旅程'
    id = 130303
    type: SkillType = SkillType.ELEMENTAL_BURST
    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 4,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost=2
    energy_gain=0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, Inspiration_Field)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Inspiration_Field(Combat_Status):
    name = 'Inspiration Field'
    name_ch = '鼓舞领域'
    def __init__(self, game:'GeniusGame', from_player:'GeniusPlayer', from_character:'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.usage = 2
    def add_dmg(self, game:'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character):
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.damage_from.health_point >=7 or self.from_character.talent:
                    if game.current_damage.main_damage_element != ElementType.PIERCING:
                        game.current_damage.main_damage += 2
    def heal(self, game:'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.from_character.health_point <=6:
                game.current_skill.from_character.heal(2, game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.add_dmg),
            (EventType.AFTER_ANY_ACTION, ZoneType.ACTIVE_ZONE, self.heal)
        ]
class Bennett(Character):
    id: int = 1303
    name: str = "Bennett"
    name_ch = "班尼特"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Strike_of_Fortune, Passion_Overload, Fantastic_Voyage]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]
