from genius_invocation.card.character.import_head import *

class Firework_FlareUp(NormalAttack):
    '''
        烟火打扬
        普通攻击
    '''
    id: int = 13051
    name = "Firework Flare-Up"
    name_ch = "烟火打扬"
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

class Niwabi_FireDance(ElementalSkill):
    '''
        焰硝庭火舞
        元素战技
    '''
    id: int = 13052
    name="Niwabi Fire-Dance"
    name_ch = "焰硝庭火舞"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.PYRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 不造成伤害

        # 召唤物/状态生成
        self.add_status(game, Niwabi_Enshou)
        # 获得能量 gain 不了一点！
        # self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Ryuukin_Saxifrage(ElementalBurst):
    '''
        琉金云间草
        元素爆发
    '''
    id: int = 13053
    name = "Ryuukin Saxifrage"
    name_ch = "琉金云间草"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.PYRO
        },
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        # 召唤物/状态生成
        self.add_combat_status(game, Aurous_Blaze)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Yoimiya(Character):
    '''宵宫'''
    id: int = 1305
    name: str = 'Yoimiya'
    name_ch = "宵宫"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Firework_FlareUp, Niwabi_FireDance, Ryuukin_Saxifrage]

    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
    def listen_talent_events(self, game:'GeniusGame'):
        status = self.character_zone.has_entity(Niwabi_Enshou)
        if status is not None:
            status.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, status.after_skill)


class Niwabi_Enshou(Status):
    name = "Niwabi Enshou"
    name_ch = "庭火焰硝"
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: Character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2
        self.is_use = False

    def infuse(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.PYRO

    def on_execute_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                game.current_damage.main_damage += 1
                self.is_use = True
                if not self.from_character.talent:
                    self.is_use = False
                    self.current_usage -= 1
                    if self.current_usage <= 0:
                        self.on_destroy(game)

    def after_skill(self, game:'GeniusGame'):
        # if game.current_damage is None:
        #     return
        # if game.current_damage.damage_from == self.from_character:
        if self.is_use:
            self.is_use = False
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                if self.from_character.talent:
                    dmg = Damage.create_damage(
                        game,
                        damage_type=SkillType.OTHER,
                        main_damage_element=ElementType.PYRO,
                        main_damage=1,
                        piercing_damage=0,
                        damage_from=self.from_character,
                        damage_to=get_opponent_active_character(game),
                        is_plunging_attack=False,
                        is_charged_attack=False
                    )
                    game.add_damage(dmg)
                    game.resolve_damage()
                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)

    def udpate(self):
        self.current_usage = self.usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_execute_damage),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infuse),
        ]
        if self.from_character.talent:
            self.listeners.append((EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill))

class Aurous_Blaze(Combat_Status):
    name = "Aurous Blaze"
    name_ch = "琉金火光"
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.from_character != self.from_character:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.PYRO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                    is_plunging_attack=False,
                    is_charged_attack=False
                )
                game.add_damage(dmg)
                game.resolve_damage()

    def on_begin_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_character.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin_phase),
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]
