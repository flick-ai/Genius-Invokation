from genius_invocation.card.character.characters.import_head import *

class Yuuban_Meigen(NormalAttack):
    id: int = 0
    name = "Yuuban Meigen"
    name_ch = "行幡鸣弦"
    type: SkillType = SkillType.NORMAL_ATTACK

    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
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

class Hanega_Song_of_the_Wind(ElementalSkill):
    id = 1
    name = "Hanega: Song of the Wind"
    name_ch = "羽画·风姿华歌"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 2
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
        self.gain_energy(game)
        self.add_status(game, Windfavored)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Kyougen_Five_Ceremonial_Plays(ElementalBurst):
    id = 2
    name = "Kyougen: Five Ceremonial Plays"
    name_ch = "狂言·式乐五番"
    type: SkillType = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 7
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ANEMO
        },
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Wanderer(Character):
    id = 1506
    name = "Wanderer"
    name_ch = "流浪者"
    element = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.OTHER

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Yuuban_Meigen, Hanega_Song_of_the_Wind, Kyougen_Five_Ceremonial_Plays]

    max_power = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0

class Windfavored(Status):
    '''
    优风倾姿
    '''
    name = "Windfavored"
    name_ch = "优风倾姿"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character') -> None:
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def on_dmg_add(self, game: 'GeniusGame') :
        # logger.debug(game.current_damage.damage_from.name)
        # logger.debug(self.from_character.name)
        if game.current_damage.damage_from != self.from_character:
            return
        if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
            game.current_damage.main_damage += 2
            target = get_opponent_active_character(game)
            ls = get_opponent_standby_character(game)
            if len(ls)>0:
                target = ls[0]
            game.current_damage.damage_to = target

            if self.from_character.talent and game.current_damage.is_charged_attack:
                status = self.from_character.character_zone.has_entity(Switch)
                if status is None:
                    status = Switch(game, self.from_player, self.from_character)
                    self.from_character.character_zone.add_entity(status)
                else:
                    status.update()

            self.current_usage -= 1
        elif game.current_damage.damage_type == SkillType.ELEMENTAL_BURST:
            game.current_damage.main_damage += 1
            self.current_usage = 0

        if self.current_usage <= 0:
            self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)
        ]

class Switch(Status):
    '''
    Talent effect
    '''
    #TODO: Check whether passive switch triggers this status?
    name = "Switch_From_Wanderer"
    name_ch = "梦迹一风-效果"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character') -> None:
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.max_usage = 1
        self.current_usage = 1

    def update(self):
        self.current_usage = self.usage

    def on_calculate(self, game:'GeniusGame'):
        if self.current_usage ==0: return False
        if game.active_player != self.from_player: return False
        if game.active_player.active_idx != self.from_character.index: return False
        if game.current_dice.use_type == SwitchType.CHANGE_CHARACTER:
            if game.current_dice.cost[0]['cost_num']>0:
                game.current_dice.cost[0]['cost_num'] -=1
                return True
        return False

    def on_switch(self, game: 'GeniusGame'):
        if self.on_calculate(game):
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
                main_damage=1,
                main_damage_element=ElementType.ANEMO,
                piercing_damage=0
            )
            game.add_damage(dmg)
            game.resolve_damage()

            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_switch)
        ]

