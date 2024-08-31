from genius_invocation.card.character.import_head import *

class Flame_of_Salvation(NormalAttack):
    name = "Flame of Salvation"
    name_ch = "振救之焰"
    id = 230201
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


class Searing_Precept(ElementalSkill):
    name = "Searing Precept"
    name_ch = "炽烈箴言"
    id = 230202
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
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Ominous_Star(ElementalBurst):
    name = "Ominous Star"
    name_ch = "天陨预兆"
    id = 230203
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.PYRO
    main_damage: int = 3
    piercing_damage: int = 0
    cost = [{'cost_num':4, 'cost_type':CostType.PYRO}]
    energy_cost: int = 2
    energy_gain: int = 0

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.consume_energy(game)
        self.resolve_damage(game)
        self.generate_summon(game, Darkfire_Furnace)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Darkfire_Furnace(Summon):
    name = "Darkfire Furnace"
    name_ch = "渊火熔炉"
    removable = True
    id = 230211
    element  = ElementType.PYRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.usage = 2
    def on_end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            dmg = Damage.create_damage(
                game,
                SkillType.SUMMON,
                main_damage_element=self.element,
                main_damage=1,
                piercing_damage=1,
                damage_from=self,
                damage_to = get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUMMON_ZONE, self.on_end_phase)
        ]

class Fiery_Rebirth(Status):
    name = "Fiery Rebirth"
    name_ch = "火之新生"
    id = 230221
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        self.set_talent = False

    def on_character_die(self, game: 'GeniusGame'):
        '''
            角色死亡时
        '''
        if not self.from_character.is_alive:
            self.from_character.is_alive = True
            self.from_character.health_point = 0
            self.from_character.heal(4, game, heal_type=HealType.REVIVE)
            self.from_character.revive_event(game)
            if self.set_talent:
                shield = Aegis_of_Abyssal_Flame(game, self.from_player, self.from_character)
                self.from_character.character_zone.add_entity(shield)
                self.from_character.talent = False
                self.from_character.character_zone.talent_card.on_destroy(game)
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        ]

class Aegis_of_Abyssal_Flame(Shield):
    name = "Aegis of Abyssal Flame"
    name_ch = "渊火加护"
    id = 230241
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2
        self.usage = 2

    def on_destroy(self, game: 'GeniusGame'):
        oppenent = game.players[1-self.from_player.index]
        for character in oppenent.character_list:
            if character.is_alive:
                dmg = Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.PIERCING,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=self,
                    damage_to=character)
                game.add_damage(dmg)
                game.resolve_damage()
        super().on_destroy(game)

class AbyssLectorFathomlessFlames(Character):
    id: int = 2302
    name: str = "Abyss Lector: Fathomless Flames"
    name_ch = "深渊咏者·渊火"
    time = 3.7
    element: ElementType = ElementType.PYRO
    weapon_type: WeaponType = WeaponType.OTHER
    country: CountryType = CountryType.MONSTER
    init_health_point: int = 6
    max_health_point: int = 6
    skill_list: List = [Flame_of_Salvation, Searing_Precept, Ominous_Star]
    max_power: int = 2

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.6] = "调整了角色牌「深渊咏者·渊火」「火之新生」状态的效果：调整为“所附属角色被击倒时：移除此效果，使角色免于被击倒，并治疗该角色到4点生命值。此效果触发后，此角色造成的火元素伤害+1"
        return log

    def init_state(self, game: 'GeniusGame'):
        rebirth = Fiery_Rebirth(game, self.from_player, self)
        self.character_zone.add_entity(rebirth)

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index: int, from_character=None, talent=False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent
        if self.talent:
            self.character_zone.has_entity(Fiery_Rebirth).set_talent = True

    def on_dmg_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self:
            if game.current_damage.main_damage_element == ElementType.PYRO:
                game.current_damage.main_damage += 1

    def revive_event(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_dmg_add)

    def equip_talent(self, game:'GeniusGame', is_action=True, talent_card=None):
        self.talent = True
        self.character_zone.talent_card = talent_card

        rebirth = self.character_zone.has_entity(Fiery_Rebirth)
        if rebirth is not None:
            rebirth.set_talent = True
        else:
            shield = self.character_zone.has_entity(Aegis_of_Abyssal_Flame)
            if shield is not None:
                shield.update()
            else:
                shield = Aegis_of_Abyssal_Flame(game, self.from_player, self)
                self.character_zone.add_entity(shield)

        game.is_change_player = is_action


