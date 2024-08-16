from genius_invocation.card.character.import_head import *

class Seal_of_Approval(NormalAttack):
    name = "Seal of Approval"
    name_ch = "火漆制印"
    id = 130801
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
        if self.from_character.talent and self.is_charged_attack:
            target = get_opponent_active_character(game)
            if target.health_point <=6:
                self.resolve_damage(game, add_main_damage=1)
            else:
                self.resolve_damage(game)
        else:
            self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Signed_Edict(ElementalSkill):
    id = 130802
    name = "Signed Edict"
    name_ch = "丹书立约"
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
        self.add_status(game, Scarlet_Seal)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Done_Deal(ElementalBurst):
    name = "Done Deal"
    name_ch = "凭此结契"
    id = 130803
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
        self.add_status(game, Scarlet_Seal)
        self.add_status(game, Brilliance)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Scarlet_Seal(Status):
    name = "Scarlet Seal"
    name_ch = '丹火印'
    id = 130821
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 1

    # 4.2更新
    def update(self):
        self.current_usage = min(self.current_usage+1, self.usage)

    def on_dmg_add(self, game:"GeniusGame"):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                if game.current_damage.is_charged_attack:
                    game.current_damage.main_damage += 2
                    self.current_usage -= 1
                    # 4.2更新
                    if self.from_character.talent:
                        if game.current_damage.is_charged_attack:
                            if game.current_damage.damage_to.health_point <= 6:
                                game.current_damage.main_damage += 1
                        self.from_player.get_card(num=1)
                    if self.current_usage <=0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)
        ]

class Brilliance(Status):
    name = 'Brilliance'
    name_ch = '灼灼'
    id = 130822
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.use_round = -1

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage<=0:
                self.on_destroy(game)

    def on_calculate_dice(self, game:'GeniusGame'):
        if self.use_round == game.round: return False
        if self.from_player.dice_zone.num()%2 != 0:
            return False
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                if game.current_dice.from_character == self.from_character:
                    if self.usage > 0:
                        if game.current_dice.cost[0]['cost_num'] > 0:
                            game.current_dice.cost[0]['cost_num'] -= 1
                            return True
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False

    def on_skill(self, game:"GeniusGame"):
        if self.on_calculate_dice(game):
            self.use_round = game.round
    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill)
        ]



class Yanfei(Character):
    id: int = 1308
    name: str = "Yanfei"
    name_ch = "烟绯"
    time = 3.8
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [Seal_of_Approval, Signed_Edict, Done_Deal]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[0]
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.3] = "调整了角色牌「烟绯」的状态「丹火印」的效果：现在丹火印最多叠加到2次"
        return log
