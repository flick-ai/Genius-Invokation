from utils import *
from typing import List, TYPE_CHECKING
from .zone import CardZone, ActiveZone, FourZone
import numpy as np

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from card.action import ActionCard

class GeniusPlayer:
    def __init__(self, deck) -> None:
        # 获取基本的牌组信息
        self.character_card = deck['character']

        # 初始化牌库和起始5张手牌
        self.card_zone = CardZone(deck['action_card']) # 牌库区
        self.hand_zone: List[ActionCard] = self.card_zone.get_card(num=5) # 手牌区

        # 环境中的基本状态
        self.dice_zone: List = []
        self.support_zone: FourZone
        self.summons_zone: FourZone
        self.active_zone: ActiveZone

        self.is_pass = False
        # self.
    
    def choose_card(self, action):
        throw_card = []
        for idx in len(self.hand_zone):
            if action[idx] == 0:
                throw_card.append(self.hand_zone.pop(idx))
        reget_card = self.card_zone.get_card(num=len(throw_card))
        self.card_zone.return_card(throw_card)
        self.hand_zone += reget_card
        
    def choose_character(self, action):
        idx = np.where(action==1)
        self.active_zone = ActiveZone(idx, self.character_card)

    def choose_dice(self, action):
        reroll_num = np.sum(action)
        reroll_dice = self.roll_dice(num=reroll_num)
        for idx in len(self.dice_zone):
            if action[idx] == 0:
                self.dice_zone.pop(idx)
        self.dice_zone += reroll_dice

    def roll_dice(self, num=8):
        return np.random.randint(0, DICENUM, num)
    
    def get_card(self, num):
        '''
            当获取到牌时
        '''
        get_cards = self.card_zone.get_card(num=num)
        for card in get_cards:
            if len(self.hand_zone) >= MAX_HANDCARD:
                break
            self.hand_zone.append(card)
            sorted(self.hand_zone, key=lambda card: card.id)
    
    def get_dice(self, dices):
        '''
            当获取到骰子时
        ''' 

    def play_card(self, game: GeniusGame, action:Action):
        card = self.hand_zone.pop(action.choice_idx)
        card.effect(game)

    def change_character(self, game: GeniusGame, action:Action):
        self.active_zone.change_character(game, action)
    
    def begin_round(self, Game):
        '''
            进行回合开始时的内容结算
        '''
        # 遍历所有对象状态

        # 维护状态结算
        self.active_zone.is_after_change_character = False

    def end_round(self, Game):
        '''
            进行回合结束阶段的内容阶段
        '''
        # 摸牌
        self.get_card(num=2)



