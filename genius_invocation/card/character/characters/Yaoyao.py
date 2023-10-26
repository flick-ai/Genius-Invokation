from genius_invocation.card.character.import_head import *

class TurnSpear(NormalAttack):
    id: int = 17041
    name: str = "Toss 'N' Turn Spear"
    name_ch = "颠扑连环枪"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.DENDRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class RaphanusSkyCluster(ElementalSkill):
    id: int = 17042
    name: str = "Raphanus Sky Cluster"
    name_ch = "云台团团降芦菔"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.generate_summon(game, Yuegui)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Yuegui(Summon):
    name: str = "Yuegui: Throwing Mode"
    name_ch = "月桂·抛掷型"
    removable = True
    element = ElementType.DENDRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            damage = 1
            heal = 1
            if self.from_character.talent and self.current_usage == 1:
                damage += 1
                heal == 1

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

            max_idx = -1
            max_damage = -1
            characters = [get_my_active_character(game)] + get_my_standby_character(game)
            for idx, char in characters:
                if char.max_health_point - char.health_point > max_damage:
                    max_idx = idx
            target = self.from_player.character_list[max_idx]
            target.heal(heal=heal, game=game)
            
            self.current_usage -= 1
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]


class MoonjadeDescent(ElementalBurst):
    id: int = 17043
    name: str = "Moonjade Descent"
    name_ch = "玉颗珊珊月中落"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.DENDRO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game,AdeptalLegacy )
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

    
class AdeptalLegacy(Combat_Status):
    name = "Adeptal Legacy"
    name_ch = "桂子仙机"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_swich(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            damage = 1
            heal = 1

            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.DENDRO,
                main_damage=damage,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()

            target = get_my_active_character(game)
            target.heal(heal=heal, game=game)
            
            self.current_usage -= 1
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.SUMMON_ZONE, self.on_swich),
        ]



class Yaoyao(Character):
    id: int = 1704
    name: str = "Yaoyao"
    name_ch = "瑶瑶"
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [TurnSpear, RaphanusSkyCluster, MoonjadeDescent]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
