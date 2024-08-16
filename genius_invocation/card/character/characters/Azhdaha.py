from genius_invocation.card.character.import_head import *

class SunderingCharge(NormalAttack):
    id: int = 260201
    name = "SunderingCharge"
    name_ch = "碎岩冲撞"
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

class AuraofMajesty(ElementalSkill):
    id: int = 260202
    name = "Aura of Majesty"
    name_ch = "磅礴之气"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        if game.current_damage.reaction == ElementalReactionType.Crystallize:
            absorb_element = game.current_damage.swirl_crystallize_type
            self.from_character.now_element = absorb_element
            if absorb_element not in self.from_character.absorbed_element:
                self.from_character.from_player.dice_zone.add([ElementToDice(absorb_element)])
                self.from_character.absorbed_element.append(absorb_element)
            if absorb_element == ElementType.PYRO:
                self.from_character.update_skills(BlazingRebuke(self.from_character))
            elif absorb_element == ElementType.CRYO:
                self.from_character.update_skills(FrostspikeWave(self.from_character))
            elif absorb_element == ElementType.HYDRO:
                self.from_character.update_skills(TorrentialRebuke(self.from_character))
            else:
                self.from_character.update_skills(ThunderstormWave(self.from_character))
        else:
            self.add_status(game, StoneFacetsElementalCrystallization)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class FrostspikeWave(ElementalSkill):
    id = 260204
    name = "Frostspike Wave"
    name_ch = "霜刺破袭"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.CRYO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class BlazingRebuke(ElementalSkill):
    id = 260205
    name = "Blazing Rebuke"
    name_ch = "炽焰重斥"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class TorrentialRebuke(ElementalSkill):
    id = 260206
    name = "Torrential Rebuke"
    name_ch = "洪流重斥"
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
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ThunderstormWave(ElementalSkill):
    name = "Thunderstorm Wave"
    name_ch = "霆雷破袭"
    id = 260207
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class DecimatingRockfall(ElementalBurst):
    id: int = 260203
    name = "Decimating Rockfall"
    name_ch = "山崩毁阵"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 4
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game, add_main_damage=len(self.from_character.absorbed_element))
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class StoneFacetsElementalCrystallization(Status):
    name = "Stone Facets: Elemental Crystallization"
    name_ch = "磐岩百相·元素凝晶"
    id = 260221
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)

    def on_after_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            absorb_element = game.current_damage.damage_type
            remove = False
            if absorb_element in [ElementType.PYRO, ElementType.CRYO, ElementType.HYDRO, ElementType.ELECTRO]:
                self.from_character.now_element = absorb_element
                if absorb_element not in self.from_character.absorbed_element:
                    self.from_character.from_player.dice_zone.add([ElementToDice(absorb_element)])
                    self.from_character.absorbed_element.append(absorb_element)
                    remove = True
                if absorb_element == ElementType.PYRO:
                    self.from_character.update_skills(BlazingRebuke(self.from_character))
                elif absorb_element == ElementType.CRYO:
                    self.from_character.update_skills(FrostspikeWave(self.from_character))
                elif absorb_element == ElementType.HYDRO:
                    self.from_character.update_skills(TorrentialRebuke(self.from_character))
                else:
                    self.from_character.update_skills(ThunderstormWave(self.from_character))

        if remove:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_after_damage),
        ]

class Azhdaha(Character):
    id: int = 2602
    name: str = "Azhdaha"
    name_ch = "若陀龙王"
    time = 4.25
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [SunderingCharge, AuraofMajesty, DecimatingRockfall]
    max_power: int = 2

    def get_element(self):
        if self.now_element is not None:
            return [self.now_element, self.element]
        else:
            return [self.element]


    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = None
        self.absorbed_element = []
        self.now_element = None

    def equip_talent(self, game:'GeniusGame', is_action=True, talent_card=None):
        # self.talent = True
        # self.character_zone.talent_card = talent_card
        self.add_status(game, StoneFacetsElementalCrystallization)
        dices = []
        for element in self.from_player.element_set:
            dices.append(ElementToDice(element))
        self.from_player.dice_zone.add(dices)
        game.is_change_player = is_action

    def add_status(self, game: 'GeniusGame', STATUS):
        status = self.from_character.character_zone.has_entity(STATUS)
        if status is None:
            status = STATUS(game, self.from_character.from_player, self.from_character)
            self.from_character.character_zone.add_entity(status)
        else:
            try:
                status.update(game)
            except:
                status.update()
    
    def update_skills(self, skill: 'ElementalSkill'):
        if len(self.skills) == 3:
            self.skills.insert(2, skill)
        else:
            self.skills[2] = skill
