from genius_invocation.card.character.characters.import_head import *

class Akara(NormalAttack):
    '''
        纳西妲
        普通攻击
    '''
    id: int = 0
    type: SkillType = SkillType.NORMAL_ATTACK
    name = "Akara"
    # damage
    damage_type: SkillType = SkillType.NORMAL_ATTACK
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 1
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 1,
            'cost_type': CostType.DENDRO
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

class All_Schemes_to_Know(ElementalSkill):
    '''
        纳西妲
        元素战技 1 小e
    '''
    id: int = 1
    name='All Schemes to Know'
    type: SkillType = SkillType.ELEMENTAL_SKILL

    #damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 2
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.DENDRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: 'Character'):
        super().__init__(from_character)


    def add_status(self, game: 'GeniusGame'):
        status = get_opponent_active_character(game).character_zone.has_entity(Seed_of_Skandha)
        if status is None:
            get_opponent_active_character(game).character_zone.add_entity(
                #TODO: Bug: player
                Seed_of_Skandha(game, get_opponent(game), get_opponent_active_character(game))
            )
        else:
            status.update()
            ls = get_opponent_standby_character(game)
            for char in ls:
                sta = char.character_zone.has_entity(Seed_of_Skandha)
                if sta is not None:
                    sta.update()
                else:
                    char.character_zone.add_entity(
                        Seed_of_Skandha(game, get_opponent(game), char)
                    )

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        # 给对方加状态: 蕴种印
        self.add_status(game)
        self.resolve_damage(game)

        # 获得能量
        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class All_Schemes_to_Know_Tathata(ElementalSkill):
    '''
        纳西妲
        元素战技 2 大e
    '''
    id: int = 2
    name='All Schemes to Know: Tathata'
    type: SkillType = SkillType.ELEMENTAL_SKILL

    # No damage
    damage_type: SkillType = SkillType.ELEMENTAL_SKILL
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 3
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 5,
            'cost_type': CostType.DENDRO
        }
    ]
    energy_cost: int = 0
    energy_gain: int = 1

    def __init__(self, from_character: Character):
        super().__init__(from_character)


    def add_status(self, game: 'GeniusGame'):

        active_char = get_opponent_active_character(game)
        status = active_char.character_zone.has_entity(Seed_of_Skandha)
        if status is None:
            get_opponent_active_character(game).character_zone.add_entity(
                Seed_of_Skandha(game, get_opponent(game), get_opponent_active_character(game))
            )
        else:
            status.update()

        ls = get_opponent_standby_character(game)
        for char in ls:
            sta = char.character_zone.has_entity(Seed_of_Skandha)
            if sta is None:
                char.character_zone.add_entity(
                    Seed_of_Skandha(game, get_opponent(game), char)
                )
            else:
                sta.update()

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)

        # 给对方加状态: 蕴种印
        self.add_status(game)
        self.resolve_damage(game)

        # 获得能量
        self.gain_energy(game)

        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Illusory_Heart(ElementalBurst):
    '''
        纳西妲
        元素爆发
    '''
    id: int = 3
    name='Illusory Heart'
    type: SkillType = SkillType.ELEMENTAL_BURST

    # damage
    damage_type: SkillType = SkillType.ELEMENTAL_BURST
    main_damage_element: ElementType = ElementType.DENDRO
    main_damage: int = 4
    piercing_damage: int = 0

    # cost
    cost = [
        {
            'cost_num': 3,
            'cost_type': CostType.DENDRO
        },
    ]
    energy_cost: int = 2
    energy_gain: int = 0

    def __init__(self, from_character: Character):
        super().__init__(from_character)

    def on_call(self, game: 'GeniusGame'):
        super().on_call(game)
        # 处理伤害
        self.resolve_damage(game)
        self.consume_energy(game)
        # 召唤物/状态生成
        self.add_combat_status(game, Shrine_of_Maya)
        game.manager.invoke(EventType.AFTER_USE_SKILL, game)

class Nahida(Character):
    '''纳西妲'''
    id: int = 1703
    name: str = 'Nahida'
    element: ElementType = ElementType.DENDRO
    weapon_type: WeaponType = WeaponType.CATALYST
    country: CountryType = CountryType.SUNERU

    init_health_point: int = 10
    max_health_point: int = 10
    skill_list = [Akara, All_Schemes_to_Know, All_Schemes_to_Know_Tathata, Illusory_Heart]

    max_power: int = 2

    def __init__(self, game: 'GeniusGame', zone: 'CharacterZone', from_player: 'GeniusPlayer', index:int, from_character = None, talent = False):
        super().__init__(game, zone, from_player, index, from_character)
        self.power = 0
        self.talent = talent

