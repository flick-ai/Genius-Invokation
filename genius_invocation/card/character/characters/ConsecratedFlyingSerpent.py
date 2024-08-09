from genius_invocation.card.character.import_head import *
from genius_invocation.card.character.characters.ConsecratedScorpion import BonecrunchersEnergyBlock

class WhirlingTail(NormalAttack):
    id: int = 25031
    name = "Whirling Tail"
    name_ch = "旋尾迅击"
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':1, 'cost_type':CostType.ANEMO}, {'cost_num':2, "cost_type":CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SwirlingSquall(ElementalSkill):
    id: int = 25032
    name = "Swirling Squall"
    name_ch = "盘绕风引"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ANEMO}]
    energy_cost: int = 0
    energy_gain: int = 1

    def calculate_card_num(self, game: 'GeniusGame'):
        num = 0
        for card in self.from_character.from_player.hand_zone.card:
            if card.name == "Bonecruncher's Energy Block":
                num += 1
        return num

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        # self.from_character.from_player.card_zone.find_card_by_name(BonecrunchersEnergyBlock.name, num=1)
        # num = min(self.from_character.round_get_cards, self.calculate_card_num(game))
        # self.from_character.round_get_cards = max(0, self.from_character.round_get_cards - num)
        self.from_character.from_player.get_card(num=1)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ScattershotVortex(ElementalBurst):
    id: int = 25033
    name = "Scattershot Vortex"
    name_ch = "错落风涡"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ANEMO
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ANEMO}]
    energy_cost: int = 2
    energy_gain: int = 0


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        cards = self.from_character.from_player.hand_zone.discard_card_by_name(BonecrunchersEnergyBlock.name, max_num=MAX_HANDCARD)
        multiply_num = 2 * (len(cards) // 2)
        self.resolve_damage(game, damage_multiply=multiply_num)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class ImmortalRemnantsAnemo(CharacterSkill):
    name = "Immortal Remnants: Anemo"
    name_ch = "不朽遗骸: 风"
    def on_call(self, game: 'GeniusGame'):
        self.from_character.from_player.card_zone.insert_evenly(
            [BonecrunchersEnergyBlock for _ in range(6)]
        )

class ConsecratedFlyingSerpent(Character):
    id: int = 2503
    name: str = "Consecrated Flying Serpent"
    name_ch = "圣骸飞蛇"
    time = 4.7
    element: ElementType = ElementType.ANEMO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    country_list: List[CountryType] = [CountryType.MONSTER, CountryType.CONSECRATED_BEAST]
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [WhirlingTail, SwirlingSquall, ScattershotVortex]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = None
        self.passive_skill = ImmortalRemnantsAnemo(self)
        self.round_get_cards = 2
        self.return_dice = False

        if self.talent:
            self.listen_talent_events(game)

    def init_state(self, game: 'GeniusGame'):
        self.passive_skill.on_call(game)

    def on_begin(self, game):
        super().on_begin(game)
        self.round_get_cards = 2

    def after_play_card(self, game: 'GeniusGame'):
        if self.talent:
            if game.current_card.name == "Bonecruncher's Energy Block":
                self.from_player.get_card(num=1)
                self.from_player.card_zone.insert_randomly([BonecrunchersEnergyBlock()], num=-1)
                self.return_dice = True

    def after_change(self, game: 'GeniusGame'):
        if self.talent and self.return_dice:
            element_dice = ElementToDice[get_active_character(game, self.from_player.index).element]
            self.from_player.dice_zone.add([element_dice.value])

    def equip_talent(self, game:'GeniusGame', is_action=True, talent_card=None):
        self.talent = True
        self.from_player.hand_zone.add([BonecrunchersEnergyBlock()])
        self.character_zone.talent_card = talent_card
        self.listen_talent_events(game)

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.AFTER_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.after_play_card)
        self.listen_event(game, EventType.AFTER_CHANGE_CHARACTER, ZoneType.CHARACTER_ZONE, self.after_change)

    def balance_adjustment():
        log = {}
        log[4.8] = "调整了角色牌「圣骸飞蛇」元素战技的效果：效果调整为“造成3点风元素伤害，抓1张牌”"
        return log