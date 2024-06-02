from genius_invocation.card.character.import_head import *

class ShatterclampStrike(NormalAttack):
    name = 'Shatterclamp Strike'
    name_ch = "重钳碎击"
    id = 23041
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
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class BusterBlaze(ElementalSkill):
    name = 'Buster Blaze'
    name_ch = '烈焰燃绽'
    id = 23042
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.PYRO
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

        self.add_status(game, ArmoredCrabCarapace)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class BattleLineDetonation(ElementalBurst):
    name = "Battle-Line Detonation"
    name_ch = "战阵爆轰"
    id = 24043
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.PYRO
        }
    ]

    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)

        Next_Skill = self.from_character.next_skill
        prepare_status = PrepareSearingBlast(game, self.from_character.from_player, self.from_character, Next_Skill)
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SearingBlast(ElementalBurst):
    name = "Searing Blast"
    name_ch = "炽烈轰破"
    id = 24044
    type = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element = ElementType.PYRO
    main_damage: int = 1
    piercing_damage: int = 0
    is_prepared_skill = True

    cost =[]
    energy_cost = 0
    energy_gain = 0
    def __init__(self, from_character: 'Character') -> None:
        super().on_call(from_character)

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.from_character.from_player.prepared_skill = None

class PrepareSearingBlast(Status):
    name = "Prepare Searing Blast"
    name_ch = "准备技能: 炽烈轰破"
    def __init__(self, game:'GeniusGame', from_player:'GeniusPlayer', from_character:'Character', next_skill: 'CharacterSkill'):
        super().__init__(game, from_player, from_character)
        self.next_skill = next_skill
        self.current_usage = 1

    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.next_skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]

class ArmoredCrabCarapace(Shield):
    name = 'Armored Crab Carapace'
    name_ch = '重甲蟹壳'
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character=None, usage=2):
        super().__init__(game, from_player, from_character)
        self.current_usage = usage

    def update(self, add_usage=2):
        self.current_usage += add_usage

    def on_add_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.ELEMENTAL_BURST:
                game.current_damage.main_damage += self.current_usage // 2
            if game.current_damage.damage_type == SkillType.ELEMENTAL_SKILL:
                if self.current_usage >= 7:
                    game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)
        ]


class EmperorofFireandIron(Character):
    id: int = 2304
    name: str = "Emperor of Fire and Iron"
    name_ch = "铁甲熔火帝皇"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 6
    max_health_point: int = 6
    skill_list: List = [ShatterclampStrike, BusterBlaze, BattleLineDetonation]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        shield = ArmoredCrabCarapace(game, self.from_player, self, 5)
        self.character_zone.add_entity(shield)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = None
        self.next_skill = SearingBlast(self)
        self.talent_usage_round = -1

    def after_any_action(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            add_usage = 0
            # 检查Active Zone
            for shield in self.from_player.team_combat_status.shield:
                add_usage += 1
                shield.on_destroy(game)
            #检查Character Zone
            for character in self.from_player.character_list:
                for status in character.character_zone.status_list:
                    if isinstance(status, Shield):
                        add_usage += 1
                        status.on_destroy(game)
            # 检查天赋
            if self.talent:
                if self.talent_usage_round != game.round:
                    self.talent_usage_round = game.round
                    add_usage += 2
            self.from_character.character_zone.add_entity(
                ArmoredCrabCarapace(game, self.from_player, self, add_usage), add_usage=add_usage
            )

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.after_any_action)
        ]

    def equip_talent(self, game: 'GeniusGame'):
        self.talent = True
        self.elemental_attach(game, ElementType.PYRO)
