from genius_invocation.card.character.import_head import *



class Favonius_ladework(NormalAttack):
    id = 15021
    name = "Favonius ladework"
    name_ch = "西风剑术"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

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

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.resolve_damage(game)
        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Gale_Blade(ElementalSkill):
    id = 15022
    name = "Gale Blade"
    name_ch = "风压剑"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 3
    piercing_damage: int = 0

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

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.from_character.need_to_switch = True
        self.resolve_damage(game)

        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Dandelion_Field(Summon):
    name = "Dandelion Field"
    name_ch = "蒲公英领域"
    removable = True
    element = ElementType.ANEMO

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from.from_player == self.from_player:
            if self.from_character.is_alive and self.from_character.talent:
                if game.current_damage.main_damage_element == ElementType.ANEMO:
                    game.current_damage.main_damage += 1

    def end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage=1,
                main_damage_element=self.element,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.from_player.character_list[self.from_player.active_idx].heal(1, game)
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.damage_add),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.end_phase)
        ]

class Dandelion_Breeze(ElementalBurst):
    id = 15023
    name = "Dandelion Breeze"
    name_ch = "蒲公英之风"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 0
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 4,
            'cost_type': CostType.ANEMO
        }
    ]
    # 4.2更新
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        for character in self.from_character.from_player.character_list:
            if character.is_alive:
                character.heal(2, game)
        self.generate_summon(game, Dandelion_Field)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Jean(Character):
    id: int = 1502
    name: str = "Jean"
    name_ch = "琴"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Favonius_ladework, Gale_Blade, Dandelion_Breeze]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.need_to_switch = False

    def special_switch(self, game: 'GeniusGame'):
        if self.need_to_switch:
            self.need_to_switch = False
            opponent = get_opponent(game) # During special_switch, the active player is always me.
            opponent.change_to_next_character()

    def update_listener_list(self):
        super().update_listener_list()
        self.listeners.append((EventType.SPECIAL_SWITCH, ZoneType.CHARACTER_ZONE, self.special_switch))