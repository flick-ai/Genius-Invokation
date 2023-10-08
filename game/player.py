import card
from zone import Card_Zone, Active_zone
import numpy as np

class GeniusPlayer:
    def __init__(self, deck) -> None:
        # 获取基本的牌组信息
        self.character_card = deck['character']

        # 初始化牌库和起始5张手牌
        self.card_zone = Card_Zone(deck['action_card']) # 牌库区
        self.hand_zone = self.card_zone.get_card(num=5) # 手牌区

        # 环境中的基本状态
        self.dice_zone: None
        self.support_zone: None
        self.summons_zone: None
        self.character_zone: None
    
    def choose_card(self, action):
        throw_card = []
        for idx in len(self.hand_zone):
            if action[idx] == 0:
                throw_card.append(self.hand_zone.pop(idx))
        self.card_zone.return_card(throw_card)

    def choose_character(self, action):
        idx = np.where(action==1)
        self.character_zone = Active_zone(idx, self.character_card)

