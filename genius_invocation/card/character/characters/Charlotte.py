from genius_invocation.card.character.import_head import *

class Cool_Color_Capture(NormalAttack):
    name = 'Cool-Color Capture'
    name_ch = "冷色摄影律"
    id: int = 111001
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.CRYO
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
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Framing_Freezing_Point_Composition(ElementalSkill):
    id = 111002
    name = 'Framing: Freezing Point Composition'
    name_ch = "取景·冰点构图法"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def add_status(self, game: 'GeniusGame'):
        targetZone = get_opponent_active_character(game).character_zone
        status = targetZone.has_entity(Snappy_Silhouette)
        if status is None:
            status = Snappy_Silhouette(game, get_opponent(game), get_opponent_active_character(game), self.from_character.talent)
            targetZone.add_entity(status)
        else:
            status.update(self.from_character.talent)
        
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        self.add_status(game)

        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Still_Photo_Comprehensive_Confirmation(ElementalBurst):
    id = 111003
    name = 'Still Photo: Comprehensive Confirmation'
    name_ch = "定格·全方位确证"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        }
    ]

    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        for character in self.from_character.from_player.character_list:
            if character.is_alive:
                character.heal(1, game)
        self.generate_summon(game, Newsflash_Field)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
class Charlotte(Character):
    id = 1110
    name = 'Charlotte'
    name_ch = "夏洛蒂"
    time = 4.5
    element = ElementType.CRYO
    weapon_type = WeaponType.CATALYST
    country = CountryType.FONTAINE

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        Cool_Color_Capture,
        Framing_Freezing_Point_Composition,
        Still_Photo_Comprehensive_Confirmation
    ]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]

class Snappy_Silhouette(Status):
    name = 'Snappy Silhouette'
    name_ch = '瞬时剪影'
    id = 111021
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', talent = False):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.use_round = -1
        self.has_talent = talent
    
    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            addition_dmg = 0
            if ElementType.CRYO in self.from_character.elemental_application and self.current_usage == 1:
                addition_dmg = 1
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.CRYO,
                main_damage=1 + addition_dmg,
                piercing_damage=0,
                damage_from=self,
                damage_to=self.from_character
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)
    
    def after_skill(self, game: 'GeniusGame'):
        if self.has_talent:
            if game.active_player != self.from_player:
                if game.current_skill.type == SkillType.NORMAL_ATTACK and self.use_round != game.round:
                    self.use_round = game.round
                    get_my_active_character(game).heal(2, game)
    def update(self, talent = False):
        self.current_usage = self.usage
        self.use_round = -1
        self.has_talent = talent
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]


class Newsflash_Field(Summon):
    name = "Newsflash Field"
    name_ch = "临场视域"
    removable = True
    element = ElementType.CRYO
    id = 111011
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

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
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.end_phase)
        ]