from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.base import ActionCard

class ShatteringWaves(NormalAttack):
    name = 'Shattering Waves'
    name_ch = "碎涛旋跃"
    id: int = 220401
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 1,'cost_type': CostType.HYDRO},{'cost_num': 2,'cost_type': CostType.BLACK}]
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

class StarfallShower(ElementalSkill):
    id = 220402
    name = 'Starfall Shower'
    name_ch = "迸落星雨"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 3,'cost_type': CostType.HYDRO},]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        add_damage = min(3, self.from_character.addtional_max_health//3)
        self.resolve_damage(game, add_damage=add_damage)
        # 获得能量
        self.gain_energy(game)

        max_idx = max_count_card(self.from_character.from_player.hand_zone.card)
        if max_idx != None:
            card = self.from_character.from_player.hand_zone.discard_card(max_idx)
            if self.from_character.talent and self.from_character.talent_round != game.round:
                self.from_character.heal(card.calculate_dice(), game)
                self.from_character.talent_round = game.round
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class RavagingDevourer(ElementalBurst):
    id = 220403
    name = 'Ravaging Devourer'
    name_ch = "横噬鲸吞"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 1
    piercing_damage: int = 1

    # cost
    cost = [{'cost_num': 3, 'cost_type': CostType.HYDRO}]

    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        damage, usage = self.from_character.domain.calculate_max_cost()[1]
        self.generate_summon(game, DarkShadow, usage=usage, damage=damage)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class AllDevouringNarwhal(Character):
    id = 2204
    name = "All-Devouring Narwhal"
    name_ch = "吞星之鲸"
    time = 4.7
    element = ElementType.HYDRO
    weapon_type = WeaponType.OTHER
    country = CountryType.MONSTER

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        ShatteringWaves,
        StarfallShower,
        RavagingDevourer
    ]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.max_health_point = self.max_health_point
        self.addtional_max_health = 0
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
        self.talent_round = -1

    def init_state(self, game: 'GeniusGame'):
        self.domain = DeepDevourersDomain(game, self.from_player, self)
        self.from_player.team_combat_status.add_entity(self.domain)

    def balance_adjustment():
        log = {}
        log[4.8] = "调整了角色牌「吞星之鲸」元素战技的效果：效果“造成1点水元素伤害，此角色每有3点无尽食欲提供的额外最大生命，此伤害+1（最多+5）”中，“最多+5”调整为“最多+4”"
        log[5.0] = "战技最多+3；回合末一次性回血"
        return log



class DeepDevourersDomain(Combat_Status):
    name = "Deep Devourers Domain"
    name_ch = "深噬之域"
    id = 220431
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.cards: List['ActionCard'] = self.from_player.tune_or_discard_cards
        self.addtional_max_health = 0

    def calculate_max_cost(self):
        max_count = max([card.calculate_dice() for card in self.cards])
        max_num = 0
        for card in self.cards:
            if card.calculate_dice() == max_count:
                max_num += 1
        return max_count, max_num

    def excute(self, game: 'GeniusGame'):
        addtional_max_health = 1
        cost = [card.calculate_dice() for card in self.cards[-3:]]
        # 统计cost中相同cost的数量
        cost_dict = {}
        for c in cost:
            if c not in cost_dict:
                cost_dict[c] = 1
            else:
                cost_dict[c] += 1

        addtional_max_health = addtional_max_health + 3 - len(cost_dict)
        self.addtional_max_health += addtional_max_health

        # self.from_character.max_health_point += addtional_max_health
        # self.from_character.addtional_max_health += addtional_max_health
        # for i in range(4-len(cost_dict)):
        #     self.from_character.heal(num=1, game=game, heal_type=HealType.MAX_HEALTH)

    def on_tune(self, game: 'GeniusGame'):
        if len(self.cards)>0 and len(self.cards) % 3 == 0:
            self.excute(game)

    def on_discard(self, game: 'GeniusGame'):
        if len(self.cards) > 0 and len(self.cards) % 3 == 0:
            self.excute(game)

    def on_end(self, game: 'GeniusGame'):
        self.from_character.max_health_point += self.addtional_max_health
        self.from_character.addtional_max_health += self.addtional_max_health
        self.from_character.heal(num=self.addtional_max_health, game=game, heal_type=HealType.MAX_HEALTH)
        self.addtional_max_health = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_TUNE_CARD, ZoneType.CARD_ZONE, self.on_tune),
            (EventType.ON_DISCARD_CARD, ZoneType.CARD_ZONE, self.on_discard),
            (EventType.ON_END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end)
        ]


class DarkShadow(Summon):
    name = "Dark Shadow"
    name_ch = "黑色幻影"
    removable = True
    id = 220411
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None, usage=0, damage=0):
        super().__init__(game, from_player, from_character)
        self.current_usage = usage
        self.damage = damage

    def update(self, usage=1, damage=1):
        self.current_usage = max(self.current_usage, usage)
        self.damage = max(self.damage, damage)

    def after_any_action(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_action.choice_type == ActionChoice.PASS:
                if len(self.from_player.hand_zone.card) <= 1:
                    damage = Damage.create_damage(
                        game=game,
                        damage_type=SkillType.SUMMON,
                        main_damage_element=ElementType.ELECTRO,
                        main_damage=self.damage,
                        piercing_damage=0,
                        damage_from=self,
                        damage_to=get_active_character(game, 1-self.from_player.index)
                    )
                    game.add_damage(damage)
                    game.resolve_damage()
                    self.current_usage -= 1
                    if self.current_usage == 0:
                        self.on_destroy(game)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage=self.damage,
                main_damage_element=ElementType.ELECTRO,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def on_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self:
            if game.current_damage.main_damage_element != ElementType.PIERCING:
                if game.current_damage.main_damage > 0:
                    game.current_damage.main_damage -= 1
                    self.current_usage -= 1
                    if self.current_usage <= 0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase),
            (EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.after_any_action),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage)
        ]
