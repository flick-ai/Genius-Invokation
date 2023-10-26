from genius_invocation.card.character.import_head import *

class RainofStone(NormalAttack):
    id: int = 16031
    name: str = "Rain of Stone"
    name_ch = "岩雨"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.GEO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class DominusLapidis(ElementalSkill):
    id: int = 16032
    name: str = "Dominus Lapidis"
    name_ch = "地心"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.generate_summon(game, StoneStele)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class DominusLapidisStrikong(ElementalSkill):
    id: int = 16033
    name: str = "Dominus Lapidis: Striking Stone"
    name_ch = "地心·磐礴"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':5, 'cost_type':CostType.GEO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.generate_summon(game, StoneStele)
        self.add_combat_shield(game, JadeShield)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class  StoneStele(Summon):
    name = " Stone Stele"
    name_ch = "岩脊"
    removable = True
    element = ElementType.GEO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            damage = 1

            if self.from_character.talent:
                if self.from_player.team_combat_status.has_shield(Combat_Shield) or self.from_character.character_zone.has_entity(Shield):
                    damage += 1

            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=damage,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]



class JadeShield(Combat_Shield):
    name = "Jade Shield"
    name_ch = "玉璋护盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2

    def update(self):
        self.current_usage = 2


class PlanetBefall(ElementalBurst):
    id: int = 16034
    name: str = "Planet Befall"
    name_ch = "天星"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 4
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.GEO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)

        target = get_opponent_active_character(game)
        target_zone = get_opponent_active_character(game).character_zone
        state = target_zone.has_status(Petrification)
        if state != None:
            state.update()
        else:
            target_zone.add_entity(Petrification(game, from_player=get_opponent(game), from_character=target))

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Petrification(Status):
    name = 'Petrification'
    name_ch = "石化"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.max_usage = 1
        self.current_usage = 1
        self.from_character.is_frozen = True

    def update(self):
        self.current_usage = self.usage

    def on_destroy(self, game):
        super().on_destroy(game)
        self.from_character.is_frozen = False

    def on_begin_phase(self, game: 'GeniusGame'):
        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin_phase),
        ]

class Zhongli(Character):
    id: int = 1603
    name: str = "Zhongli"
    name_ch = "钟离"
    element: ElementType = ElementType.GEO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [RainofStone, DominusLapidis, DominusLapidisStrikong, PlanetBefall]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]
