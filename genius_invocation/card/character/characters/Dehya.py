from genius_invocation.card.character.characters.import_head import *

class Sandstorm_Assault(NormalAttack):
    id: int = 0
    name="Sandstorm Assault"
    name_ch = "拂金剑斗术"
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
            'cost_type': CostType.PYRO
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


class Molten_Inferno(ElementalSkill):
    id: int = 1
    name="Monlten Inferno"
    name_ch = "熔铁流狱"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.PYRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 不造成伤害
        if self.from_character.from_player.summon_zone.has_entity(Fiery_Sanctum_Field):
            self.resolve_damage(game)

        # 召唤物/状态生成
        self.generate_summon(game, Fiery_Sanctum_Field)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Leonine_Bite(ElementalBurst):
    id: int = 2
    name = "Leonine Bite"
    name_ch = "炎啸狮子咬"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 4,
            'cost_type': CostType.HYDRO
        }
    ]
    energy_cost=2
    energy_gain=0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.gain_energy(game)
        Next_Skill = self.from_character.next_skill
        prepare_status = Prepare_Incineration_Drive(game, self.from_character.from_player, self.from_character, Next_Skill)
        assert self.from_character.character_zone.has_entity(Prepare_Incineration_Drive) is None
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Incineration_Drive(ElementalBurst):
    name = "Incineration Drive"
    name_ch = "焚落踢"
    id = 3
    type = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    is_prepared_skill = True

    cost =[]
    energy_cost = 0
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.from_character.from_player.prepared_skill = None



class Fiery_Sanctum_Field(Summon):
    name = "Fiery Sanctum Field"
    name_ch = "净焰剑狱领域"
    id = 0
    element = ElementType.PYRO
    usage = 3
    max_usage = 3
    removable = True

    def on_end_phase(self, game:'GeniusGame'):
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
            if self.current_usage <=0:
                self.on_destroy(game)
    
    def update(self):
        self.current_usage = max(self.current_usage, self.usage)
        self.last_round = -1

    def on_execute_dmg(self, game:"GeniusGame"):
        if self.from_character.is_active: return
        if not self.from_character.is_active: return
        if self.last_round == game.round: return
        if game.current_damage.damage_to != self.from_player: return
        if game.current_damage.main_damage <= 0: return
        if game.current_damage.main_damage_element == ElementType.PIERCING: return
        self.last_round = game.round
        game.current_damage.main_damage -= 1
        if self.from_character.health_point >=7:
            dmg = Damage.create_damage(
                game,
                SkillType.OTHER,
                ElementType.PIERCING,
                1,
                0,
                game.current_damage.damage_from,
                self.from_character
            )
            game.add_damage(dmg)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg)
        ]

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.usage
        self.last_round = -1
class Dehya(Character):
    id = 1309
    name = "Dehya"
    name_ch = "迪希雅"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.SUMERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Sandstorm_Assault, Molten_Inferno, Leonine_Bite]

    max_power = 2
    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.next_skill = Incineration_Drive(self)
        self.talent_skill = self.skills[1]
        if self.talent:
            self.listen_event(game, EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)

    def on_end_phase(self, game:'GeniusGame'):
        if self.talent:
            if game.active_player == self.from_player:
                if self.health_point <=6:
                    self.heal(2)

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)

class Prepare_Incineration_Drive(Status):
    name = "Prepare Incineration Drive"
    name_ch = "准备技能: 焚落踢"
    def __init__(self, game:'GeniusGame', from_player:'GeniusPlayer', from_character:'Character', next_skill: 'CharacterSkill'):
        super().__init__(game, from_player, from_character)
        self.next_skill = next_skill
        self.current_usage = 1

    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.next_skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]
