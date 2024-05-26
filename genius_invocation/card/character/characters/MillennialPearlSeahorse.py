from genius_invocation.card.character.import_head import *


class TailSweep(NormalAttack):
    '''
        旋尾扇击
    '''
    id: int = 24031
    type: SkillType = SkillType.NORMAL_ATTACK
    name: str = "Tail Sweep"
    name_ch = "旋尾扇击"



class PearlArmor(Status):
    name = "Pearl Armor"
    name_ch = "原海明珠"

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None, equip_talent=False):
        super().__init__(game, from_player, from_character)
        self.max_usage = 10000
        if equip_talent:
            self.usage = 1
        else:
            self.usage = 2
        self.summon_used_this_round = 0
        self.current_usage = self.usage
    
    def update(self):
        self.current_usage += 1
    
    def on_execute_dmg(self, game: 'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element != ElementType.PIERCING:
                if game.current_damage.main_damage > 0:
                    game.current_damage.main_damage -= 1
                    if game.current_damage.damage_type == SkillType.SUMMON:
                        self.summon_used_this_round += 1
                        if self.from_character.talent:
                            # 装备有此牌的千年珍珠骏麟所附属的原海明珠抵消召唤物伤害时，改为每回合2次不消耗可用次数
                            if self.summon_used_this_round > 2:
                                self.current_usage -= 1
                        else:
                            # 每回合1次，抵消来自召唤物的伤害时不消耗可用次数
                            if self.summon_used_this_round > 1:
                                self.current_usage -= 1
                    else:
                        self.current_usage -= 1
                    if self.current_usage <= 0:
                        self.on_destroy(game)

    def after_action(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            if game.active_player.is_pass:
                if get_my_active_character(game) == self.from_character:
                    self.from_player.get_card(1)

    def on_begin(self, game: 'GeniusGame'):
        self.summon_used_this_round = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_execute_dmg),
            (EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.after_action)
        ]


# class MillennialPearlSeahorse(Character):
#     '''
#         千年珍珠骏麟
#     '''
#     id: int = 2403
#     name: str = 'Millennial Pearl Seahorse'
#     name_ch = '千年珍珠骏麟'
#     element: ElementType = ElementType.ELECTRO
#     weapon_type: WeaponType = WeaponType.OTHER
#     country: CountryType = CountryType.MONSTER
#     init_health_point: int = 8
#     max_health_point: int = 8
#     skill_list: List = [Icespike_Shot, IceRingWaltz, PlungingIceShards]

#     max_power: int = 2

#     def init_state(self, game: GeniusGame):
#         '''
#             被动技能: 战斗开始时，本角色附属原海明珠。
#         '''
#         pearl_armor