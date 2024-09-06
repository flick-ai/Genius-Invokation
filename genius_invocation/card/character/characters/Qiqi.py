from genius_invocation.card.character.import_head import *

class Ancient_Sword_Art(NormalAttack):
    name = 'Ancient Sword Art'
    name_ch = "云来古剑法"
    id: int = 110801
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

class Adeptus_Art_Herald_of_Frost(ElementalSkill):
    id = 110802
    name = 'Adeptus Art: Herald of Frost'
    name_ch = "仙法·寒病鬼差"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
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
        self.generate_summon(game, Herald_of_Frost)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Adeptus_Art_Preserver_of_Fortune(ElementalBurst):
    id = 110803
    name = 'Adeptus Art: Preserver of Fortune'
    name_ch = "仙法·救苦度厄"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 3
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

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, Fortune_Preserving_Talisman)

        if self.from_character.talent:
            if self.from_character.use_revive <2:
                self.from_character.use_revive += 1

                for i in range(3):
                    char = self.from_character.from_player.character_list[i]
                    if not char.is_alive:
                        char.revive(game)
                        char.heal(heal=2, game=game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Qiqi(Character):
    id = 1108
    name = 'Qiqi'
    name_ch = "七七"
    time = 4.0
    element = ElementType.CRYO
    weapon_type = WeaponType.SWORD
    country = CountryType.LIYUE

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        Ancient_Sword_Art,
        Adeptus_Art_Herald_of_Frost,
        Adeptus_Art_Preserver_of_Fortune
    ]
    max_power = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.use_revive = 0
        self.talent_skill = self.skills[2]

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.7] = "调整了角色牌「七七」元素战技召唤的召唤物「寒病鬼差」的效果；其治疗相关效果调整为“此召唤物在场时，七七使用「普通攻击」后：治疗受伤最多的我方角色1点；每回合1次：再治疗我方出战角色1点。”（增加了额外的治疗效果）"
        return log

class Herald_of_Frost(Summon):
    name = 'Herald of Frost'
    name_ch = "寒病鬼差"
    element = ElementType.CRYO
    removable = True
    id = 110811

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 3
        self.usage = 3
        # 4.7平衡性调整: 增加每回合一次对出战角色的治疗
        self.heal_usage_round = -1

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character==self.from_character:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                max_dmg_taken = -1
                max_taken_char = None
                ls: List[int] = []
                id = self.from_player.active_idx
                for i in range(self.from_player.character_num):
                    ls.append(id)
                    id += 1
                    if id >= self.from_player.character_num:
                        id = 0

                for i in ls:
                    char = self.from_player.character_list[i]
                    dmg_taken = char.max_health_point - char.health_point
                    if dmg_taken > max_dmg_taken:
                        max_dmg_taken = dmg_taken
                        max_taken_char = char
                max_taken_char.heal(1,game=game)

                # 4.7平衡性调整: 增加每回合一次对出战角色的治疗
                if self.heal_usage_round != game.round:
                    self.heal_usage_round = game.round
                    get_my_active_character(game).heal(1, game=game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
            (EventType.AFTER_USE_SKILL, ZoneType.SUMMON_ZONE, self.after_skill)
        ]

class Fortune_Preserving_Talisman(Combat_Status):
    name = 'Fortune-Preserving Talisman'
    name_ch = "度厄真符"
    id = 110831
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 3
        self.usage = 3

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self.from_character and game.current_skill.type == SkillType.ELEMENTAL_BURST: return
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.from_character.health_point != game.current_skill.from_character.max_health_point:
                game.current_skill.from_character.heal(2,game=game)
                self.current_usage -= 1
                if self.current_usage<=0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]
