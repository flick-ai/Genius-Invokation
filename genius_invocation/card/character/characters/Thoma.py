from genius_invocation.card.character.import_head import *


class Swiftshatter_Spear(NormalAttack):
    id: int = 13111
    name = "Swiftshatter Spear"
    name_ch = "迅破枪势"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.PYRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Blazing_Blessing(ElementalSkill):
    id: int = 13112
    name = "Blazing Blessing"
    name_ch = "烈烧佑命之侍护"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.add_combat_shield(game, Blazing_Barrier)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Blazing_Barrier(Combat_Shield):
    name = "Blazing Barrier"
    name_ch = "烈烧佑命护盾" 
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = 1

    def update(self):
        self.current_usage = min(self.current_usage + 1, self.usage)



class Crimson_Ooyoroi(ElementalBurst):
    id: int = 13113
    name = "Crimson Ooyoroi"
    name_ch = "真红炽火之大铠"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_shield(game, Blazing_Barrier)
        self.add_combat_status(game, Scorching_Ooyoroi)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Scorching_Ooyoroi(Combat_Status):
    name = "Scorching Ooyoroi"
    name_ch = "炽火大铠"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        if self.from_character.talent:
            self.usage = 3
        else:
            self.usage = 2
        self.current_usage = self.usage

    def update(self):
        if self.from_character.talent:
            self.usage = 3
        self.current_usage = max(self.current_usage, self.usage)

    def after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.PYRO,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()
                
                shield = self.from_player.team_combat_status.has_shield(Blazing_Barrier)
                if shield is not None:
                    shield.update()
                else:
                    shield = Blazing_Barrier(game, from_player=self.from_player, from_character=self.from_character)
                    self.from_player.team_combat_status.add_entity(shield)

                self.current_usage -= 1
                if self.current_usage <=0 :
                    self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.after_skill)
        ]


class Thoma(Character):
    id: int = 1311
    name: str = "Thoma"
    name_ch = "托马"
    time = 4.4
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Swiftshatter_Spear, Blazing_Blessing, Crimson_Ooyoroi]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[2]
