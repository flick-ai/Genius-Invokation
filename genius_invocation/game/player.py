from genius_invocation.utils import *
from typing import List, TYPE_CHECKING
from genius_invocation.game.zone import CardZone, ActiveZone, SummonZone, SupportZone, DiceZone, CharacterZone, HandZone, Dice
import numpy as np
from genius_invocation.card.character import CharacterSkill
# from genius_invocation.card.character.characters import *
import genius_invocation.card.character.characters as chars
# You may use chars like following print examples:
# print(chars.tartaglia) The python file(If the name of file is same as charater, it will not return the file)
# print(chars.Tartaglia) The character class
# print(chars.Akara) The status
from genius_invocation.entity.entity import Entity
from genius_invocation.card.action import ActionCard
from genius_invocation.card.character import CharacterSkill
from copy import deepcopy

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.action import Action
    from genius_invocation.card.action import ActionCard
    from genius_invocation.card.character import CharacterSkill

class GeniusPlayer:
    def __init__(self, game: 'GeniusGame', deck, idx) -> None:
        # 初始化角色状态区
        self.index: int = idx
        self.active_idx: int = -1
        self.character_list: List[Character] = []
        self.element_list: List[ElementType] = []
        self.element_set: set = set()
        for id, name in enumerate(deck['character']):
            zone = CharacterZone(game, self)
            self.character_list.append(eval("chars."+name)(
                game = game,
                zone = zone,
                from_player = self,
                index = id,
                from_character = None,
                talent = False))
        self.character_num = len(self.character_list)
        self.update_element_list()
        # 初始化牌库、起始5张手牌、骰子区
        self.card_zone: CardZone = CardZone(game, self, deck['action_card']) # 牌库区
        self.hand_zone: HandZone = HandZone(game, self) # 手牌区
        arcanes = self.card_zone.find_card(ActionCardType.EVENT_ARCANE_LEGEND, num=-1)
        self.hand_zone.add(self.card_zone.get_card(num=5-len(arcanes))+arcanes)
        self.dice_zone: DiceZone = DiceZone(game, self)

        # 环境中的基本状态
        self.support_zone: SupportZone = SupportZone(game, self)
        self.summon_zone: SummonZone = SummonZone(game, self)
        self.team_combat_status: ActiveZone = ActiveZone(game, self)

        # 回合pass
        self.game = game
        self.is_pass: bool
        self.play_arcane_legend: bool = False

        # 切换角色基本信息
        self.is_after_change: bool
        self.is_quick_change: bool
        self.change_num: int
        self.last_die_round: int = -1

        # 扔骰子基本信息
        self.roll_num: int = 8
        self.roll_time: int = 1
        self.fix_dice = []

        self.prepared_skill: Entity = None

        # Mask
        self.action_mask: np.array

        # Damage Type
        self.suffer_damage_type = []

        # Play cards
        self.played_cards = []

    def update_element_list(self):
        ''' Only For La Signora right now. Refresh the element list, which may be used by some skills and talents.'''
        self.element_list = []
        for char in self.character_list:
            self.element_list.append(char.element)
        self.element_set = set(self.element_list)

    def choose_card(self, action: 'Action'):
        '''
            非标准行动: 制衡手牌
        '''
        throw_card = self.hand_zone.remove(action.choice_list)
        reget_card = self.card_zone.get_card(num=len(throw_card))
        self.card_zone.return_card(throw_card)
        self.hand_zone.add(reget_card)

    def choose_character(self, action: 'Action'):
        '''
            非标准行动: 选择出战角色
        '''
        idx = action.target_idx
        self.change_to_id(idx)


    def choose_dice(self, action: 'Action'):
        '''
            非标准行动: 选择重新投掷的骰子
        '''
        reroll_num = len(action.choice_list)
        reroll_dice = self.roll_dice(num=reroll_num)
        self.dice_zone.remove(action.choice_list)
        self.dice_zone.add(reroll_dice)

    def roll_dice(self, num=8, is_basic=False, is_different=False,):
        '''
            基本行动: 投掷骰子
        '''
        if is_basic:
                if is_different:
                    return self.game.random.choice(DICENUM-1, num, replace=False).tolist()
                return self.game.random.randint(0, DICENUM-1, num).tolist()
        if self.game.is_omni:
            return  [DiceType.OMNI.value for i in range(num)]
        else:
            return self.game.random.randint(0, DICENUM, num).tolist()


    def get_card(self, num):
        '''
            基本行动: 获取牌
        '''
        get_cards = self.card_zone.get_card(num=num)
        self.hand_zone.add(get_cards)

    def change_to_id(self, idx: int):
        '''
            基本行动: 切换到指定人
        '''
        if self.active_idx in range(self.character_num):
            self.game.current_switch["from"] = self.character_list[self.active_idx]
        if self.active_idx >= 0:
            self.character_list[self.active_idx].is_active = False
        self.active_idx = idx
        self.character_list[self.active_idx].is_active = True
        self.game.current_switch["to"] = self.character_list[self.active_idx]
        self.game.manager.invoke(EventType.AFTER_CHANGE_CHARACTER, self.game)
        self.character_list[self.active_idx].on_switched_to()
        self.game.current_switch = {"from": None, "to": None}

    def change_to_previous_character(self):
        '''
            基本行动: 切换到前一个人
        '''
        idx = (self.active_idx - 1) % self.character_num
        while self.character_list[idx].is_alive == False:
            idx = (idx - 1) % self.character_num
        self.change_to_id(idx)

    def change_to_next_character(self):
        '''
            基本行动: 切换到下一个人
        '''
        idx = (self.active_idx + 1) % self.character_num
        while self.character_list[idx].is_alive == False:
            idx = (idx + 1) % self.character_num
        self.change_to_id(idx)

    def use_skill(self, game: 'GeniusGame'):
        '''
            标准行动: 使用技能
        '''
        idx = game.current_action.choice_idx
        skill = self.character_list[self.active_idx].skills[idx]
        skill.before_use_skill(game)
        self.use_dice(game)
        game.current_dice = Dice(from_player=self,
                                 from_character=self.character_list[self.active_idx],
                                 use_type=skill.type,
                                 cost=deepcopy(skill.cost))
        self.character_list[self.active_idx].skill(idx, game)

    def play_card(self, game: 'GeniusGame'):
        '''
            标准行动: 打出手牌/调和手牌
        '''
        self.use_dice(game)
        idx = game.current_action.choice_idx
        card: ActionCard = self.hand_zone.use(idx)
        game.current_card = card
        if game.current_action.target_type == ActionTarget.DICE_REGION:
            card.on_tuning(game)
        else:
            if card.name not in self.played_cards:
                self.played_cards.append(card.name)
            if card.card_type == ActionCardType.EQUIPMENT_TALENT:
                game.current_dice= Dice(from_player=self,
                                        from_character=None,
                                        use_type=card.card_type,
                                        name = card.name,
                                        cost = deepcopy(card.cost))
            else:
                game.current_dice = Dice(from_player=self,
                                    from_character=None,
                                    use_type=card.card_type,
                                    name = card.name,
                                    cost = [{'cost_num':card.cost_num, 'cost_type':card.cost_type}])
            game.manager.invoke(EventType.ON_PLAY_CARD, game)

            if game.can_play_card:
                card.on_played(game)
            else:
                game.can_play_card = True
        game.current_card = None #Finish use the card.

    def change_character(self, game: 'GeniusGame'):
        '''
            标准行动: 切换角色
        '''
        self.use_dice(game)
        idx = game.current_action.target_idx
        target_char = self.character_list[idx]
        game.current_dice = Dice(from_player=self,
                                 from_character=None,
                                 use_type=SwitchType.CHANGE_CHARACTER,
                                 cost=[{'cost_num':1, 'cost_type':CostType.BLACK}],
                                 to_character=target_char)
        self.change_num += 1
        self.is_quick_change = False
        game.manager.invoke(EventType.ON_CHANGE_CHARACTER, game)
        self.change_to_id(idx)
        if self.is_quick_change:
            game.is_change_player = False


    def use_dice(self, game: 'GeniusGame'):
        '''
            基本行动: 消耗骰子
        '''
        dices = game.current_action.choice_list
        self.dice_zone.remove(dices)

    def generate_mask(self, game: 'GeniusGame'):
        '''
            基本行动: 为每个行动生成Mask
            如何判断一个行动是否合法？
            1. 行动目标是否存在？
            2. 行动要求是否满足？
            2. 行动所需骰子是否足够？
            TODO:我们使用一个3维矩阵来维护,但是实际上这个矩阵十分稀疏,可以考虑使用稀疏矩阵来提升系统系能
        '''

        # print(game.game_phase, game.active_player_index, "generate_mask")
        self.action_mask = np.zeros((18, 15, 5)).astype(np.int32)

       # 非标准行动的 Mask
        if game.game_phase == GamePhase.ACTION_PHASE:
            self.action_mask[15][1][0] = 1
        if game.game_phase == GamePhase.ROLL_PHASE:
            self.action_mask[16][13][0] = 1
            self.action_mask[16][13][1] = self.dice_zone.num()
            return
        if game.game_phase == GamePhase.SET_CARD:
            self.action_mask[17][14][0] = 1
            self.action_mask[17][14][1] = self.hand_zone.num()
            return
        if game.game_phase == GamePhase.SET_CHARACTER:
            if game.special_phase != None and isinstance(game.special_phase, ActionCard):
                has_target = game.special_phase.refind_target(game)
                game.special_phase.on_finished(game)
                if has_target != None:
                    for target in has_target:
                        self.action_mask[14][target+2][0] = 1
                return
            else:
                for idx, character in enumerate(self.character_list):
                    character: Character
                    if character.is_alive and not character.is_active:
                        self.action_mask[14][idx+2][0] = 1
                return

        # 计算能否打出手牌和烧牌
        for idx, action_card in enumerate(self.hand_zone.card):
            action_card: 'ActionCard'
            if action_card.card_type == ActionCardType.EQUIPMENT_TALENT:
                has_target = action_card.find_target(game)
                if self.character_list[self.active_idx].power >= action_card.cost_power:
                    has_dice = self.calculate_dice(game, Dice(from_player=self,
                                                            from_character=None,
                                                            use_type=action_card.card_type,
                                                            name=action_card.name,
                                                            cost = deepcopy(action_card.cost)))
                else:
                    has_dice = False
            else:
                has_target = action_card.find_target(game)
                has_dice = self.calculate_dice(game, Dice(from_player=self,
                                                        from_character=None,
                                                        use_type=action_card.card_type,
                                                        name=action_card.name,
                                                        cost = [{'cost_num':action_card.cost_num, 'cost_type':action_card.cost_type}]))
            if has_target is not None and has_dice:
                for target in has_target:
                    self.action_mask[idx][target][0] = 1
                    for i, cost in enumerate(game.current_dice.cost):
                        self.action_mask[idx][target][i*2+1] = cost['cost_num']
                        self.action_mask[idx][target][i*2+2] = cost['cost_type'].value if cost['cost_type'] is not None else 0


            active_dice = ElementToDice[self.character_list[self.active_idx].element]
            can_tune = self.dice_zone.calculate_dice(Dice(from_player=self,
                                                     from_character=None,
                                                     use_type=SwitchType.ELEMENTAL_RESONANCE,
                                                     cost = [{'cost_num':1, 'cost_type':active_dice}]))
            if can_tune:
                self.action_mask[idx][13][0] = 1
                self.action_mask[idx][13][1] = 1
                self.action_mask[idx][13][2] = - (active_dice.value)


        # 计算能否使用技能
        for idx, skill in enumerate(self.character_list[self.active_idx].skills):
            skill: CharacterSkill
            has_dice = self.calculate_dice(game, Dice(from_player=self,
                                                      from_character=self.character_list[self.active_idx],
                                                      use_type=skill.type,
                                                      cost=deepcopy(skill.cost)))
            can_use = not self.character_list[self.active_idx].is_frozen
            if skill.type == SkillType.ELEMENTAL_BURST:
                can_use = can_use and self.character_list[self.active_idx].max_power == self.character_list[self.active_idx].power
            if can_use and has_dice:
                self.action_mask[idx+10][0][0] = 1
                for i, cost in enumerate(game.current_dice.cost):
                    self.action_mask[idx+10][0][i*2+1] = cost['cost_num']
                    self.action_mask[idx+10][0][i*2+2] = cost['cost_type'].value

        # 计算能否切换角色
        for idx, character in enumerate(self.character_list):
            character: Character
            if character.is_active:
                continue
            has_dice = self.calculate_dice(game, Dice(from_player=self,
                                                from_character=get_my_active_character(game),
                                                to_character=character,
                                                use_type=SwitchType.CHANGE_CHARACTER,
                                                cost=[{'cost_num':1, 'cost_type':CostType.BLACK}]))
            if not has_dice:
                continue
            if character.is_alive:
                self.action_mask[14][idx+2][0] = 1
            for i, cost in enumerate(game.current_dice.cost):
                    self.action_mask[14][idx+2][i*2+1] = cost['cost_num']
                    self.action_mask[14][idx+2][i*2+2] = cost['cost_type'].value

    def calculate_dice(self, game: 'GeniusGame', dice: Dice):
        '''
            结算时刻: 计算骰子时
        '''
        game.current_dice = dice
        game.manager.invoke(EventType.CALCULATE_DICE, game)
        return self.dice_zone.calculate_dice(game.current_dice)

    def begin_roll_phase(self, game: 'GeniusGame'):
        '''
            结算时刻: 行动阶段开始时
        '''
        # 维护状态结算
        self.roll_num = 8
        self.roll_time = 1
        self.fix_dice = []
        # 事件
        self.dice_zone.remove_all()
        game.manager.invoke(EventType.BEGIN_ROLL_PHASE, game)
        self.roll_num = self.roll_num - len(self.fix_dice)
        dices = self.fix_dice + self.roll_dice(num=self.roll_num)
        self.dice_zone.add(dices)


    def begin_action_phase(self, game: 'GeniusGame'):
        '''
            结算时刻: 行动阶段开始时
        '''
        # 维护状态结算
        self.is_pass = False
        self.is_after_change = False
        self.is_quick_change = False
        self.change_num = 0

        # 事件
        game.manager.invoke(EventType.BEGIN_ACTION_PHASE, game)

    def end_phase(self, game: 'GeniusGame'):
        '''
            结算时刻: 结束阶段时
        '''
        # 事件
        game.manager.invoke(EventType.END_PHASE, game)
        self.roll_time = 2
        self.get_card(num=2)





