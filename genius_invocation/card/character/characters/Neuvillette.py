from genius_invocation.card.character.import_head import *

class As_Water_Seeks_Equilibrium(NormalAttack):
    name = 'As Water Seeks Equilibrium'
    name_ch = '如水从平'
    id = 121001
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.HYDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class O_Tears_I_Shall_Repay(ElementalSkill):
    name = "O Tears, I Shall Repay"
    name_ch = "泪水啊, 我必偿还"
    id = 121002
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.add_combat_status(game, Sourcewater_Dropout)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class O_Tides_I_Have_Returned(ElementalBurst):
    name = "O Tides, I Have Returned"
    name_ch = "潮水啊, 我已归来"
    id = 121003
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 1
    cost = [{'cost_num':3, 'cost_type':CostType.HYDRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        # add twice
        self.add_combat_status(game, Sourcewater_Dropout)
        self.add_combat_status(game, Sourcewater_Dropout)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Sourcewater_Dropout(Combat_Status):
    name = "Sourcewater Dropout"
    name_ch = "源水之滴"
    id = 121031

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int = 3
        self.current_usage: int = 1
    def update(self, game: 'GeniusGame'):
        self.current_usage = min(self.current_usage+1, self.usage)

    def after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                if self.from_character.character_zone.has_entity(Prepare_Equitable_Judgement) is None:
                    self.current_usage -= 1
                    self.from_character.heal(2, game)
                    Next_Skill = self.from_character.next_skill
                    prepare_status = Prepare_Equitable_Judgement(game, self.from_player, self.from_character, Next_Skill)
                    self.from_character.character_zone.add_entity(prepare_status)
                    self.from_character.from_player.prepared_skill = prepare_status
                    if self.current_usage <= 0:
                        self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]

class Equitable_Judgement(NormalAttack):
    name = "Equitable Judgement"
    name_ch = "平推裁断"
    id = 121004
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0
    is_prepared_skill = True

    cost = []
    energy_cost: int = 0
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        if self.from_character.health_point>=6:
            self.resolve_damage(game, add_main_damage=1)
            game.add_damage(Damage.create_damage(game, self.damage_type, ElementType.PIERCING,
                              1,
                              0,
                              self.from_character, self.from_character,
                              ))
            game.resolve_damage()

        else:
            self.resolve_damage(game)

        self.from_character.from_player.prepared_skill = None


class Prepare_Equitable_Judgement(Status):
    name = "Prepare Equitable Judgement"
    name_ch = "准备技能: 平推裁断"
    id = 121021
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int = 1
        self.current_usage: int = 0

    def __init__(self, game:'GeniusGame', from_player:'GeniusPlayer', from_character:'Character', next_skill: 'CharacterSkill'):
        super().__init__(game, from_player, from_character)
        self.next_skill = next_skill
        self.current_usage = 1

    def after_change(self,game:'GeniusGame'):
        if game.current_switch.from_character == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.next_skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]

class Neuvillette(Character):
    id: int = 1210
    name: str = "Neuvillette"
    name_ch = "那维莱特"
    time = 4.5
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.FONTAINE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [As_Water_Seeks_Equilibrium, O_Tears_I_Shall_Repay, O_Tides_I_Have_Returned]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[0]
        self.next_skill = Equitable_Judgement(self)
        if self.talent:
            self.listen_talent_events(game)

    def on_damage_add_after_reaction(self, game: 'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character) and game.current_damage.damage_from.from_player == self.from_player:
            if game.current_damage.reaction in [ElementalReactionType.Vaporize,
                                                ElementalReactionType.Frozen,
                                                ElementalReactionType.Bloom,
                                                ElementalReactionType.Electro_Charged] \
                or game.current_damage.swirl_crystallize_type == ElementType.HYDRO and game.current_damage.reaction in [ElementalReactionType.Swirl, ElementalReactionType.Crystallize]:
                self.add_status(game) # Not Implemented yet
    def on_attach_reaction(self, game: 'GeniusGame'):
        if game.current_skill is not None:
            if game.current_skill.from_character.from_player == self.from_player:
                if game.current_attach_reaction in [ElementalReactionType.Vaporize,
                                                ElementalReactionType.Frozen,
                                                ElementalReactionType.Bloom,
                                                ElementalReactionType.Electro_Charged]:
                    self.add_status(game)

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.CHARACTER_ZONE, self.on_damage_add_after_reaction)
        self.listen_event(game, EventType.ELEMENTAL_APPLICATION_REATION, ZoneType.CHARACTER_ZONE, self.on_attach_reaction)

    def add_status(self, game: 'GeniusGame'):
        status = self.character_zone.has_entity(Past_Draconic_Glories)
        if status is None:
            status = Past_Draconic_Glories(game, self.from_player, self)
            self.character_zone.add_entity(status)
        else:
            status.update(game)


class Past_Draconic_Glories(Status):
    name = "Past Draconic Glories"
    name_ch = "遗龙之荣"
    id = 121022
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage: int = 2
        self.current_usage: int = 2

    def dmg_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character and game.current_damage.damage_to!=self.from_character:
            game.current_damage.main_damage += 1
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.dmg_add)
        ]
