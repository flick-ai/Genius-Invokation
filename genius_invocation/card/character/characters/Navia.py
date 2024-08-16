from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.base import ActionCard


class CrystalShrapnel(ActionCard):
    id: int = 160871
    name = "Crystal Shrapnel"
    name_ch = "裂晶弹片"
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.EVENT

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame'):
        dmg = Damage.create_damage(
            game,
            damage_type=SkillType.OTHER,
            main_damage_element=ElementType.PHYSICAL,
            main_damage=1,
            piercing_damage=0,
            damage_from=self.zone,
            damage_to=get_active_character(game, 1-self.zone.from_player.index),
        )
        game.add_damage(dmg)
        game.resolve_damage()
        self.zone.from_player.get_card(num=1)

class MutualAssistanceNetwork(CharacterSkill):
    id = 160804
    name = 'Mutual Assistance Network'
    name_ch = '互助关系网'
    def on_call(self, game:'GeniusGame'):
        self.from_character.from_player.card_zone.return_card([CrystalShrapnel() for i in range(3)])

class BluntRefusal(NormalAttack):
    id: int = 160801
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Blunt Refusal"
    name_ch = "直率的辞绝"
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0
    cost = [{
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

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.resolve_damage(game)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class GEOElementalInfusion(Combat_Status):
    name = "GEO Elemental Infusion"
    name_ch = "岩元素附魔"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)
        self.max_usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.max_usage

    def on_infuse(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.PYRO

    def on_end(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.ACTIVE_ZONE, self.on_infuse),
            (EventType.FINAL_END, ZoneType.ACTIVE_ZONE, self.on_end)
        ]

class CeremonialCrystalshot(ElementalSkill):
    id: int = 160802
    name = "Ceremonial Crystalshot"
    name_ch = "典仪式晶火"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.GEO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1
    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        cards = self.from_character.from_player.hand_zone.discard_card_by_name(name="Crystal Shrapnel", num=5)
        self.resolve_damage(game, add_main_damage=len(cards))
        self.gain_energy(game)
        self.add_status(game, GEOElementalInfusion)
        self.from_character.from_player.get_card(num=len(cards))
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class RosulaDorataSalute(Summon):
    id = 160811
    name: str = "Rosula Dorata Salute"
    name_ch = "金花礼炮"
    removable = True
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.GEO,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()

            cards = self.from_player.card_zone.find_card_by_name("Crystal Shrapnel", num=1)
            self.from_player.hand_zone.add(cards)

            self.current_usage -= 1
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class SingingSalute(ElementalBurst):
    id = 160803
    name="As the Sunlit Sky's Singing Salute"
    name_ch = "如霰澄天的鸣礼"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.GEO
    main_damage: int = 1
    piercing_damage: int = 1

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
        self.generate_summon(game, RosulaDorataSalute)
        self.from_character.from_player.hand_zone.add([CrystalShrapnel()])
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Navia(Character):
    id = 1608
    name = "Navia"
    name_ch = "娜维娅"
    time = 4.8
    element = ElementType.GEO
    weapon_type: WeaponType = WeaponType.CLAYMORE
    country: CountryType = CountryType.FONTAINE

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [BluntRefusal, CeremonialCrystalshot, SingingSalute]
    max_power: int = 2

    def init_state(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.CHARACTER_ZONE, self.on_reaction)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]
        self.passive_skill = MutualAssistanceNetwork(self)
        self.talent_round_usage = 1

    def on_reaction(self, game: 'GeniusGame'):
        if game.current_damage.damage_to.from_player.index == 1 - self.from_player.index:
            if game.current_damage.reaction == ElementalReactionType.Crystallize:
                self.passive_skill.on_reaction(game)

    def after_use_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self:
            if self.talent:
                if self.talent_round_usage > 0:
                    cards = self.from_player.card_zone.find_card_by_name("Crystal Shrapnel", num=2)
                    self.from_player.hand_zone.add(cards)
                    self.talent_round_usage -= 1

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_use_skill)

