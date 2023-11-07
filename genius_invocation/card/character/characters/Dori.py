from genius_invocation.card.character.import_head import *


class MarvelousSwordDance(NormalAttack):
    id: int = 14101
    name = "Marvelous Sword-Dance (Modified)"
    name_ch = "妙显剑舞·改"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.ELECTRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class TroubleshooterCannon(ElementalSkill):
    id: int = 14102
    name = "Spirit-Warding Lamp: Troubleshooter Cannon"
    name_ch = "镇灵之灯·烦恼解决炮"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.generate_summon(game, AfterSales)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class AfterSales(Summon):
    name = "After-Sales Service Rounds"
    name_ch = "售后服务弹"
    removable = True
    element = ElementType.ELECTRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
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

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class Jinni(Summon):
    name = "Jinni"
    name_ch = "灯中幽精"
    removable = True
    element = ElementType.ELECTRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            character = get_my_active_character(game)
            need_heal = 2
            need_power = 1
            if self.from_character.talent:
                if character.health_point <= 6:
                    need_heal += 1
                if character.power == 0:
                    need_power += 1
            character.heal(heal=need_heal, game=game)
            character.get_power(power=need_power)
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class Alcazarzaray(ElementalBurst):
    id: int = 14103
    name = "Alcazarzaray's Exactitude"
    name_ch = "卡萨扎莱宫的无微不至"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Jinni)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Dori(Character):
    id: int = 1410
    name: str = "Dori"
    name_ch = "多莉"
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.SUNERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [MarvelousSwordDance, TroubleshooterCannon, Alcazarzaray]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]

