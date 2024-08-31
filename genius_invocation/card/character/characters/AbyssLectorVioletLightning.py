from genius_invocation.card.character.import_head import *

class DenofThunder(NormalAttack):
    name = "Den of Thunder"
    name_ch = "渊薮落雷"
    id = 240601
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.ELECTRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class ShockoftheEnigmaticAbyss(ElementalSkill):
    name = "Shock of the Enigmatic Abyss"
    name_ch = "秘渊虚霆"
    id = 240602
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
        target = get_opponent_active_character(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        if target.elemental_application == ElementType.ELECTRO:
            target.loose_power(1)
            self.from_character.get_power(1)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class WildThunderburst(ElementalBurst):
    name = "Wild Thunderburst"
    name_ch = "狂迸骇雷"
    id = 240603
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        add_damage = 0
        if get_opponent_active_character(game).power <= 1:
            add_damage = 2
        self.resolve_damage(game, add_main_damage=add_damage)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ElectricRebirth(Status):
    name = "Electric Rebirth"
    name_ch = "雷之新生"
    id = 240621
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.set_talent = False

    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时
        '''
        if not self.from_character.is_alive:
            self.from_character.is_alive = True
            self.from_character.health_point = 0
            self.from_character.heal(4, game, heal_type=HealType.REVIVE)
            self.from_character.revive_event(game)
            if self.set_talent:
                target = get_active_character(game, 1-self.from_player.index)
                target.loose_power(1)
                self.from_character.talent = False
                self.from_character.character_zone.talent_card.on_destroy(game)
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        ]

class AbyssLectorVioletLightning(Character):
    id: int = 2406
    name: str = "Abyss Lector - Violet Lightning"
    name_ch = "深渊咏者·紫电"
    time = 5.1
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 6
    max_health_point: int = 6
    skill_list: List = [DenofThunder, ShockoftheEnigmaticAbyss, WildThunderburst]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        rebirth = ElectricRebirth(game, self.from_player, self)
        self.character_zone.add_entity(rebirth)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        if self.talent:
            self.character_zone.has_entity(ElectricRebirth).set_talent = True

    def on_dmg_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self:
            if game.current_damage.main_damage_element == ElementType.ELECTRO:
                game.current_damage.main_damage += 1

    def revive_event(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)

    def equip_talent(self, game:'GeniusGame', is_action=True, talent_card=None):
        self.talent = True
        self.character_zone.talent_card = talent_card
        if self.character_zone.has_entity(ElectricRebirth) is None:
            target = get_opponent_active_character(game)
            target.loose_power(1)
        self.listen_event(game, EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)

    def on_character_die(self, game: 'GeniusGame'):
        if not self.from_character.is_alive:
            if self.from_character.talent:
                target = get_opponent_active_character(game)
                target.loose_power(1)

