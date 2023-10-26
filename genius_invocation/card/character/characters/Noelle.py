from genius_invocation.card.character.import_head import *

class Favonius_Bladework_Maid(NormalAttack):
    id = 0
    name = 'Favonius Bladework - Maid'
    name_ch = "西风剑术·女仆"
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
            'cost_type': CostType.GEO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Breastplate(ElementalSkill):
    id = 1
    name = 'Breastplate'
    name_ch = "护心铠"
    type = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.GEO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.add_combat_shield(game, Full_Plate)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Sweeping_Time(ElementalBurst):
    name = 'Sweeping Time'
    name_ch = "大扫除"
    id = 2
    type = SkillType.ELEMENTAL_BURST

    damage_type = SkillType.ELEMENTAL_BURST
    main_damage_element = ElementType.GEO
    main_damage = 4
    piercing_damage = 0

    cost = [
        {
            'cost_num': 4,
            'cost_type': CostType.GEO
        }
    ]
    energy_cost = 2
    energy_gain = 0

    def on_call(self, game:'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_status(game, Sweeping_Time_Status)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Noelle(Character):
    id = 1602
    name = 'Noelle'
    name_ch = "诺艾尔"
    element = ElementType.GEO
    weapon_type = WeaponType.CLAYMORE
    country = CountryType.MONDSTADT

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [
        Favonius_Bladework_Maid, Breastplate, Sweeping_Time
    ]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.heal_last_round = -1
        self.talent_skill = self.skills[1]
    
    def listen_talent_events(self, game:'GeniusGame'):
        status = self.from_player.team_combat_status.has_shield(Full_Plate)
        if status:
            status.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE_SHIELD, status.after_skill)

class Full_Plate(Combat_Shield):
    name = "Full Plate"
    name_ch = "护体岩铠"
    id = 0
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def after_skill(self, game:"GeniusGame"):
        if self.from_character.talent and self.from_character.heal_last_round != game.round:
            if game.current_skill.from_character == self.from_character:
                if game.current_skill.type == SkillType.NORMAL_ATTACK:
                    self.from_character.heal_last_round = game.round
                    for chars in self.from_character.from_player.character_list:
                        if chars.is_alive:
                            chars.heal(1,game=game)
    def on_dividing(self, game:"GeniusGame"):
        if game.current_damage.main_damage_element == ElementType.PHYSICAL:
            if game.current_damage.damage_to.from_player == self.from_player:
                if game.current_damage.damage_to.is_active:
                    game.current_damage = (game.current_damage + 1)//2

    def on_execute_dmg(self, game:'GeniusGame'):
        if game.current_damage.damage_to.from_player == self.from_player:
            if game.current_damage.damage_to.is_active:
                if game.current_damage.main_damage_element != ElementType.PIERCING:
                    if game.current_damage.main_damage >= self.current_usage:
                        game.current_damage.main_damage -= self.current_usage
                        self.current_usage = 0
                        self.on_destroy(game)
                    else:
                        self.current_usage -= game.current_damage.main_damage
                        game.current_damage.main_damage = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.DIVIDE_DAMAGE, ZoneType.ACTIVE_ZONE_SHIELD, self.on_dividing),
            (EventType.EXECUTE_DAMAGE, ZoneType.ACTIVE_ZONE_SHIELD, self.on_execute_dmg)
        ]
        if self.from_character.talent:
            self.listeners.append((EventType.AFTER_USE_SKILL, ZoneType.ACTIVE_ZONE_SHIELD, self.after_skill))



class Sweeping_Time_Status(Status):
    name = 'Sweeping Time'
    name_ch = "大扫除-效果"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.usage = 2
        self.current_usage = 2
        self.last_saving_round = -1

    def update(self):
        self.current_usage = max(self.usage, self.current_usage)
        self.last_saving_round = -1

    def on_calculation(self, game:"GeniusGame"):
        if self.last_saving_round != game.round:
            if game.active_player_index == self.from_player.index:
                if game.current_dice.use_type is SkillType.NORMAL_ATTACK:
                    if game.current_dice.from_character == self.from_character:  #Noelle will use normal attack
                        if game.current_dice[0]['cost_num']>0:
                            game.current_dice[0]['cost_num'] -= 1
                            return True
                        elif game.current_dice[1]['cost_num'] >0:
                            game.current_dice[1]['cost_num'] -= 1
                            return True
        return False

    def on_damage_add(self, game:"GeniusGame"):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                game.current_damage.main_damage += 2

    def on_skill(self, game:"GeniusGame"):
        if self.on_calculation(game):
            self.last_saving_round = game.round

    def infusion(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                    game.current_damage.main_damage_element = ElementType.GEO
    def begin_phase(self, game:"GeniusGame"):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage <=0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.begin_phase),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculation),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion)
        ]

