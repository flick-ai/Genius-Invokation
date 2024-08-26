from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.equipment.specialskill import SpecialSkillCard
from genius_invocation.entity.status import Frozen_Status, SpecialSkill

class PersTimer(Status):
    name = 'Pers Timer'
    name_ch = "佩伊刻计"
    id = 111221
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.pressurelevel = 0

    def on_get_card(self, game: 'GeniusGame'):
        if game.current_get_card.from_player == self.from_player:
            self.pressurelevel += game.current_get_card.num

    def after_skill(self, game: 'GeniusGame'):
        if self.pressurelevel >= 4:
            damage = Damage.create_damage(
                damage_type=None,
                main_damage_element=ElementType.PHYSICAL,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game))
            game.add_damage(damage)
            game.resolve_damage()
        if self.pressurelevel >= 2:
            self.on_destroy(game)

    def on_use_skill(self, game: 'GeniusGame'):
        self.on_calculate_dice(game)

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.current_dice.from_character == self.from_character:
            if game.current_dice.use_type == SkillType.ELEMENTAL_SKILL:
                if self.pressurelevel >= 2:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
        return False

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_GET_CARD, ZoneType.CHARACTER_ZONE, self.on_get_card),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_use_skill),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice)
        ]

class SubnauticalHunterMode(Status):
    name = "Subnautical Hunter Mode"
    name_ch = "潜猎模式"
    id = 111222
    def __init__(self, game:'GeniusGame', from_player:'GeniusPlayer', from_character:'Character'):
        super().__init__(game, from_player, from_character)
        self.card_num = 0
        self.current_usage = 2

    def after_skill(self, game: 'GeniusGame'):
         if game.current_dice.from_character == self.from_character:
            if game.current_dice.use_type in [SkillType.ELEMENTAL_SKILL,
                                              SkillType.NORMAL_ATTACK]:
                card_ids = multi_max_count_card(self.from_player.hand_zone.card, 2)
                cards = self.from_player.hand_zone.remove(card_ids)
                self.from_player.card_zone.return_card_bottom(cards)
                self.from_player.get_card(num=len(cards))

    def on_get_card(self, game: 'GeniusGame'):
        if game.current_get_card.from_player == self.from_player:
            self.card_num += game.current_get_card.num
            shield_num = min(2, self.card_num // 3)
            self.card_num = self.card_num % 3
            self.from_character.add_status(Shield(game, self.from_player, self.from_character, shield_num))

    def on_final_end(self, game: 'GeniusGame'):
        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_GET_CARD, ZoneType.CHARACTER_ZONE, self.on_get_card),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_final_end)
        ]



class FlowingEddies(NormalAttack):
    name = 'Flowing Eddies'
    name_ch = "洑流剑"
    id: int = 111201
    type: SkillType = SkillType.NORMAL_ATTACK

    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [{'cost_num': 1,'cost_type': CostType.CRYO},{'cost_num': 2,'cost_type': CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class PressurizedFloe(ElementalSkill):
    id = 111202
    name = 'Pressurized Floe'
    name_ch = "浮冰增压"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [{'cost_num': 3,'cost_type': CostType.CRYO},]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)

        if self.from_character.character_zone.has_entity(PersTimer) is None:
            self.add_status(PersTimer(game, self.from_player, self.from_character))

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class ShadowhuntersAmbush(ElementalBurst):
    id = 111203
    name = "Shadowhunter's Ambush"
    name_ch = "猎影潜袭"
    type: SkillType = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 4
    piercing_damage: int = 0

    cost = [{'cost_num': 3, 'cost_type': CostType.CRYO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_status(SubnauticalHunterMode(game, self.from_player, self.from_character))
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Freminet(Character):
    id = 1112
    name = "Freminet"
    name_ch = "菲米尼"
    time = 5.0
    element = ElementType.CRYO
    weapon_type = WeaponType.CLAYMORE
    country = CountryType.FONTAINE
    country_list: List[CountryType] = [CountryType.FONTAINE, CountryType.FATUI]

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        FlowingEddies,
        PressurizedFloe,
        ShadowhuntersAmbush
    ]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
        self.talent_usage = 2

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_use_skill)
        self.listen_event(game, EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_final_end)

    def after_use_skill(self, game: 'GeniusGame'):
        if self.talent:
            if game.current_skill.from_character == self:
                if self.talent_usage > 0:
                    self.from_player.get_card(num=1)
                    self.talent_usage -= 1

    def on_final_end(self, game: 'GeniusGame'):
        if self.talent:
            self.talent_usage = 2