from genius_invocation.card.character.import_head import *
from genius_invocation.card.action.base import ActionCard

class SoloistsSolicitation(NormalAttack):
    name = "Soloist's Solicitation"
    name_ch = "独舞之邀"
    id: int = 121101
    type: SkillType = SkillType.NORMAL_ATTACK

    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 1,'cost_type': CostType.HYDRO},{'cost_num': 2,'cost_type': CostType.BLACK}]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        if self.from_character.card_round != game.round:
            if not self.from_character.from_player.hand_zone.has_card(SeatsSacredandSecular):
                self.from_character.from_player.hand_zone.add([SeatsSacredandSecular()])
                self.from_character.card_round = game.round
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class SalonSolitaire(ElementalSkill):
    id = 121102
    name = 'Salon Solitaire'
    name_ch = "孤心沙龙"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 3,'cost_type': CostType.HYDRO},]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 获得能量
        self.gain_energy(game)
        self.generate_summon(game, FurinaSummon)
        if self.from_character.talent:
            self.add_status(game, CenterofAttention)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class LetthePeopleRejoice(ElementalBurst):
    id = 121103
    name = 'Let the People Rejoice'
    name_ch = "万众狂欢"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.HYDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [{'cost_num': 3, 'cost_type': CostType.HYDRO}]

    energy_cost: int = 3
    energy_gain: int = 0

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.consume_energy(game)
        self.resolve_damage(game)
        self.add_combat_status(game, LetthePeopleRejoice)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)


class Furina(Character):
    id = 1211
    name = "Furina"
    name_ch = "芙宁娜"
    time = 4.7
    element = ElementType.HYDRO
    weapon_type = WeaponType.SWORD
    country = CountryType.MONSTER
    arkhen = ArkhenType.PNEUMA

    init_health_point = 10
    max_health_point = 10
    skill_list = [
        SoloistsSolicitation,
        SalonSolitaire,
        LetthePeopleRejoice
    ]
    max_power = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.arkhen = self.arkhen

        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[1]

        self.card_round = -1

    def init_state(self, game: 'GeniusGame'):
        self.from_player.hand_zone.add([SeatsSacredandSecular()])

    def change_state(self, game: 'GeniusGame'):
        if self.arkhen == ArkhenType.PNEUMA:
            self.arkhen = ArkhenType.OUSIA
        else:
            self.arkhen = ArkhenType.PNEUMA

        summon = self.from_player.summon_zone.has(FurinaSummon)
        if summon is not None:
            summon.update_state(game)


class LetthePeopleRejoice(Combat_Status):
    name = "Let the People Rejoice"
    name_ch = "普世欢腾"
    max_usage = 2
    id = 121131
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.max_usage

    def update(self):
        self.current_usage = self.max_usage

    def excute(self, game: 'GeniusGame'):
        self.from_player.team_combat_status.add_entity(
            Revelry(game, self.from_player, self.from_character)
        )

    def after_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            self.excute(game)

    def after_heal(self, game:'GeniusGame'):
        if game.current_heal.heal_to_character == self.from_character:
            self.excute(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.after_damage),
            (EventType.AFTER_HEAL, ZoneType.CHARACTER_ZONE, self.after_heal),
        ]

class Revelry(Combat_Status):
    name = "Revelry"
    name_ch = "狂欢值"
    id = 121132
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def update(self):
        self.current_usage += 1

    def on_damage_add(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_damage.damage_from.from_player == self.from_player:
                game.current_damage.main_damage += 1
                self.current_usage -= 1
                if self.current_usage <= 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_damage_add),
        ]

