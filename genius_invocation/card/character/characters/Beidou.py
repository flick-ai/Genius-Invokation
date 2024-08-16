from genius_invocation.card.character.import_head import *


class Oceanborne(NormalAttack):
    id: int = 140501
    name = "Oceanborne"
    name_ch = "征涛"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num': 1,'cost_type': CostType.ELECTRO},{'cost_num': 2,'cost_type': CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Tidecaller(ElementalSkill):
    id = 140502
    type: SkillType = SkillType.ELEMENTAL_SKILL
    name = "Tidecaller"
    name_ch = "捉浪"
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num': 3,'cost_type': CostType.ELECTRO}]
    energy_cost=0
    energy_gain=1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.gain_energy(game)
        Next_Skill = self.from_character.next_skill
        prepare_status = TidecallerSurfEmbrace(game, self.from_character.from_player, self.from_character, Next_Skill)
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Wavestrider(ElementalSkill):
    name = 'Wavestrider'
    name_ch = '踏潮'
    id = 140504
    type = SkillType.ELEMENTAL_SKILL
    damage_type= SkillType.ELEMENTAL_SKILL
    main_damage_element = ElementType.ELECTRO
    main_damage = 3
    piercing_damage = 0
    is_prepared_skill = True
    cost =[]
    energy_cost = 0
    energy_gain = 0
    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        # game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.from_character.from_player.prepared_skill = None

class ShieldTidecallerSurfEmbrace(Shield):
    name = "Shield of  Tidecaller: Surf Embrace"
    name_ch = "捉浪·涛拥之守的盾"
    id = 140541
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', from_prepare_status: 'Status'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.from_prepare_status = from_prepare_status

class TidecallerSurfEmbrace(Status):
    name = "Tidecaller: Surf Embrace"
    name_ch = "捉浪·涛拥之守"
    id = 140521
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', Next_Skill: 'CharacterSkill'):
        assert self.from_character.character_zone.has_entity(ShieldTidecallerSurfEmbrace) is None
        shield = ShieldTidecallerSurfEmbrace(game, from_player, from_character, self)
        self.from_character.character_zone.add_entity(shield) # add shield before the status

        super().__init__(game, from_player, from_character)
        self.skill = Next_Skill
        

    def on_call(self, game: 'GeniusGame'):
        self.skill.on_call(game)
        self.on_destroy(game)

    def after_change(self,game:'GeniusGame'):
        if game.current_switch["from"] == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]
    
    def on_destroy(self, game: 'GeniusGame'):
        shield = self.from_character.character_zone.has_entity(ShieldTidecallerSurfEmbrace)
        if shield is not None:
            shield.on_destroy(game)
        super().on_destroy(game)

class Stormbreaker(ElementalBurst):
    name = "Stormbreaker"
    name_ch = "斫雷"
    id = 140503
    type = SkillType.ELEMENTAL_BURST
    damage_type= SkillType.ELEMENTAL_SKILL
    main_damage_element = ElementType.ELECTRO
    main_damage = 2
    piercing_damage = 0
    cost =[{'cost_num': 3,'cost_type': CostType.HYDRO}]
    energy_cost = 3
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, ThunderbeastsTarge)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ThunderbeastsTarge(Combat_Status):
    name = "Thunderbeast's Targe"
    name_ch =  "雷兽之盾"
    id = 140531
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage
    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_execute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_to.from_player == self.from_player:
            if game.current_damage.damage_to.is_active:
                if game.current_damage.main_damage_element != ElementType.PIERCING:
                    if game.current_damage.main_damage >= 3:
                        game.current_damage.main_damage -= 1
    def after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.ELECTRO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_execute_dmg),
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin),
        ]

class Beidou(Character):
    id: int = 1405
    name: str = "Beidou"
    name_ch = "北斗"
    time = 3.4
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Oceanborne, Tidecaller, Stormbreaker]
    max_power: int = 3
    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
        self.next_skill = Wavestrider(self)
        self.last_talent_round = -1
        # self.execute_dmg = 0

    # def on_begin(self, game: 'GeniusGame'):
    #     super().on_begin(game)
    #     self.execute_dmg = 0

    def on_calculate(self, game: 'GeniusGame'):
        # 4.2更新
        if self.last_talent_round != game.round:
            if game.active_player == self.from_player:
                if game.current_dice.use_type is SkillType.NORMAL_ATTACK:
                    if game.current_dice.from_character == self:  #Beidou will use normal attack
                        if game.current_dice[1]['cost_num'] >0:
                            game.current_dice[1]['cost_num'] -= 1
                            return True
        return False

    def on_skill(self, game: "GeniusGame"):
        if self.on_calculate(game):
            self.last_talent_round = game.round

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate)
        self.listen_event(game, EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.8] = "调整了「七圣召唤」中，角色牌「北斗」元素战技伤害，元素爆发所需元素骰和伤害：元素战技的踏潮，造成2点雷元素伤害调整为造成3点雷元素伤害；元素爆发所需元素骰由4个雷元素骰调整为3个雷元素骰，造成3点雷元素伤害调整为造成2点雷元素伤害"
        return log