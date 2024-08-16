from genius_invocation.card.character.import_head import *


class Sharpshooter(NormalAttack):
    id: int = 130401
    name = "Sharpshooter"
    name_ch = "神射手"
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


class ExplosivePuppet(ElementalSkill):
    id: int = 130402
    name = "Explosive Puppet"
    name_ch = "爆弹玩偶"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = None
    main_damage: int = 0
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.generate_summon(game, BaronBunny)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class BaronBunny(Summon):
    name = 'Baron Bunny'
    name_ch = '兔兔伯爵'
    element = ElementType.PYRO
    removable = False
    id = 130411
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = self.usage
        status = ShieldfromBaron(game,self.from_player,self.from_character,self)
        self.from_player.team_combat_status.add_entity(status)

    def on_end_phase(self, game: 'GeniusGame'): 
        if game.active_player == self.from_player:
            if self.current_usage==0:    
                
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.SUMMON,
                    main_damage_element=self.element,
                    main_damage=2,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()
                self.on_destroy(game)

    def update(self, game: 'GeniusGame'):
        if self.current_usage == 0:
            self.current_usage = self.usage
            status = ShieldfromBaron(game,self.from_player,self.from_character,self)
            self.from_player.team_combat_status.add_entity(status)
        else:
            self.current_usage = max(self.current_usage,self.usage)
            self.from_player.team_combat_status.has_status(ShieldfromBaron).update()

    def add_usage(self, game: 'GeniusGame', count: int):
        self.current_usage += count
        if self.current_usage==count:
            status = ShieldfromBaron(game,self.from_player,self.from_character,self)
            self.from_player.team_combat_status.add_entity(status)
        self.from_player.team_combat_status.has_status(ShieldfromBaron).update()

    def minus_usage(self, game: 'GeniusGame', count: int):
        if self.current_usage == 0: return
        self.current_usage -= count
        self.current_usage = max(0, self.current_usage)
        if self.current_usage == 0:
            self.from_player.team_combat_status.has_status(ShieldfromBaron).on_destroy(game)

    def on_destroy(self, game: 'GeniusGame'):
        status = self.from_player.team_combat_status.has_status(ShieldfromBaron)
        if status is not None:
            status.on_destroy(game)
        super().on_destroy(game)

    def on_after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            # 4.2更新
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.SUMMON,
                    main_damage_element=self.element,
                    main_damage=4,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=get_opponent_active_character(game),
                )
                game.add_damage(dmg)
                game.resolve_damage()
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]
        if self.from_character.talent:
            self.listeners.append((EventType.AFTER_USE_SKILL, ZoneType.SUMMON_ZONE, self.on_after_skill))

class ShieldfromBaron(Combat_Status):
    name="Shield from Baron"
    name_ch = "兔之盾"
    id = 130431
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, from_summon:'Summon' = None):
        super().__init__(game, from_player, from_character)
        self.from_summon = from_summon
        self.current_usage = self.from_summon.current_usage
        self.usage = self.from_summon.usage

    def on_damage_execute(self, game:'GeniusGame'):
        if self.from_summon.current_usage <=0: return
        if game.current_damage.main_damage <=0: return
        if game.current_damage.main_damage_element==ElementType.PIERCING: return
        if game.current_damage.damage_to.from_player == self.from_player:
            if game.current_damage.damage_to.is_active:
                game.current_damage.main_damage  = max(game.current_damage.main_damage-2, 0)
                self.from_summon.current_usage -= 1
                self.current_usage = self.from_summon.current_usage
                if self.from_summon.current_usage ==0:
                    self.on_destroy(game) # Only destroy the combat_status here

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE, self.on_damage_execute)
        ]

    def update(self):
        self.current_usage = self.from_summon.current_usage



class FieryRain(ElementalBurst):
    id: int = 130403
    name = "Fiery Rain"
    name_ch = "箭雨"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
    piercing_damage: int = 2
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Amber(Character):
    id: int = 1304
    name: str = "Amber"
    name_ch = "安柏"
    time = 3.7
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Sharpshooter, ExplosivePuppet, FieryRain]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]

    def listen_talent_events(self, game: 'GeniusGame'):
        status = self.from_player.summon_zone.has_entity(BaronBunny)
        if status is not None:
            status.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.SUMMON_ZONE, status.on_after_skill)

