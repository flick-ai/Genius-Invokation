import card
from utils import *
from typing import List
from zone import CardZone, ActiveZone, FourZone
import numpy as np

class GeniusPlayer:
    def __init__(self, deck) -> None:
        # 获取基本的牌组信息
        self.character_card = deck['character']

        # 初始化牌库和起始5张手牌
        self.card_zone = CardZone(deck['action_card']) # 牌库区
        self.hand_zone = self.card_zone.get_card(num=5) # 手牌区

        # 环境中的基本状态
        self.dice_zone: List = []
        self.support_zone: FourZone
        self.summons_zone: FourZone
        self.active_zone: ActiveZone
    
    def choose_card(self, action):
        throw_card = []
        for idx in len(self.hand_zone):
            if action[idx] == 0:
                throw_card.append(self.hand_zone.pop(idx))
        self.card_zone.return_card(throw_card)

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