class FurinaSummon(Summon):
    name = "Salon Members"
    name_ch = "沙龙成员"
    removable = True
    max_usage = 4
    id = 121111

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character' = None, usage=2):
        super().__init__(game, from_player, from_character)
        if self.from_character.arkhen == ArkhenType.PNEUMA:
            self.name = self.name
            self.name_ch = self.name_ch
        else:
            self.name = "Singer of Many Waters"
            self.name_ch = "众水的歌者"
        self.current_usage = usage

    def update_state(self, game: 'GeniusGame'):
        if self.from_character.arkhen == ArkhenType.PNEUMA:
            self.name = "Salon Members"
            self.name_ch = "沙龙成员"
        else:
            self.name = "Singer of Many Waters"
            self.name_ch = "众水的歌者"

    def update(self, usage=2):
        self.current_usage = min(self.current_usage+usage, self.max_usage)

    def max_dmg_taken(self, game: 'GeniusGame'):
        max_dmg_taken = -1
        max_taken_char = None
        ls: List[int] = []
        id = self.from_player.active_idx
        for i in range(self.from_player.character_num):
            ls.append(id)
            id += 1
            if id >= self.from_player.character_num:
                id = 0

        for i in ls:
            char = self.from_player.character_list[i]
            dmg_taken = char.max_health_point - char.health_point
            if dmg_taken > max_dmg_taken:
                max_dmg_taken = dmg_taken
                max_taken_char = char
        return max_taken_char

    def min_dmg_taken(self, game: 'GeniusGame'):
        min_dmg_taken = 10000
        min_taken_char = None
        ls: List[int] = []
        id = self.from_player.active_idx
        for i in range(self.from_player.character_num):
            ls.append(id)
            id += 1
            if id >= self.from_player.character_num:
                id = 0

        for i in ls:
            char = self.from_player.character_list[i]
            dmg_taken = char.max_health_point - char.health_point
            if dmg_taken < min_dmg_taken:
                min_dmg_taken = dmg_taken
                min_taken_char = char
        return min_taken_char

    def check_health_more(self, game: 'GeniusGame', target_point: int=6):
        for character in self.from_player.character_list:
            if character.health_point >= character.max_health_point:
                return True
        return False

    def check_health_less(self, game: 'GeniusGame', target_point: int=5):
        for character in self.from_player.character_list:
            if character.health_point <= character.max_health_point:
                return True
        return False

    def damage(self, game: 'GeniusGame'):
        damage1 = Damage.create_damage(
            game,
            damage_type=SkillType.SUMMON,
            main_damage=1,
            main_damage_element=ElementType.HYDRO,
            piercing_damage=0,
            damage_from=self,
            damage_to=get_opponent_active_character(game),
        )
        game.add_damage(damage1)
        game.resolve_damage()

        if self.check_health_more(game):
            damage_self = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.PIERCING,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=self.min_dmg_taken(game),
            )
            game.add_damage(damage_self)
            game.resolve_damage()

            damage2 = Damage.create_damage(
                game,
                damage_type=SkillType.SUMMON,
                main_damage_element=ElementType.HYDRO,
                main_damage=1,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(damage2)
            game.resolve_damage()

    def heal(self, game: 'GeniusGame'):
        for character in self.from_player.character_list:
                character.heal(1, game)
        if self.check_health_less(game):
            self.min_dmg_taken(game).heal(1, game)

    def end_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            if self.from_character.arkhen == ArkhenType.PNEUMA:
                self.damage(game)
            else:
                self.heal(game)
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.end_phase),
        ]

class SeatsSacredandSecular(ActionCard):
    name = "Seats Sacred and Secular"
    name_ch = "圣俗杂座"
    id = 121171
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.EVENT
    def __init__(self) -> None:
        super().__init__()

    def get_from_character(self, game: 'GeniusGame') -> 'Character':
        for character in game.active_player.character_list:
            if character.name == Furina.name:
                return character
        return None

    def on_played(self, game: 'GeniusGame') -> None:
        if self.get_from_character(game) is not None:
            self.get_from_character(game).change_state(game)

    def find_target(self, game: 'GeniusGame'):
        return [1]

class CenterofAttention(Status):
    name = "Center of Attention"
    name_ch = "万众瞩目"
    id = 121121
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1

    def min_dmg_taken(self, game: 'GeniusGame'):
        min_dmg_taken = 10000
        min_taken_char = None
        ls: List[int] = []
        id = self.from_player.active_idx
        for i in range(self.from_player.character_num):
            ls.append(id)
            id += 1
            if id >= self.from_player.character_num:
                id = 0

        for i in ls:
            char = self.from_player.character_list[i]
            dmg_taken = char.max_health_point - char.health_point
            if dmg_taken < min_dmg_taken:
                min_dmg_taken = dmg_taken
                min_taken_char = char
        return min_taken_char

    def on_infusion(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_damage.damage_from == self.from_character:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                        game.current_damage.main_damage += 1
                        self.current_usage -= 1
        if self.current_usage <= 0:
            self.on_destroy(game)

    def on_damage_add(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    if self.from_character.arkhen == ArkhenType.PNEUMA:
                        game.current_damage.main_damage += 2

                        damage = Damage.create_damage(
                            game,
                            damage_type=SkillType.OTHER,
                            main_damage=1,
                            main_damage_element=ElementType.PIERCING,
                            piercing_damage=0,
                            damage_from=self.from_character,
                            damage_to=self.min_dmg_taken(game),
                        )
                        game.add_damage(damage)
                        game.resolve_damage()

                        self.current_usage -= 1

    def on_skill(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_skill.from_character == self.from_character:
                if game.current_skill.damage_type == SkillType.NORMAL_ATTACK:
                    if self.from_character.arkhen == ArkhenType.OUSIA:
                        for character in self.from_player.character_list:
                            character.heal(1, game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.on_infusion),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
        ]


