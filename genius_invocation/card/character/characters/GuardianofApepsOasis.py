from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.base import ActionCard

class StrikeoftheDispossessed(NormalAttack):
    name = 'Strike of the Dispossessed'
    name_ch = "失乡重击"
    id: int = 270201
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 1,'cost_type': CostType.DENDRO},{'cost_num': 2,'cost_type': CostType.BLACK}]
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

class LifeStream(ElementalSkill):
    id = 270202
    name = 'Life Stream'
    name_ch = "生命流束"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 3,'cost_type': CostType.DENDRO},]
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

        self.from_character.from_player.card_zone.find_card_by_name(
            AwakenMyKindred.name, num=1, 
        )
        self.add_combat_status(game, OasisNourishment, usage=1)

        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class TheEndFalls(ElementalBurst):
    id = 270203
    name = 'The End Falls'
    name_ch = "终景迸落"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 3, 'cost_type': CostType.DENDRO}]

    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        self.from_character.from_player.card_zone.find_card_by_name(
            AwakenMyKindred.name, num=1, 
        )
        self.add_combat_status(game, OasisNourishment, usage=2)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class GuardianofApepsOasis(Character):
    id = 2702
    name = "Guardian of Apep's Oasis"
    name_ch = "阿佩普的绿洲守望者"
    time = 4.7
    element = ElementType.DENDRO
    weapon_type = WeaponType.OTHER
    country = CountryType.MONSTER

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        StrikeoftheDispossessed,
        LifeStream,
        TheEndFalls
    ]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]

        self.proliferated_organism = 0
        self.listen_event(game, EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.after_any_action)
    
    def init_state(self, game: 'GeniusGame'):
        self.from_player.card_zone.insert_randomly(
            [AwakenMyKindred() for i in range(6)], num=-1
        )

    def after_any_action(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.proliferated_organism == 4:
                self.from_character.character_zone.add_entity(
                    ReignitedHeartofOasis(game, self.from_player, self)
                )
                self.from_character.character_zone.add_entity(
                    ThisShield(game, self.from_player, self)
                )
    
    def on_play_talent(self, game: 'GeniusGame'):
        self.from_player.card_zone.insert_randomly(
            [AwakenMyKindred() for i in range(4)], num=-1
        )
        


class ReignitedHeartofOasis(Status):
    name = 'Reignited Heart of Oasis'
    name_ch = "重燃的绿洲之心"
    id = 270221
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self:
            if game.current_damage.main_damage_element != ElementType.PIERCING:
                game.current_damage.main_damage += 3

    def after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self:
            status = self.from_player.team_combat_status.has_status(OasisNourishment)
            if status is not None:
                layer = status.current_usage
                status.on_destroy(game)
                self.from_character.heal(heal=layer, game=game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill)
        ]

class OasisNourishment(Combat_Status):
    name = 'Oasis Nourishment'
    name_ch = "绿洲之滋养"
    max_usage = 3
    id = 270231
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None, usage=1):
        super().__init__(game, from_player, from_character)
        self.current_usage = usage

    def update(self, usage=1):
        self.current_usage = min(self.max_usage, self.current_usage + usage)

    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in ActionCardType:
                if game.current_dice.name == AwakenMyKindred.name:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[1]['cost_num'] - 1)
                    return True
        return False
    
    def on_play_card(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.current_usage -= 1
            if self.current_usage == 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
            (EventType.ON_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.on_play_card),
        ]

class ProliferatedOrganism(Summon):
    name = "Proliferated Organism"
    name_ch = "增殖生命体"
    removable = True
    element = ElementType.DENDRO
    id = 270211

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        if self.from_character != None:
            self.from_character.roliferated_organism += 1
        self.current_usage = 1
        

    def end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            damage = 1
            if self.from_character.talent:
                damage += 1
            
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage=damage,
                main_damage_element=self.element,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.end_phase)
        ]

class AwakenMyKindred(ActionCard):
    name = "Awaken, My Kindred"
    name_ch = "唤醒眷属"
    cost_num = 2
    id = 270271
    cost_type = CostType.DENDRO
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()

    def get_from_character(self, game: 'GeniusGame') -> 'Character':
        for character in game.active_player.character_list:
            if character.name == GuardianofApepsOasis.name:
                return character
        return None

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.summon_zone.add_entity(
            ProliferatedOrganism(game, game.active_player, self.get_from_character(game)),
            independent=True,
        )

    def on_discard(self, game: 'GeniusGame'):
        game.active_player.summon_zone.add_entity(
            ProliferatedOrganism(game, game.active_player, self.get_from_character(game)),
            independent=True,
        )

    def find_target(self, game: 'GeniusGame'):
        return [1]
    
class ThisShield(Shield):
    name = "Shield When Reignited"
    name_ch = "重燃之盾"
    id = 270241
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2