class Shrine_of_Maya(Combat_Status):
    name = "Shrine of Maya"
    def __init__(self, game, from_player: 'GeniusPlayer', from_character: Character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2
        if self.from_character.talent:
            elemental_list = [self.from_player.character_list[i].element for i in range(self.from_player.character_num)]
            if ElementType.HYDRO in elemental_list:
                self.usage = 3
                self.max_usage = 3
                self.current_usage = 3

            if ElementType.ELECTRO in elemental_list:
                status = get_opponent_active_character(game).character_zone.has_entity(Seed_of_Skandha)
                if status is not None:
                    status.add_one_usage()

                chars = get_opponent_standby_character(game)
                for char in chars:
                    sta = char.character_zone.has_entity(Seed_of_Skandha)
                    if sta is not None:
                        sta.add_one_usage()

    def on_damage_add_reaction(self, game: 'GeniusGame'):
        if game.current_damage.reaction is not None:
            if isinstance(game.current_damage.damage_from, Character):
                if game.current_damage.damage_from.from_player == self.from_player:
                    game.current_damage.main_damage += 1


    def on_begin_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_character.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update(self, game: 'GeniusGame'):
        if not self.from_character.talent:
            self.current_usage = self.max_usage
        else:
            elemental_list = [self.from_player.character_list[i].element for i in range(self.from_player.character_num)]
            if ElementType.HYDRO in elemental_list:
                self.usage = 3
                self.max_usage = 3
                self.current_usage = 3
            if ElementType.ELECTRO in elemental_list:
                status = get_opponent_active_character(game).character_zone.has_entity(Seed_of_Skandha)
                if status is not None:
                    status.add_one_usage()

                chars = get_opponent_standby_character(game)
                for char in chars:
                    sta = char.character_zone.has_entity(Seed_of_Skandha)
                    if sta is not None:
                        sta.add_one_usage()

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD_AFTER_REACTION, ZoneType.ACTIVE_ZONE, self.on_damage_add_reaction),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin_phase)
        ]

class Seed_of_Skandha(Status):
    name = "Seed of Skandha"
    # 蕴种印， from_player: 附属一方， from_character: 附属的角色
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 2
        self.max_usage = 2
        self.current_usage = 2

    def add_one_usage(self):
        self.current_usage += 1

    def update(self):
        self.current_usage = max(self.max_usage, self.current_usage)

    def after_take_dmg(self, game: 'GeniusGame'):
        # logger.debug(game.current_damage.main_damage)
        # logger.debug(game.current_damage.main_damage_element)
        if game.current_damage.reaction is None: return
        if game.current_damage.damage_to.from_player != self.from_player: return

        reaction_target = game.current_damage.damage_to # Character
        if reaction_target!=self.from_character:
            dmg = Damage.create_damage(
                game,
                damage_type=SkillType.OTHER,
                main_damage_element=ElementType.PIERCING,
                main_damage=1,
                piercing_damage=0,
                damage_from=None,
                damage_to=self.from_character,
            )
            game.add_damage(dmg)
            # game.resolve_damage()

        else:
            if game.players[0] == self.from_player:
                Nahida_Player = game.players[1]
            else:
                Nahida_Player = game.players[0]
            Nahida_Char = get_character_with_name(Nahida_Player, Nahida)
            if Nahida_Char.talent:
                elemental_list = [Nahida_Player.character_list[i].element for i in range(Nahida_Player.character_num)]
                if ElementType.PYRO in elemental_list:
                    dmg = Damage.create_damage(
                        game,
                        damage_type=SkillType.OTHER,
                        main_damage_element=ElementType.DENDRO,
                        main_damage=1,
                        piercing_damage=0,
                        damage_from=None,
                        damage_to=self.from_character,
                    )
                else:
                    dmg =Damage.create_damage(
                        game,
                        damage_type=SkillType.OTHER,
                        main_damage_element=ElementType.PIERCING,
                        main_damage=1,
                        piercing_damage=0,
                        damage_from=None,
                        damage_to=self.from_character,
                    )
                game.add_damage(dmg)
                # game.resolve_damage()
            else:
                dmg =Damage.create_damage(
                    game,
                    damage_type=SkillType.OTHER,
                    main_damage_element=ElementType.PIERCING,
                    main_damage=1,
                    piercing_damage=0,
                    damage_from=None,
                    damage_to=self.from_character,
                )
                game.add_damage(dmg)
                # game.resolve_damage()
        self.current_usage -= 1
        if self.current_usage<=0:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners= [
            (EventType.AFTER_TAKES_DMG, ZoneType.CHARACTER_ZONE, self.after_take_dmg)
        ]

