from genius_invocation.card.character.import_head import *





class Wind_Spirit_Creation(NormalAttack):
    name = "Wind Spirit Creation"
    name_ch = "简式风灵作成"
    id = 15011
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ANEMO
        },
        {
            'cost_num': 1,
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


class Astable_Anemohypostasis_Creation_6308(ElementalSkill):
    name = "Astable Anemohypostasis Creation - 6308"
    name_ch = "风灵作成·陆叁零捌"
    id = 15012
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

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        # 会在special switch里调用
        self.from_character.need_to_switch = True
        self.resolve_damage(game)
        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class Large_Wind_Spirit(Summon):
    name = "Large Wind Spirit"
    name_ch = "大型风灵"
    removable = True
    element = ElementType.ANEMO

    def __init__(self, game:'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' =None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = 3
        self.infuse_element= ElementType.ANEMO

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from.from_player == self.from_player:
            if self.from_character.talent and self.infuse_element != ElementType.ANEMO:
                if game.current_damage.main_damage_element == self.infuse_element:
                    game.current_damage.main_damage += 1

    def on_reaction(self, game:'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character) or isinstance(game.current_damage.damage_from, Summon):
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.reaction == ElementalReactionType.Swirl:
                    if self.infuse_element == ElementType.ANEMO:
                        self.infuse_element = game.current_damage.swirl_crystallize_type
                        
    def end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.infuse_element,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.SUMMON_ZONE, self.on_reaction),
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.end_phase),
            (EventType.DAMAGE_ADD, ZoneType.SUMMON_ZONE, self.damage_add)
        ]


class Forbidden_Creation_Isomer_75_Type_II(ElementalBurst):
    name = "Forbidden Creation - Isomer 75 / Type II"
    name_ch = "禁·风灵作成·柒伍同构贰型"
    id = 15013
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
    piercing_damage: int = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: Character) -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        self.generate_summon(game, Large_Wind_Spirit)
        self.resolve_damage(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Sucrose(Character):
    id: int = 1501
    name: str = "Sucrose"
    name_ch = "砂糖"
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Wind_Spirit_Creation, Astable_Anemohypostasis_Creation_6308, Forbidden_Creation_Isomer_75_Type_II]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.need_to_switch = False

    def special_switch(self, game: 'GeniusGame'):
        if self.need_to_switch:
            self.need_to_switch = False
            opponent = get_opponent(self.from_character.from_player.index)
            opponent.change_to_previous_character(game)

    def update_listener_list(self):
        super().update_listener_list()
        self.listeners.append((EventType.SPECIAL_SWITCH, ZoneType.CHARACTER_ZONE, self.special_switch))



