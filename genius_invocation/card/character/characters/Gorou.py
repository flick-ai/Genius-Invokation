from genius_invocation.card.character.import_head import *
from genius_invocation.entity.status import Crystallize_Shield

class RippingFangFletching(NormalAttack):
    id: int = 16061
    name = "Ripping Fangs Fletching"
    name_ch = "呲牙裂扇箭"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.GEO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class InuzakaAllRoundDefense(ElementalSkill):
    id: int = 16062
    name = "Inuzaka All-Round Defense"
    name_ch = "犬坂吠吠方圆阵"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.add_combat_status(game, FGeneralsWarBanner)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class FGeneralsWarBanner(Combat_Status):
    name = "Frostgeneral's War-Banner"
    name_ch = "大将旗指物"
    max_usage = 3
    init_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.damage_add = 1
        self.current_usage = self.init_usage
        self.talent_usage = 1
     
    def update(self):
        self.current_usage = min(self.max_usage, self.current_usage + self.init_usage)

    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from.from_player == self.from_player:
            if game.current_damage.main_damage_element == ElementType.GEO:
                game.current_damage.main_damage += 1
                if self.from_character.talent and self.talent_usage > 0:
                    self.from_player.get_card(num=1)
                    self.talent_usage -= 1

    def on_end(self, game:'GeniusGame'):
        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_add_damage),
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end)
        ]

class JuugaForwardUntoVictory(ElementalBurst):
    id: int = 16063
    name = "Juuga Forward, Unto Victory"
    name_ch = "兽牙逐突形胜战法"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, FGeneralsWarBanner)
        self.generate_summon(game, GeneralsGlory)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class GeneralsGlory(Summon):
    name = "General's Glory"
    name_ch = "大将威仪"
    removable = True
    element = ElementType.GEO
    max_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.max_usage

    def update(self):
        self.current_usage = max(self.current_usage, self.max_usage)

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
            self.from_player.team_combat_status.add_entity(Crystallize_Shield(game, self.from_player, None))
            self.current_usage -= 1
            if self.current_usage == 0 :
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class Gorou(Character):
    id: int = 1606
    name: str = "Gorou"
    name_ch = "五郎"
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [
        RippingFangFletching,
        InuzakaAllRoundDefense,
        JuugaForwardUntoVictory
    ]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]

    def listen_talent_events(self, game: 'GeniusGame'):
        pass
