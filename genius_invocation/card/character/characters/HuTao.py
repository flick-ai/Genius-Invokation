from genius_invocation.card.character.import_head import *

class Secret_Spear_of_Wangsheng(NormalAttack):
    name = 'Secret Spear of Wangsheng'
    name_ch = '往生秘传枪法'
    id = 130701
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


class Guide_to_Afterlife(ElementalSkill):
    name = 'Guide to Afterlife'
    name_ch = '蝶引来生'
    id = 130702

    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 2,
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
        # 召唤物/状态生成
        self.add_status(game, Paramita_Papilio)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Spirit_Soother(ElementalBurst):
    name = 'Spirit Soother'
    name_ch = '安神秘法'
    id = 130703
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost=3
    energy_gain=0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        if self.from_character.health_point<=6:
            self.resolve_damage(game,add_main_damage=1)
            self.from_character.heal(3, game)
        else:
            self.resolve_damage(game)
            self.from_character.heal(2, game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Paramita_Papilio(Status):
    name = 'Paramita Papilio'
    name_ch = '彼岸蝶舞'
    id = 130721
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def infusion(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.PYRO
    def dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PYRO:
                game.current_damage.main_damage += 1
    def execute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.is_charged_attack:
                target = game.current_damage.damage_to
                status = target.character_zone.has_entity(Blood_Blossom)
                if status is None:
                    status = Blood_Blossom(game, target.from_player, target)
                    target.character_zone.add_entity(status)
                else:
                    status.update()
    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.dmg_add),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.execute_dmg)
        ]
class Blood_Blossom(Status):
    name = 'Blood Blossom'
    name_ch = '血梅香'
    id = 130722
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
    def end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage=1,
                main_damage_element=ElementType.PYRO,
                piercing_damage=0,
                damage_from=None,
                damage_to=self.from_character,
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.on_destroy(game)
    def update(self):
        self.current_usage = self.usage
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.end_phase)
        ]

class HuTao(Character):
    id: int = 1307
    name: str = "Hu Tao"
    name_ch = "胡桃"
    time = 3.7
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Secret_Spear_of_Wangsheng, Guide_to_Afterlife, Spirit_Soother]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        if self.talent:
            self.listen_talent_events(game)

    def dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self:
            if game.current_damage.main_damage_element == ElementType.PYRO:
                if self.health_point<=6:
                    game.current_damage += 1

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.dmg_add)

