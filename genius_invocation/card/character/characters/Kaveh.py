from genius_invocation.card.character.import_head import *
from genius_invocation.entity.status import Dendro_Core
from genius_invocation.entity.summon import BountifulCore
from copy import deepcopy

class SchematicSetup(NormalAttack):
    id: int = 17081
    name = "Schematic Setup"
    name_ch = "旋规设矩"
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

class ArtisticIngenuity(ElementalSkill):
    id: int = 17082
    name = "Artistic Ingenuity"
    name_ch = "画则巧施"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 2
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
        self.resolve_damage(game)
        self.add_combat_status(game, BurstScan, usage=1)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class PaintedDome(ElementalBurst):
    id: int = 17083
    name = "Painted Dome"
    name_ch = "繁绘隅穹"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.DENDRO
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
        self.add_status()
        self.add_combat_status(game, BurstScan, usage=2)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class MehraksAssistance(Status):
    name = "Mehrak's Assistance"
    name_ch = "梅赫拉克的助力"
    max_usage = 2
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.max_usage

    def on_damage_add(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_damage.damage_from == self.from_character:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    game.current_damage.main_damage += 1

    def on_infuse(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_damage.damage_from == self.from_character:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                        game.current_damage.main_damage_element == ElementType.DENDRO

    def after_skill(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_skill.from_character == self.from_character:
                if game.current_skill.type == SkillType.NORMAL_ATTACK:
                    self.from_player.team_combat_status.add_entity(
                        BurstScan(game, self.from_player, self.from_character),
                        usage=1,
                    )

    def on_end(self, game: 'GeniusGame'):
        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.on_infuse),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
        ]

class BurstScan(Combat_Status):
    name = "Burst Scan"
    name_ch = "迸发扫描"
    max_usage = 3
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: 'Character'=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.is_cost = False
        self.talent_usage_round = -1

    def update(self, usage):
        self.current_usage = min(self.max_usage, self.current_usage + usage)

    def before_action(self, game: 'GeniusGame'):
        status: Dendro_Core = self.from_player.team_combat_status.has_status(Dendro_Core)
        summon: BountifulCore = self.from_player.summon_zone.has_entity(BountifulCore)
        if status is not None:
            status.lose_one_usage(game)
        elif summon is not None:
            summon.lose_one_usage(game)
        else:
            return

        card = self.from_player.card_zone.discard_card(idx=0)
        if self.from_character.talent:
            self.from_player.hand_zone.add([deepcopy(card)])
            if card.card_type == ActionCardType.SUPPORT_LOCATION:
                self.is_cost = True


        damage = Damage.create_damage(
            game=game,
            damage_type=SkillType.OTHER,
            main_damage_element=ElementType.DENDRO,
            main_damage=card.calculate_dice(game)+1,
            piercing_damage=0,
            damage_from=self,
            damage_to=get_active_character(game, 1-self.from_player.index)
        )
        game.add_damage(damage)
        game.resolve_damage()

        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def on_calculate_dice(self, game: 'GeniusGame'):
        if self.is_cost:
            if self.talent_usage_round != game.round:
                if game.active_player_index == self.from_player.index:
                    if game.current_dice.use_type == ActionCardType.SUPPORT_LOCATION:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                                game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num']-2)
                                return True
        return False

    def on_play_card(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.is_cost = False
            self.talent_usage_round = game.round

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEFORE_ANY_ACTION, ZoneType.ACTIVE_ZONE, self.before_action)
        ]
        if self.from_character.talent:
            self.listeners.append(
                (EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, self.on_calculate_dice),
                (EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, self.on_play_card),
            )



class Kaveh(Character):
    id: int = 1708
    name: str = 'Kaveh'
    name_ch = "卡维"
    time = 4.7
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.SUMERU
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [SchematicSetup, ArtisticIngenuity, PaintedDome]

    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]

    def listen_talent_events(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status(BurstScan)
        if status is not None:
            status.listen_event(game, EventType.CALCULATE_DICE, ZoneType.ACTIVE_ZONE, status.on_calculate_dice)
            status.listen_event(game, EventType.ON_PLAY_CARD, ZoneType.ACTIVE_ZONE, status.on_play_card)
