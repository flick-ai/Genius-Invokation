from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.base import ActionCard


class OverchargedBall(ActionCard):
    id: int = 131371
    name = "Overcharged Ball"
    name_ch = "超量装药弹头"
    cost_num = 2
    cost_type = CostType.PYRO
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.OTHER,
            main_damage_element=ElementType.PYRO,
            main_damage=1,
            piercing_damage=0,
            damage_from=self.zone,
            damage_to=get_active_character(game, 1-self.zone.from_player.index),
        )
        game.add_damage(dmg)
        game.resolve_damage()
        game.is_change_player = True

    def on_discard(self, game: 'GeniusGame'):
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.OTHER,
            main_damage_element=ElementType.PYRO,
            main_damage=1,
            piercing_damage=0,
            damage_from=self.zone,
            damage_to=get_active_character(game, 1-self.zone.from_player.index),
        )
        game.add_damage(dmg)
        game.resolve_damage()
        game.is_change_player = True

class VerticalForceCoordination(CharacterSkill):
    id = 131304
    name = 'Vertical Force Coordination'
    name_ch = '纵阵武力统筹'
    def on_call(self, game:'GeniusGame'):
        self.from_character.from_player.hand_zone.add([OverchargedBall()])

class LineBayonetThrustEX(NormalAttack):
    id: int = 131301
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Invokers Spear"
    name_ch = "线列枪刺·改"
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{
            'cost_num': 1,
            'cost_type': CostType.PYRO
        },
        {
            'cost_num': 2,
            'cost_type': CostType.BLACK
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class ShortRangeRapidInterdictionFire(ElementalSkill):
    id: int = 131302
    name = "Short-Range Rapid Interdiction Fire"
    name_ch = "近迫式急促拦射"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.PYRO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1
    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        card = self.from_character.from_player.hand_zone.has_card(OverchargedBall)
        if card is not None:
            card.on_dsicard(game)
            character = max_dmg_taken(self.from_character.from_player)
            character.heal(heal=1, game=game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class SecondaryExplosiveShells(Combat_Status):
    id = 131331
    name = "Secondary Explosive Shells"
    name_ch = "二重毁伤弹"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def on_swith(self, game:'GeniusGame'):
        if game.current_switch['from'].from_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.PYRO,
                main_damage=1,
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
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.ACTIVE_ZONE, self.on_swith)
        ]

class RingofBurstingGrenades(ElementalBurst):
    id = 131303
    name="Ring of Bursting Grenades"
    name_ch = "圆阵掷弹爆轰术"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.PYRO
        }
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character') -> None:
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        target_zone = get_opponent(game).team_combat_status
        state = target_zone.has_status(SecondaryExplosiveShells)
        if state != None:
            state.update()
        else:
            target_zone.add_entity(SecondaryExplosiveShells(game, from_player=get_opponent(game), from_character=None))
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class PyroQuill(Combat_Status):
    id: int = 131332
    name: str = "Pyro Quill"
    name_ch = "火翎"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = 2
        self.last_use_round = -1

    def update(self):
        self.current_usage = self.usage

    def on_dmg_add(self, game: 'GeniusGame'):
        if not isinstance(game.current_damage.damage_from, Character): return
        if game.current_damage.main_damage_element in [ElementType.PYRO,
                                                       ElementType.ELECTRO]:
            if game.current_damage.damage_from.from_player == self.from_player:
                game.current_damage.main_damage += 1
                if self.from_character.talent and game.current_damage.damage_type==SkillType.NORMAL_ATTACK and self.last_use_round!= game.round:
                    self.last_use_round = game.round
                else:
                    self.current_usage -= 1
                    if self.current_usage <= 0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
           (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_dmg_add)
        ]

class Chevreuse(Character):
    id = 1313
    name = "Chevreuse"
    name_ch = "夏沃蕾"
    time = 4.8
    element = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.POLEARM
    country: CountryType = CountryType.FONTAINE

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [LineBayonetThrustEX,
                  ShortRangeRapidInterdictionFire,
                  RingofBurstingGrenades]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.CHARACTER_ZONE, self.on_reaction)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = None
        self.passive_skill = VerticalForceCoordination(self)

    def on_reaction(self, game: 'GeniusGame'):
        if game.current_damage.damage_to.from_player.index == 1 - self.from_player.index:
            if game.current_damage.reaction == ElementalReactionType.Overloaded:
                self.passive_skill.on_reaction(game)
            if self.talent:
                self.from_player.team_combat_status.add_entity(PyroQuill(game, from_player=self.from_player, from_character=self))

