from genius_invocation.card.character.import_head import *

class Dough_Fu(NormalAttack):
    name = 'Dough-Fu'
    name_ch = '白案功夫'
    id = 130201
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


class Guoba_Attack(ElementalSkill):
    name = 'Guoba Attack'
    name_ch = '锅巴出击'
    id = 130202
    type: SkillType = SkillType.ELEMENTAL_SKILL
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
        # 不造成伤害
        if self.from_character.talent:
            self.resolve_damage(game)

        # 召唤物/状态生成
        self.generate_summon(game, Guoba)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Pyronado(ElementalBurst):
    name = 'Pyronado'
    name_ch = '旋火轮'
    id = 130203
    type: SkillType = SkillType.ELEMENTAL_BURST
    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
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
        self.add_combat_status(game, Pyronado_Combat_Status)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class Pyronado_Combat_Status(Combat_Status):
    name = 'Pyronado'
    name_ch = '旋火轮'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.usage = 2
    def update(self):
        self.current_usage = max(self.current_usage, self.usage)
    def after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.PYRO,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -=1
            if self.current_usage<=0:
                self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]

class Guoba(Summon):
    name = 'Guoba'
    name_ch = '锅巴'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.usage = 2
    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def end_phase(self, game:'GeniusGame'):
        if game.active_player != self.from_player: return
        dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.PYRO,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
        )
        game.add_damage(dmg)
        game.resolve_damage()
        self.current_usage -=1
        if self.current_usage<=0:
            self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.end_phase)
        ]
class Xiangling(Character):
    id: int = 1302
    name: str = "Xiangling"
    name_ch = "香菱"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Dough_Fu, Guoba_Attack, Pyronado]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
