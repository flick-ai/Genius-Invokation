from genius_invocation.card.character.import_head import *
from typing import Optional

class Garyuu_Bladework(NormalAttack):
    name = 'Garyuu Bladework'
    name_ch = "我流剑术"
    id = 150501
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage = 0

    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ANEMO
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
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SpecialAttack(Garyuu_Bladework):
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.from_character.from_player.prepared_skill = None


class Chihayaburu(ElementalSkill):
    name = 'Chihayaburu'
    name_ch = "千早振る"
    id = 150502
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def add_status(self, game: 'GeniusGame'):
        assert self.from_character.character_zone.has_entity(Midare_Ranzan) is None
        status = Midare_Ranzan(game, self.from_character.from_player, self.from_character, self.from_character.last_swirl)
        self.from_character.character_zone.add_entity(status)
        self.from_character.from_player.prepared_skill = status

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        self.add_status(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.from_character.from_player.change_to_next_character()


class Kazuha_Slash(ElementalBurst):
    name = 'Kazuha Slash'
    name_ch = "万叶之一刀"
    id = 150503
    type: SkillType = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        self.generate_summon(game, Autumn_Whirlwind)
        self.resolve_damage(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Midare_Ranzan(Status):
    name = "Midare Ranzan"
    name_ch = "乱岚拨止"
    id = 150521
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' =None, element: Optional[ElementType] = None):
        super().__init__(game, from_player, from_character)
        if element is None:
            self.element = ElementType.ANEMO
        else:
            self.element = element
        self.prepared_skill = SpecialAttack(from_character)
        self.usage = 1
        self.current_usage = 1

    def on_change_character(self, game:'GeniusGame'):
        if game.current_switch.to_character == self.from_character:
            self.from_player.is_quick_change = True


    def infusion(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                game.current_damage.main_damage_element = self.element

    # def before_any_action(self, game:'GeniusGame'):
    #     if self.from_character.is_active:
    #         skill = self.from_character.skills[0]
    #         skill.before_use_skill(game)
    #         skill.on_call(game)
    #         if not get_opponent(game).is_pass:
    #             game.change_active_player()
    #         self.on_destroy(game)

    def on_call(self, game:'GeniusGame'):
        self.prepared_skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            # (EventType.BEFORE_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.before_any_action),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion),
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_change_character)
        ]

class Autumn_Whirlwind(Summon):
    name = "Autumn Whirlwind"
    name_ch = "流风秋野"
    removable = True
    element = ElementType.ANEMO
    id = 150511
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' =None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = 3
        self.infuse_element= ElementType.ANEMO

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_reaction(self, game:'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character) or isinstance(game.current_damage.damage_from, Summon):
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.reaction == ElementalReactionType.Swirl:
                    if self.infuse_element == ElementType.ANEMO:
                        self.infuse_element = game.current_damage.swirl_crystallize_type

    def on_end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.infuse_element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.SUMMON_ZONE, self.on_reaction),
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]


class Enhance_by_Swirl(Combat_Status):
    element: ElementType
    name = "Enhance_by_Swirl"
    id = 150530
    name_ch = "扩散触发元素增伤(基类)，如果看到这句话就寄了"
    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' =None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_dmg_add(self, game:'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character) or isinstance(game.current_damage.damage_from, Summon):
            if game.current_damage.main_damage_element == self.element:
                game.current_damage.main_damage += 1
                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_dmg_add)
        ]

class Enhance_CRYO_by_Swirl(Enhance_by_Swirl):
    element: ElementType = ElementType.CRYO
    name = "Enhance_CRYO_by_Swirl"
    name_ch = "扩散触发冰元素增伤"
    id = 150531

class Enhance_PYRO_by_Swirl(Enhance_by_Swirl):
    element: ElementType = ElementType.PYRO
    name = "Enhance_PYRO_by_Swirl"
    name_ch = "扩散触发火元素增伤"
    id = 150532

class Enhance_HYDRO_by_Swirl(Enhance_by_Swirl):
    element: ElementType = ElementType.HYDRO
    name = "Enhance_HYDRO_by_Swirl"
    name_ch = "扩散触发水元素增伤"
    id = 150533

class Enhance_ELECTRO_by_Swirl(Enhance_by_Swirl):
    element: ElementType = ElementType.ELECTRO
    name = "Enhance_ELECTRO_by_Swirl"
    name_ch = "扩散触发雷元素增伤"
    id = 150534


class KaedeharaKazuha(Character):
    id: int = 1505
    name: str = "Kaedehara Kazuha"
    name_ch = "枫原万叶"
    time = 3.8
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Garyuu_Bladework, Chihayaburu, Kazuha_Slash]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.last_swirl = None
        if self.talent:
            self.listen_talent_events(game)
        self.talent_skill = self.skills[1]

    def add_combat_status(self, game: 'GeniusGame', STATUS):
        # Add a combat status in active zone of current player
        # Here STATUS is the "class" of Combat_Status, is not an instance of status
        status = self.from_player.team_combat_status.has_status(STATUS)
        if status is None:
            status = STATUS(game, self.from_character.from_player, self.from_character)
            self.from_player.team_combat_status.add_entity(status)
        else:
            status.update()

    def on_excute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self:
            if game.current_damage.main_damage_element == ElementType.ANEMO:
                if game.current_damage.reaction == ElementalReactionType.Swirl:
                    self.last_swirl = game.current_damage.swirl_crystallize_type
                else:
                    self.last_swirl = None

    def after_skill(self, game: "GeniusGame"):
        if game.current_skill.from_character == self:
            if self.last_swirl is not None:
                if self.talent:
                    match self.last_swirl:
                        case ElementType.CRYO:
                            self.add_combat_status(game, Enhance_CRYO_by_Swirl)
                        case ElementType.PYRO:
                            self.add_combat_status(game, Enhance_PYRO_by_Swirl)
                        case ElementType.HYDRO:
                            self.add_combat_status(game, Enhance_HYDRO_by_Swirl)
                        case ElementType.ELECTRO:
                            self.add_combat_status(game, Enhance_ELECTRO_by_Swirl)
                self.last_swirl = None

    def update_listener_list(self):
        super().update_listener_list()
        self.listeners += [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_excute_dmg),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill)
        ]


    # def listen_talent_events(self, game: 'GeniusGame'):
        # self.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill)

    def balance_adjustment():
        log = {}
        log[4.8] = ["调整了角色牌「枫原万叶」元素爆发的伤害：由3点风元素伤害调整为1点；",
                    "调整了角色牌「枫原万叶」元素战技的伤害：由3点风元素伤害调整为1点；",
                    "调整了角色牌「枫原万叶」状态「乱岚拨止」的效果：效果调整为“我方下次通过「切换角色」行动切换到所附属角色时：将此次切换视为「快速行动」而非「战斗行动」。我方选择行动前：如果所附属角色为「出战角色」，则直接使用「普通攻击」；本次「普通攻击」造成的物理伤害变为风元素伤害，结算后移除此效果。”"]
        return log