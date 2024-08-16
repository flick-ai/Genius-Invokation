from genius_invocation.card.character.import_head import *

class Shinobus_Shadowsword(NormalAttack):
    id: int = 141101
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Shinobu's Shadowsword"
    name_ch = "忍流飞刃斩"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.PHYSICAL
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.ELECTRO
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
        # 处理伤害
        self.resolve_damage(game)
        # 获得能量
        self.gain_energy(game)
        # after skill
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Sanctifying_Ring(ElementalSkill):
    id: int = 141102
    name = "Sanctifying Ring"
    name_ch = "越祓雷草之轮"
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
        },
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        self.add_combat_status(game, Grass_Ring_of_Sanctification)
        if self.from_character.health_point>=6:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.PIERCING,
                main_damage=2,
                piercing_damage=0,
                damage_from=self.from_character,
                damage_to=self.from_character,
            )
            game.add_damage(dmg)
            game.resolve_damage()
        self.gain_energy(game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Gyoei_Narukami_Kariyama_Rite(ElementalBurst):
    id = 141103
    name="Gyoei Narukami Kariyama Rite"
    name_ch = "御咏鸣神刈山祭"
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.ELECTRO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.ELECTRO
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
        self.from_character.heal(2, game)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)



class KukiShinobu(Character):
    id: int = 1411
    name = "Kuki Shinobu"
    name_ch = "久岐忍"
    time = 4.6
    element = ElementType.ELECTRO
    weapon_type: WeaponType = WeaponType.SWORD
    country: CountryType = CountryType.INAZUMA

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Shinobus_Shadowsword, Sanctifying_Ring, Gyoei_Narukami_Kariyama_Rite]

    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.talent = talent
        self.power = 0
        self.talent_skill = self.skills[2]
        self.talent_round = -1

    def on_character_die(self, game: 'GeniusGame'):
        if (not self.from_character.is_alive or self.from_character.health_point<=0) and self.talent_round != game.round:
            self.from_character.is_alive = True
            self.from_character.health_point = 0
            self.from_character.heal(1, game, heal_type=HealType.REVIVE)
            self.talent_round = game.round

    def dmg_add(self, game:'GeniusGame'):
        if self.health_point<=5 and game.current_damage.damage_from == self and game.current_damage.damage_to.from_player!=self.from_player:
            game.current_damage.main_damage += 1

    def listen_talent_events(self, game: 'GeniusGame'):
        self.listen_event(game, EventType.CHARACTER_WILL_DIE, ZoneType.CHARACTER_ZONE, self.on_character_die)
        self.listen_event(game, EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.dmg_add)

class Grass_Ring_of_Sanctification(Combat_Status):
    name = "Grass Ring of Sanctification"
    name_ch = "雷草之轮"
    id = 141131
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character:'Character'=None):
        super().__init__(game, from_player, from_character)
        self.usage = 3
        self.current_usage = self.usage
        self.last_round = -1

    def update(self):
        self.current_usage = max(self.current_usage, self.usage)
        self.last_round = -1

    def on_swich(self, game: 'GeniusGame'):
        if game.active_player == self.from_player and self.last_round != game.round:
            damage = 1
            heal = 1

            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.ELECTRO,
                main_damage=damage,
                piercing_damage=0,
                damage_from=self,
                damage_to=get_opponent_active_character(game),
            )
            game.add_damage(dmg)
            game.resolve_damage()

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
            max_taken_char.heal(1,game=game)

            self.current_usage -= 1
            if(self.current_usage <= 0):
                self.on_destroy(game)
            self.last_round = game.round

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.ACTIVE_ZONE, self.on_swich),
        ]

