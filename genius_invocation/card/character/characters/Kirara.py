from genius_invocation.card.character.import_head import *

class Boxcutter(NormalAttack):
    id: int = 17071
    name = "Boxcutter"
    name_ch = "箱纸切削术"
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

class MeowteorKick(ElementalSkill):
    id: int = 17072
    name = "Meowteor Kick"
    name_ch = "呜喵町飞足"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 0
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

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 不造成伤害

        # 召唤物/状态生成
        self.add_combat_status(game, UrgentNekoParcel)
        self.add_combat_shield(game, ShieldofSafeTransport)
        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ShieldofSafeTransport(Combat_Shield):
    name = "Shield of Safe Transport"
    name_ch = "安全运输护盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)


class UrgentNekoParcel(Combat_Status):
    name = "Urgent Neko Parcel"
    name_ch = "猫箱急件"
    max_usage = 2
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def update(self):
        self.current_usage = min(self.current_usage+1, self.max_usage)


    def on_switch(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            if game.current_switch['from'] == self.from_character:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.SUMMON,
                    main_damage_element=ElementType.DENDRO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()

                self.from_player.get_card(num=1)

                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.ACTIVE_ZONE, self.on_switch),
        ]

class SecretArtSurpriseDispatch(ElementalBurst):
    id: int = 17073
    name = "Secret Art: Surprise Dispatch"
    name_ch = "秘法·惊喜特派"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.CRYO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        # 处理伤害
        self.resolve_damage(game)
        # 召唤物/状态生成
        target_zone = get_opponent(game).team_combat_status
        target_zone.add_entity(CatGrassCardamom(game, from_player=get_opponent(game), from_character=None))

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class CatGrassCardamom(Combat_Status):
    name = "Cat Grass Cardamom"
    name_ch = "猫草豆蔻"
    max_usage = 2
    max_count = 2
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.max_usage
        self.count = 0

    def update(self):
        self.current_usage = self.max_usage
        self.count = 0

    def on_after_play_card(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            self.count += 1
            if self.count >= self.max_count:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.SUMMON,
                    main_damage_element=ElementType.DENDRO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_my_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()
                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)


    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_after_play_card),
        ]



class Kirara(Character):
    id: int = 1707
    name: str = 'Kirara'
    name_ch = "绮良良"
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Boxcutter, MeowteorKick, SecretArtSurpriseDispatch]

    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]

        self.save_switch_dice_round = -1
        if self.talent:
            self.listen_talent_events(game)

    def on_switch(self, game:'GeniusGame'):
        if self.calculation_dice(game):
            self.save_switch_dice_round = game.round

    def calculation_dice(self, game:'GeniusGame'):
        if not self.talent: return False
        if self.save_switch_dice_round == game.round: return False
        if game.active_player!=self.from_player: return False
        if game.current_dice.use_type == SwitchType.CHANGE_CHARACTER:
            if game.current_dice.from_character == self:
                if game.current_dice.cost[0]['cost_num']>0:
                    game.current_dice.cost[0]['cost_num']-=1
                    return True

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.calculation_dice)
        self.listen_event(game, EventType.ON_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.on_switch)
