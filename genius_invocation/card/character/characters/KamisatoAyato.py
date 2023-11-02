from genius_invocation.card.character.import_head import *

class KamisatoArt_Marobashi(NormalAttack):
    name = 'Kamisato Art: Marobashi'
    name_ch = "神里流·转"
    id = 12061
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
            'cost_type': CostType.HYDRO
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


class KamisatoArt_Kyouka(ElementalSkill):
    id = 12062
    name = 'Kamisato Art: Kyouka'
    name_ch = "神里流·镜花"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.add_status(game, Takimeguri_Kanka)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class KamisatoArt_Suiyuu(ElementalBurst):
    name = 'Kamisato Art: Suiyuu'
    name_ch = '神里流·水囿'
    id = 12063
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.HYDRO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Garden_of_Purity)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Takimeguri_Kanka(Status):
    name = 'Takimeguri_Kanka'
    name_ch = '泷廻鉴花'
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.usage = 2

    def infusion(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.HYDRO
    def on_dmg_add(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                game.current_damage.main_damage += 1
                if self.from_character.talent and game.current_damage.damage_to.health_point<=6:
                    game.current_damage.main_damage += 1
                self.current_usage -= 1
                if self.current_usage<=0:
                    self.on_destroy(game)
    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infusion),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)
        ]
class Garden_of_Purity(Summon):
    name = 'Garden of Purity'
    name_ch = "清净之园囿"
    element = ElementType.HYDRO
    removable = True

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.current_usage = self.usage

    def end_phase(self, game:'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                SkillType.SUMMON,
                self.element,
                2,
                0,
                self,
                get_opponent_active_character(game)
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage<=0:
                self.on_destroy(game)
    def on_dmg_add(self, game:'GeniusGame'):
        if isinstance(game.current_damage.damage_from, Character):
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    game.current_damage.main_damage += 1
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.SUMMON_ZONE, self.on_dmg_add),
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.end_phase)
        ]
class KamisatoAyato(Character):
    id: int = 1206
    name: str = "Kamisato Ayato"
    name_ch = "神里绫人"
    element: ElementType = ElementType.HYDRO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [KamisatoArt_Marobashi, KamisatoArt_Kyouka, KamisatoArt_Suiyuu]
    max_power: int = 3

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        self.talent_skill = self.skills[1]
