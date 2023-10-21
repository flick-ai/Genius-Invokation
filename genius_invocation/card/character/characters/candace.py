from genius_invocation.card.character.characters.import_head import *

class Gleaming_Spear_Guardian_Stance(NormalAttack):
    id: int = 0
    name = "Gleaming Spear: Guardian Stance"
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.HYDRO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Sacred_Rite_Herons_Sanctum(ElementalSkill):
    id: int = 1
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 0
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost=0
    energy_gain=1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.gain_energy(game)
        Next_Skill = self.from_character.next_skill # The Skill instance now is stored in character, somewhere else maybe better?
        prepare_status = Heron_Shield(game, self.from_character.from_player, self.from_character, Next_Skill)
        assert self.from_character.character_zone.has_entity(Heron_Shield) is None
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Heron_Strike(ElementalSkill):
    name = 'Heron Strike'
    id = 3
    type = SkillType.ELEMENTAL_SKILL

    damage_type= SkillType.ELEMENTAL_SKILL
    main_damage_element = ElementType.HYDRO
    main_damage = 3
    piercing_damage = 0

    cost =[]
    energy_cost = 0
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.from_character.from_player.prepared_skill = None


class Sacred_Rite_Wagtails_Tide(ElementalBurst):
    name = "Sacred Rite: Wagtail's Tide"
    id = 2
    type = SkillType.ELEMENTAL_BURST

    damage_type= SkillType.ELEMENTAL_SKILL
    main_damage_element = ElementType.HYDRO
    main_damage = 2
    piercing_damage = 0

    cost =[
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost = 2
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.add_combat_status(game, Prayer_of_the_Crimson_Crown)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Candace(Character):
    id = 1207
    name = "Candace"
    element = ElementType.HYDRO
    weapon_type = WeaponType.POLEARM
    country = CountryType.SUNERU

    init_health_point = 10
    max_health_point = 10
    skill_list = [Gleaming_Spear_Guardian_Stance, Sacred_Rite_Herons_Sanctum, Sacred_Rite_Wagtails_Tide]

    max_power = 2
    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.next_skill = Heron_Strike(self)

class Heron_Shield(Shield):
    name = "Heron Shield"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', Next_Skill: 'CharacterSkill'):
        super().__init__(game, from_player, from_character)
        self.skill = Next_Skill
        self.current_usage = 2

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)
        #TODO: Check when the shield disappear. Answer: the same point of damage, even the shield is 0. 
        #In this implement, the prepare_status is destroy after the stage of after_skill in the process of on_call.
    
    def on_execute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element != ElementType.PIERCING:
                if game.current_damage.main_damage >= self.current_usage:
                    game.current_damage.main_damage -= self.current_usage
                    self.current_usage = 0
                else:
                    self.current_usage -= game.current_damage.main_damage
                    game.current_damage.main_damage = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg)
        ]

class Prayer_of_the_Crimson_Crown(Combat_Status):
    name = "Prayer of the Crimson Crown"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2
        self.additional_damage_round = -1
        self.last_switch_round = -1
    
    def infusion(self, game:'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character):
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.damage_from.weapon_type in [WeaponType.SWORD, WeaponType.CLAYMORE, WeaponType.POLEARM]:
                    if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                        game.current_damage.main_damage_element = ElementType.HYDRO
    
    def on_dmg_add(self, game:'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character):
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    game.current_damage.main_damage += 1

    def after_skill(self, game:'GeniusGame'):
        if not self.from_character.talent: return
        if self.additional_damage_round == game.round: return
        if game.current_skill.from_character.from_player != self.from_player: return
        if game.current_skill.type == SkillType.NORMAL_ATTACK:
            self.additional_damage_round = game.round
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.HYDRO,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
    
    def on_switch(self, game:'GeniusGame'):
        if self.last_switch_round == game.round: return
        if game.active_player != self.from_player: return
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.OTHER,
            main_damage_element=ElementType.HYDRO,
            main_damage=1,
            piercing_damage=0,
            damage_from=self,
            damage_to=get_opponent_active_character(game)
        )
        game.add_damage(dmg)
        game.resolve_damage()
        self.last_switch_round = game.round
    
    def on_begin_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage == 0:
                self.on_destroy(game)
    
    def update(self):
        self.current_usage = self.usage
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_switch)
        ]
