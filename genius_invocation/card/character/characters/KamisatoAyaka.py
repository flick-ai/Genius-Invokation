from genius_invocation.card.character.import_head import *

class KamisatoArt_Kabuki(NormalAttack):
    name = 'Kamisato Art: Kabuki'
    name_ch = '神里流·倾'
    id = 11051
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

class KamisatoArt_Hyouka(ElementalSkill):
    name = 'Kamisato Art: Hyouka'
    name_ch = '神里流·冰华'
    id = 11052
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 3
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
        self.heal_round = -1
    
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class KamisatoArt_Soumetsu(ElementalBurst):
    name = 'Kamisato Art: Soumetsu'
    name_ch = '神里流·霜灭'
    id = 11053
    type = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        }
    ]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Frostflake_Seki_no_To)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class Frostflake_Seki_no_To(Summon):
    name = 'Frostflake Seki no To'
    name_ch = '霜见雪关扉'
    removable = True
    element = ElementType.CRYO
    
    def on_end_phase(self, game: 'GeniusGame'):
        '''
            结束阶段: 造成2点冰元素伤害
            结束阶段分先后手两次调用on_end_phase, 所以需要判断
        '''
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=2,
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
        self.current_usage = max(self.usage, self.current_usage)

    def update_listener_list(self):
        '''
            更新需要监听的事件, 在init时会调用并自动监听
        '''
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

class KamisatoArt_Senho(CharacterSkill): # passive skill
    name = 'Kamisato Art: Senho'
    name_ch = '神里流·霰步'
    def on_call(self, game:'GeniusGame'):
        self.add_status(game, Cryo_Elemental_Infusion)

class Cryo_Elemental_Infusion(Status):
    name = 'Cryo Elemental Infusion'
    name_ch = '冰元素附魔'

    def __init__(self, game, from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1

    def update(self):
        self.current_usage = self.usage

    def infuse(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.CRYO

    def on_dmg_add(self, game: 'GeniusGame'):
        if self.from_character.talent:
            if game.current_damage.damage_from == self.from_character:
                if game.current_damage.main_damage_element == ElementType.CRYO:
                    game.current_damage.main_damage += 1

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_character.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infuse),
        ]
        if self.from_character.talent:
            self.listeners.append((EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add))

class KamisatoAyaka(Character):
    id: int = 1105
    name: str = "Kamisato Ayaka"
    name_ch = "神里绫华"
    element: ElementType = ElementType.CRYO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [KamisatoArt_Kabuki, KamisatoArt_Hyouka, KamisatoArt_Soumetsu]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.passive_skill = KamisatoArt_Senho(self)
        self.save_switch_dice_round = -1
        if self.talent:
            self.listen_talent_events(game)
        self.talent_skill = None

    def on_switched_to(self):
        super().on_switched_to()
        self.passive_skill.on_call(self.from_player.game)

    def calculation_dice(self, game:'GeniusGame'):
        if not self.talent: return False
        if self.save_switch_dice_round == game.round: return False
        if game.active_player!=self.from_player: return False
        if game.current_dice.use_type == SwitchType.CHANGE_CHARACTER:
            if game.current_dice.to_character == self:
                if game.current_dice.cost[0]['cost_num']>0:
                    game.current_dice.cost[0]['cost_num']-=1
                    return True
    
    def on_switch(self, game:'GeniusGame'):
        if self.calculation_dice(game):
            self.save_switch_dice_round = game.round
    
    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.calculation_dice)
        self.listen_event(game, EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_switch)
        status = self.character_zone.has_entity(Cryo_Elemental_Infusion)
        if status is not None:
            status.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, status.on_dmg_add)

    def equip_talent(self, game: 'GeniusGame', is_action=False):
        self.talent = True
        game.is_change_player = is_action