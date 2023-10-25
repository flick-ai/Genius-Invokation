from genius_invocation.card.character.import_head import *


class Origin(NormalAttack):
    name = 'Origin'
    name_ch = '源流'
    id: int = 0
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
            'cost_type': CostType.ELECTRO
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

class Transcendence_Baleful_Omen(ElementalSkill):
    id = 1
    name = "Transcendence: Baleful Omen"
    name_ch = "神变·恶曜开眼"
    type = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type = SkillType.ELEMENTAL_SKILL
    main_damage_element = ElementType.ELECTRO
    main_damage = 0
    piercing_damage = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        },
    ]
    energy_cost = 0
    energy_gain = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 召唤杀生樱
        self.generate_summon(game, Eye_of_Stormy_Judgement)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Secret_Art_Musou_Shinsetsu(ElementalBurst):
    id = 2
    name="Secret Art: Musou Shinsetsu"
    name_ch = "奥义·梦想真说"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 4,
            'cost_type': CostType.ELECTRO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        status = self.from_character.character_zone.has_entity(Chakra_Desiderata)
        assert status is not None
        self.consume_energy(game)
        if self.from_character.talent:
            self.resolve_damage(game, add_main_damage=status.current_usage *2)
        else:
            self.resolve_damage(game, status.current_usage)
        status.current_usage = 0
        for char in get_my_standby_character(game):
            char.power += 2
            if char.power > char.max_power:
                char.power = char.max_power
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Raiden_Shogun(Character):
    id: int = 1407
    name: str = "Raiden Shogun"
    name_ch = "雷电将军"
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = []
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        assert self.character_zone.has_entity(Chakra_Desiderata) is None
        status = Chakra_Desiderata(game, self.from_player, self)
        self.character_zone.add_entity(status)
    
    def revive(self, game:'GeniusGame'):
        super().revive(game)
        self.init_state(game)


    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]

class Eye_of_Stormy_Judgement(Summon):
    name = "Eye of Stormy Judgement"
    name_ch = "雷罚恶曜之眼"
    removable = True
    element = ElementType.ELECTRO
    usage = 3
    max_usage = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage) 
    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if(self.current_usage <= 0):
            self.on_destroy(game)

    def on_dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_type == SkillType.ELEMENTAL_BURST:
            if game.current_damage.damage_to.from_player == self.from_player:
                game.current_damage.main_damage += 1
                # TODO: Check Dehya's Elemental Burst, Here assume that will gain 1 additional damage per attack.
    


    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
            (EventType.DAMAGE_ADD, ZoneType.SUMMON_ZONE, self.on_dmg_add)
        ]

class Chakra_Desiderata(Status):
    name = "Chakra Desiderata"
    name_ch = "诸愿百眼之轮"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 0
        self.usage = 3
    
    def after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.type == SkillType.ELEMENTAL_BURST:
                if game.current_skill.from_character != self.from_character:
                    if game.current_skill.is_prepared_skill == False:
                        self.current_usage += 1
                        if self.current_usage > self.usage:
                            self.current_usage = self.usage
                        # TODO: Check Dehya!
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill)
        ]