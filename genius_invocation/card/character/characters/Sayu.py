from genius_invocation.card.character.import_head import *


class Shuumatsuban_Ninja_Blade(NormalAttack):
    name = "Shuumatsuban Ninja Blade"
    name_ch = "忍刀·终末番"
    id = 15071
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

class Yoohoo_Art_Fuuin_Dash(ElementalSkill):
    name = "Yoohoo Art: Fuuin Dash"
    name_ch = "呜呼流·风隐急进"
    id = 15072
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 1
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

        self.resolve_damage(game)
        self.gain_energy(game)
        Next_Skill = self.from_character.next_skill
        prepare_status = Prepare_Fuufuu_Whirlwind_Kick(game, self.from_character.from_player, self.from_character, Next_Skill)
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Fuufuu_Whirlwind_Kick(ElementalSkill):
    name = "Fuufuu Whirlwind Kick"
    name_ch = "风风轮舞踢"
    id = 15074
    type = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL

    main_damage: int = 2
    piercing_damage: int = 0
    is_prepared_skill = True

    cost =[]
    energy_cost = 0
    energy_gain = 0
    def __init__(self, from_character: 'Character') -> None:
        super().on_call(from_character)
        self.main_damage_element = ElementType.ANEMO
        
        
    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.main_damage_element = self.from_character.last_swirl if self.from_character.last_swirl is not None else ElementType.ANEMO
        self.resolve_damage(game)
        # game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.from_character.from_player.prepared_skill = None


class Prepare_Fuufuu_Whirlwind_Kick(Status):
    name = "Prepare Prepare_Fuufuu_Whirlwind_Kick"
    name_ch = "准备技能: 风风轮舞踢"
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


class Yoohoo_Art_Mujina_Flurry(ElementalBurst):
    name = "Yoohoo Art: Mujina Flurry"
    name_ch = "呜呼流·影貉缭乱"
    id = 15073
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

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)
        
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        self.consume_energy(game)
        self.generate_summon(game, Muji_Muji_Daruma)
        self.resolve_damage(game)
        
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Muji_Muji_Daruma(Summon):
    name: str = "Muji-Muji Daruma"
    name_ch = "不倒貉貉"
    removable = True
    element = ElementType.ANEMO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
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

            max_idx = -1
            max_damage = -1
            characters = [get_my_active_character(game)] + get_my_standby_character(game)
            for idx, char in enumerate(characters):
                if char.is_alive and char.max_health_point - char.health_point > max_damage:
                    max_idx = idx
            target = self.from_player.character_list[max_idx]
            target.heal(heal=2, game=game)
            
            self.current_usage -= 1
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class Sayu(Character):
    id: int = 1507
    name: str = "Sayu"
    name_ch = "早柚"
    time = 4.4
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Shuumatsuban_Ninja_Blade, Yoohoo_Art_Fuuin_Dash, Yoohoo_Art_Mujina_Flurry]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        self.next_skill = Fuufuu_Whirlwind_Kick(self)
        self.last_swirl = None
        self.talent_round = -1
    
    def on_excute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self:
            if game.current_damage.reaction == ElementalReactionType.Swirl:
                self.last_swirl = game.current_damage.swirl_crystallize_type
            else:
                self.last_swirl = None
        
        if game.current_damage.damage_from.from_player == self.from_player:
            if self.is_active and self.talent and self.talent_round != game.round:
                self.from_player.get_card(2)
                self.talent_round = game.round
    def update_listener_list(self):
        super().update_listener_list()
        self.listeners += [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_excute_dmg)
        ]
