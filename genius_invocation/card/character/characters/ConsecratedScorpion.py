from genius_invocation.card.character.import_head import *

class ScorpionStrike(NormalAttack):
    id: int = 24051
    name = "Scorpion Strike"
    name_ch = "蝎爪钳击"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.ELECTRO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class StingingSpine(ElementalSkill):
    id: int = 24052
    name = "Stinging Spine"
    name_ch = "蝎尾锥刺"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        self.from_character.from_player.card_zone.insert_randomly([BonecrunchersEnergyBlock()], 2)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ThunderboreBlast(ElementalBurst):
    id: int = 24053
    name = "Thunderbore Blast"
    name_ch = "雷锥散射"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 2
    energy_gain: int = 0


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        cards = self.from_character.from_player.hand_zone.discard_card_by_name(
            name="Bonecruncher's Energy Block",
            max_count=3
        )
        if len(cards) > 0:
            target_zone = get_opponent(game).team_combat_status
            target_zone.add_entity(ThunderboreTrap(game, from_player=get_opponent(game), from_character=None,
                                                   usage=len(cards)))
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ThunderboreTrap(Combat_Status):
    name = "Thunderbore Trap"
    name_ch = "雷锥陷阱"
    max_usage = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, usage=1):
        super().__init__(game, from_player, from_character)
        self.current_usage = usage

    def update(self, usage=1):
        self.current_usage = min(self.current_usage + usage, self.max_usage)

    def on_after_skill(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.ELECTRO,
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

class ImmortalRemnantsElectro(CharacterSkill):
    name = "Immortal Remnants: Electro"
    name_ch = "不朽遗骸:雷"
    def on_call(self, game: 'GeniusGame'):
        self.from_character.from_player.card_zone.insert_randomly(
            [BonecrunchersEnergyBlock() for _ in range(2)],
            num=10,
        )

class ConsecratedScorpion(Character):
    id: int = 2405
    name: str = "Consecrated Scorpion"
    name_ch = "圣骸毒蝎"
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    country_list: List[CountryType] = [CountryType.MONSTER, CountryType.CONSECRATED_BEAST]
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [ScorpionStrike, StingingSpine, ThunderboreBlast]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = None
        self.passive_skill = ImmortalRemnantsElectro(self)
        self.listen_event(game, EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end)

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.passive_skill.on_call(game)

    def after_play_card(self, game: 'GeniusGame'):
        if self.talent:
            if game.current_card.name == "Bonecruncher's Energy Block":
                self.from_player.get_card(num=1)
                self.from_player.card_zone.insert_randomly([BonecrunchersEnergyBlock()], num=-1)

    def equip_talent(self, game:'GeniusGame', is_action=True, talent_card=None):
        self.talent = True
        self.from_player.hand_zone.add([BonecrunchersEnergyBlock()])
        self.character_zone.talent_card = talent_card
        self.listen_talent_events(game)

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.AFTER_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.after_play_card)


class HasBonecrunchersEnergyBlock(Combat_Status):
    name: str = "Bonecruncher's Energy Block"
    name_ch = '噬骸能量块'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_end(self, game:'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end),
        ]

class BonecrunchersEnergyBlock(ActionCard):
    name = "Bonecruncher's Energy Block"
    name_ch = "噬骸能量块"
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        game.active_player.team_combat_status.add_entity(HasBonecrunchersEnergyBlock(game, game.active_player))

        game.active_player.hand_zone.discard_card(max_count_card(game.active_player.hand_zone.card))

        element_dice = ElementToDice[get_my_active_character(game).element]
        game.active_player.dice_zone.add([element_dice.value])

        character = get_my_active_character(game)
        if hasattr(character, 'country_list'):
            if CountryType.CONSECRATED_BEAST in character.country_list:
                character.get_power(power=1)

    def find_target(self, game: 'GeniusGame'):
        if game.active_player.last_die_round == game.round :
            if game.active_player.team_combat_status.has_status(HasBonecrunchersEnergyBlock) is None:
                return [1]
        return []
