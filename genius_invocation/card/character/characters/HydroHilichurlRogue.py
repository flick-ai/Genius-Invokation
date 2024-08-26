from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.equipment.specialskill import SpecialSkillCard
from genius_invocation.entity.status import Frozen_Status, SpecialSkill

class MistBubblePrison(Status):
    name = 'Mist Bubble Prison'
    name_ch = "水泡围困"
    id = 220521
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.from_character.is_frozen = True

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.is_frozen = False

    def on_final_end(self, game: 'GeniusGame'):
        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_final_end),
        ]

class PrepareMistBubbleSlimeStatus(Status):
    name = "Prepare Mist Bubble Slime"
    name_ch = "准备技能: 水泡战法"
    id = 220522
    def __init__(self, game:'GeniusGame', from_player:'GeniusPlayer', from_character:'Character', next_skill: 'CharacterSkill'):
        super().__init__(game, from_player, from_character)
        self.next_skill = next_skill
        self.current_usage = 1

    def after_change(self,game:'GeniusGame'):
        if game.current_switch.from_character == self.from_character:
            self.from_character.from_player.prepared_skill = None
            self.on_destroy(game)

    def on_call(self, game: 'GeniusGame'):
        self.next_skill.on_call(game)
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)
        ]

class MistBubbleSlimeEntity(SpecialSkill):
    name: str = "Mist Bubble Slime"
    name_ch = "水泡战法"
    id = "2205s1"
    cost = [{'cost_num': 1, 'cost_type': CostType.WHITE}]
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        Next_Skill = PrepareMistBubbleSlime(game, self.from_player, self.from_character)
        prepare_status = PrepareMistBubbleSlimeStatus(game, self.from_character.from_player, self.from_character, Next_Skill)
        self.from_character.character_zone.add_entity(prepare_status)
        self.from_character.from_player.prepared_skill = prepare_status
        self.check_usage(game)
        game.manager.invoke(EventType.AFTER_USE_SPECIAL, game)

class PrepareMistBubbleSlime(SpecialSkill):
    name: str = "Mist Bubble Slime"
    name_ch = "水泡战法"
    id = "2205s2"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)

    def on_call(self, game: 'GeniusGame'):
        opponent = get_opponent_active_character(game)
        damage = Damage(damage_type=SkillType.SPECIAL_SKILL,
                        main_damage_element=ElementType.HYDRO,
                        main_damage=1,
                        piercing_damage=0,
                        damage_from=self,
                        damage_to=opponent)
        game.add_damage(damage)
        game.resolve_damage()

        opponent.character_zone.add([MistBubblePrison(game, get_opponent(game), opponent)])
        self.from_player.prepared_skill = None


class MistBubbleSlime(SpecialSkillCard):
    id: int = 220571
    name: str = "Mist Bubble Slime"
    name_ch = "水泡史莱姆"
    time: float = 5.0
    cost_num: int = 0
    cost_type: CostType = None

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = MistBubbleSlimeEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)



class WhirlingScythe(NormalAttack):
    name = 'Whirling Scythe'
    name_ch = "镰刀旋斩"
    id: int = 220501
    type: SkillType = SkillType.NORMAL_ATTACK

    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    cost = [{'cost_num': 1,'cost_type': CostType.HYDRO},{'cost_num': 2,'cost_type': CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SlashofSurgingTides(ElementalSkill):
    id = 220502
    name = 'Slash of Surging Tides'
    name_ch = "狂澜镰击"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 3
    piercing_damage: int = 0

    cost = [{'cost_num': 3,'cost_type': CostType.HYDRO},]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)

        has_status = False
        for character in get_opponent(game).character_list:
            if character.is_alive:
                if character.character_zone.has_entity(Frozen_Status):
                    has_status = True
                    break
                if character.character_zone.has_entity(MistBubblePrison):
                    has_status = True
                    break
        if has_status and game.round != self.from_character.element_skill_round:
            self.gain_energy(game)
            self.from_character.element_skill_round = game.round

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class BubblefloatBlitz(ElementalBurst):
    id = 220503
    name = 'Bubblefloat Blitz'
    name_ch = "浮泡攻势"
    type: SkillType = SkillType.ELEMENTAL_BURST

    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 3
    piercing_damage: int = 0

    cost = [{'cost_num': 3, 'cost_type': CostType.HYDRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)

        self.from_character.from_player.hand_zone.add([MistBubbleSlime()])

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class HydroHilichurlRogue(Character):
    id = 2205
    name = "Hydro Hilichurl Rogue"
    name_ch = "丘丘水行游侠"
    time = 5.0
    element = ElementType.HYDRO
    weapon_type = WeaponType.OTHER
    country = CountryType.MONSTER
    country_list: List[CountryType] = [CountryType.MONSTER, CountryType.HILICHURL]

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        WhirlingScythe,
        SlashofSurgingTides,
        BubblefloatBlitz
    ]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
        self.talent_round = -1
        self.element_skill_round = -1

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.ON_USE_SPECIAL, ZoneType.CHARACTER_ZONE, self.on_special_skill)
        self.listen_event(game, EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate)

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SkillType.SPECIAL_SKILL:
                if self.talent_round != game.round:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
                    if len(game.current_dice.cost)>1:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False

    def on_special_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.talent_round = game.round