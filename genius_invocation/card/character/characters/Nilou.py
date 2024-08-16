from genius_invocation.card.character.import_head import *
from genius_invocation.entity.status import GoldenChalice
from genius_invocation.entity.summon import BountifulCore

class DanceofSamser(NormalAttack):
    id: int = 120801
    name = "Dance of Samser"
    name_ch = "弦月舞步"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.HYDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class DanceofHaftkarsvar(ElementalSkill):
    id: int = 120802
    name = "Dance of Haftkarsvar"
    name_ch = "七域舞步"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        if self.from_character.satisfy_element:
            self.add_combat_status(game, GoldenChalice)     
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class DanceofAbzendegi(ElementalBurst):
    id: int = 120803
    name = "Dance of Abzendegi: Distant Dreams, Listening Spring"
    name_ch = "浮莲舞步·远梦聆泉"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)

        target = get_opponent_active_character(game)
        status = target.character_zone.has_entity(LingeringAeon)
        if not status:
            target.character_zone.add_entity(LingeringAeon(game, from_player=get_opponent(game), from_character=target))
        else:
            status.update()

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class LingeringAeon(Status):
    name = "Lingering Aeon"
    name_ch = "永世流沔"
    id = 120821
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1

    def end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game, 
                damage_type=SkillType.OTHER,
                main_damage=3,
                main_damage_element=ElementType.HYDRO,
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


class Nilou(Character):
    id: int = 1208
    name: str = "Nilou"
    name_ch = "妮露"
    time = 4.2
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.SUMERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [DanceofSamser, DanceofHaftkarsvar, DanceofAbzendegi]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        
        self.satisfy_element:bool = False
        unique_element_set = self.from_player.element_set
        if len(unique_element_set) == 2 and ElementType.HYDRO in unique_element_set and ElementType.DENDRO in unique_element_set:
            self.satisfy_element = True
        
