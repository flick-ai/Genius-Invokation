from genius_invocation.card.character.import_head import *

class ForcefulFistsofFrost(NormalAttack):
    name = 'Forceful Fists of Frost'
    name_ch = "迅烈倾霜拳"
    id: int = 111101
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 1,'cost_type': CostType.CRYO},{'cost_num': 2,'cost_type': CostType.BLACK}]
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

class IcefangRush(ElementalSkill):
    id = 111102
    name = 'Icefang Rush'
    name_ch = "冰牙突驰"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 3,'cost_type': CostType.CRYO},]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        self.add_status(game, ChillingPenalty)

        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class DarkgoldWolfbite(ElementalBurst):
    id = 111103
    name = 'Darkgold Wolfbite'
    name_ch = "黑金狼噬"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.CRYO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 3, 'cost_type': CostType.CRYO}]

    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, LingeringIcicles)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Wriothesley(Character):
    id = 1111
    name = 'Wriothesley'
    name_ch = "莱欧斯利"
    time = 4.7
    element = ElementType.CRYO
    weapon_type = WeaponType.CATALYST
    country = CountryType.FONTAINE

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        ForcefulFistsofFrost,
        IcefangRush,
        DarkgoldWolfbite
    ]
    max_power = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[0]

        self.round_heal = 0
        self.round_damage = 0
        self.penalty = 0

        self.listen_event(game, EventType.AFTER_HEAL, ZoneType.CHARACTER_ZONE, self.on_heal)
        self.listen_event(game, EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage)
        self.listen_event(game, EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice)
        self.listen_event(game, EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill)
        if self.talent:
            self.listen_talent_events(game)

    def on_begin(self, game: 'GeniusGame'):
        super().on_begin(game)
        self.round_damage = 0
        self.round_heal = 0

    def on_heal(self, game: 'GeniusGame'):
        if game.current_heal.heal_to_character == self:
            self.round_heal += 1
            if self.talent:
                self.penalty += 1

    def on_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self:
            self.round_damage += 1
            if self.talent:
                self.penalty += 1

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.current_dice.from_character == self:
            if game.current_dice.use_type == SkillType.ELEMENTAL_BURST:
                count = self.from_character.round_damage + self.from_character.round_heal
                dice_num = min(count // 2, 2)
                if game.current_dice.cost[0]['cost_num'] > 0:
                    game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[1]['cost_num'] - dice_num)
                    return True
        return False

    def on_skill(self, game: 'GeniusGame'):
        self.on_calculate_dice(game)

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self:
                if game.current_damage.damage_type in [SkillType.NORMAL_ATTACK,
                                                       SkillType.ELEMENTAL_SKILL,
                                                       SkillType.ELEMENTAL_BURST]:
                    if self.talent and self.penalty >= 3:
                        game.current_damage.main_damage += 1
                        self.penalty -= 3

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add)



class ChillingPenalty(Status):
    name = 'Chilling Penalty'
    name_ch = "寒烈的惩裁"
    id = 111121
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character', talent = False):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.is_heal = False

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.from_character == self.from_character:
                if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                    if self.from_character.health_point >= 6:
                        if self.current_usage > 0:
                            if game.current_dice.cost[1]['cost_num'] > 0:
                                game.current_dice.cost[1]['cost_num'] = max(0, game.current_dice.cost[1]['cost_num'] - 1)
                                return True

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    game.current_damage.main_damage += 1
                    self.current_usage -= 1
                    if self.from_character.health_point >= 6:
                        damage = Damage.create_damage(
                            game=game,
                            damage_type=SkillType.OTHER,
                            main_damage_element=ElementType.PIERCING,
                            main_damage=1,
                            damage_from=self.from_character,
                            damage_to=self.from_character,
                        )
                        game.add_damage(damage)
                        game.resolve_damage()
                    else:
                        self.is_heal = True

    def on_skill(self, game: 'GeniusGame'):
        self.on_calculate_dice(game)

    def after_skill(self, game: 'GeniusGame'):
        if self.is_heal:
            self.from_character.heal(1, game)
            self.is_heal = False
        if self.current_usage == 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill)
        ]

class LingeringIcicles(Combat_Status):
    name = 'Lingering Icicles'
    name_ch = "余威冰锥"
    id = 111131
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def update(self):
        assert False # Should no update!

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage=2,
                main_damage_element=ElementType.PYRO,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEFORE_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]