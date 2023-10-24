from genius_invocation.card.character.characters.import_head import *


class Sparkling_Scatter(NormalAttack):
    '''
    凝光
    普通攻击
    '''
    id: int = 0
    name = "Sparkling Scatter"
    name_ch = "千金掷"
    type: SkillType = SkillType.NORMAL_ATTACK

    #damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 1
    piercing_damage = 0
    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.GEO
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

class Jade_Screen(ElementalSkill):
    '''
    凝光元素战技
    '''
    id: int = 1
    name = "Jade Screen"
    name_ch = "璇玑屏"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 2
    piercing_damage = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.GEO
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
        # 获得能量
        self.gain_energy(game)
        # add status
        self.add_combat_status(game, Jade_Screen_Status)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Starshatter(ElementalBurst):
    '''
    凝光元素爆发
    '''
    id: int = 2
    name = "Starshatter"
    name_ch = "天权崩玉"
    type: SkillType = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 6
    piercing_damage = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.GEO
        },
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        self.resolve_damage(game)

        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
class Ningguang(Character):
    id = 1601
    name = "Ningguang"
    name_ch = "凝光"
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.LIYUE

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Sparkling_Scatter, Jade_Screen, Starshatter]

    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]


class Jade_Screen_Status(Combat_Status):
    '''
    璇玑屏
    '''
    name = "Jade Screen"
    name_ch = "璇玑屏"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def on_execute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to.from_player == self.from_player:
            if game.current_damage.main_damage_element == ElementType.PIERCING:
                return
            if game.current_damage.damage_to.is_active:
                if game.current_damage.main_damage >=2:
                    game.current_damage.main_damage -= 1
                    self.current_usage -=1
                    if self.current_usage <=0:
                        self.on_destroy(game)

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.ELEMENTAL_BURST:
                game.current_damage += 2

        if self.from_character.is_alive and game.current_damage.damage_from is not None and game.current_damage.damage_from.from_player == self.from_player:
            if game.current_damage.main_damage_element == ElementType.GEO:
                game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_damage_add),
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_execute_dmg),
        ]
