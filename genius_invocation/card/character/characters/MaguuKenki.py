from genius_invocation.card.character.import_head import *


class Ichimonji(NormalAttack):
    id: int = 25011
    name = "Ichimonji"
    name_ch = "一文字"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.ANEMO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class BlusteringBlade(ElementalSkill):
    id: int = 25012
    name = "Blustering Blade"
    name_ch = "孤风刀势"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ANEMO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.generate_summon(game, ShadowswordLoneGale)
        self.gain_energy(game)
        if self.from_character.talent:
            self.from_character.from_player.change_to_next_character()
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ShadowswordLoneGale(Summon):
    name = "Shadowsword: Lone Gale"
    name_ch = "剑影·孤风"
    removable = True
    element = ElementType.ANEMO

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

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
        if(self.current_usage <= 0):
            self.on_destroy(game)

    def on_use(self, game:'GeniusGame'):
        if game.current_skill.damage_type == SkillType.ELEMENTAL_BURST:
            if game.current_skill.from_character == self.from_character:
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

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class ShadowswordGallopingFrost(Summon):
    name = "Shadowsword: Galloping Frost"
    name_ch = "剑影·霜驰"
    removable = True
    element = ElementType.CRYO

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

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
        if(self.current_usage <= 0):
            self.on_destroy(game)

    def on_use(self, game:'GeniusGame'):
        if game.current_skill.damage_type == SkillType.ELEMENTAL_BURST:
            if game.current_skill.from_character == self.from_character:
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

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class FrostyAssault(ElementalSkill):
    id: int = 25013
    name = "Frosty Assault"
    name_ch = "霜驰影突"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.CRYO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.generate_summon(game, ShadowswordGallopingFrost)
        self.gain_energy(game)
        if self.from_character.talent:
            self.from_character.from_player.change_to_previous_character()
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class PseudoTenguSweeper(ElementalBurst):
    id: int = 25014
    name = "Pseudo Tengu Sweeper"
    name_ch = "机巧伪天狗抄"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 4
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ANEMO}]
    energy_cost: int = 3
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        for summon in self.from_character.from_player.summon_zone.space:
            if type(summon) in [ShadowswordLoneGale, ShadowswordGallopingFrost]:
                summon.on_use(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class MaguuKenki(Character):
    id: int = 2501
    name: str = "Maguu Kenki"
    name_ch = "魔偶剑鬼"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Ichimonji, BlusteringBlade, FrostyAssault, PseudoTenguSweeper]
    max_power: int = 3

    def get_element(self):
        return [self.element, ElementType.CRYO]

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.3] = "调整了「七圣召唤」中角色牌「魔偶剑鬼」元素爆发造成的伤害：由“造成6点风元素伤害…”调整为“造成4点风元素伤害…”"
        log[3.4] = "调整了「七圣召唤」中角色牌「魔偶剑鬼」元素战技「孤风刀势」和「霜驰影突」造成的伤害：这两个元素战技将不再造成伤害，仅分别召唤剑影·孤风和剑影·霜驰"
        return log