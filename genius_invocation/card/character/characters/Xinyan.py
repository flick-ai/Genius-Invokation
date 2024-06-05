from genius_invocation.card.character.import_head import *

class DanceonFire(NormalAttack):
    id: int = 13121
    name = "Dance on Fire"
    name_ch = "炎舞"
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


class SweepingFervor(ElementalSkill):
    id: int = 13122
    name = "Sweeping Fervor"
    name_ch = "热情拂扫"
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

        max_idx = max_count_card(self.from_character.from_player.hand_zone.card)
        self.from_character.from_player.hand_zone.discard_card(max_idx)

        self.add_combat_shield(game, ShieldofPassion)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ShieldofPassion(Combat_Shield):
    name = "Shield of Passion"
    name_ch = "热情护盾"
    max_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.max_usage

    def update(self):
        self.current_usage = self.max_usage



class RiffRevolution(ElementalBurst):
    id: int = 13123
    name = "Riff Revolution"
    name_ch = "叛逆刮弦"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 3
    piercing_damage: int = 2
    cost = [{'cost_num':3, 'cost_type':CostType.PYRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)

        for idx in range(self.from_character.from_player.hand_zone.num()):
            self.from_character.from_player.hand_zone.discard_card(idx=idx)

        self.add_combat_status(game, FestiveFires)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class FestiveFires(Combat_Status):
    name = "Festive Fires"
    name_ch = "氛围烈焰"
    max_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.max_usage

    def update(self):
        self.current_usage = self.max_usage

    def after_any_action(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_action.choice_type == ActionChoice.PASS:
                if len(self.from_player.hand_zone.card) <= 1:
                    damage = Damage.create_damage(
                        game=game,
                        damage_type=SkillType.OTHER,
                        main_damage_element=ElementType.PYRO,
                        main_damage=1,
                        piercing_damage=0,
                        damage_from=self,
                        damage_to=get_active_character(game, 1-self.from_player.index)
                    )
                    game.add_damage(damage)
                    game.resolve_damage()
                    self.current_usage -= 1
                    if self.current_usage == 0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_ANY_ACTION, ZoneType.ACTIVE_ZONE, self.after_any_action)
        ]


class Xinyan(Character):
    id: int = 1312
    name: str = "Xinyan"
    name_ch = "辛焱"
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.LIYUE
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [DanceonFire, SweepingFervor, RiffRevolution]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[0]

        self.use_talent_round = -1
        if self.talent:
            self.listen_talent_events(game)

    def damage_add(self, game: 'GeniusGame'):
        if self.use_talent_round  != game.round:
            if game.current_damage.damage_from == self:
                if self.from_player.hand_zone.num() <= 1:
                    game.current_damage.main_damage += 2
                    self.use_talent_round = game.round

    def listen_talent_events(self, game: GeniusGame):
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.damage_add)
