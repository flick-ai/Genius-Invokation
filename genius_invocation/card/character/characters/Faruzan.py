from genius_invocation.card.character.import_head import *

class Parthian_Shot(NormalAttack):
    id: int = 15091
    name = "Parthian Shot"
    name_ch = "迴身箭术"
    type: SkillType = SkillType.NORMAL_ATTACK

    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage = 0

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

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)


        self.resolve_damage(game)

        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Wind_Realm_of_Nasamjnin(ElementalSkill):
    id = 15092
    name = "Wind Realm of Nasamjnin"
    name_ch = "非想风天"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 3
    piercing_damage = 0

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
        self.resolve_damage(game)
        self.add_status(game, Manifest_Gale)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class The_Winds_Secret_Ways(ElementalBurst):
    id = 15093
    name = "The Wind's Secret Ways"
    name_ch = "抟风秘道"
    type: SkillType = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Dazzling_Polyhedron)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Faruzan(Character):
    id = 1509
    name = "Faruzan"
    name_ch = "珐露珊"
    element = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.SUMERU

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Parthian_Shot, Wind_Realm_of_Nasamjnin, The_Winds_Secret_Ways]

    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[2]

class Manifest_Gale(Status):
    name = "Manifest Gale"
    name_ch = "疾风示现"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character') -> None:
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1

    def update(self):
        self.current_usage = self.usage

    def on_infusion(self, game: 'GeniusGame'):
        if game.current_damage.damage_from != self.from_character:
            return
        if game.current_damage.damage_type == SkillType.NORMAL_ATTACK and game.current_damage.is_charged_attack:
            game.current_damage.main_damage_element = ElementType.ANEMO
            self.current_usage -= 1
            # TODO: Here we add status on the target character, check if possible to have behavior inproper
            target = game.current_damage.damage_to
            target_player = target.from_player
            for char in target_player.character_list:
                if not char.is_alive: continue
                status = char.character_zone.has_entity(Pressurized_Collapse)
                if status is not None:
                    status.on_destroy(game)
            
            status = Pressurized_Collapse(game, target_player, target)
            target.character_zone.add_entity(status)

            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_calc_dice(self, game: 'GeniusGame'):
        if self.from_player.dice_zone.num()%2 != 0:
            return False
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                if game.current_dice.from_character == self.from_character:
                    if self.current_usage > 0:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False

    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.on_infusion),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calc_dice)
        ]

class Pressurized_Collapse(Status):
    name = "Pressurized Collapse"
    name_ch = '风压坍陷'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character') -> None:
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
    
    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            if not self.from_character.is_active:
                self.from_player.change_to_id(self.from_character.index)
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]

class Dazzling_Polyhedron(Summon):
    name = "Dazzling Polyhedron"
    name_ch = "赫耀多方面体"
    element: ElementType = ElementType.ANEMO
    removable = True

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = 3
        if self.from_character.talent:
            self.from_player.dice_zone.add([DiceType.ANEMO.value])

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.ANEMO,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_to.from_player != self.from_player:
            if game.current_damage.main_damage_element == ElementType.ANEMO:
                game.current_damage.main_damage += 1

    def update(self):
        self.current_usage = self.usage

    def on_begin_action_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player and self.from_character.talent:
            self.from_player.dice_zone.add([DiceType.ANEMO.value])
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
            (EventType.DAMAGE_ADD, ZoneType.SUMMON_ZONE, self.on_dmg_add),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUMMON_ZONE, self.on_begin_action_phase)
        ]