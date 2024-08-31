from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.equipment.specialskill import SpecialSkillCard
from genius_invocation.entity.status import Frozen_Status, SpecialSkill

class ScorpionBlessing(Combat_Status):
    name = "Scorpion Blessing"
    name_ch = "魔蝎祝福"
    id = 230331
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1

    def update(self, usage:int = 1):
        self.usage += usage

    def on_add_damage(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.name == "Viny Razorscale":
                game.current_damage.main_damage += 1
                self.usage -= 1
                if self.usage <= 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_add_damage),
        ]

class BurningAssault(SpecialSkill):
    name: str = "Burning Assault"
    name_ch = "炙烧攻势"
    id = "2303s1"
    cost = [{'cost_num': 2,'cost_type': CostType.WHITE}]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_call(self, game: 'GeniusGame'):
        damage = Damage(damage_type=None,
                        main_damage_element=ElementType.PYRO,
                        main_damage=2,
                        piercing_damage=0,
                        damage_from=self,
                        damage_to=get_opponent_active_character(game))
        game.add_damage(damage)
        game.resolve_damage()
        self.check_usage(game)
        game.manager.invoke(EventType.AFTER_USE_SPECIAL, game)

class SpiritofOmenPyroScorpion(SpecialSkillCard):
    id: int = 230371
    name: str = "Spirit of Omen: Pyro Scorpion"
    name_ch = "厄灵·炎之魔蝎"
    time: float = 5.1
    cost_num: int = 0
    cost_type: CostType = None
    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = BurningAssault

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

class SearingGlare(NormalAttack):
    name = "Searing Glare"
    name_ch = "烧蚀之光"
    id = 230301
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.PYRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class BlazingStrike(ElementalSkill):
    name = "Blazing Strike"
    name_ch = "炎晶迸击"
    id = 230302
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        self.add_combat_status(game, ScorpionBlessing, usage=1)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SpiritofOmensAwakeningPyroScorpion(ElementalBurst):
    name = "Spirit of Omen's Awakening: Pyro Scorpion"
    name_ch = "厄灵苏醒·炎之魔蝎"
    id = 230303
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        if not self.from_character.has_brust:
            self.from_character.has_brust = True
            self.from_character.from_player.hand_zone.add([SpiritofOmenPyroScorpion()])
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class SpiritofOmensPower(CharacterSkill):
    name = "Spirit of Omen's Power"
    name_ch = "厄灵之能"
    id = 230304
    def on_call(self, game: 'GeniusGame'):
        if self.from_character.health_point <= 7 and self.from_character.passive_round_usage > 0:
            self.from_character.passive_round_usage -= 1
            self.from_character.get_power(1)

class EremiteScorchingLoremaster(Character):
    id: int = 2303
    name: str = "Eremite Scorching Loremaster"
    name_ch = "镀金旅团·炽沙叙事人"
    time = 4.3
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.EREMITES
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [SearingGlare, BlazingStrike, SpiritofOmensAwakeningPyroScorpion]

    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        self.listen_event(game, EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.on_excute_damage)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]
        self.passive_skill = SpiritofOmensPower(self)
        self.passive_round_usage = 1
        self.has_brust = False
        self.last_skill = False

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.passive_round_usage = 1

    def on_excute_damage(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self:
            self.passive_skill.on_call(game)

    def on_die(self, game: 'GeniusGame'):
        if game.current_die.from_player != self.from_player:
            if self.last_skill:
                self.from_character.from_player.hand_zone.add([SpiritofOmenPyroScorpion()])
                self.from_player.team_combat_status.add_entity(ScorpionBlessing(game, self.from_player, self), usage=1)

    def on_use_special(self, game: 'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.name == "Burning Assault":
                self.last_skill = True

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.ON_USE_SPECIAL, ZoneType.CHARACTER_ZONE, self.on_use_special)
        self.listen_event(game, EventType.CHARACTER_DIE, ZoneType.CHARACTER_ZONE, self.on_die)


    def balance_adjustment():
        log = {}
        log[5.1] = "重做，类似叶轮舞者"
        return log



