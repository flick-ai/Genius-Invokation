from genius_invocation.card.character.import_head import *


class TheClassicsofAcupuncture(NormalAttack):
    id: int = 17051
    name = "The Classics of Acupuncture"
    name_ch = "金匮针解"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.DENDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class UniversalDiagnosis(ElementalSkill):
    id: int = 17052
    name = "Universal Diagnosis"
    name_ch = "太素诊要"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.generate_summon(game, GossamerSprite)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class GossamerSprite(Summon):
    name = "Gossamer Sprite"
    name_ch = "游丝徵灵"
    removable = True
    element = ElementType.DENDRO
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
            character = get_my_active_character(game)
            character.heal(heal=1, game=game)
            self.current_usage -= 1
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class PulsingClarity(Combat_Status):
    name = "Pulsing Clarity"
    name_ch = "脉摄宣明"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            shield = self.from_player.team_combat_status.has_shield(SeamlessShield)
            if shield is None:
                self.from_player.team_combat_status.add_entity(SeamlessShield(
                    game, self.from_player, self.from_character
                ))
            else:
                shield.update(game)
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin),
        ]

class SeamlessShield(Combat_Shield):
    name = "Seamless Shield"
    name_ch = "无郤气护盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def effect(self, game):
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.SUMMON,
            main_damage_element=ElementType.DENDRO,
            main_damage=1,
            piercing_damage=0,
            damage_from=self,
            damage_to=get_active_character(game, 1-self.from_player.index),
            )
        game.add_damage(dmg)
        game.resolve_damage()
        character = get_active_character(game, self.from_player.index)
        character.heal(heal=1, game=game)
        if self.from_character.talent:
            self.from_player.dice_zone.add([ElementToDice(character.element).value])

    def on_destroy(self, game):
        self.effect(game)
        super().on_destroy(game)

    def update(self, game):
        self.effect(game)
        super().update()

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE_SHIELD, self.on_execute_dmg)
        ]

class HolisticRevivification(ElementalBurst):
    id: int = 17053
    name = "Holistic Revivification"
    name_ch = "愈气全形论"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num':4, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.add_combat_status(game, PulsingClarity)
        self.add_combat_shield(game, SeamlessShield)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Baizhu(Character):
    id: int = 1705
    name: str = "Baizhu"
    name_ch = "白术"
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [TheClassicsofAcupuncture, UniversalDiagnosis, HolisticRevivification]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]

