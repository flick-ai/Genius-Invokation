from genius_invocation.card.character.import_head import *


class Kaboom(NormalAttack):
    id: int = 130601
    name = "Kaboom!"
    name_ch = "砰砰"
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

class JumpyDumpty(ElementalSkill):
    id: int = 130602
    name = "Jumpy Dumpty"
    name_ch = "蹦蹦炸弹"
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
        self.add_status(game, ExplosiveSpark)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ExplosiveSpark(Status):
    name = "Explosive Spark"
    name_ch = "爆裂火花"
    id = 130621
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
        if self.from_character.talent:
            self.usage = 2
            self.current_usage += 1
    def update(self):
        if self.from_character.talent:
            self.usage = 2
        self.current_usage = max(self.current_usage, self.usage)
        
    def on_calculate_dice(self, game:'GeniusGame'):
        if self.from_player.dice_zone.num()%2 != 0:
            return False
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                if game.current_dice.from_character == self.from_character:
                    if self.current_usage > 0:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] -= 1
                            return True
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False
    
    def on_skill(self, game:"GeniusGame"):
        self.on_calculate_dice(game)
            
    def on_dmg_add(self, game:"GeniusGame"):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                if game.current_damage.is_charged_attack:
                    game.current_damage.main_damage += 1
                    self.current_usage -= 1
                    if self.current_usage <=0:
                        self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)
        ]

class SparksnSplash(ElementalBurst):
    id: int = 130603
    name = "Sparks 'n' Splash"
    name_ch = "轰轰火花"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 3
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        target_zone = get_opponent(game).team_combat_status
        state = target_zone.has_status(SparksnSplashStatus)
        if state != None:
            state.update()
        else:
            target_zone.add_entity(SparksnSplashStatus(game, from_player=get_opponent(game), from_character=None))

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SparksnSplashStatus(Combat_Status):
    name = "Sparks 'n' Splash"
    name_ch = "轰轰火花"
    id = 130631
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def on_after_skill(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.PYRO,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_my_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE, self.on_after_skill)
        ]


class Klee(Character):
    id: int = 1306
    name: str = "Klee"
    name_ch = "可莉"
    time = 3.4
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.MONDSTADT
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Kaboom, JumpyDumpty, SparksnSplash]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
