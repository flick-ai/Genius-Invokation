from genius_invocation.card.character.import_head import *

class Supplicants_Bowmanship(NormalAttack):
    id = 170101
    name = "Supplicant's Bowmanship"
    name_ch = "祈颂射艺"
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
            'cost_type': CostType.DENDRO
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


class Floral_Brush(ElementalSkill):
    id = 170102
    name = "Floral Brush"
    name_ch = "拂花偈叶"
    type = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.DENDRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1
    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)
        self.talent_round = -1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        if self.from_character.talent and self.talent_round != game.round:
            self.add_combat_status(game, Sprout)
            self.talent_round = game.round
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class TrumpCard_Kitty(ElementalBurst):
    name = 'Trump-Card Kitty'
    name_ch = "猫猫秘宝"
    id = 170103
    type = SkillType.ELEMENTAL_BURST

    damage_type = SkillType.ELEMENTAL_BURST
    main_damage_element = ElementType.DENDRO
    main_damage = 2
    piercing_damage = 0

    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.DENDRO
        }
    ]
    energy_cost = 2
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Cuilein_Anbar)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Cuilein_Anbar(Summon):
    name = "Cuilein Anbar"
    name_ch = "柯里安巴"
    element = ElementType.DENDRO
    removable = True
    id = 170111
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
    
    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage == 0:
                self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

class Sprout(Combat_Status):
    name_ch = "新叶"
    name = "Sprout"
    id = 170131
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.max_usage = 1
        self.current_usage = 1
        self.is_use = False
    def on_execute_dmg(self, game: 'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character):
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.reaction in [ElementalReactionType.Bloom, ElementalReactionType.Burning, ElementalReactionType.Quicken]:
                    self.is_use = True
    def after_skill(self, game:'GeniusGame'):
        if self.is_use:
            dmg = Damage.create_damage(
                game,
                SkillType.OTHER,
                main_damage_element=ElementType.DENDRO,
                main_damage=1,
                piercing_damage=0,
                damage_from=None,
                damage_to=get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_execute_dmg),
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]



class Collei(Character):
    id: int = 1701
    name: str = "Collei"
    name_ch = "柯莱"
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.SUMERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Supplicants_Bowmanship, Floral_Brush, TrumpCard_Kitty]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]


