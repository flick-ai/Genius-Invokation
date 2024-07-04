from genius_invocation.card.character.import_head import *


class TenguBowmanship(NormalAttack):
    id: int = 14061
    name = "Tengu Bowmanship"
    name_ch = "天狗传弓术"
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

class TenguStormcall(ElementalSkill):
    id: int = 14062
    name = "Tengu Stormcall"
    name_ch = "鸦羽天狗霆雷召咒"
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':3, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 0
    energy_gain: int = 1
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.generate_summon(game, TenguJuuraiAmbush)
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class TenguJuuraiAmbush(Summon):
    name = "Tengu Juurai: Ambush"
    name_ch = "天狗咒雷·伏"
    removable = True
    element = ElementType.ELECTRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = self.usage

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)

    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            character = get_my_active_character(game)
            status = character.character_zone.has_entity(CrowfeatherCover)
            if status is None:
                character.character_zone.add_entity(CrowfeatherCover(game, self.from_player, character))
            else:
                status.update()
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class TenguJuuraiStormcluster(Summon):
    name = "Tengu Juurai: Stormcluster"
    name_ch = "天狗咒雷·雷砾"
    removable = True
    element = ElementType.ELECTRO
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
                main_damage_element=self.element,
                main_damage=2,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            character = get_my_active_character(game)
            status = character.character_zone.has_entity(CrowfeatherCover)
            if status is None:
                character.character_zone.add_entity(CrowfeatherCover(game, self.from_player, character, self.from_character))
            else:
                status.update()
            if(self.current_usage <= 0):
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase),
        ]

class CrowfeatherCover(Status):
    name = "Crowfeather Cover"
    name_ch = "鸣煌护持"
    def __init__(self, game: 'GeniusGame', from_player:'GeniusPlayer', from_character=None, belong_to=None):
        super().__init__(game, from_player, from_character)
        self.belong_to = belong_to
        self.usage = 2
        self.current_usage = 2

    def update(self):
        self.current_usage = self.usage

    def on_add_damage(self, game:"GeniusGame"):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.ELEMENTAL_SKILL or game.current_damage.damage_type == SkillType.ELEMENTAL_BURST:
                damage_add = 1
                if self.belong_to.talent and self.belong_to.is_alive:
                    if self.from_character.element == ElementType.ELECTRO:
                        damage_add += 1
                game.current_damage.main_damage += damage_add

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage),
        ]



class SubjugationKoukouSendou(ElementalBurst):
    id: int = 14063
    name = "Subjugation: Koukou Sendou"
    name_ch = "煌煌千道镇式"
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 1
    piercing_damage: int = 0
    cost = [{'cost_num':4, 'cost_type':CostType.ELECTRO}]
    energy_cost: int = 2
    energy_gain: int = 0
    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, TenguJuuraiStormcluster)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class KujouSara(Character):
    id: int = 1406
    name: str = "Kujou Sara"
    name_ch = "九条裟罗"
    time: float = 3.5
    element: ElementType = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.BOW
    country: CountryType = CountryType.INAZUMA
    init_health_point: int = 10
    max_health_point: int = 10
    skill_list: List = [TenguBowmanship, TenguStormcall, SubjugationKoukouSendou]
    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        # 4.2更新
        self.talent_skill = self.skills[1]
