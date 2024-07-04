from genius_invocation.card.character.import_head import *


class AbductiveReasoning(NormalAttack):
    id: int = 17061
    name = "Abductive Reasoning"
    name_ch = "溯因反绎法"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.DENDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Universality_An_Elaboration_on_Form(ElementalSkill):
    id: int = 17062
    name = "Universality: An Elaboration on Form"
    name_ch = "共相·理式摹写"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        self.add_status(game, ChiselLight_Mirror)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ChiselLight_Mirror(Status):
    name = "Chisel-Light Mirror"
    name_ch = "琢光镜"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = 2

    def update(self):
        self.current_usage = min(self.usage, self.current_usage + 2)

    def on_infuse(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.DENDRO
    def after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.DENDRO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()

                if game.current_skill.is_charged_attack:
                    self.current_usage = min(self.current_usage + 1, self.usage)
    
    def on_begin_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage<=0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.on_infuse),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase)
        ]

class Particular_Field_Fetters_of_Phenomena(ElementalBurst):
    id: int = 17063
    name = "Particular Field: Fetters of Phenomena"
    name_ch = "殊境·显象缚结"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 4
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        status = self.from_character.character_zone.has_entity(ChiselLight_Mirror)
        add_dmg = 0
        if status is not None:
            add_dmg = status.current_usage
        self.consume_energy(game)
        self.resolve_damage(game, add_main_damage=add_dmg)
        if status is None:
            self.add_status(game, ChiselLight_Mirror)

        status = self.from_character.character_zone.has_entity(ChiselLight_Mirror)
        if self.talent and add_dmg>0:
            status.current_usage = 3
            self.from_character.from_player.get_card(1)
        else:
            status.current_usage = 3-add_dmg

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Alhaitham(Character):
    id: int = 1706
    name: str = "Alhaitham"
    name_ch = "艾尔海森"
    time = 4.3
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.SUMERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [AbductiveReasoning, Universality_An_Elaboration_on_Form, Particular_Field_Fetters_of_Phenomena]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]
    
    