from genius_invocation.card.character.import_head import *

class Card_Force_Translocation(NormalAttack):
    id: int = 13101
    name="Card Force Translocation"
    name_ch = "迫牌易位式"
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

class Prop_Arrow(NormalAttack):
    id: int = 13102
    name="Prop Arrow"
    name_ch = "隐具魔术箭"
    type: SkillType = SkillType.NORMAL_ATTACK

    # No damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
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

        self.resolve_damage(game)
        # 召唤物/状态生成
        self.generate_summon(game, GrinMalkin_Hat)
        self.add_status(game, Prop_Surplus)
        if self.from_character.health_point >= 6:
            game.add_damage(Damage.create_damage(game, self.damage_type, ElementType.PIERCING,
                              1,
                              0,
                              self.from_character, self.from_character,
                              ))
            game.resolve_damage()
            game.manager.invoke(EventType.AFTER_USE_SKILL, game)
        self.gain_energy(game)

class GrinMalkin_Hat(Summon):
    id: int = 13105
    name="GrinMalkin Hat"
    name_ch = "怪笑猫猫帽"
    element: ElementType = ElementType.PYRO
    removable: bool = True

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
            '''
                Entity在被移除时, 调用on_destroy移除监听并执行对应的移除操作(在对应区域中移除此entity等)
            '''
            self.on_destroy(game)
    def update(self):
        self.current_usage = min(self.usage, self.current_usage + 1)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 1

class Prop_Surplus(Status):
    name = "Prop Surplus"
    name_ch = "隐具余数"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.usage = 3
    
    def update(self):
        self.current_usage = min(self.usage, self.current_usage + 1)
    

class Bewildering_Lights(ElementalSkill):
    id: int = 13103
    name="Bewildering Lights"
    name_ch = "眩惑光戏法"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
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
        stacks = 0
        status = self.from_character.has_status(Prop_Surplus)
        if status is not None:
            stacks = status.current_usage
            status.on_destroy(game)
    
        self.resolve_damage(game, add_main_damage=stacks)
        if stacks > 0:
            self.from_character.heal(stacks, game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Wondrous_Trick_Miracle_Parade(ElementalBurst):
    id: int = 13104
    name = "Wondrous Trick: Miracle Parade"
    name_ch = "大魔术·灵迹巡游"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.PYRO
        }
    ]
    energy_cost=2
    energy_gain=0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, GrinMalkin_Hat)
        self.add_status(game, Prop_Surplus)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class Lyney(Character):
    id = 1310
    name = "Lyney"
    name_ch = "林尼"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.FONTAINE
    country_list: List[CountryType] = [CountryType.FONTAINE, CountryType.FATUI]

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Card_Force_Translocation, Prop_Arrow, Bewildering_Lights, Wondrous_Trick_Miracle_Parade]

    max_power = 2
    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
        self.talent_round = -1
        if self.talent:
            self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.dmg_add)

    def refresh_talent(self, game:'GeniusGame'):
        self.talent_round = -1

    def dmg_add(self, game: 'GeniusGame'):
        if self.talent_round == game.round:
            return
        if ElementType.PYRO in game.current_damage.damage_to.elemental_application:
            if game.current_damage.damage_from == self or \
                    isinstance(game.current_damage.damage_from, GrinMalkin_Hat) and game.current_damage.damage_from.from_character == self:
                game.current_damage.main_damage += 2
                self.talent_round = game.round
    


    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
