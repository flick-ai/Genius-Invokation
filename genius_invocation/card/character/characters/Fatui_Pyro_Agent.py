from genius_invocation.card.character.characters.import_head import *

class Thrust(NormalAttack):
# 突刺
    id = 0
    name = 'Thrust'
    name_ch = '突刺'
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


class Prowl(ElementalSkill):
    #伺机而动
    name = 'Prowl'
    name_ch = '伺机而动'
    id = 1

    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 1
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
        self.add_status(game, Stealth)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Blade_Ablastion(ElementalBurst):
    #焚毁之风
    name = 'Blade Ablastion'
    name_ch = '焚毁之风'
    id = 2
    type = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 5
    piercing_damage: int = 0

    cost =[{
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }]
    energy_cost = 2
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Stealth(Status):
    #潜行
    name = 'Stealth'
    name_ch = '潜行'

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.usage = 2
        if self.from_character.talent:
            self.max_usage = 3
            self.usage = 3

        self.current_usage = self.usage

    def update(self):
        if self.from_character.talent:
            self.max_usage = 3
            self.usage = 3
        self.current_usage = max(self.current_usage, self.usage)

    def on_execute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element != ElementType.PIERCING:
                if game.current_damage.main_damage > 0:
                    game.current_damage.main_damage -= 1
                    self.current_usage -= 1
                    if self.current_usage <=0:
                        self.on_destroy(game)

    def on_dmg_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            game.current_damage.main_damage += 1
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)

    def infusion(self, game:'GeniusGame'):
        if self.from_character.talent:
            if self.from_character == game.current_damage.damage_from:
                if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                    game.current_damage.main_damage_element = ElementType.HYDRO
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)
        ]
        if self.from_character.talent:
            self.listeners.append((EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion))
    
class Fatui_Pyro_Agent(Character):
    name = 'Fatui Pyro Agent'
    name_ch = '愚人众·火之债务处理人'
    id = 2301
    element = ElementType.PYRO
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.FATUI
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Thrust, Prowl, Blade_Ablastion]
    max_power = 2
    
    def init_state(self, game: 'GeniusGame'):
        assert self.character_zone.has_entity(Stealth) is None
        status = Stealth(game, self.from_player, self)
        self.character_zone.add_entity(status)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]

    def listen_talent_events(self, game: 'GeniusGame'):
        status = self.character_zone.has_entity(Stealth)
        if status is not None:
            status.listen_event(game, EventType.INFUSION, ZoneType.CHARACTER_ZONE, status.infusion)